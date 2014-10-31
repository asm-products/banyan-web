import pdb

from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

from core.models import Story, Piece, StoryUserAccess
from accounts.models import BanyanUser

class StoryAuthorization(Authorization):
    #API authorization classes
    def read_list(self, object_list, bundle):
        """ 
        object_list is a queryset. 
        Return another queryset so that sorting can be applied on it
        """
        return object_list
    
    def read_detail(self, object_list, bundle):
        '''
        When a story is being flagged, tastypie still needs to access the story.
        Similary for when a new activity is being created for the story.
        Simply relying on can_read_story() will not allow anyone to flag stories once the
        number of flags for that story is more than the max allowed.
        '''
        if bundle.request.method == 'POST' and (("flag_object" in bundle.request.path) or ("activity" in bundle.request.path)):
            return True
        
        user = bundle.request.user
        story = bundle.obj
        userstoryaccess, created = StoryUserAccess.objects.get_or_create(user=user, story=story)
        return userstoryaccess.canRead
    
    def create_list(self, object_list, bundle):
        """ Sorry, can't create a list """
        return []
    
    def create_detail(self, object_list, bundle):
        """ Any valid user can create """
        user = bundle.request.user
        if user.is_authenticated():
            return True
        else:
            return False
    
    def update_list(self, object_list, bundle):
        """" Sorry, can't update a list """
        return []
    
    def update_detail(self, object_list, bundle):
        user = bundle.request.user
        return bundle.obj.can_edit_story(user)
    
    def delete_list(self, object_list, bundle):
        """ Sorry, can't delete a list """
        return []
    
    def delete_detail(self, object_list, bundle):
        """ Only allow to delete if user is the author """
        user = bundle.request.user
        if user.is_authenticated() and user.id == bundle.obj.author.id:
            return True
        else:
            return False
        
class PieceAuthorization(Authorization):
    #API authorization classes
    def read_list(self, object_list, bundle):
        """ 
        object_list is a queryset. 
        Return another queryset so that sorting can be applied on it
        """
        user = bundle.request.user
        obj_ids_to_return = []
        for piece in object_list.iterator():
            if piece.can_read_piece(user):
                obj_ids_to_return.append(piece.pk)
        return object_list.filter(pk__in=obj_ids_to_return)
    
    def read_detail(self, object_list, bundle):
        '''
        When a piece is being flagged, tastypie still needs to access the piece.
        Similary for when a new activity is being created for the piece.
        Simply relying on can_read_piece() will not allow anyone to flag pieces once the
        number of flags for that piece is more than the max allowed.
        '''
        if bundle.request.method == 'POST' and (("flag_object" in bundle.request.path) or ("activity" in bundle.request.path)):
            return True
        
        user = bundle.request.user
        return bundle.obj.can_read_piece(user)
    
    def create_list(self, object_list, bundle):
        """ Sorry, can't create a list """
        return []
    
    def create_detail(self, object_list, bundle):
        user = bundle.request.user
        return bundle.obj.can_edit_piece(user)
    
    def update_list(self, object_list, bundle):
        """ Sorry, can't update a list """
        return []
    
    def update_detail(self, object_list, bundle):
        user = bundle.request.user
        return bundle.obj.can_edit_piece(user)
    
    def delete_list(self, object_list, bundle):
        """ Sorry, can't delete a list """
        return []
    
    def delete_detail(self, object_list, bundle):
        """ Only allow to delete if user is the author """
        user = bundle.request.user
        if user.is_authenticated() and (user.id == bundle.obj.author.id or user.id == bundle.obj.story.author.id):
            return True
        else:
            return False

class ActivityAuthorization(Authorization):
    #API authorization classes
    def read_list(self, object_list, bundle):
        """ For now, return all the activities """
        return object_list
    
    def read_detail(self, object_list, bundle):
        """ Only allow to get if user is the creator of the activity """
        user = bundle.request.user
        return bundle.obj.user == user
    
    def create_list(self, object_list, bundle):
        """ Sorry, can't create a list """
        return []
    
    def create_detail(self, object_list, bundle):
        return bundle.request.user.is_authenticated()
    
    def update_list(self, object_list, bundle):
        """ Sorry, can't update a list """
        return []
    
    def update_detail(self, object_list, bundle):
        return bundle.request.user.is_authenticated()
    
    def delete_list(self, object_list, bundle):
        """ Sorry, can't delete a list """
        return []
    
    def delete_detail(self, object_list, bundle):
        """ Only allow to delete if user is the creator of the activity """
        user = bundle.request.user
        return bundle.obj.user == user