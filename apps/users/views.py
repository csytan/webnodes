from django import forms
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.db import IntegrityError

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


### Forms ###
class SigninForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput, required=False)

class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(required=False, label='Email (optional)')
    password = forms.CharField(widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput, required=False)

### Views ###
def sign_in(request):
    next = {'next': request.GET.get('next', '/')}
    
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
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
        form = SigninForm(initial=next)
        
    return render_to_response('sign_in.html', {
        'signin_form': form,
        'signup_form': SignupForm(initial=next)
    }, context_instance=RequestContext(request))


def sign_up(request):
    next = {'next': request.GET.get('next', '/')}
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                return sign_in(request)
            except IntegrityError:
                form.errors['username'] = ['Username has been taken']
    else:
        form = SignupForm(initial=next)
        
    return render_to_response('sign_in.html', {
        'signin_form': SigninForm(initial=next),
        'signup_form': form
    }, context_instance=RequestContext(request))


def sign_out(request):
    logout(request)
    redirect = request.GET.get('next', '/')
    return HttpResponseRedirect(redirect)
