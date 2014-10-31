import pdb

from django.conf.urls import url
from django.utils import six

from tastypie import fields, http
from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication, Authentication, SessionAuthentication, MultiAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.exceptions import NotFound
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from tastypie.utils import trailing_slash

from core.models import Story, Piece
from accounts.models import BanyanUser, BanyanUserDevices
from accounts.views import register_by_access_token
from accounts.permissions import BanyanUserAuthorization, BanyanUserDevicesAuthorization
        
class BanyanUserDevicesResource(ModelResource):
    class Meta:
        queryset = BanyanUserDevices.objects.all()
        resource_name = 'installations'
        list_allowed_methods = []
        detail_allowed_methods = ['put']
        authentication = ApiKeyAuthentication() #Only from the devices
        authorization = BanyanUserDevicesAuthorization()

class BanyanUserResource(ModelResource):
    social_data = fields.DictField(attribute='social_data', use_in='detail', null=True)
    api_key = fields.CharField(attribute='api_key', use_in='detail', null=True)

    class Meta:
        queryset = BanyanUser.objects.all()
        resource_name = 'users'
        always_return_data = True
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser', 'email']
        list_allowed_methods = ['post']
        detail_allowed_methods = ['get', 'post', 'put']
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication(), Authentication())
        authorization = BanyanUserAuthorization()
    
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/installations%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('create_user_device'), name="api_create_user_device"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/notifications%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_user_notifications'), name="api_get_user_notifications"),
        ]

    def get_user_notifications(self, request, **kwargs):
        from core.api import BanyanUserNotificationsResource
        notifications_resource = BanyanUserNotificationsResource()
        if request.user.is_authenticated():
            return notifications_resource.get_list(request, user=request.user)
        else:
            return http.HttpNoContent()

    def create_user_device(self, request, **kwargs):
        user_devices_resource = BanyanUserDevicesResource()
        if request.user.is_authenticated():
            return user_devices_resource.put_detail(request, user=request.user)
        else:
            return http.HttpNoContent()
    
    def dehydrate(self, bundle):
        if 'users' in bundle.request.path and bundle.request.method.lower() == 'get':
            requestingUser = bundle.request.user
            requestedUser = bundle.obj
            bundle.data['user_details'] = requestedUser.get_details_for_profile_from_user(requestingUser)
            bundle.data['usage_details'] = Piece.usage_details_of_user(requestedUser, requestingUser)
        facebook = bundle.data.get("facebook", None)
        if facebook:
            facebookId = facebook['id']
            bundle.data["facebook"] = {"facebookId":facebookId}
        if bundle.request.user.is_authenticated() and (bundle.request.user.pk == bundle.obj.pk):
            # If the user himeself is asking for the data, send his own email
            bundle.data['email'] = bundle.obj.email
        bundle.data['name'] = bundle.obj.get_full_name()
        if bundle.request.method.lower() != 'post':
            bundle.data.pop('api_key', None)
        return bundle
    
    def dehydrate_social_data(self, bundle):
        returnDict = {}
        facebook = bundle.data.get("facebook", None)
        if facebook:
            returnDict['facebook'] = {'friends_on_banyan':list(bundle.obj.get_my_facebook_friends_on_banyan_values())}
        return returnDict

    def dehydrate_api_key(self, bundle):
        if bundle.request.method.lower() == 'post':
            return bundle.obj.api_key.key
    
    def obj_create(self, bundle, **kwargs):
        data = bundle.data
        if "facebook" in data.keys():
            info = data.get("facebook")
            user = register_by_access_token(bundle.request, "facebook", **info)
        elif bundle.request.user:
            user = bundle.request.user
        else:
            raise NotFound("Unsupported backend used")

        if not user:
            raise NotFound("A model instance matching the provided arguments could not be found or created.")
        bundle.obj = user
        ''' Now update the object with the other parameters '''
        return super(BanyanUserResource, self).obj_update(bundle, **kwargs)
    
'''
!!! NOTE !!!
class BanyanUserNotificationsResource(ModelResource)
Moved to core.api
'''