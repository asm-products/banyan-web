from content_feedback.models import HiddenObject, FlaggedObject
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from accounts.models import BanyanUser
from django.core.cache import cache
import pdb

@receiver(post_save, sender=FlaggedObject)
def flagged_object_post_save(sender, **kwargs):
    # if a new object has been set hidden, clear the cache for the user
    flagged_object = kwargs.get('instance')
    delete_flagged_object_caches(flagged_object)

@receiver(post_delete, sender=FlaggedObject)
def flagged_object_post_delete(sender, **kwargs):
    # if a new object has been set hidden, clear the cache for the user
    flagged_object = kwargs.get('instance')
    delete_flagged_object_caches(flagged_object)

'''
Warning: This is also called from post_delete signal so be careful
about what you do with the flagged_object
'''
def delete_flagged_object_caches(flagged_object):
    cache_key = '%s:%s:%s'%(flagged_object.content_object.__class__.__name__, str(flagged_object.pk), FlaggedObject.FLAGGED_OBJECT_COUNT_CACHE_KEY)
    cache.delete(cache_key)

@receiver(post_save, sender=HiddenObject)
def hidden_object_post_save(sender, **kwargs):
    # if a new object has been set hidden, clear the cache for the user
    hidden_object = kwargs.get('instance')
    delete_hidden_object_caches(hidden_object)
    
@receiver(post_delete, sender=HiddenObject)
def hidden_object_post_delete(sender, **kwargs):
    # if a new object has been set hidden, clear the cache for the user
    hidden_object = kwargs.get('instance')
    delete_hidden_object_caches(hidden_object)

'''
Warning: This is also called from post_delete signal so be careful
about what you do with the hidden_object
'''
def delete_hidden_object_caches(hidden_object):
    cache_key = '%s:%s' % (str(hidden_object.user.id), HiddenObject.HIDDEN_STORIES_ID_LIST_CACHE_KEY)
    cache.delete(cache_key)