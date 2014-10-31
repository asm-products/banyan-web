from django import template
from datetime import datetime

register = template.Library()

@register.filter(expects_localtime=True)
def datetime_object(value):
    try:
        retObj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
        return retObj
    except:
        return None

@register.filter
def keyvalue(dict, key):
    if not dict:
        return None
    return dict.get(key, None)