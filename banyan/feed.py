import base64
import urllib, urllib2, httplib

from django import http
from django.conf import settings

from django.core.context_processors import request
from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed

from django.utils import simplejson as json
from django.utils.http import base36_to_int

from Crypto.Cipher import AES
from Crypto import Random

class UserFeed(Feed):
        
    def __init__(self, user_id=None, fb_id=None):
        if user_id is not None:
            self.__class__.user_id = user_id
        if fb_id is not None:
            self.__class__.fb_id = fb_id            
   
    title = "Banyan Stories news"
    link = "/"
    def items(self):
        stories = []
        uri = '/%s' % (settings.CUSTOM_CLASS_LIST[1])
        url = settings.API_ROOT + uri
        http_verb = 'GET'

        parse_request = urllib2.Request(url, None)
        parse_request.add_header('Content-type', 'application/json')
        auth_header =  "Basic %s" % base64.b64encode('%s:%s' % (settings.APPLICATION_ID, settings.MASTER_KEY))
        parse_request.add_header("Authorization", auth_header)
        parse_request.get_method = lambda: http_verb

        try:
            response = urllib2.urlopen(parse_request)
        except urllib2.URLError, e:
            return HttpResponse(content=json.dumps({'error_message': e.msg}), mimetype = 'application/json', status=e.code)
        
        response_body = response.read()
        response_dict = json.loads(response_body)
        results =  response_dict.get('results', None)
        for result in results:    
            user_id_in_public_contributors_list = False
            user_id_in_public_viewers_list = False           
            if self.user_id is not None or self.fb_id is not None:
                public_contributors_list = result.get('invitedToContribute', None)
                public_viewers_list = result.get('invitedToView', None)
                    
                if public_contributors_list:
                    for item in public_contributors_list:
                        if type(item).__name__ == 'dict':
                            if self.user_id in item.values() or self.fb_id in item.values():
                                user_id_in_public_contributors_list = True
                        else:            
                            if item.find(self.user_id) != -1 or item.find(self.fb_id) != -1:
                                user_id_in_public_contributors_list = True
            
                if public_viewers_list:
                    for item in public_viewers_list:
                        if type(item).__name__ == 'dict':
                            if self.user_id in item.values() or self.fb_id in item.values():
                                user_id_in_public_viewers_list = True
                        else:
                            if item.find(self.user_id) != -1 or item.find(self.fb_id) != -1:
                                user_id_in_public_viewers_list = True

            public_contributors = result.get('publicContributors', None)
            public_viewers = result.get('publicViewers', None)

            if public_contributors is True:          
                stories.append(result)

            elif user_id_in_public_contributors_list is True:
                stories.append(result)

            elif public_viewers is True:
                stories.append(result)
                
            elif user_id_in_public_viewers_list is True:
                stories.append(result)
               
        return stories

    def item_title(self, item):
        return item.get('title', None)

    def item_description(self, item):
        return item.get('text', None)
    
    def item_link(self, item):
        Id = item.get('objectId', None)
        if Id is not None:
            Id = xor_crypt_string(plaintext = Id, key = settings.OBFUSCATE_KEY)
            link = reverse("read_story", args=[Id])
            return link    
        else:
            return '/'
            
def xor_crypt_string(plaintext, key):
    '''
    This view is used for encryption of a string
    Remember using a Sixteen byte key
    '''
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(plaintext)
    return msg.encode("hex")
             
        
