import pdb
import logging
import sys

from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from core.models import Story, Piece, Activity, RemoteObject, StoryGroupAccess, StoryUserAccess
from core.tasks import delete_media, story_permission_notifications, new_piece, new_activity, update_story_access
from accounts.models import BanyanUser

# Get an instance of a logger
logger = logging.getLogger(__name__)

def remoteobject_pre_delete(object):
    medias = object.media
    for media in medias:
        delete_media.delay(media)

@receiver(pre_save, sender=Story)
def story_pre_save(sender, **kwargs):
    story = kwargs.get('instance')
    if not story.pk:
        """ This is probably a new story """
        """ Don't do anything here """
        return
    
    """ Get the old instance from the database """
    oldStory = Story.objects.get(pk=story.pk)
    if not oldStory:
        """ 
        There was no copy of old story in the database. This is probably a new story 
        Let the post_save signal handle new signals for now
        """
        return

    """ 
    This is a PUT. Check if the permissions have changed, and if so, invalidate the userPermissions for this story
    """
    old_user_read_permissions = oldStory.readAccess
    new_user_read_permissions = story.readAccess
    old_user_write_permissions = oldStory.writeAccess
    new_user_write_permissions = story.writeAccess
    if not (cmp(old_user_read_permissions, new_user_read_permissions) == 0 and cmp(old_user_write_permissions, new_user_write_permissions) == 0):
        update_story_access.delay(story)
        # Queue the task to calculate and update permissions
        story_permission_notifications.delay(story = story)

@receiver(post_save, sender=Story)
def story_post_save(sender, **kwargs):
    """
    A signal for sending push notification to contributors and viewers
    """
    if kwargs.get('created') is False:
        return

    story = kwargs.get('instance')
        
    update_story_access.delay(story)

    # Queue the task to calculate and update permissions
    story_permission_notifications.delay(story = story)
    
    # Create an activity for the current user to follow the story
    new_activities = [Activity(content_object = story, user = story.author, type = Activity.FOLLOW_STORY)]
    # Story author has already viewed the story
    new_activities.extend([Activity(content_object = story, user = story.author, type = Activity.VIEW)])
    Activity.objects.bulk_create(new_activities)

@receiver(pre_delete, sender=Story)
def story_pre_delete(sender, **kwargs):
    story = kwargs.get('instance')
    remoteobject_pre_delete(story)

@receiver(post_save, sender=StoryGroupAccess)
def storygroupaccess_post_save(sender, **kwargs):
    '''
    Signal when a new group is given access to a story.
    All the user's in this group are given the relevant permission
    '''
    storygroupaccess = kwargs.get('instance')
    group = storygroupaccess.group
    story = storygroupaccess.story
    users = group.users.all()
    for user in users:
        storyuseraccess, created = StoryUserAccess.objects.get_or_create(story = story, user = user)
        storyuseraccess.canRead = storyuseraccess.canRead or storygroupaccess.canRead
        storyuseraccess.canWrite = storyuseraccess.canWrite or storygroupaccess.canWrite
        storyuseraccess.isInvited = storyuseraccess.isInvited or storygroupaccess.isInvited
        storyuseraccess.save()

@receiver(pre_delete, sender=StoryGroupAccess)
def storygroupaccess_pre_delete(sender, **kwargs):
    '''
    Signal when a story revokes access to a group
    The permission for all the user's in the group is revoked
    '''
    storygroupaccess = kwargs.get('instance')
    group = storygroupaccess.group
    story = storygroupaccess.story
    users = group.users.all()
    for user in users:
        storyuseraccess, created = StoryUserAccess.objects.get_or_create(story = story, user = user)
        storyuseraccess.recalculate_permissions(ignore_groups=[group])

@receiver(post_save, sender=Piece)
def piece_post_save(sender, **kwargs):
    """
    A signal for sending push notification to contributors and viewers about a new piece
    """
    if kwargs.get('created') is False:
        return

    piece = kwargs.get('instance')
    new_piece.delay(piece)

    # Piece author has already viewed the piece
    Activity.objects.create(content_object = piece, user = piece.author, type = Activity.VIEW)

@receiver(pre_delete, sender=Piece)
def piece_pre_delete(sender, **kwargs):
    piece = kwargs.get('instance')
    remoteobject_pre_delete(piece)

@receiver(post_save, sender=Activity)
def activity_post_save(sender, **kwargs):
    activity = kwargs.get('instance')

    if kwargs.get('created') is False:
        raise ValueError("Activity can not be edited")

    new_activity.delay(activity)