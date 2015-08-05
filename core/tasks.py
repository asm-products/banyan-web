from __future__ import absolute_import

import pdb
import logging
import sys

from celery import shared_task

from utils.aws import sns_send_push_notification_to_user, s3_delete_object_with_key
from core.models import Story, Piece, Activity, RemoteObject, StoryGroupAccess, StoryUserAccess
from accounts.models import BanyanUser, BanyanUserDevices, BanyanUserNotifications
from access_groups.models import AccessGroup, GroupMembership, SoloGroupDesc, FbFriendOfGroupDesc, PublicGroupDesc

# Get an instance of a logger
logger = logging.getLogger(__name__)

@shared_task
def delete_media(media):
    """
    Delete the media and related resources from S3
    """
    key = media.get('filename', None)
    if key:
        s3_delete_object_with_key(key)
    key = media.get('thumbnailfilename', None)
    if key:
        s3_delete_object_with_key(key)
        
@shared_task
def story_permission_notifications(story = None):
    """
    Check the permissions of the story and send notifications accordingly
    """
    
    # To bulk create new notifications for "createStory"
    new_notifications = []
    
    contributors_fb = story.writeAccess.get('inviteeList').get('facebookFriends', [])
    contributors_fb_ids = [contributors['id'] for contributors in contributors_fb if 'id' in contributors]
    
    viewers_fb = story.readAccess.get('inviteeList').get('facebookFriends', [])
    viewers_fb = [x for x in viewers_fb if x not in contributors_fb]
    viewers_fb_ids = [viewers['id'] for viewers in viewers_fb if 'id' in viewers]

    # Contributors
    for contributor_fb_id in set(contributors_fb_ids):
        user = BanyanUser.user_with_facebook_id(contributor_fb_id)
        if user:
            description = "{from_user} invited you to contribute to story \"{story}\"".format(from_user = story.author.get_full_name(),
                                                                                              story=story.title)
            notif = BanyanUserNotifications(content_object = story, 
                                              from_user = story.author, 
                                              user = user, 
                                              type = BanyanUserNotifications.CONTRIB_INVITE_NOTIF,
                                              description = description)
            new_notifications.extend([notif])
    
    # Viewers
    for viewer_fb_id in set(viewers_fb_ids):
        user = BanyanUser.user_with_facebook_id(viewer_fb_id)
        if user:
            description = "{from_user} invited you to read the story \"{story}\"".format(from_user = story.author.get_full_name(),
                                                                                         story=story.title)
            notif = BanyanUserNotifications(content_object = story, 
                                              from_user = story.author, 
                                              user = user, 
                                              type = BanyanUserNotifications.VIEW_INVITE_NOTIF,
                                              description = description)
            new_notifications.extend([notif])

    # Send notifications to all facebook friends who are already on Banyan
    all_fb_friends = story.readAccess.get('inviteeList').get('allFacebookFriendsOf', [])
    all_fb_friends_ids = [viewers['id'] for viewers in all_fb_friends if 'id' in viewers]
    for viewer_fb_id in all_fb_friends_ids:
        user = BanyanUser.user_with_facebook_id(viewer_fb_id)
        for fb_friend in user.get_my_facebook_friends_on_banyan():
            fb_friend_social_auth = fb_friend.social_auth.filter(provider="facebook").first()
            if not fb_friend_social_auth:
                # User hadn't logged in through facebook
                continue
            if fb_friend_social_auth.uid in viewers_fb_ids or fb_friend_social_auth.uid in contributors_fb_ids:
                # Already sending notifications to this friend.
                continue
            description = "{from_user} has started a new story \"{story}\"".format(from_user = story.author.get_full_name(),
                                                                                    story=story.title)
            notif = BanyanUserNotifications(content_object = story,
                                              from_user = story.author,
                                              user = fb_friend,
                                              type = BanyanUserNotifications.STORY_STARTED_NOTIF,
                                              description = description)
            new_notifications.extend([notif])

    BanyanUserNotifications.bulk_save_all(new_notifications)

