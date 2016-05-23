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
from core import paginator

from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken

from modules.member.models import Member, MemberTag, MemberHasTag, UserSentMassMsgLog, MESSAGE_TYPE_NEWS, MESSAGE_TYPE_TEXT,WebAppUser,CANCEL_SUBSCRIBED,SUBSCRIBED

from weixin.message.material.models import News
from member.member_list import build_member_has_tags_json

from watchdog.utils import watchdog_warning, watchdog_error
from datetime import datetime

########################################################################
# send_mass_text_message: 发送文本消息
########################################################################
def send_mass_text_message(user_profile, group_id, content):
	if group_id == -1:
		#当group_id等于-1时发送给全部会员
		openid_list = get_openid_list_by_webapp_id(user_profile.webapp_id)
	else:
		openid_list = get_openid_list(group_id)
	
	return send_mass_text_message_with_openid_list(user_profile, openid_list, content, group_id)

##################################################################################
# send_mass_text_message_with_openid_list: 直接使用已给的openid_list发送文本消息
##################################################################################
def send_mass_text_message_with_openid_list(user_profile, openid_list, content, log_id=None, group_id=0):
	user = user_profile.user
	if len(openid_list) > 0 and content != None and content != '' and user:
		mpuser_access_token = _get_mpuser_access_token(user)
		if mpuser_access_token:
			mesage = TextMessage(openid_list, content)
			weixin_api = get_weixin_api(mpuser_access_token)
			if log_id:
				sent_log = UserSentMassMsgLog.objects.filter(id=log_id).first()
			else:
				sent_log = UserSentMassMsgLog.create(user_profile.webapp_id, '', MESSAGE_TYPE_TEXT, content, group_id)
			try:
				result = weixin_api.send_mass_message(mesage, True)
				#增加群发任务失败处理
				sent_log.msg_id = result['msg_id']
				sent_log.message_type = MESSAGE_TYPE_TEXT
				sent_log.message_content = content
				if result['errcode'] != 0:
					sent_log.status = 'send fail code: %d' % result['errcode']
					if result['errcode'] == -1: #微信系统繁忙，则稍后重试
						sent_log.save()
						return False
				sent_log.save()
				return True
			except:
				notify_message = u"群发文本消息异常send_mass_message, cause:\n{}".format(unicode_full_stack())
				print notify_message
				watchdog_warning(notify_message)
				sent_log.status = 'send failed'
				sent_log.save()
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

	return send_mass_news_message_with_openid_list(user_profile, openid_list, material_id, group_id)


####################################################################################
# send_mass_news_message_with_openid_list: 直接使用已给的openid_list发送图文消息
####################################################################################
def send_mass_news_message_with_openid_list(user_profile, openid_list, material_id, log_id=None, group_id=0):


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
			if log_id:
				sent_log = UserSentMassMsgLog.objects.filter(id=log_id).first()
			else:
				sent_log = UserSentMassMsgLog.create(user_profile.webapp_id, '', MESSAGE_TYPE_NEWS, material_id, group_id)
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
								new.text = re.sub(r'(?P<img_pre><img\s+[^>]*?\s*?src=[\"\'])(?P<img_url>[^>\s]*?\.(png|jpg))(?=[\"\'])',
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
				#增加群发任务失败处理
				sent_log.msg_id = result['msg_id']
				sent_log.message_type = MESSAGE_TYPE_NEWS
				sent_log.message_content = material_id
				if result['errcode'] != 0:
					sent_log.status = 'send failed code: %d' % result['errcode']
					if result['errcode'] == -1: #微信系统繁忙，则稍后重试
						sent_log.save()
						return False
				sent_log.save()
				return True
			except:
				notify_message = u"群发图文消息异常send_mass_message, cause:\n{}".format(unicode_full_stack())
				print notify_message
				watchdog_warning(notify_message)
				sent_log.status = 'send failed'
				sent_log.save()
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

def get_members_from_webapp_user_ids(webapp_user_ids,sort_attr=None):
		if not webapp_user_ids:
			return [],[],[]
		member_all_ids = WebAppUser.objects.filter(id__in=webapp_user_ids).values_list('member_id', flat=True)
		members = Member.objects.filter(id__in=member_all_ids, status__in=[CANCEL_SUBSCRIBED,SUBSCRIBED], is_for_test=0)
		if sort_attr:
			members = members.order_by(sort_attr)
		member_subscribed_ids = members.filter(status=SUBSCRIBED).values_list('id', flat=True)
		member_ids = members.values_list('id', flat=True)
		return members,member_ids,member_subscribed_ids

def build_member_json(member):
	return {
		'id': member.id,
		'username': member.username_for_title,
		'username_truncated': member.username_truncated,
		'user_icon': member.user_icon,
		'grade_name': member.grade.name,
		'integral': member.integral,
		'factor': member.factor,
		'remarks_name': member.remarks_name,
		'created_at': datetime.strftime(member.created_at, '%Y-%m-%d'),
		'last_visit_time': datetime.strftime(member.last_visit_time, '%Y-%m-%d') if member.last_visit_time else '-',
		'session_id': member.session_id,
		'friend_count':  member.friend_count,
		'source':  member.source,
		'tags':build_member_has_tags_json(member),
		'is_subscribed':member.is_subscribed,
		'experience': member.experience,
	}


def get_tags_json(webapp_id):
	
	tags = MemberTag.get_member_tags(webapp_id)

	tags_json = []
	for tag in tags:
		tags_json.append({'id':tag.id,'name': tag.name})

	return tags_json

def get_members_by(webapp_user_ids,**kwargs):
	if kwargs.has_key('cur_page'):
		cur_page=kwargs['cur_page']
	else:
		cur_page = None
	if kwargs.has_key('count_per_page'):
		count_per_page=kwargs['count_per_page']
	else:
		count_per_page = None
	if kwargs.has_key('sort_attr'):
		sort_attr=kwargs['sort_attr']
	else:
		sort_attr = None
	if kwargs.has_key('webapp_id'):
		webapp_id=kwargs['webapp_id']
	else:
		webapp_id = None 
	members,member_ids,member_subscribed_ids = get_members_from_webapp_user_ids(webapp_user_ids, sort_attr)
	data = {}
	data['sortAttr'] = sort_attr
	try:
		total_count = members.count()
	except:
		total_count = len(members)
	data['total_count'] = total_count
	if cur_page and count_per_page:
		pageinfo, members = paginator.paginate(
			members,
			cur_page,
			count_per_page,
			)
		items = []
		for member in members:
			items.append(build_member_json(member))
		data['items'] = items
		data['pageinfo'] = paginator.to_dict(pageinfo)
		data['member_ids'] = list(member_ids)
		data['member_subscribed_ids'] = list(member_subscribed_ids)
	else:
		data["members"] = members
	if webapp_id:
		tags_json = get_tags_json(webapp_id)
		data['tags'] = tags_json

	return data

