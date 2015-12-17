# -*- coding: utf-8 -*-

__author__ = 'bert'

import os
import re
from django.conf import settings

from core.wxapi.weixin_api import *
from core.wxapi import get_weixin_api
from core.wxapi.weixin_api import WeixinApi
from core.wxapi.api_send_mass_message import TextMessage, NewsMessage
from core.wxapi.api_upload_news import Articles
from core.exceptionutil import full_stack, unicode_full_stack
from core import emotion

from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken

from modules.member.models import Member, MemberTag, MemberHasTag, UserSentMassMsgLog, MESSAGE_TYPE_NEWS, MESSAGE_TYPE_TEXT

from weixin.message.material.models import News

from watchdog.utils import watchdog_warning, watchdog_error

########################################################################
# send_mass_text_message: 发送文本消息
########################################################################
def send_mass_text_message(user_profile, group_id, content):
	if group_id == -1:
		#当group_id等于-1时发送给全部会员
		openid_list = get_openid_list_by_webapp_id(user_profile.webapp_id)
	else:
		openid_list = get_openid_list(group_id)
	
	return send_mass_text_message_with_openid_list(user_profile, openid_list, content)

##################################################################################
# send_mass_text_message_with_openid_list: 直接使用已给的openid_list发送文本消息
##################################################################################
def send_mass_text_message_with_openid_list(user_profile, openid_list, content, log_id=None):
	user = user_profile.user
	if len(openid_list) > 0 and content != None and content != '' and user:
		mpuser_access_token = _get_mpuser_access_token(user)
		if mpuser_access_token:
			mesage = TextMessage(openid_list, content)
			weixin_api = get_weixin_api(mpuser_access_token)
			try:
				result = weixin_api.send_mass_message(mesage, True)
				if result.has_key('msg_id'):
					if log_id:
						UserSentMassMsgLog.objects.filter(id=log_id).update(msg_id=result['msg_id'], message_type=MESSAGE_TYPE_TEXT, message_content=content)
					else:
						UserSentMassMsgLog.create(user_profile.webapp_id, result['msg_id'], MESSAGE_TYPE_TEXT, content)
				return True
			except:
				notify_message = u"群发文本消息异常send_mass_message, cause:\n{}".format(unicode_full_stack())
				print notify_message
				watchdog_warning(notify_message)
				return False
		else:
			return False

	return True

########################################################################
# send_mass_new_message: 发送图文消息
########################################################################
def send_mass_new_message(user_profile, group_id, material_id):
	if group_id == -1:
		#当group_id等于-1时发送给全部会员
		openid_list = get_openid_list_by_webapp_id(user_profile.webapp_id)
	else:
		openid_list = get_openid_list(group_id)

	return send_mass_news_message_with_openid_list(user_profile, openid_list, material_id)


####################################################################################
# send_mass_news_message_with_openid_list: 直接使用已给的openid_list发送图文消息
####################################################################################
def send_mass_news_message_with_openid_list(user_profile, openid_list, material_id, log_id=None):
	

	user = user_profile.user
	if len(openid_list) > 0 and material_id != None and material_id != '' and user:
		news = News.get_news_by_material_id(material_id)
		mpuser_access_token = _get_mpuser_access_token(user)
		if mpuser_access_token:
			weixin_api = get_weixin_api(mpuser_access_token)

			def pic_re(matched):
				pic_astr = matched.group("img_url")
				if pic_astr.startswith('/') and pic_astr.find('http') == -1:
					pic_astr = pic_astr[1:]
					pic_url = os.path.join(settings.PROJECT_HOME, '../', pic_astr)
				else:
					pic_url = pic_astr

				pic_result = weixin_api.upload_content_media_image(pic_url, True)
				pic_result_url = ''
				if pic_result.has_key('url'):
					pic_result_url = pic_result['url']
				
				try:
					if not pic_result_url:
						watchdog_error(u'上传多媒体文件失败 url:{}, pic_result:{}'.format(pic_url, pic_result_url))
				except:
					pass
				pic_pre = matched.group("img_pre")
				pic_result_url = pic_pre + pic_result_url
				return pic_result_url
			
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
						elif new.url.startswith('/m/') or new.url.startswith('./m/') or new.url.startswith('m/'):
							if new.url.startswith('/m/'):
								new.url = '%s%s' % (user_profile.host, new.url)
							elif new.url.startswith('./m/'):
								new.url = '%s%s' % (user_profile.host, new.url)
							else:
								new.url = '%s/%s' % (user_profile.host, new.url)
								
						if len(new.text.strip()) != 0:
							if new.text.find('<img') :
								#content = new.text.replace('/static/',('http://%s/static/' % user_profile.host))
								#if new.text.find('.jpg') :
								new.text = re.sub(r'(?P<img_pre><img\s+[^>]*?\s*?src=[\"\'])(?P<img_url>[^>]*?\.(png|jpg))(?=[\"\'])',
									pic_re,new.text)
							if new.text.find('background-image:') :
								new.text = re.sub(r'(?P<img_pre>background-image:\s*?url\((\"|\'|&quot;)?)(?P<img_url>[^\)]+?\.(png|jpg))(?=(\"|\'|&quot;)?\))',
										pic_re,new.text)
								content = new.text

							else:
								content = new.text
						else:
							content = new.text						

						article.add_article(result_info['media_id'], new.title, content, new.url, None, new.summary)
				result = weixin_api.upload_media_news(article)
				message = NewsMessage(openid_list, result['media_id'])
				result = weixin_api.send_mass_message(message, True)
				if result.has_key('msg_id'):
					if log_id:
						UserSentMassMsgLog.objects.filter(id=log_id).update(msg_id=result['msg_id'], message_type=MESSAGE_TYPE_NEWS, message_content=material_id)
					else:
						UserSentMassMsgLog.create(user_profile.webapp_id, result['msg_id'], MESSAGE_TYPE_NEWS, material_id)
				return True
			except:
				notify_message = u"群发图文消息异常send_mass_message, cause:\n{}".format(unicode_full_stack())
				watchdog_warning(notify_message)
				return False
		else:
			return False
 
	return True

########################################################################
# delete_mass_message: 删除群发消息
# 只有已经发送成功的消息才能删除删除消息只是将消息的图文详情页失效，
# 已经收到的用户，还是能在其本地看到消息卡片。 
# 另外，删除群发消息只能删除图文消息和视频消息，其他类型的消息一经发送，无法删除
########################################################################
def delete_mass_message(user_profile, msg_id):
	user = user_profile.user
	if msg_id != None and msg_id != '' and user:
		mpuser_access_token = _get_mpuser_access_token(user)
		if mpuser_access_token:
			weixin_api = get_weixin_api(mpuser_access_token)
			try:
				result = weixin_api.delete_mass_message(msg_id.strip())
				if result.has_key('errmsg') and result['errmsg'] == 'ok':
					UserSentMassMsgLog.objects.filter(webapp_id=user_profile.webapp_id,msg_id=msg_id).update(status='delete')
				return True
			except:
				notify_message = u"删除群发消息异常delete_mass_message, cause:\n{}".format(unicode_full_stack())
				print notify_message
				watchdog_warning(notify_message)
				return False

	return False

def get_openid_list(group_id):
	openid_list = []
	members = MemberHasTag.get_member_list_by_tag_id(group_id)
	for member in members:
		if member.is_subscribed:
			openid = member.member_open_id
			if openid:
				openid_list.append(openid)
	return openid_list

def get_openid_list_by_webapp_id(webapp_id):
	openid_list = []
	members = Member.get_members(webapp_id)
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

	if mpuser_access_token:
		return mpuser_access_token
	else:
		return None
