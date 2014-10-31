from django import template
from django.conf import settings
from core.models import Story, Piece

import logging
import sys
import pdb

# Get an instance of a logger
logger = logging.getLogger(__name__)
register = template.Library()

@register.filter
def piece_slug(value, arg):
    piece_id = value.get('bnObjectId')
    piece = Piece.objects.get(pk=piece_id)
    return piece.object_slug(arg)