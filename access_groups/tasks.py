from __future__ import absolute_import

import pdb
import logging
import sys

from celery import shared_task

from accounts.models import BanyanUser

# Get an instance of a logger
logger = logging.getLogger(__name__)

@shared_task
def clean_stale_access():
    '''
    Syncs accesses to all the stories, and removes stale permissions.
    The most common cause of stale access is if a celery task fails when a story access changes,
    in which case the story groups needs to be fixed.
    '''
    from core.models import Story, StoryGroupAccess, StoryUserAccess
    from core.tasks import update_story_access
    from accounts.tasks import update_user_groups

    # Loop over all users and check for group membership consistency
    for user in BanyanUser.objects.all():
        update_user_groups(user)

    # Loop over all stories and check for group consistency
    for story in Story.objects.all():
        update_story_access(story)