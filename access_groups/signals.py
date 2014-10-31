import pdb
import logging
import sys

from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

from access_groups.models import GroupMembership
from access_groups.tasks import clean_stale_access

# Get an instance of a logger
logger = logging.getLogger(__name__)

@receiver(post_save, sender=GroupMembership)
def groupmembership_post_save(sender, **kwargs):
    '''
    Signal when a new user is added to the group.
    Provide the user with permissions to all the stories that belongs to this group
    '''
    from core.models import StoryUserAccess
    groupmembership = kwargs.get('instance')
    group = groupmembership.group
    user = groupmembership.user
    stories = group.stories.all()
    for story in stories:
        storyuseraccess, created = StoryUserAccess.objects.get_or_create(story = story, user = user)
        storyuseraccess.recalculate_permissions()

@receiver(pre_delete, sender=GroupMembership)
def groupmembership_pre_delete(sender, **kwargs):
    '''
    Signal when a user is removed from a group.
    Permissions to all the stories that this group has access to is revoked
    '''
    from core.models import StoryUserAccess
    groupmembership = kwargs.get('instance')
    group = groupmembership.group
    user = groupmembership.user
    stories = group.stories.all()
    for story in stories:
        storyuseraccess, created = StoryUserAccess.objects.get_or_create(story = story, user = user)
        storyuseraccess.recalculate_permissions()