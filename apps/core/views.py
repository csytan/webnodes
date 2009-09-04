# Django imports
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext

# Local imports
from models import LanguagePair, TranslationJob


def index(request):
    if request.method == 'POST':
        job = TranslationJob(
            fr_lang=request.POST['fr_lang'],
            to_lang=request.POST['to_lang'],
            text=request.POST['text']
        )
        job.put()
    return render_to_response('index.html', 
        context_instance=RequestContext(request))

def translator_jobs(request):
    return render_to_response('jobs.html', {
        'jobs': TranslationJob.translator_jobs(request.user)
    }, context_instance=RequestContext(request))

def translator_job(request, id):
    job = TranslationJob.get_by_id(int(id))
    if request.method == 'POST':
        if request.POST['action'] == 'save':
            job.translated_text = request.POST['translated_text']
            job.put()
            return HttpResponse(1)
        else:
            job.translated_text = request.POST['translated_text']
            
    return render_to_response('translation_job.html', {
        'job': job
    }, context_instance=RequestContext(request))
    
def client_jobs(request):
    
    TranslationJob.get_orders(request.user)
    
def client_job(request, id):
    pass