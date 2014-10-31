import ast
import logging
import sys
import pdb

from jsonfield import JSONField

from django.db import models
from django.core.exceptions import MultipleObjectsReturned
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify, truncatechars
from django.core.cache import cache

from accounts.models import BanyanUser, BanyanUserNotifications
from content_feedback.models import FlaggedObject, HiddenObject
from access_groups.models import AccessGroup

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Activity(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(BanyanUser, null=True, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    '''
    These activities should be similar to the ones used in the mobile app
    '''
    LIKE = 'like'
    FOLLOW_USER = 'followUser'
    FOLLOW_STORY = 'followStory'
    VIEW = 'view'
    ACTIVITY_TYPE_CHOICES = (
                             (LIKE, 'like'),
                             (FOLLOW_USER, 'following user'),
                             (FOLLOW_STORY, 'following story'),
                             (VIEW, 'view')
                             )
    type = models.CharField(max_length = 20, choices=ACTIVITY_TYPE_CHOICES, db_index=True)
    '''
    Cache keys
    These are the cache keys related to this model
    '''
    class Meta:
        unique_together = ('user', 'object_id', 'content_type', 'type')
        
    def __unicode__(self):
        return u'{} from user {} for object {}'.format(self.get_type_display(), self.user, self.content_object)

class RemoteObject(models.Model):
    # Class than encapusulates common information between story and piece
    bnObjectId = models.AutoField(primary_key=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    isLocationEnabled = models.BooleanField(default=False)
    location = JSONField(null=True, blank=True)
    author = models.ForeignKey(BanyanUser, related_name="%(app_label)s_%(class)s_author")
    contributors = models.ManyToManyField(BanyanUser, null=True, blank=True, related_name="%(app_label)s_%(class)s_contributors")
    timeStamp = models.IntegerField(db_index=True)
    tags = models.CharField(max_length=500, null=True, blank=True)
    flags = generic.GenericRelation(FlaggedObject)
    activities = generic.GenericRelation(Activity)
    notifications = generic.GenericRelation(BanyanUserNotifications) # Needed so that when the object is deleted, the relationship is also deleted
    
    class Meta:
        abstract = True

    def is_flagged(self, user):
        if not user.is_authenticated() or user.id != self.author.id:
            # If the user is not the author, only allow to read if the
            # piece is not flagged.
            # We only allow the author to read the piece because it is
            # his name on the piece
            cache_key = '%s:%s:%s'%(self.__class__.__name__, str(self.pk), FlaggedObject.FLAGGED_OBJECT_COUNT_CACHE_KEY)
            flags_count = cache.get(cache_key)
            if flags_count is None:
                flags_count = self.flags.filter(resolved=False).count()
                cache.set(cache_key, flags_count, None) # timeout forever
            if flags_count >= FlaggedObject.FLAGGED_OBJECT_MAX_REVIEWS_BEFORE_HIDING_OBJECT:
                return True
        
        return False

class Story(RemoteObject):
    # Story information class
    title = models.CharField(max_length=200)
    readAccess = JSONField()
    writeAccess = JSONField()
    media = JSONField(null=True, blank=True)
    permittedGroups = models.ManyToManyField(AccessGroup, null=True, blank=True, related_name="stories", through="StoryGroupAccess")
    permittedUsers = models.ManyToManyField(BanyanUser, null=True, blank=True, related_name="stories", through="StoryUserAccess")
    
    '''
    Cache keys
    These are the cache keys related to this model
    '''
    
    class Meta(RemoteObject.Meta):
        ordering = ['-timeStamp']
                
    def __unicode__(self):
        return u'%s' % (self.title)

    def can_read_story(self, user):
        '''
        Check if the user has the permission to read the story
        '''
        # Nobody can see a flagged story until it is resolved
        if self.is_flagged(user):
            return False
        
        if user.is_authenticated():
            try:
                storyuseraccess = StoryUserAccess.objects.get(story=self, user=user)
            except StoryUserAccess.DoesNotExist:
                return False
            return storyuseraccess.canRead
        else:
            return self.is_public()

    def can_edit_story(self, user):
        '''
        Check if the user has the permission to edit the story
        '''
        if user.is_authenticated():
            try:
                storyuseraccess = StoryUserAccess.objects.get(story=self, user=user)
            except StoryUserAccess.DoesNotExist:
                return False
            return storyuseraccess.canWrite
        else:
            return False

    def is_public(self):
        '''
        See if this story is public or not
        '''
        public_groupdesc, created = PublicGroupDesc.objects.get_or_create()
        publicgroup = public_groupdesc.group()
        try:
            storygroupaccess = StoryGroupAccess.objects.get(story=self, group=publicgroup)
        except StoryGroupAccess.DoesNotExist:
            return False
        return storygroupaccess.canRead

    def object_slug(self, length):
        slug = slugify(truncatechars(self.title, length))
        return (slug) if len(slug) > 0 else slugify("no description")

class StoryAccess(models.Model):
    canRead = models.BooleanField(default=False)
    canWrite = models.BooleanField(default=False)
    isInvited = models.BooleanField(default=False)
    lastUpdated = models.DateTimeField(auto_now = True)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def set_perms(self, canRead = False, canWrite = False, isInvited = False):
        self.canRead = canRead
        self.canWrite = canWrite
        self.isInvited = isInvited
        self.save()

    def api_dict(self):
        return {'canRead': self.canRead, 'canWrite':self.canWrite, 'isInvited':self.isInvited}

class StoryGroupAccess(StoryAccess):
    '''
    Through field for group access to a story
    '''
    story = models.ForeignKey(Story, null=False, blank=False)
    group = models.ForeignKey(AccessGroup, null=False, blank=False)
    
    class Meta(StoryAccess.Meta):
        unique_together = ('group', 'story')

    def __unicode__(self):
        return u"StoryGroupAccess for group {} and story {}".format(self.group, self.story)
    
class StoryUserAccess(StoryAccess):
    '''
    Through field for user access to a story
    '''
    story = models.ForeignKey(Story, null=False, blank=False)
    user = models.ForeignKey(BanyanUser, null=False, blank=False)
    
    class Meta(StoryAccess.Meta):
        unique_together = ('user', 'story')

    def __unicode__(self):
        return u"StoryUserAccess for user {} and story {}".format(self.user, self.story)

    def recalculate_permissions(self, ignore_groups=[]):
        '''
        Recalculates the permissions based on the group permissions
        TODO: Need to hide it from the user if story is flagged or hidden
        '''
        user_groups = self.user.access_groups.all()
        story_groups = self.story.permittedGroups.all()
        relevant_groups = story_groups.filter(pk__in = user_groups)
        self.canRead = False
        self.canWrite = False
        self.isInvited = False
        for group in relevant_groups:
            if group in ignore_groups:
                continue
            try:
                storygroupaccess = StoryGroupAccess.objects.get(story = self.story, group = group)
            except StoryGroupAccess.DoesNotExist:
                logger.error('core.models.StoryUserAccess.recalculate_permissions:\nError {} shouldnt have been newly created'.format(storygroupaccess))
                continue
            self.canRead = self.canRead or storygroupaccess.canRead
            self.canWrite = self.canWrite or storygroupaccess.canWrite
            self.isInvited = self.isInvited or storygroupaccess.isInvited
        if self.canRead:
            self.save()
        else:
            self.delete()
        
class Piece(RemoteObject):
    # Piece information class
    shortText = models.TextField(null=True, blank=True)
    longText = models.TextField(null=True, blank=True)
    story = models.ForeignKey(Story, related_name='pieces')
    media = JSONField(null=True, blank=True)        

    class Meta(RemoteObject.Meta):
        ordering = ['timeStamp']
    
    #Note unicode is also used to create notifications description
    def __unicode__(self):
        return u'{}'.format(self.piece_description(12))
    
    def can_read_piece(self, user):
        if self.is_flagged(user):
            return False
        return self.story.can_read_story(user)
    
    def can_edit_piece(self, user):
        return self.story.can_edit_story(user)
    
    def piece_description(self, length):
        desc = ''
        if self.shortText:
            desc = self.shortText
        elif self.longText:
            desc = self.longText
        else:
            pass
        return (desc[:length-2] + '..') if len(desc) > length else desc
    
    def object_slug(self, length):
        slug = slugify(self.piece_description(length))
        return (slug) if len(slug) > 0 else slugify("no description")
        
    @classmethod
    def usage_details_of_user(cls, requested_user, requesting_user, **kwargs):
        '''
        For details, we need-
        1. Number of stories by this user
        2. Number of pieces by this user
        3. List of stories authored by this user that the requesting_user can see   
        '''
        num_stories = Story.objects.filter(author=requested_user).count()
        num_pieces = Piece.objects.filter(author=requested_user).count()
        return {'num_stories':num_stories, 'num_pieces':num_pieces}