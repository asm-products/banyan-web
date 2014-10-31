from django.db import models
from accounts.models import BanyanUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
    
class FlaggedObject(models.Model):
    FLAGGED_OBJECT_MAX_REVIEWS_BEFORE_HIDING_OBJECT = 2
    
    # Class that encapsulates information about a flagged object from the user
    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(BanyanUser, null=True, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    message = models.CharField(max_length=200, null=True, blank=True)
    resolved = models.BooleanField(default=False, blank=True)
    verified = models.BooleanField(default=False, blank=True)
    '''
    Cache keys
    These are the cache keys related to this model
    '''
    FLAGGED_OBJECT_COUNT_CACHE_KEY = 'flagged_object_count'

    def __unicode__(self):
        return u'Flagged object {} from user {} with message {}'.format(self.content_object, self.user, self.message)
    
class HiddenObject(models.Model):
    # Class that encapsulates information about a flagged object from the user
    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(BanyanUser)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    '''
    Cache keys
    These are the cache keys related to this model
    '''
    HIDDEN_STORIES_ID_LIST_CACHE_KEY = 'hidden_stories_id'
    def __unicode__(self):
        return u'Hidden object {} from user {}'.format(self.content_object, self.user)