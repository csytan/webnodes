from django import forms
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext


### Forms ###
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField()

### Views ###
def users_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=None
            )
            user = authenticate(
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password']
            )
            login(request, user)
            redirect = request.GET.get('next', '/')
            return HttpResponseRedirect(redirect)
    else:
        form = RegistrationForm()
        
    return render_to_response('users/login.html', {
        'registration_form': form,
        'login_form': LoginForm()
    }, context_instance=RequestContext(request))
    
def users_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    redirect = request.GET.get('next', '/')
                    return HttpResponseRedirect(redirect)
                else:
                    return HttpResponse('disabled acct')
            else:
                return HttpResponse(str(user))
    else:
        form = LoginForm()
        
    return render_to_response('users/login.html', {
        'login_form': form,
        'registration_form': RegistrationForm()
    }, context_instance=RequestContext(request))
    
def users_logout(request):
    logout(request)
    redirect = request.GET.get('next', '/')
    return HttpResponseRedirect(redirect)