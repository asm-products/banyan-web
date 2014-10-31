import pdb
import logging
import sys

from tastypie import fields, http
from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication, Authentication, SessionAuthentication, MultiAuthentication
from tastypie.exceptions import NotFound
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from tastypie.utils import trailing_slash

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Max, Count
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.conf.urls import url
from django.contrib.contenttypes.models import ContentType

from core.permissions import StoryAuthorization, PieceAuthorization, ActivityAuthorization
from core.paginator import StoryPaginator
from core.models import RemoteObject, Story, Piece, Activity, StoryUserAccess, StoryGroupAccess
from accounts.views import register_by_access_token
from accounts.models import BanyanUser, BanyanUserNotifications
from accounts.api import BanyanUserResource
from accounts.permissions import BanyanUserNotificationsAuthorization
from content_feedback.models import HiddenObject
from access_groups.models import PublicGroupDesc

# Get an instance of a logger
logger = logging.getLogger(__name__)

class RemoteObjectResource(ModelResource):
    author = fields.ForeignKey('accounts.api.BanyanUserResource', 'author', full=True)
    perma_link = fields.CharField(readonly = True)
    
    class Meta:
        always_return_data = True
        abstract = True
        ordering = ['timeStamp']

    def dehydrate_media(self, bundle):
        return bundle.obj.media
    
    def dehydrate_location(self, bundle):
        return bundle.obj.location
        
class StoryResource(RemoteObjectResource):
    permission = fields.DictField(null=False, blank=False, readonly=True)
    pieces = fields.ToManyField('core.api.PieceResource',
                                attribute="pieces",
                                full=True, null=True, blank=True, readonly=True)
    stats = fields.DictField(null=True, blank=True, readonly = True)
    
    class Meta(RemoteObjectResource.Meta):
        queryset = Story.objects.select_related()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication(), Authentication())
        authorization = StoryAuthorization()
        paginator_class = StoryPaginator

    def get_object_list(self, request):
        story_queryset = Story.objects.none()
        if request.user.is_authenticated():
            story_queryset = request.user.stories.all()
            cache_key = '%s:%s' % (str(request.user.id), HiddenObject.HIDDEN_STORIES_ID_LIST_CACHE_KEY)
            hidden_stories_id_list = cache.get(cache_key)
            if hidden_stories_id_list is None:
                ctype = ContentType.objects.get(app_label="core", model="story", name="story")
                hidden_stories_qs = HiddenObject.objects.filter(content_type = ctype, user = request.user)
                hidden_stories_id_list = hidden_stories_qs.values_list('object_id', flat=True)
                cache.set(cache_key, hidden_stories_id_list, None) # timeout forever
            remaining_stories_qs = story_queryset.exclude(pk__in = hidden_stories_id_list)
            return remaining_stories_qs
        else:
            public_groupdesc, created = PublicGroupDesc.objects.get_or_create()
            publicgroup = public_groupdesc.group()
            story_queryset = publicgroup.stories.all()
        return story_queryset
    
    def dehydrate_pieces(self, bundle):
        piece_bundles = bundle.data.get("pieces")
        user = bundle.request.user
        # pieces is an array
        for piece_bundle in piece_bundles:
            #if this content should not be returned, don't return it
            if piece_bundle.obj.is_flagged(user):
                piece_bundles.remove(piece_bundle)
        return piece_bundles

    def dehydrate_permission(self, bundle):
        story = bundle.obj
        user = bundle.request.user
        if user.is_authenticated():
            try:
                storyuseraccess = StoryUserAccess.objects.get(story=story, user=user)
                return storyuseraccess.api_dict()
            except StoryUserAccess.DoesNotExist:
                return {"canRead":False, "canWrite":False, "isInvited":False}
        else:
            public_groupdesc, created = PublicGroupDesc.objects.get_or_create()
            publicgroup = public_groupdesc.group()
            if (StoryGroupAccess.objects.filter(story=story, group=publicgroup).exists()):
                return {"canRead":True, "canWrite":False, "isInvited":False}
            else:
                return {"canRead":False, "canWrite":False, "isInvited":False}

    def dehydrate_writeAccess(self, bundle):
        return bundle.obj.writeAccess
        
    def dehydrate_readAccess(self, bundle):
        return bundle.obj.readAccess
    
    def dehydrate_perma_link(self, bundle):
        storyId = bundle.obj.bnObjectId
        link = reverse("story_short", args=(storyId,))
        return bundle.request.build_absolute_uri(link)

    def dehydrate_stats(self, bundle):
        # Get the queryset first so that it can be cached
        all_activities = bundle.obj.activities.all()
        numViews = all_activities.filter(type=Activity.VIEW).count()
        followActivityUri = None
        if bundle.request.user.is_authenticated():
            user_activities = all_activities.filter(user = bundle.request.user)
            userViewed = user_activities.filter(type=Activity.VIEW).count() > 0
            try:
                activity = user_activities.get(type=Activity.FOLLOW_STORY)
                activityResource = ActivityResource()
                followActivityUri = activityResource.get_resource_uri(activity)
            except Activity.DoesNotExist:
                followActivityUri = None
            except:
                logger.error("core.api.dehydrate_stats {}{}".format(sys.exc_info()[0], sys.exc_info()[1]))
                pass
        else:
            userViewed = False
        return {"numViews":numViews, "userViewed":userViewed, "followActivity":followActivityUri}
    
