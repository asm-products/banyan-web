import re
import base64
import urllib, urllib2
import httplib

from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import smart_unicode
from django.utils.http import int_to_base36

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site


alnum_re = re.compile(r"^\w+$")


class LoginForm(forms.Form):

    username = forms.CharField(
        label = _("Username"),
        max_length = 30,
        widget = forms.TextInput(attrs={'class':'required'})
    )
    
    password = forms.CharField(
        label = _("Password"),
        widget = forms.PasswordInput(render_value=False, attrs={'class':'required'})
    )
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["password"].label = ugettext("Password")
        self.fields["password"].required = True
        self.fields['password'].widget.attrs['class'] = 'required'    

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = ugettext("Username")
        self.fields["username"].required = True
        self.fields['username'].widget.attrs['class'] = 'required'    
            
    def clean(self):
        try:
            username = str(self.cleaned_data["username"])
        except:
            self._errors["username"] = self.error_class([(_("Enter a User Name to Login"))])
        try:
            password = str(self.cleaned_data["password"])
        except:
            self._errors["password"] = self.error_class([(_("Enter a Password to Login"))])
            
        return self.cleaned_data


class SignupForm(forms.Form):
    
    username = forms.CharField(
        label = _("Username"),
        max_length = 30,
        widget = forms.TextInput(attrs={'class':'required'})
    )
    
    name = forms.CharField(
        label = _("Name"),
        max_length = 30,
        widget = forms.TextInput(attrs={'class':'required'})
    )
    
    password1 = forms.CharField(
        label = _("Password"),
        widget = forms.PasswordInput(render_value=False, attrs={'class':'required'})
    )
    password2 = forms.CharField(
        label = _("Password (again)"),
        widget = forms.PasswordInput(render_value=False, attrs={'class':'required'})
    )
    email = forms.EmailField(widget=forms.TextInput())
    confirmation_key = forms.CharField(
        max_length = 40,
        required = False,
        widget = forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = ugettext("E-mail")
        self.fields["email"].required = True
        self.fields['email'].widget.attrs['class'] = 'required'    

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = ugettext("Username")
        self.fields["username"].required = True
        self.fields['username'].widget.attrs['class'] = 'required'    

    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            if self.data.get("mode", None) == "api":
                self._errors["username"] = self.error_class([(("Usernames can only contain letters, numbers and underscores and can be in English only."))])		
            else:
                self._errors["username"] = self.error_class([(_("Usernames can only contain letters, numbers and underscores and can be in English only."))])		
        try:
            user = User.objects.get(username__iexact=self.cleaned_data["username"])
        except User.DoesNotExist:
            return self.cleaned_data["username"]
        if self.data.get("mode", None) == "api":
            self._errors["username"] = self.error_class([(("This username is already taken. Please choose another."))])
        else:
            self._errors["username"] = self.error_class([(_("This username is already taken. Please choose another."))])
			
    def clean_email(self):
        value = self.cleaned_data["email"]
        try:
            User.objects.get(email__iexact=value)
            self._errors["email"] = self.error_class([(("A user is registered with this e-mail address."))])
        except User.DoesNotExist:
            return value
        if self.data.get("mode", None) == "api":
            self._errors["email"] = self.error_class([(("A user is registered with this e-mail address."))])
        else:    
            self._errors["email"] = self.error_class([(_("A user is registered with this e-mail address."))])
        return value
    
    def clean(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                if self.data.get("mode", None) == "api":
                    self._errors["password2"] = self.error_class([(("You must type the same password each time."))])
                else:
                    self._errors["password2"] = self.error_class([(_("You must type the same password each time."))])
        return self.cleaned_data        
                

