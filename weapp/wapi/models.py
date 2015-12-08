# -*- coding: utf-8 -*-

#from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
#import json
#import time


class OAuthToken(models.Model):
	"""
	内部使用授权token，用于WGlass访问API用(类似OAuth的token)
	"""
	user = models.ForeignKey(User, related_name='owned_tokens')
	token = models.CharField(max_length=50, db_index=True)
	expire_time = models.DateTimeField()
	
	class Meta:
		db_table = 'wapi_oauthtoken'
		unique_together=("token",)
