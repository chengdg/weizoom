# -*- coding: utf-8 -*-

__author__ = 'bert'


from models import *

def is_auth_user(username):
	return ERPAuthUser.objects.filter(username=username).count()
