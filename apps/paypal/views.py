# Python imports
import urllib

# Django imports
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseServerError
from django.template import RequestContext

# Local imports


PAYPAL_URL = "https://www.sandbox.paypal.com/cgi-bin/webscr"
#PAYPAL_URL = "https://www.paypal.com/cgi-bin/webscr"

def ipn(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['cmd'] = '_notify-validate'
        
        response = urllib.urlopen(PAYPAL_URL, urllib.urlencode(data))
        
        if response.read() == 'VERIFIED':
            # good
            pass
        else:
            import logging
            logging.error("IPN", "The paypal payment could not be verified")
        
    return HttpResponse(1)
