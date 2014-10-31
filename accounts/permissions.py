from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from accounts.models import BanyanUser
import pdb

class BanyanUserAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # No bulk reads
        return []

    def read_detail(self, object_list, bundle):
        '''
        Since we pass on the author during a PUT of piece or story as well, it is possible that the user
        who is editing the story is not the one who is the author. In that case, when tastypie tries to read_detail
        the author, it will get an Unauthorized() error. The following is a work around to allow anyone to read
        the author when a story or piece is being edited
        '''
        if bundle.request.method == 'PUT' and ("piece" in bundle.request.path or "story" in bundle.request.path):
            return True
        
        '''
        If this is a GET request, allow any one to read the information
        '''
        if bundle.request.method == 'GET':
            return True
        
        # Is the requested object owned by the user?
        return bundle.obj == bundle.request.user

    def create_list(self, object_list, bundle):
        # Assuming their auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user

    def update_list(self, object_list, bundle):
        # No bulk updates
        return []

    def update_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
    
class BanyanUserDevicesAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no reads.")

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        # Assuming their auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        # No bulk updates
        return []

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
    
class BanyanUserNotificationsAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no reads.")

    def create_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no creates.")

    def create_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no creates.")

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")