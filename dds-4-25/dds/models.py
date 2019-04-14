import hashlib
from base64 import b32encode

from boto.s3.connection import S3Connection
from bson.json_util import dumps
from account.models import Account
from django.contrib import admin
from django.db.models import Model, ForeignKey, DateTimeField, CharField, TextField, IntegerField, BooleanField
from pymongo import MongoClient
from tablib import Dataset

from dds.settings import DDS_DB, DDS_EXPORT_LIMIT, MONGODB_URI, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, CUSTOMER_EXPORT_BUCKET
from dds.tasks import do_export


client = MongoClient(MONGODB_URI)
export_bucket = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).get_bucket(CUSTOMER_EXPORT_BUCKET)


class CensusField(Model):
    readable_name = CharField(max_length=30, unique=True)
    db_column = CharField(max_length=30, unique=True)
    description = TextField(blank=True)
    indexed = BooleanField(default=True)

    def __unicode__(self):
        return self.readable_name


class Query(Model):
    account = ForeignKey(Account, null=True, blank=True)
    name = CharField(max_length=255, blank=True)
    sort_by = ForeignKey(CensusField)
    sample = TextField(blank=True)
    num_records = IntegerField(default=0)

    class Meta:
        unique_together = (("account", "name"),)

    def is_owned_by(self, user):
        return not self.id or self.account == user.account

    def update_results(self):
        c = self.get_cursor()
        self.num_records = c.count()
        self.sample = dumps(list(c.limit(10)))
        return self

    def get_filter_dict(self):
        d = {}
        for f in self.queryfilter_set.iterator():
            f_col = f.field.db_column
            f_val = f.value.upper()
            if f.type == 'eq':
                d[f_col] = f_val
            else:
                if f_col not in d: d[f_col] = {}
                d[f_col]["$" + f.type] = f_val
        return d

    def get_cursor(self):
        db = client[DDS_DB]
        collection = db.companies
        cursor = collection.find(self.get_filter_dict())
        if self.sort_by:
            cursor = cursor.sort(self.sort_by.db_column)
        return cursor

    @classmethod
    def from_strings(cls, ss):
        q = cls()
        q.save()
        for s in ss:
            qf = QueryFilter.from_string(s)
            qf.query = q
            qf.save()
        return q

    def __unicode__(self):
        return self.name or '(unnamed) query #' + str(self.id)


class QueryFilter(Model):
    field = ForeignKey(CensusField)
    value = CharField(max_length=255)
    type = CharField(max_length=10)
    query = ForeignKey(Query)

    class Meta:
        unique_together = (("field", "query"),)

    def is_owned_by(self, user):
        return (not self.id) or self.query.account == user.account

    def save(self, *args, **kwargs):
        super(QueryFilter, self).save(*args, **kwargs)
        self.query.update_results().save()

    def delete(self, *args, **kwargs):
        query = self.query
        super(QueryFilter, self).delete(*args, **kwargs)
        query.update_results().save()

    @classmethod
    def from_string(cls, s):
        tokens = s.split(' ')
        field = CensusField.objects.get(db_column=tokens[0])
        return cls(field=field, type=tokens[1], value=tokens[2])

    def __unicode__(self):
        if not self.id:
            return "uninitialized QueryFilter"
        else:
            return (self.field.db_column or "unknown column") + ' ' + self.type + ' ' + self.value


class ExportJob(Model):
    export_filename = CharField(max_length=30, blank=True, null=True)
    export_format = CharField(max_length=4)
    query = ForeignKey(Query)
    requested = DateTimeField(auto_now_add=True)
    begin = DateTimeField(blank=True, null=True)
    end = DateTimeField(blank=True, null=True)

    def is_owned_by(self, user):
        return not self.id or self.query.account == user.account

    def __unicode__(self):
        return str(self.query) + " as " + self.export_format

    def save(self, *args, **kwargs):
        super(ExportJob, self).save(*args, **kwargs)
        if not self.begin:
            do_export.apply_async((self,))

    def make_filename(self):
        h = hashlib.new('sha256')
        h.update(self.query.account.user.username)
        h.update(self.query.sample)
        h.update(self.export_format)
        h.update(str(self.requested))
        h.update(str(self.id))
        return b32encode(h.digest())[0:16] + '.' + self.export_format

    def get_temporary_url(self):
        if not self.end: return ''
        k = export_bucket.get_key(self.export_filename)
        return k.generate_url(60 * 60 * 24)

    def get_indirect_link(self):
        if not self.end: return ''
        return '/exported_file/' + self.export_filename

    def do_export(self):
        c = self.query.get_cursor().limit(DDS_EXPORT_LIMIT)
        col_names = CensusField.objects.all().values_list('db_column', flat=True)
        data = Dataset(headers=col_names, title=self.query.name)
        for row in c:
            data.append(list(row.get(col_name, '') for col_name in col_names))
        if self.export_format in ['csv', 'xls', 'xlsx', 'json', 'tsv', 'yaml', 'ods', 'html']:
            self.export_filename = self.make_filename()
            k = export_bucket.new_key(self.export_filename)
            k.set_contents_from_string(data.__getattribute__(self.export_format), policy="private")
            self.save()


admin.site.register(CensusField)
admin.site.register(Query)
admin.site.register(QueryFilter)
admin.site.register(ExportJob)
