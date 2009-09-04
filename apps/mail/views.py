# Python imports
import email
from email.utils import getaddresses
import urllib

# Appengine imports
from google.appengine.api import mail

# Django imports
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils import simplejson

def get_translation(text):
    service = 'http://ajax.googleapis.com/ajax/services/language/translate?v=1.0'
    response = urllib.urlopen(service + '&q=' + urllib.quote(text) + '&langpair=en%7Cfr')
    data = simplejson.loads(response.read())
    return data['responseData']['translatedText']


def get_first_text_part(msg):
    if msg.is_multipart():
        msg = msg.get_payload(0)
        return get_first_text_part(msg)
    return msg.get_payload(decode=True)


def handle_mail(request):
    sender = request.GET.get('from', '')
    recipient = request.GET.get('to', '')
    
    msg = email.message_from_string(request.raw_post_data)
    tos = msg.get_all('to', [])
    ccs = msg.get_all('cc', [])
    recipients = getaddresses(tos + ccs)
    subject = msg.get('subject', 'No Subject')
    body = get_first_text_part(msg)
    
    if recipient == 'translate@webnodes.org':
        mail.send_mail(
            sender='csytan@gmail.com',
            to=sender,
            subject=get_translation(subject),
            body=get_translation(body),
            reply_to='translate@webnodes.org'
        )
    
    return HttpResponse(1)