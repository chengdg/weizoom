# -*- coding: utf-8 -*-

__author__ = 'bert'

import os
from django.conf import settings

from core.wxapi.weixin_api import *
from core.wxapi import get_weixin_api
from core.wxapi.weixin_api import WeixinApi
from core.wxapi.api_send_mass_message import TextMessage, NewsMessage
from core.wxapi.api_upload_news import Articles
from core.exceptionutil import full_stack, unicode_full_stack

from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken

from modules.member.models import MemberTag, MemberHasTag, UserSentMassMsgLog, MESSAGE_TYPE_NEWS, MESSAGE_TYPE_TEXT

from weixin.message.material.models import News

from watchdog.utils import watchdog_warning, watchdog_error

########################################################################
# send_mass_text_message: 发送文本消息
########################################################################
def send_mass_text_message(user_profile, group_id, content):
	openid_list = _get_openid_list(group_id)
	user = user_profile.user
	if len(openid_list) > 0 and content != None and content != '' and user:
		mpuser_access_token = _get_mpuser_access_token(user)
		if mpuser_access_token:
			mesage = TextMessage(openid_list, content)
			weixin_api = get_weixin_api(mpuser_access_token)
			try:
				result = weixin_api.send_mass_message(mesage, True)
				if result.has_key('msg_id'):
					UserSentMassMsgLog.create(user_profile.webapp_id, result['msg_id'], MESSAGE_TYPE_TEXT, content)
				return True
			except:
				notify_message = u"群发文本消息异常, cause:\n{}".format(unicode_full_stack())
				watchdog_warning(notify_message)
				return False
		else:
			return False

	return False

########################################################################
# send_mass_new_message: 发送图文消息
########################################################################
def send_mass_new_message(user_profile, group_id, material_id):
	openid_list = _get_openid_list(group_id)
	user = user_profile.user
	if len(openid_list) > 0 and material_id != None and material_id != '' and user:
		news = News.get_news_by_material_id(material_id)
		mpuser_access_token = _get_mpuser_access_token(user)
		if mpuser_access_token:
			weixin_api = get_weixin_api(mpuser_access_token)
			try:
				article = Articles()
				for new in news:
					if new.pic_url:
						if new.pic_url.startswith('/') and new.pic_url.find('http') == -1:
							new.pic_url = new.pic_url[1:]
							#TODO::::目前是 把服务器上的图片上传到weixin  后期修改upyun的时候要做处理
							pic_url = os.path.join(settings.PROJECT_HOME, '../', new.pic_url)
						else:
							pic_url = new.pic_url

						result_info = weixin_api.upload_media_image(pic_url, True)
						if new.url.startswith('./?'):
							new.url = '%s/workbench/jqm/preview%s' % (user_profile.host, new.url[1:])
						
						if len(new.text.strip()) != 0:
							if new.text.find('img') and new.text.find('http') == -1:
								content = new.text.replace('/static/',('http://%s/static/' % user_profile.host))
							#added by chuter
							else:
								content = new.summary
						else:
							content = new.summary						

						article.add_article(result_info['media_id'], new.title, content, new.url, None, new.summary)
				result = weixin_api.upload_media_news(article)
				message = NewsMessage(openid_list, result['media_id'])
				result = weixin_api.send_mass_message(message, True)
				if result.has_key('msg_id'):
					UserSentMassMsgLog.create(user_profile.webapp_id, result['msg_id'], MESSAGE_TYPE_NEWS, material_id)
				return True
			except Exception, e:
				notify_message = u"群发图文消息异常, cause:\n{}".format(unicode_full_stack())
				watchdog_warning(notify_message)
				return False
		else:
			return False

	return True

def _get_openid_list(group_id):
	openid_list = []
	members = MemberHasTag.get_member_list_by_tag_id(group_id)
	for member in members:
		openid = member.member_open_id
		if openid:
			openid_list.append(openid)
	return openid_list

def _get_mpuser_access_token(user):
	mp_user = get_binding_weixin_mpuser(user)
	if mp_user:
		mpuser_access_token = get_mpuser_accesstoken(mp_user)
	else:
		return False

	if mpuser_access_token is None:
		return False

	if mpuser_access_token.is_active:
		return mpuser_access_token
	else:
		return None