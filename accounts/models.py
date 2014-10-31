import re
import logging
import sys
import pdb

from facebook import GraphAPI
from jsonfield import JSONField

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.cache import cache

# Get an instance of a logger
logger = logging.getLogger(__name__)
    
class BanyanUser(AbstractUser):
    '''
    Cache keys
    These are the cache keys related to this model
    '''
    FB_FRIENDS_CACHE_KEY = 'fbfriends'
    
    '''
    Constant strings
    '''
    ANONYMOUS_USER_STRING = 'anon'

    notifications = generic.GenericRelation('accounts.models.BanyanUserNotifications') # Needed so that when the object is deleted, the relationship is also deleted

    def get_details_for_profile_from_user(self, requesting_user, **kwargs):
        '''
        For the details, we need:
        1. Cover pic
        2. Profile pic
        3. Location if available
        More details about usage from core.models     
        '''
        access_token = self.social_auth.get(provider="facebook").extra_data.get("access_token")
        graph = GraphAPI(access_token)
        details_dict = {}
        try:
            info = graph.get_object("me", fields="picture, cover, location")
            details_dict['picture'] = info.get('picture', {}).get('data', {}).get('url', None)
            details_dict['cover'] = info.get('cover', {}).get('source', None)
            details_dict['location'] = info.get('location', {}).get('name', None)
            return details_dict
        except:
            logger.error("accounts.models.BanyanUser:get_details_for_profile_from_user {}{} access_token:{}".format(sys.exc_info()[0], sys.exc_info()[1], access_token))
            return []
        
    def get_my_facebook_friends(self):
        access_token = self.social_auth.get(provider="facebook").extra_data.get("access_token")
        cache_key = '%s:%s' % (str(self.id), BanyanUser.FB_FRIENDS_CACHE_KEY)
        '''
        First try to get the friend's list from cache if available
        If not, do a network request
        '''
        my_friends = cache.get(cache_key)
        if my_friends is None:
            try:
                from facebook import GraphAPI
                graph = GraphAPI(access_token)
                result = graph.get_connections("me", "friends")
                my_friends = result.get('data', [])
                cache.set(cache_key, my_friends, 3600) # 1 hour timeout
            except:
                logger.error("accounds.models.BanyanUser:get_my_facebook_friends:GraphAPI err {}{} user:{}".format(sys.exc_info()[0], sys.exc_info()[1], self.id))
                return []
        return my_friends
    
    def get_my_facebook_friends_on_banyan(self):       
        try:
            my_friends = self.get_my_facebook_friends()
            get_id = lambda x : x.get('id', None)
            return BanyanUser.objects.filter(social_auth__provider="facebook", social_auth__uid__in=map(get_id, my_friends))
        except BanyanUser.DoesNotExist:
            logger.info("User {} has no friends on Banyan".format(self))
            return []
        except:
            logger.error("accounts.models.BanyanUser:get_my_facebook_friends_on_banyan {}{} user:{}".format(sys.exc_info()[0], sys.exc_info()[1], self.id))
            return []

    def get_my_facebook_friends_on_banyan_values(self):       
        try:
            my_friends_in_banyan = self.get_my_facebook_friends_on_banyan()
            if my_friends_in_banyan:
                return my_friends_in_banyan.extra(select={'facebook_id': 'SELECT uid FROM social_auth_usersocialauth WHERE social_auth_usersocialauth.id = accounts_banyanuser.id'}).values('first_name', 'last_name', 'email', 'id', 'facebook_id')
            else:
                return []
        except:
            logger.error("accounts.models.BanyanUser:get_my_facebook_friends_on_banyan_values {}{} user:{}".format(sys.exc_info()[0], sys.exc_info()[1], self.id))
            return []

    @classmethod
    def user_with_facebook_id(cls, fbid=None):
        try:
            u = cls.objects.get(social_auth__provider="facebook", social_auth__uid=fbid)
            return u
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            logger.error("accounts.models.user_with_facebook_id. User with facebook id {} has multiple results".format(fbid))
            return None
        except:
            logger.error("accounts.models.user_with_facebook_id. Unknown error {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
            return None

class BanyanUserDevices(models.Model):
    # Information about user devices
    device_token = models.CharField(max_length=200, primary_key=True)
    type = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    user = models.ForeignKey(BanyanUser, related_name='installations')
    '''
    These push endpoint types should be similar to the ones used in mobile
    '''
    INVITED_TO_CONTRIBUTE = 'InvitedToContribute'
    INVITED_TO_VIEW = 'InvitedToView'
    PIECE_ADDED = 'PieceAdded'
    PIECE_ACTION = 'PieceAction'
    USER_FOLLOWING = 'UserFollowing'
    push_endpoints = JSONField(null=True, blank=True)
        
    def __unicode__(self):
        return u'user: {} type {} endpoints {}'.format(self.user.get_full_name(), self.type, self.push_endpoints)

class BanyanUserNotifications(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(BanyanUser, related_name = 'notifications', null=False, blank=False, db_index=True)
    from_user = models.ForeignKey(BanyanUser, related_name = '+', null=True, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    activity = models.ForeignKey('core.Activity', null=True, blank=True)
    description = models.CharField(max_length=500)
    '''
    Notification types
    '''
    LIKE_NOTIF = 'like'
    FOLLOW_NOTIF = 'follow'
    JOIN_NOTIF = 'join'
    STORY_STARTED_NOTIF = 'story_start'
    PIECE_ADDED_NOTIF = 'piece_add'
    VIEW_INVITE_NOTIF = 'view_inv'
    CONTRIB_INVITE_NOTIF = 'contrib_inv'
    
    NOTIFICATION_TYPE_CHOICES = (
                             (LIKE_NOTIF, 'loves the piece'),
                             (FOLLOW_NOTIF, 'is following'),
                             (JOIN_NOTIF, 'has joined Banyan'),
                             (STORY_STARTED_NOTIF, 'has started story'),
                             (PIECE_ADDED_NOTIF, 'has added piece'),
                             (VIEW_INVITE_NOTIF, 'has invited you to read'),
                             (CONTRIB_INVITE_NOTIF, 'has invited you to contribute to')
                             )
    type = models.CharField(max_length = 20, choices=NOTIFICATION_TYPE_CHOICES, db_index=True)
    '''
    Cache keys
    These are the cache keys related to this model
    '''
    class Meta:
        unique_together = ('user', 'from_user', 'object_id', 'content_type', 'type')
        ordering = ['-createdAt']

    def __unicode__(self):
        return u"{from_user} {verb} {object}".format(from_user = self.from_user.get_full_name(), verb=self.get_type_display(), object=unicode(self.content_object))
    
    @classmethod
    def bulk_save_all(cls, notifications=[]):
        for notification in notifications:
            try:
                notification.save()
            except IntegrityError:
                continue
            except:
                logger.info("accounts.models.BanyanUserNotifications::bulk_save_all error {} {} in creating notification".format(sys.exc_info()[0], sys.exc_info()[1]))
                continue