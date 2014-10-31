from tastypie import fields, http
from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication, Authentication, SessionAuthentication, MultiAuthentication
from tastypie.exceptions import NotFound
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from content_feedback.models import FlaggedObject, HiddenObject
from core.models import Story, Piece
from core.api import StoryResource, PieceResource
from tastypie.authorization import Authorization
from tastypie.cache import SimpleCache

class ContentFlagResource(ModelResource):
    user = fields.ForeignKey('accounts.api.BanyanUserResource', 'user')
    content_object = GenericForeignKeyField({
        Story: StoryResource,
        Piece: PieceResource,
    }, 'content_object')
    
    class Meta:
        resource_name = 'flag_object'
        queryset = FlaggedObject.objects.all()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication(), Authentication())
        authorization = Authorization()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        
    def hydrate_user(self, bundle):
        if bundle.request.user.is_authenticated():
            bundle.data['user'] = bundle.request.user
        return bundle
    
class ContentHideResource(ModelResource):
    user = fields.ForeignKey('accounts.api.BanyanUserResource', 'user')
    content_object = GenericForeignKeyField({
        Story: StoryResource,
        Piece: PieceResource,
    }, 'content_object')
    
    class Meta:
        resource_name = 'hide_object'
        queryset = HiddenObject.objects.all()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
        authorization = Authorization()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        cache = SimpleCache()
        
    def hydrate_user(self, bundle):
        if bundle.request.user.is_authenticated():
            bundle.data['user'] = bundle.request.user
        return bundle