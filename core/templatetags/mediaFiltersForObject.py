from django import template
from django.conf import settings
from core.models import Story, Piece
from accounts.models import BanyanUser
from random import randrange

import logging
import sys

# Get an instance of a logger
logger = logging.getLogger(__name__)
register = template.Library()

@register.filter
def imageUrlForObject(value):
    medias = value.get("media", None)
    if medias is not None:
        for media in medias:
            if media.get("mediaType", None) == "image":
                # this is an image media, return the url
                return media.get("url", None)
    return None

@register.filter
def thumbnailUrlForObject(value):
    medias = value.get("media", None)
    if medias is not None:
        for media in medias:
            if media.get("mediaType", None) == "image":
                # this is a thumbnail of image media, return the url
                return media.get("thumbnailURL", None)
    return None

class ListImageForObjectNode(template.Node):
    def __init__(self, media_object, large_mode):
        self.media_object = template.Variable(media_object)
        self.large_mode = template.Variable(large_mode)
    def render(self, context):
        _media_object = self.media_object.resolve(context)
        medias = _media_object.get("media", None)
        media_context = {}
        if medias is not None:
            for media in medias:
                if media.get("mediaType", None) == "image":
                    media_context['url'] = media.get("url", None)

                    if self.large_mode.resolve(context):
                        _height = 522
                    else:
                        _height = 256
                    media_context['height'] = _height
                    media_context['width'] = _height
                    media_context['thumb_dimensions'] = "%sx%s" % (_height, _height)

        context['cover'] = media_context
        return ''

@register.tag(name="list_image_for_object")
def list_image_for_object(parser, token):
    try:
        tag_name, story, large_mode = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return ListImageForObjectNode(story, large_mode)

@register.filter
def audioUrlForObject(value):
    medias = value.get("media", None)
    if medias is not None:
        for media in medias:
            if media.get("mediaType", None) == "audio":
                # this is an image media, return the url
                return media.get("url", None)
    return None

@register.filter
def contributorStringForStory(value):
    try:
        if 'pieces' not in value:
            # This is not a story object
            return None
        id = value['bnObjectId']
        story = Story.objects.get(bnObjectId=id)
        contributors = []
        contributors.append(story.author.get_full_name())
        for piece in story.pieces.all():
            if piece.author.get_full_name() not in contributors:
                contributors.append(piece.author.get_full_name())
        return ", ".join(contributors)
    except:
        logger.error("core.templatetags.contributorStringForStory {}{} object:{}".format(sys.exc_info()[0], sys.exc_info()[1], value))
        return None
