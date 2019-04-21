# -*- coding: utf-8 -*-
"""
API settings.
"""

# sort json response keys.
JSON_SORT_KEYS = False

# return json as ascii.
JSON_AS_ASCII = True

# pretty print json response.
JSONIFY_PRETTYPRINT_REGULAR = True

# json mimetype.
JSONIFY_MIMETYPE = 'application/json'

# default status code of api responses.
DEFAULT_STATUS_CODE = 200

# trusted ips to accept requests from. (['*'], ['192.168.3.43'])
TRUSTED_IPS = ['*']

# minimum android client version to accept requests from. ('1.2', '*')
MIN_ANDROID_VERSION = '*'

# minimum ios client version to accept requests from. ('1.2', '*')
MIN_IOS_VERSION = '*'

# minimum web client version to accept requests from. ('1.2', '*')
MIN_WEB_VERSION = '*'

# android client api key that client should put in every request.
ANDROID_API_KEY = ''

# ios client api key that client should put in every request.
IOS_API_KEY = ''

# web client api key that client should put in every request.
WEB_API_KEY = ''
