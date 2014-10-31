import base64
import urllib, urllib2, httplib
import pdb

from social.apps.django_app.utils import strategy
from tastypie.http import *
from tastypie.serializers import Serializer

from django import http
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext, Context, loader
from django.utils.http import base36_to_int
from django.utils.safestring import mark_safe
from django.utils.translation import check_for_language, ugettext, ugettext_lazy as _

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from accounts.forms import SignupForm, LoginForm

@strategy() 
def register_by_access_token(request, backend, *args, **kwargs):
    backend = request.strategy.backend
    access_token = kwargs.get('access_token')
    if not access_token:
        raise AuthMissingParameter(backend, 'access_token')
    user = backend.do_auth(access_token)
    if user and user.is_active:
        login(request, user)
    return user
                               
def login_view(request, mode = None ,**kwargs):
    template_name = kwargs.pop("template_name", "account/login.html")
    form_class = kwargs.pop("form_class", LoginForm)
    print request.user
    if request.method == "POST":
        form = form_class(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = str(form.cleaned_data['username'])
            password = str(form.cleaned_data['password'])
            user = authenticate(username=username, password=password)
            if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home_view')) # Redirect after POST
            else:
                data = {'error': True}
                return render_to_response(template_name, data, context_instance=RequestContext( request ))        
        else:
            data={"errors": form.errors, 'form': form}
            return render_to_response(template_name, data, context_instance=RequestContext( request ))                
    
    else:
        form = LoginForm() # An unbound form
        
    data = {
         'form': form,
        }
    return render_to_response(template_name, data, context_instance=RequestContext( request ))

def logout_view(request, mode=None):
    logout(request)
    return HttpResponseRedirect(reverse('banyan-download')) # Redirect after logout

def signup_view(request, mode = None ,**kwargs):
    template_name = kwargs.pop("template_name", "account/signup.html")
    form_class = kwargs.pop("form_class", SignupForm)
    if request.method == "POST":
        form = form_class(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = str(form.cleaned_data['username'])
            name = str(form.cleaned_data['name'])
            password1 = str(form.cleaned_data['password1'])
            password2 = str(form.cleaned_data['password2'])
            email = str(form.cleaned_data['email'])
            user = User.objects.create(username=username, email=email, password = password1)          
            user.save()
            
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home_view')) # Redirect after POST
        else:
            data={"errors": form.errors, 'form': form}
            return render_to_response(template_name, data, context_instance=RequestContext( request ))
    else:
        form = SignupForm() # An unbound form
        
    data = {
        'form': form,
    }
    return render_to_response(template_name, data, context_instance=RequestContext( request ))

