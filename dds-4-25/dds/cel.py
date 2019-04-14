from __future__ import absolute_import

from os import environ
from celery import Celery

from django.conf import settings


environ.setdefault('DJANGO_SETTINGS_MODULE', 'dds.settings')
app = Celery('dds', broker='django://', backend='django://')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

if __name__ == '__main__':
    app.start()

