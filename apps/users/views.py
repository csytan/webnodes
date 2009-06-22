from django import forms
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


### Forms ###
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput, required=False)


### Views ###
def users_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password']
            )
            
            if user is None:
                # sign up user if they don't have an account
                user_exists = User.all().filter('username =', 'username').get()
                if not user_exists:
                    User.objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'],
                        email=None
                    )
                    user = authenticate(
                        username=form.cleaned_data['username'], 
                        password=form.cleaned_data['password']
                    )
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    redirect = request.POST.get('next', '/')
                    return HttpResponseRedirect(redirect)
                else:
                    return HttpResponse('disabled acct')
    else:
        form = LoginForm()
        
    return render_to_response('basic_form.html', {
        'form': form
    }, context_instance=RequestContext(request))
    
def users_logout(request):
    logout(request)
    redirect = request.GET.get('next', '/')
    return HttpResponseRedirect(redirect)