class PieceResource(RemoteObjectResource):
    story = fields.ForeignKey(StoryResource, 'story')
    stats = fields.DictField(null=True, blank=True, readonly = True)
    
    class Meta(RemoteObjectResource.Meta):
        queryset = Piece.objects.select_related()
        authentication = MultiAuthentication(ApiKeyAuthentication(),  Authentication())
        authorization = PieceAuthorization()
        filtering = {
                     'story': ALL_WITH_RELATIONS,
                     'user': ALL_WITH_RELATIONS,
                     'timeStamp': ['exact', 'gt', 'gte', 'lt', 'lte', 'range']
                     }
    
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/like%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_piece_likes'), name="api_get_piece_likes"),
        ]
        
    def get_piece_likes(self, request, **kwargs):
        pk = kwargs['pk']
        try:
            bundle = self.build_bundle(data={'pk': pk}, request=request)
            obj = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return http.HttpGone()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        activities_resource = ActivityResource()
        return activities_resource.get_list(request, object_id = pk, content_type = ContentType.objects.get_for_model(bundle.obj), type='like')
        
    def dehydrate_perma_link(self, bundle):
        pieceId = bundle.obj.bnObjectId
        link = reverse("piece_short", args=(pieceId,))
        return bundle.request.build_absolute_uri(link)
    
    def dehydrate_stats(self, bundle):
        # Get the queryset first so that it can be cached
        all_activities = bundle.obj.activities.all()

        numViews = all_activities.filter(type=Activity.VIEW).count()
        numLikes = all_activities.filter(type=Activity.LIKE).count()
        likeActivityUri = None
        if bundle.request.user.is_authenticated():
            user_activities = all_activities.filter(user = bundle.request.user)
            userViewed = user_activities.filter(type=Activity.VIEW).count() > 0
            try:
                activity = user_activities.get(type=Activity.LIKE)
                activityResource = ActivityResource()
                likeActivityUri = activityResource.get_resource_uri(activity)
            except Activity.DoesNotExist:
                likeActivity = None
            except:
                logger.error("core.api.dehydrate_stats {}{}".format(sys.exc_info()[0], sys.exc_info()[1]))
                pass        
        else:
            userViewed = False
        return {"numViews":numViews, "userViewed":userViewed, "numLikes":numLikes, "likeActivity":likeActivityUri}
    
class ActivityResource(ModelResource):
    user = fields.ForeignKey(BanyanUserResource, 'user', full=True)
    content_object = GenericForeignKeyField({
        Story: StoryResource,
        Piece: PieceResource,
        BanyanUser: BanyanUserResource,
    }, 'content_object')

    class Meta:
        always_return_data = True
        queryset = Activity.objects.all()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication(), Authentication())
        authorization = ActivityAuthorization()
        filtering = {
                     'object_id': ALL_WITH_RELATIONS,
                     'content_type': ALL_WITH_RELATIONS,
                     'user': ALL_WITH_RELATIONS,
                     'type': ['exact']
                     }
        
    def hydrate_user(self, bundle):
        if bundle.request.user.is_authenticated():
            bundle.data['user'] = bundle.request.user
        return bundle

'''
This should ideally be in accounts.api. However moving it here since there is
a cyclic dependency which doesn't seem to get resolved.
banyan.url: from core.api import StoryResource, PieceResource, ActivityResource ->
core.api: from accounts.api import BanyanUserResource ->
accounts.api: class BanyanUserNotificationsResource(ModelResource) ->
core.api: import StoryResource, PieceResource
'''
class BanyanUserNotificationsResource(ModelResource):
    user = fields.ForeignKey('accounts.api.BanyanUserResource', 'user')
    from_user = fields.ForeignKey('accounts.api.BanyanUserResource', 'from_user', null=True, blank=True)
    content_object = GenericForeignKeyField({
        Story: StoryResource,
        Piece: PieceResource,
        BanyanUser: BanyanUserResource,
    }, 'content_object', null = True, blank = True)
    
    class Meta:
        queryset = BanyanUserNotifications.objects.all()
        resource_name = 'notifications'
        list_allowed_methods = []
        detail_allowed_methods = ['get']
        authentication = ApiKeyAuthentication() #Only from the devices
        authorization = BanyanUserNotificationsAuthorization()
        filtering = {
                     'user': ALL_WITH_RELATIONS,
                     }