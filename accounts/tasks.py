from __future__ import absolute_import

import pdb
import logging
import sys

from celery import shared_task
from celery.contrib import rdb

from django.db import IntegrityError

from core.models import Story, Piece, Activity
from accounts.models import BanyanUser, BanyanUserNotifications, BanyanUserDevices
from access_groups.models import AccessGroup, GroupMembership, SoloGroupDesc, FbFriendOfGroupDesc, PublicGroupDesc
from utils.aws import sns_send_push_notification_to_user

# Get an instance of a logger
logger = logging.getLogger(__name__)

@shared_task
def update_user_groups(user):
    '''
    Update all the groups this user belongs to. These include:
    1. public group
    2. solo group (with fbid, userid)
    3. FacebookFriendsOf group of this user's friends
    '''
    user_groups_id = []
    # 1. Public group
    public_groupdesc, created = PublicGroupDesc.objects.get_or_create()
    membership, created = GroupMembership.objects.get_or_create(user=user, group = public_groupdesc.group())
    user_groups_id.extend([public_groupdesc.group().pk])
    
    # 2. Solo group
    # Get a group with the user's credentials, and then update with userid
    user_fb_id = user.social_auth.get(provider='facebook').uid
    solo_groupdesc, created = SoloGroupDesc.objects.get_or_create(fb_id = user_fb_id)
    solo_groupdesc.user_id = user.pk
    solo_groupdesc.save()
    membership, created = GroupMembership.objects.get_or_create(user=user, group = solo_groupdesc.group())
    user_groups_id.extend([solo_groupdesc.group().pk])
    
    # 3. FacebookFriendsOF groups
    my_fb_friends = user.get_my_facebook_friends()
    for fb_friend in my_fb_friends:
        fb_id = fb_friend.get('id', None)
        if not fb_id:
            # There is a problem, send an email
            logger.error("accounts.tasks.update_user_groups :1 no facebook id in {}".format(fb_friend))
        facebookfriendsof_groupdesc, created = FbFriendOfGroupDesc.objects.get_or_create(fb_id = fb_id)
        membership, created = GroupMembership.objects.get_or_create(user=user, group = facebookfriendsof_groupdesc.group())
        user_groups_id.extend([facebookfriendsof_groupdesc.group().pk])
        
    # Remove membership to stale user groups
    stale_group_membership = GroupMembership.objects.filter(user = user).exclude(group__pk__in = user_groups_id)
    stale_group_membership_count = stale_group_membership.count()
    if stale_group_membership_count > 0:
        print "Removing {} stale group membership for user {}".format(stale_group_membership_count, user)
    stale_group_membership.delete()
    
@shared_task
def new_user(user):
    """
    A new user has been created

    This is a new user.
    Create a notification for this user's friends
    """
    new_notifications = []
    
    my_byn_friends = user.get_my_facebook_friends_on_banyan()
    for friend in my_byn_friends:
        description = "{from_user} joined Banyan".format(from_user = user.get_full_name())
        notif = BanyanUserNotifications(from_user = user,
                                        user = friend,
                                        description = description,
                                        type = BanyanUserNotifications.JOIN_NOTIF,)
        new_notifications.extend([notif])
        pass
    BanyanUserNotifications.bulk_save_all(new_notifications)

@shared_task
def like_notif(notification):
    """
    A like notification is created
    """
    # Push notification sent in core.new_activity
    pass

@shared_task
def inv_contribute_notif(notification):
    """
    A notification about invitation to contribute is created
    """
    if not isinstance(notification.content_object, Story):
        logger.error("accounts.tasks.inv_contribute_notif error Invalid object %s for Invited to view notification" % (notification.content_object.__class__.__name__))
        raise ValueError("Invalid object %s for Invited to contribute notification" % (notification.content_object.__class__.__name__))

    story = notification.content_object
    user = notification.user
    message = "{} has invited you to contribute to story {}!".format(story.author.get_full_name(), story.title)
    dataInSns = {'story':story.bnObjectId}
    sns_send_push_notification_to_user(endpoint=BanyanUserDevices.INVITED_TO_CONTRIBUTE, message=message, data=dataInSns, user=user)
    try:
        Activity.objects.create(content_object = story, user = user, type = Activity.FOLLOW_STORY)
    except IntegrityError as e:
        logger.info("accounts.tasks.inv_contribute_notif info Integrity error when saving follow activity story: {} user: {}".format(story, user))
    except:
        logger.error("accounts.tasks.inv_contribute_notif error {} {} ".format(sys.exc_info()[0], sys.exc_info()[1]))

@shared_task
def inv_view_notif(notification):
    """
    A notification about invitation to view is created
    """
    if not isinstance(notification.content_object, Story):
        logger.error("accounts.tasks.inv_view_notif error Invalid object %s for Invited to view notification" % (notification.content_object.__class__.__name__))
        raise ValueError("Invalid object %s for Invited to view notification" % (notification.content_object.__class__.__name__))

    story = notification.content_object
    user = notification.user
    message = "{} has invited you to view the story {}!".format(story.author.get_full_name(), story.title)
    dataInSns = {'story':story.bnObjectId}
    sns_send_push_notification_to_user(endpoint=BanyanUserDevices.INVITED_TO_VIEW, message=message, data=dataInSns, user=user)
    try:
        Activity.objects.create(content_object = story, user = user, type = Activity.FOLLOW_STORY)
    except IntegrityError as e:
        logger.info("accounts.tasks.inv_view_notif info Integrity error when saving follow activity story: {} user: {}".format(story, user))
    except:
        logger.error("accounts.tasks.inv_view_notif error {} {} ".format(sys.exc_info()[0], sys.exc_info()[1]))
        
@shared_task
def piece_add_notif(notification):
    """
    A notification about a piece being added is created
    """
    piece = notification.content_object
    story = piece.story
    user= notification.user

    message = "{} has added a new piece to the story {}!".format(piece.author.get_full_name(), story.title)
    dataInSns = {'story':story.bnObjectId, 'piece':piece.bnObjectId}
    sns_send_push_notification_to_user(endpoint=BanyanUserDevices.PIECE_ADDED, message=message, data=dataInSns, user=user)

@shared_task
def story_start_notif(notification):
    """
    A notification about a user starting a new story
    """
    if not isinstance(notification.content_object, Story):
        logger.error("accounts.tasks.story_start_notif error Invalid object %s for Invited to view notification" % (notification.content_object.__class__.__name__))
        raise ValueError("Invalid object %s for Story start notification" % (notification.content_object.__class__.__name__))

    story = notification.content_object
    user = notification.user
    message = "{} has started a new story {}!".format(story.author.get_full_name(), story.title)
    dataInSns = {'story':story.bnObjectId}
    sns_send_push_notification_to_user(endpoint=BanyanUserDevices.INVITED_TO_VIEW, message=message, data=dataInSns, user=user)
    try:
        Activity.objects.create(content_object = story, user = user, type = Activity.FOLLOW_STORY)
    except IntegrityError as e:
        logger.info("accounts.tasks.story_start_notif info Integrity error when saving follow activity story: {} user: {}".format(story, user))
    except:
        logger.error("accounts.tasks.story_start_notif error {} {} ".format(sys.exc_info()[0], sys.exc_info()[1]))