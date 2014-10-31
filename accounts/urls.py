from django.conf import settings
from django.conf.urls import *

from accounts.forms import SignupForm
from accounts.views import *

urlpatterns = patterns("",
    url(r"^signup/$", signup_view, { "mode":"simple" }, name="signup_view"),
    url(r"^login/$", login_view, { "mode":"simple" }, name="login_view"),
    url(r"^logout/$", logout_view, { "mode":"simple" }, name="logout_view"),    
    )