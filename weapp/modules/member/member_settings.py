# -*- coding: utf-8 -*-

__author__ = 'bert'

from django.conf import settings

#filed names for identify the specific current request 
#member, shopname request for and the social account using
FOLLOWED_MEMBER_TOKEN_SESSION_KEY = 'fmt'
FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD = 'fmt'

UUID_SESSION_KEY = 'uuid'

FOLLOWED_MEMBER_SHARED_URL_SESSION_KEY = 'fmsurl'

#relate to field token of model SocialAccount
SOCIAL_ACCOUNT_TOKEN_SESSION_KEY = 'sct'
SOCIAL_ACCOUNT_TOKEN_URL_QUERY_FIELD = 'sct'

NON_MEMBER_UUID_SESSION_KEY = UUID_SESSION_KEY

OPENID_WEBAPP_ID_KEY = 'openid_webapp_id'

if settings.IS_MESSAGE_OPTIMIZATION:
	MESSAGE_URL_QUERY_FIELD = 'opid'
else:
	MESSAGE_URL_QUERY_FIELD = 'sct'

URL_OPENID = 'opid'