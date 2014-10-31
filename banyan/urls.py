from django.conf.urls import *
from django.conf import settings
from django.contrib import admin
from tastypie.api import Api
from core.api import StoryResource, PieceResource, ActivityResource
from accounts.api import BanyanUserResource
from content_feedback.api import ContentFlagResource, ContentHideResource
from django.views.generic import TemplateView

v1_api = Api(api_name='v1')
v1_api.register(StoryResource())
v1_api.register(ActivityResource())
v1_api.register(PieceResource())
v1_api.register(BanyanUserResource())
v1_api.register(ContentFlagResource())
v1_api.register(ContentHideResource())

admin.autodiscover()

handler500 = 'core.views.server_error'
handler404 = 'core.views.not_found'

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r"^$", TemplateView.as_view(template_name='download.html'), name="banyan-download"),
    url(r'^api/', include(v1_api.urls)),
    url(r"^", include("core.urls")),
    url(r"^account/", include("accounts.urls")),
    url('', include('social.apps.django_app.urls', namespace='social')),
)

urlpatterns += patterns("",
    url('^privacy/$', TemplateView.as_view(template_name='privacy.html'), name="banyan-privacy"),
    url('^copyright/$', TemplateView.as_view(template_name='copyright.html'), name="banyan-copyright"),
    url('^terms/$', TemplateView.as_view(template_name='terms.html'), name="banyan-terms")
)

urlpatterns += patterns("",
     url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^404/$', 'django.views.defaults.page_not_found'),
		url(r'^500/$', 'core.views.server_error'),
	)
