import json
import logging
import pdb
import sys
import os

import boto
import boto.sns
from boto.exception import BotoServerError

from django.conf import settings

from accounts.models import BanyanUser


# Get an instance of a logger
logger = logging.getLogger(__name__)

def sns_send_push_notification_to_user(endpoint=None, message=None, data=None, user=None, **kwargs):
    if not user:
        return

    boto.set_stream_logger('boto')
    sns = boto.sns.connect_to_region('us-east-1')
    
    apns_dict = {'aps':{'alert':message,'sound':'default'}}
    if data:
        apns_dict['data'] = data
    apns_string = json.dumps(apns_dict, ensure_ascii=False)
    message = {'default':message, settings.AWS_SNS_APNS_PLATFORM:apns_string}
    messageJSON = json.dumps(message, ensure_ascii=False)
    
    try:
        for device in user.installations.all():
            apns_endpoint = None
            apns = device.push_endpoints.get('apns', None)
            if apns:
                apns_endpoint = apns.get(endpoint, None)
            if apns_endpoint:
                msg_id = sns.publish(topic=None, message = messageJSON, target_arn=apns_endpoint, message_structure='json')
    except BotoServerError as e:
        logger.error("utils.aws.sns_send_push_notification_to_user. Boto error {} to user {}".format(e.code, user))
    except:
        logger.error("utils.aws.sns_send_push_notification_to_user. Unknown error {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))

def s3_delete_object_with_key(key=None, **kwargs):
    s3 = boto.connect_s3()
    try:
        bucket = s3.get_bucket(settings.AWS_S3_MEDIA_BUCKET)
        possible_key = bucket.get_key(key)
        if possible_key:
            possible_key.delete()
        else:
            logger.error("utils.aws.s3_delete_object_with_key missing key {}".format(key, sys.exc_info()[0], sys.exc_info()[1]))
    except:
        logger.error("utils.aws.s3_delete_object_with_key {}.Unknown error {} {}".format(key, sys.exc_info()[0], sys.exc_info()[1]))
