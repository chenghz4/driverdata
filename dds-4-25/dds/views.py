from account.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from dds.models import ExportJob


def homepage(request):
    return render_to_response('homepage.html', context_instance=RequestContext(request))


@login_required
def get_exported_file(request, filename):
    job = get_object_or_404(ExportJob, export_filename=filename)
    if job.query.account.user == request.user:
        return HttpResponseRedirect(job.get_temporary_url())
    else:
        return HttpResponse('Unauthorized', status=401)