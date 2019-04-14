<link rel='stylesheet' href='markdown9.css'/>

Database upload/update procedure
--------------------------------

Use scp/rsync to upload the .txt database to a temporary location on the server.

Then:

    cd /path/to/file/
    python /srv/dds/scripts/update_census.py filename.txt censusYYYYi

where `filename.txt` is the uploaded file and `censusYYYYi` is the name of the database to which to upload.

Recommended convention: YYYY - the full year, i - an incrementing letter.

Example:

    census2014a - first database of 2014
    census2014b - second database revision
    census2015a - first database of 2015
    ...

The update_census.py script creates a new collection named companies in the new database. 

Once the MongoDB database has been updated, the temporary file can (should) be removed to save disk space.

In order to add admin-configurable indices to the new database, run (from /srv/dds/) "python manage.py ensure_indices" while in the DDS virtualenv.

Database settings
-----------------

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dds',
            'USER': 'dds',
            'PASSWORD': 'y8M36LkeVgGn',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

Secret key
----------

Generated on server:

    t2-(_76h2+aohc5fn_$!n76nb5##w$ae^#o5+27a%hivj0&u#^

Django superuser credentials
----------------------------

    admin nzLdtrgHNMMe

Django admin panel
------------------

Log in at datadrivenshipping.com/admin

South
-----

Installed South
Created initial migrations for dds, kombu.transport.django, and tastypie
Fake migrated dds
Actually migrated tastypie

allowed_hosts
-------------

    *.datadrivenshipping.com
    127.0.0.1

New Relic/Gunicorn run script
-----------------------------

    NEW_RELIC_CONFIG_FILE=/srv/dds/newrelic.ini \
    newrelic-admin \
    run-program \
    gunicorn dds.wsgi:application --bind 127.0.0.1:8001

New Relic application page
--------------------------

https://rpm.newrelic.com/accounts/633953/applications/2825017

Front page benchmarks
---------------------

    Transactions:                  24501 hits
    Availability:                 100.00 %
    Elapsed time:                  81.03 secs
    Data transferred:              66.59 MB
    Response time:                  0.65 secs
    Transaction rate:             302.37 trans/sec
    Throughput:                     0.82 MB/sec
    Concurrency:                  197.97
    Successful transactions:       24501
    Failed transactions:               1
    Longest transaction:           16.43
    Shortest transaction:           0.38
 
Ran `siege -b` from two hosts, achieved around 15k RPM

