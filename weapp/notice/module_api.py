# -*- coding: utf-8 -*-

__author__ = 'herry'

from django.contrib.auth.models import User

from watchdog.utils import watchdog_warning

from models import Notice
import datetime

def create_notice_for_user(user, notice_title, notice_content):
	try:
		Notice(owner_id=user.id, title=notice_title, content=notice_content, create_time=datetime.datetime.now(), has_read=False).save()
	except:
		return 0

#user为'test1,test2,test3'字符串
# def create_notice_for_some_user(user, notice_title, notice_content):
# 	try:
# 		for receive_user in user.split(','):
# 			create_notice_for_user(User.objects.get(username = receive_user), notice_title, notice_content)
# 	except:
# 		raise 0

def create_notice_for_all_user(notice_title, notice_content):
	try:
		for user in User.objects.all():
			create_notice_for_user(user, notice_title, notice_content)
	except:
		return 0

def get_unread_notice_count(user):
	if user is None:
		return 0
	try:
		return Notice.objects.filter(owner_id=user.id, has_read=False).count()
	except:
		#TODO 需要进行预警操作？？
		return 0