@shared_task
def update_story_access(story):
    '''
    Update story access permissions to various groups
    '''

    story_groups_id = []
    isPublic = False
    # Author can read and write.
    # This needs to be done first because if someone else has invited the author, then that can be be set to True
    solo_user_groupdesc, created = SoloGroupDesc.objects.get_or_create(user_id = story.author.pk)
    solo_user_group_access, created = StoryGroupAccess.objects.get_or_create(story = story, group = solo_user_groupdesc.group())
    solo_user_group_access.canRead = True
    solo_user_group_access.canWrite = True
    solo_user_group_access.isInvited = False
    solo_user_group_access.save()
    story_groups_id.extend([solo_user_groupdesc.group().pk])

    ## First read, then write! ##

    inviteeListRd = story.readAccess.get('inviteeList', None)
    # Anyone can read
    if inviteeListRd.get('isPublic', False):
        public_groupdesc, created = PublicGroupDesc.objects.get_or_create() # There is one and only one public group
        group_access, created = StoryGroupAccess.objects.get_or_create(story = story, group = public_groupdesc.group())
        group_access.set_perms(True, False, False)
        isPublic = True
        story_groups_id.extend([public_groupdesc.group().pk])
            
    readFacebookInvitees = inviteeListRd.get('allFacebookFriendsOf', [])
    for item in readFacebookInvitees:
        user_fb_id = item.get('id', None)
        if not user_fb_id:
            # There is a problem, send an email
            logger.error("core.tasks.update_story_access :2 no facebook id in {}".format(item))
        all_fb_groupdesc, created = FbFriendOfGroupDesc.objects.get_or_create(fb_id = user_fb_id)
        all_fb_group_access, created = StoryGroupAccess.objects.get_or_create(story = story, group = all_fb_groupdesc.group())
        all_fb_group_access.set_perms(True, False, False)
        story_groups_id.extend([all_fb_groupdesc.group().pk])
            
    readFacebookInvitees = inviteeListRd.get('facebookFriends', [])
    for item in readFacebookInvitees:
        user_fb_id = item.get('id', None)
        if not user_fb_id:
            # There is a problem, send an email
            logger.error("core.tasks.update_story_access :1 no facebook id in {}".format(item))
        solo_fb_groupdesc, created = SoloGroupDesc.objects.get_or_create(fb_id = user_fb_id)
        solo_fb_group_access, created = StoryGroupAccess.objects.get_or_create(story = story, group = solo_fb_groupdesc.group())
        solo_fb_group_access.set_perms(True, False, True)
        story_groups_id.extend([solo_fb_groupdesc.group().pk])

    inviteeListWr = story.writeAccess.get('inviteeList', None)
    # Anyone can write
    if inviteeListWr.get('isPublic', False):
        public_groupdesc, created = PublicGroupDesc.objects.get_or_create() # There is one and only one public group
        group_access, created = StoryGroupAccess.objects.get_or_create(story = story, group = public_groupdesc.group())
        group_access.set_perms(True, True, False)
        isPublic = True
        story_groups_id.extend([public_groupdesc.group().pk])
            
    # Invite selected facebook friends
    writeFacebookInvitees = inviteeListWr.get('facebookFriends', [])
    for item in writeFacebookInvitees:
        user_fb_id = item.get('id', None)
        if not user_fb_id:
            # There is a problem, send an email
            logger.error("core.tasks.update_story_access :1 no facebook id in {}".format(item))
        solo_fb_groupdesc, created = SoloGroupDesc.objects.get_or_create(fb_id = user_fb_id)
        solo_fb_group_access, created = StoryGroupAccess.objects.get_or_create(story = story, group = solo_fb_groupdesc.group())
        solo_fb_group_access.set_perms(True, True, True)
        story_groups_id.extend([solo_fb_groupdesc.group().pk])

    # Remove access to all groups that are not in story_groups
    stale_group_access = StoryGroupAccess.objects.filter(story = story).exclude(group__pk__in = story_groups_id)
    stale_group_access_count = stale_group_access.count()
    if stale_group_access_count > 0:
        print "Removing {} stale access groups for story {}".format(stale_group_access_count, story)
    stale_group_access.delete()
    
    """
    Commenting this out and living on the edge.
    Instead of doing brute force, make sure that the updates are actually more robust.
    # Some times just updating the groups doesn't update the user permissions,
    # So update the permissions for each user individually
    # This can happen if there is an issue with updating user permissions from groups
    if not isPublic:
        storyuseraccesses = StoryUserAccess.objects.filter(story = story)
        for storyuseraccess in storyuseraccesses:
            storyuseraccess.recalculate_permissions()
    """

@shared_task
def new_piece(piece):
    """
    Send notifications and update story when a new piece is added
    """

    story = piece.story
    
    """
    Update the timeStamp of the story to get the last updated stamp
    """
    if piece.timeStamp > story.timeStamp:
        story.timeStamp = piece.timeStamp
        Story.objects.filter(pk=story.pk).update(timeStamp=piece.timeStamp) # So as not to call pre-save/post-save

    # Create notification for followers
    followActivities = story.activities.filter(type=Activity.FOLLOW_STORY)
    
    """
    No need to dedupe here since follow activities are guaranteed to be unique
    because of the unique constraint in the model
    """
    new_notifications = []
    for followActivity in followActivities:
        user = followActivity.user
        """
        If this is the author of the piece, don't do anything
        """
        if user == piece.author:
            continue

        # Create a notification entries for this follower
        description = "{from_user} has added a new piece \"{piece}\" to the story \"{story}\"".format(from_user = piece.author.get_full_name(),
                                                                                                      piece = piece.piece_description(40),
                                                                                                      story = story.title)
        notif = BanyanUserNotifications(content_object = piece, 
                                          from_user = piece.author, 
                                          user = user, 
                                          type = BanyanUserNotifications.PIECE_ADDED_NOTIF,
                                          description = description)
        new_notifications.extend([notif])
    
    BanyanUserNotifications.bulk_save_all(new_notifications)
    
@shared_task
def new_activity(activity_id):
    """
    Method called when an activity is saved
    """
    try:
        activity = Activity.objects.get(pk=activity_id)
    except Activity.DoesNotExist:
        return

    # We only send notifications for a like activity
    if activity.type == Activity.LIKE:
        """
        A signal for sending push notification to author whose piece was liked
        """
        object = activity.content_object
        
        # The likes can only be for a piece
        if not isinstance(object, Piece):
            return
        
        piece = object
        
        # Don't send a notification if the author himself/herself likes the piece
        if activity.user == piece.author:
            return
        
        # Send the notification now!    
        message = "{} loves your piece- {}!".format(activity.user.get_full_name(), piece.piece_description(20))
        dataInSns = {'story':piece.story.bnObjectId, 'piece':piece.bnObjectId}
    
        sns_send_push_notification_to_user(endpoint=BanyanUserDevices.PIECE_ACTION, message=message, data=dataInSns, user=piece.author)
        
        # Create a notification for the user
        new_notifications = []
        description = "{from_user} loves the piece \"{piece}\"".format(from_user = activity.user.get_full_name(), piece=piece.piece_description(40))
        notif = BanyanUserNotifications(content_object = piece, 
                                          from_user = activity.user, 
                                          user = piece.author, 
                                          type = BanyanUserNotifications.LIKE_NOTIF,
                                          description = description,
                                          activity = activity)
        new_notifications.extend([notif])
        BanyanUserNotifications.bulk_save_all(new_notifications)