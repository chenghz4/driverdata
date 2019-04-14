from django.core.management import BaseCommand
import pymongo

from dds.models import CensusField
from dds.settings import DDS_DB


class Command(BaseCommand):
    args = ''
    help = 'Ensures indices on selected DDS census fields'

    def handle(self, *args, **kwargs):
        uri = "mongodb://127.0.0.1:27017/"
        client = pymongo.MongoClient(uri + DDS_DB)
        db = client[DDS_DB]
        collection = db.companies

        for field in CensusField.objects.iterator():
            if field.indexed:
                self.stdout.write('Ensuring index on '+field.db_column+'\n')
                collection.ensure_index(field.db_column)