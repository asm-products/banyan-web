import ast
import logging
import sys
import pdb

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from accounts.models import BanyanUser

class AccessGroup(models.Model):
    '''
    A concrete class that has a one-to-one relationship with a group descriptor model
    '''
    users = models.ManyToManyField(BanyanUser, related_name="access_groups", through="GroupMembership")
    groupdesc_content_type = models.ForeignKey(ContentType)
    groupdesc_object_id = models.PositiveIntegerField()
    groupdesc_object = generic.GenericForeignKey('groupdesc_content_type', 'groupdesc_object_id')

    class Meta:
        unique_together = ('groupdesc_content_type', 'groupdesc_object_id')
        
    def __unicode__(self):
        return u'Group for {} users in group desc {}'.format(self.users.all().count(), self.groupdesc_object)
    
class GroupMembership(models.Model):
    '''
    Class to have additional information about the membership of a user in a group
    '''
    group = models.ForeignKey(AccessGroup, related_name='memberships')
    user = models.ForeignKey(BanyanUser, related_name='memberships')
    last_updated = models.DateTimeField(auto_now = True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('group', 'user')
        
    def __unicode__(self):
        return u'Membership for user {} in group {}'.format(self.user, self.group)

class AbstractGroupDesc(models.Model):
    '''
    Abstract class to describe the common functionalities of all the other groups
    '''
    class Meta:
        abstract = True
    
    def group(self):
        ctype = ContentType.objects.get_for_model(self)
        mygroup, created = AccessGroup.objects.get_or_create(groupdesc_content_type = ctype, groupdesc_object_id = self.pk)
        return mygroup

class SoloGroupDesc(AbstractGroupDesc):
    '''
    A group descriptor for an individual user. Every user has one and only one Solo group for himself
    '''
    fb_id = models.CharField(max_length = 255, unique = True, null=True, blank=True)
    user_id = models.PositiveIntegerField(unique = True, null=True, blank=True)
    
    class Meta(AbstractGroupDesc.Meta):
        pass
    
    def __unicode__(self):
        return u'GroupDesc for solo user with fbid: {} userid: {}'.format(self.fb_id, self.user_id)
    
class FbFriendOfGroupDesc(AbstractGroupDesc):
    '''
    A group descriptor for all the facebook friends of a user.
    Since facebook friendship is reciprocatory, whether a user belongs to this group or not can be figured out from
    a user's friend list
    '''
    fb_id = models.CharField(max_length = 255,
                             unique = True,
                             help_text = "Facebook Id of user whose friends belong to this group")
    
    class Meta(AbstractGroupDesc.Meta):
        pass
    
    def __unicode__(self):
        return u'GroupDesc of fb friends of user with id {}'.format(self.fb_id)
    
class PublicGroupDesc(AbstractGroupDesc):
    '''
    A group descriptor for everyone. Every user belongs to this group.
    There is one and only one public group
    '''
    class Meta(AbstractGroupDesc.Meta):
        pass

    def __unicode__(self):
        return u'Public GroupDesc'