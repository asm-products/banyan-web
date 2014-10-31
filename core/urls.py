from django.conf import settings
from django.conf.urls import *

from core.views import home, read_story, StorySlugifyRedirectView, PieceSlugifyRedirectView

urlpatterns = patterns("",
        url(r"^feed/$", home, name="home_view"),
        # Piece URLS first before story URLs (since some piece urls have the same pattern as story
        # urls, they can get caught there
        url(r'^p/(?P<piece_id>\d+)/$', PieceSlugifyRedirectView.as_view(), name="piece_short"),
        url(r'^piece/(?P<piece_id>\d+)/$', PieceSlugifyRedirectView.as_view(), name="piece_short"),
        url(r'^story/(?P<story_id>\d+)/piece/(?P<piece_id>\d+)/$', PieceSlugifyRedirectView.as_view()),
        url(r'^story/(?P<story_id>\d+)/piece/(?P<piece_id>\d+)/(?P<slug>\S+)/$', read_story, name="read_piece"),
        url(r'^s/(?P<story_id>\d+)/$', StorySlugifyRedirectView.as_view(), name="story_short"),
        url(r'^story/(?P<story_id>\d+)/$', StorySlugifyRedirectView.as_view()),
        url(r'^story/(?P<story_id>\d+)/(?P<slug>\S+)/$', read_story, name="read_story"),
    )
