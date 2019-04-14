from celery import Celery
from djcelery.utils import now


app = Celery('tasks', broker='django://')


@app.task(ignore_result=True)
def do_export(job):
    job.begin = now()
    job.save()
    job.do_export()
    job.end = now()
    job.save()