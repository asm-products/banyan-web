import base64
import urllib, urllib2, httplib
import os
import textwrap
import json
import pdb

from datetime import datetime, timedelta
from time import time
from cStringIO import StringIO
from Crypto.Cipher import AES
from Crypto import Random

from django import http
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Context, loader
from django.utils.http import base36_to_int
from django.utils.safestring import mark_safe
from django.utils.translation import check_for_language, ugettext, ugettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.views.generic.base import RedirectView

from core.models import Story, Piece
from api import StoryResource

def home(request):
    template_name = "banyan/index.html"
    res = StoryResource()
    request_bundle = res.build_bundle(request=request)
    queryset = res.cached_obj_get_list(request_bundle)
    bundles = []
    for obj in queryset.iterator():
        bundle = res.build_bundle(obj=obj, request=request)
        bundles.append(res.full_dehydrate(bundle, for_list=True))

    list_json = res.serialize(None, bundles, "application/json")
    list_json = json.loads(list_json)

    paginator = Paginator(list_json, settings.API_DEFAULT_ITEMS_PER_PAGE)
    page = request.GET.get('page')
    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        stories = paginator.page(1)
    except EmptyPage:
        stories = paginator.page(paginator.num_pages)

    return render_to_response( template_name, {'stories':stories},
                               context_instance = RequestContext( request ) )

class StorySlugifyRedirectView(RedirectView):
    query_string = True;
    pattern_name = 'read_story'
    
    def get_redirect_url(self, *args, **kwargs):
        story_id = kwargs.get('story_id', None)
        story = get_object_or_404(Story, pk=story_id)
        slug = story.object_slug(40)
        kwargs['slug'] = slug
        return super(StorySlugifyRedirectView, self).get_redirect_url(*args, **kwargs)
    
class PieceSlugifyRedirectView(RedirectView):
    query_string = True;
    pattern_name = 'read_piece'
    
    def get_redirect_url(self, *args, **kwargs):
        piece_id = kwargs.get('piece_id', None)
        piece = get_object_or_404(Piece, pk=piece_id)
        slug = piece.object_slug(40)
        story = piece.story
        kwargs['story_id'] = story.bnObjectId
        kwargs['slug'] = slug
        return super(PieceSlugifyRedirectView, self).get_redirect_url(*args, **kwargs)
    
def read_story(request, story_id=None, piece_id=None, slug=None):
    """
    Read Story

    Templates: :"banyan/inner.html"
    """
    template_name = "banyan/inner.html"

    res = StoryResource()
    request_bundle = res.build_bundle(request=request)
    
    try:
        storyObj = res.cached_obj_get(request_bundle, **{"bnObjectId":story_id})
        bundle = res.build_bundle(obj=storyObj, request=request)
        story_json = res.serialize(None, res.full_dehydrate(bundle, for_list=False), "application/json")
        story = json.loads(story_json)
    except:
        raise Http404

    ''' TO DO: Permission error seperately '''
#     if story is None or story.get('read', False) is not True:
#         return  render_to_response( "banyan/permission_error.html", context_instance = RequestContext( request ) )

    pieces = story.get('pieces', [])
    piece = None
    next_piece = None
    previous_piece = None
    if len(pieces):
        if piece_id is None:
            next_piece = pieces[0]
        else:
            piece_id = int(piece_id)
            # This is a piece view
            for index, piece in enumerate(pieces):
                if piece.get('bnObjectId') == piece_id:
                    if index > 0:
                        previous_piece = pieces[index-1]
                    if index < len(pieces)-1:
                        next_piece = pieces[index + 1]
                    break
        
    return render_to_response(template_name,
        {'story': story, 'previous_piece':previous_piece, 'piece': piece, 'next_piece':next_piece,},
        context_instance=RequestContext(request))

def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: :template:`500.html`
    Context: None
    """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return http.HttpResponseServerError('<h1>Server Error (500)</h1>')
    return http.HttpResponseServerError(template.render(Context()))

def not_found(request, template_name='404.html'):
    """
    404 error handler.

    Templates: :template:`404.html`
    Context: None
    """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return http.HttpResponseServerError('<h1>404 Error</h1>')
    return http.HttpResponseServerError(template.render(Context()))