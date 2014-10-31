import pdb
import logging
import sys

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import BanyanUser, BanyanUserNotifications
# from accounts.tasks import * # See the warning below

# Warning!! This module is imported in accounts.__init__.py
# This can cause cyclic dependencies since accounts is imported in the other apps as well (core, content_feedback) 
# Be careful as to what project modules are imported here. Otherwise, import them within the methods

# Get an instance of a logger
logger = logging.getLogger(__name__)

@receiver(post_save, sender=BanyanUser)
def banyanuser_post_save(sender, **kwargs):
    from tastypie.models import create_api_key
    from accounts.tasks import new_user, update_user_groups

    user = kwargs.get('instance')
    
    create_api_key(sender, **kwargs)
    
    update_user_groups.delay(user)
    
    if kwargs.get('created') is False:
        return
    
    user = kwargs.get('instance')
    new_user.delay(user)

@receiver(post_save, sender=BanyanUserNotifications)
def banyanusernotifications_post_save(sender, **kwargs):
    """
    Post save when a new notification is created
    
    The notification is guaranteed to be unique for a particular type, object and user.
    Create relevant activities if required, and alert the user through push notifications
    """
    from accounts.tasks import like_notif, inv_contribute_notif, inv_view_notif, piece_add_notif, story_start_notif
    notification = kwargs.get('instance')
    
    if kwargs.get('created') is False:
        raise ValueError("Notifications can not be edited")
    
    try:
        if notification.type == BanyanUserNotifications.LIKE_NOTIF:
            like_notif.delay(notification)
        elif notification.type == BanyanUserNotifications.FOLLOW_NOTIF:
            pass
        elif notification.type == BanyanUserNotifications.JOIN_NOTIF:
            pass
        elif notification.type == BanyanUserNotifications.STORY_STARTED_NOTIF:
            story_start_notif.delay(notification)
        elif notification.type == BanyanUserNotifications.PIECE_ADDED_NOTIF:
            piece_add_notif.delay(notification)
        elif notification.type == BanyanUserNotifications.VIEW_INVITE_NOTIF:
            inv_view_notif.delay(notification)
        elif notification.type == BanyanUserNotifications.CONTRIB_INVITE_NOTIF:
            inv_contribute_notif.delay(notification)
        else:
            raise ValueError("Unknown notification type {}".format(notification.type))
    except:
        logger.error("accounts.signals.banyanusernotifications_post_save error {} {} ".format(sys.exc_info()[0], sys.exc_info()[1]))