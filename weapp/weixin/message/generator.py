# -*- coding: utf-8 -*-
"""@package weixin.generator
生成微信response的工具

"""

import time
import base64

from modules.member import member_settings


REQUEST_TEXT_TMPL = u"""
<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%d</CreateTime>
	<MsgType><![CDATA[text]]></MsgType>
	<Content><![CDATA[%s]]></Content>
	<MsgId>%d</MsgId>
</xml>
"""
def get_text_request(to_user, from_user, content):
	timestamp = int(time.time())
	return REQUEST_TEXT_TMPL % (to_user, from_user, timestamp, content, timestamp)





REQUEST_SUBSCRIBE_EVENT_TMPL = u"""
<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%d</CreateTime>
	<MsgType><![CDATA[event]]></MsgType>
	<Event><![CDATA[%s]]></Event>
	<EventKey><![CDATA[]]></EventKey>
</xml>
"""
def get_subscribe_event(to_user, from_user='weizoom'):
	timestamp = int(time.time())
	return REQUEST_SUBSCRIBE_EVENT_TMPL % (to_user, from_user, timestamp, 'subscribe')

def get_unsubscribe_event(to_user, from_user='weizoom'):
	timestamp = int(time.time())
	return REQUEST_SUBSCRIBE_EVENT_TMPL % (to_user, from_user, timestamp, 'unsubscribe')

REQUEST_QRCODE_EVET_TMPL = u"""
<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%s</CreateTime>
	<MsgType><![CDATA[event]]></MsgType>
	<Event><![CDATA[%s]]></Event>
	<EventKey><![CDATA[qrscene_123123]]></EventKey>
	<Ticket><![CDATA[%s]]></Ticket>
</xml>"""

def get_qrcode_subscribe_event(to_user, ticket, from_user='weizoom'):
	timestamp = int(time.time())
	return REQUEST_QRCODE_EVET_TMPL % (to_user, from_user, timestamp, 'subscribe', ticket)


NEWS_BEG_TMPL = u"""
	<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%d</CreateTime>
	<MsgType><![CDATA[news]]></MsgType>
	<ArticleCount>%d</ArticleCount>
	<Articles>
	"""

NEWS_END_TMPL = u"""
	</Articles>
	<FuncFlag>1</FuncFlag>
	</xml>
	"""

NEWS_ITEM_WITH_URL_TMPL = u"""
	<item>
	<Title><![CDATA[%s]]></Title>
	<Description><![CDATA[%s]]></Description>
	<PicUrl><![CDATA[%s]]></PicUrl>
	<Url><![CDATA[%s]]></Url>
	</item>
	"""

NEWS_ITEM_WITHOUT_URL_TMPL = u"""
	<item>
	<Title><![CDATA[%s]]></Title>
	<Description><![CDATA[%s]]></Description>
	<PicUrl><![CDATA[%s]]></PicUrl>
	</item>
	"""

def __get_default_news_url(news):
	user_profile = news.user.get_profile()
	return u'http://%s/weixin/message/material/news_detail/mshow/%d/' % (user_profile.host, news.id)

def __get_absolute_url(orig_url, user_profile, material_id=None):
	absolute_url = None

	path = 'workbench/jqm/preview'
	if user_profile.is_use_wepage and 'home_page' in orig_url:
		path = 'termite2/webapp_page'

	if orig_url.startswith('/apps/'):
		path = 'm'

	if orig_url.startswith('/m/'):
		absolute_url = u'http://%s%s' % (user_profile.host, orig_url)
	elif orig_url.startswith('/'):
		absolute_url = u'http://%s/%s%s' % (user_profile.host, path, orig_url)
	elif orig_url.startswith('.'):
		absolute_url = u'http://%s/%s%s' % (user_profile.host, path, orig_url[1:])
	else:
		if not orig_url.startswith('http'):
			absolute_url = u'http://%s/%s/%s' % (user_profile.host, path, orig_url)
	if material_id and ('model=share_red_envelope&action=get' in absolute_url):
		absolute_url = '%s&material_id=%s' % (absolute_url, material_id)
	return absolute_url if (absolute_url is not None) else orig_url

def add_token_to_url(orig_url, token, user_profile):
	"""
		去掉opid sct  不再需要他们
	"""
	return orig_url

	if token is None:
		return orig_url

	if len(orig_url.strip()) == 0:
		return orig_url

	if orig_url.find(user_profile.host) == -1:
		#如果图文消息中配置的链接不是本站的地址不进行任何处理
		return orig_url

	if orig_url.endswith('/'):
		new_url = u'%s?%s=%s' % (orig_url,
			member_settings.MESSAGE_URL_QUERY_FIELD, token)
	elif orig_url.find('?') > 0:
		new_url = u'%s&%s=%s' % (orig_url,
			member_settings.MESSAGE_URL_QUERY_FIELD, token)
	else:
		new_url = u'%s/?%s=%s' % (orig_url,
			member_settings.MESSAGE_URL_QUERY_FIELD, token)

	return new_url

def get_news_response(from_user_name, to_user_name, newses, token):
	timestamp = int(time.time())
	buf = []
	buf.append(NEWS_BEG_TMPL % (from_user_name, to_user_name, timestamp, len(newses)))

	user_profile = None
	for news in newses:
		if len(news.url.strip()) == 0:
			news.url = __get_default_news_url(news)

		if user_profile is None:
			user_profile = news.user.get_profile()

		absolute_news_url = __get_absolute_url(news.url, user_profile, news.material_id)
		if token:
			url = add_token_to_url(absolute_news_url, token, user_profile)
		else:
			url = absolute_news_url
		#------------------OLD-------------------#
		# if len(url.strip()) > 0:
		# 	buf.append(NEWS_ITEM_WITH_URL_TMPL % (news.title, news.summary, 'http://%s%s' % (user_profile.host, news.pic_url), url))
		# else:
		# 	buf.append(NEWS_ITEM_WITHOUT_URL_TMPL % (news.title, news.summary, 'http://%s%s' % (user_profile.host, news.pic_url)))
		#-----------------NEWS-------------------#
		pic_url =  'http://%s%s' % (user_profile.host, news.pic_url) if news.pic_url.find('http') == -1 else news.pic_url
		if len(url.strip()) > 0:
			member_check = base64.encodestring(from_user_name).replace('=', '').strip()
			buf.append(NEWS_ITEM_WITH_URL_TMPL % (news.title, news.summary,pic_url, url.replace("${member}", from_user_name).replace("${member_check}", member_check)))
		else:
			buf.append(NEWS_ITEM_WITHOUT_URL_TMPL % (news.title, news.summary, pic_url))

	buf.append(NEWS_END_TMPL)
	return ''.join(buf)


AUDIO_TMPL = u"""
	<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%d</CreateTime>
	<MsgType><![CDATA[music]]></MsgType>
	<Music>
	<Title><![CDATA[月光水岸]]></Title>
	<Description><![CDATA[Bandari专辑中一曲。]]></Description>
	<MusicUrl><![CDATA[http://srv02.vicp.net:81/down/music/moon-light.mp3]]></MusicUrl>
	<HQMusicUrl><![CDATA[http://srv02.vicp.net:81/down/music/moon-light.mp3]]></HQMusicUrl>
	</Music>
	<FuncFlag>0</FuncFlag>
	</xml>
	"""






RESPONSE_TEXT_TMPL = u"""
	<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%d</CreateTime>
	<MsgType><![CDATA[text]]></MsgType>
	<Content><![CDATA[%s]]></Content>
	<FuncFlag>0</FuncFlag>
	</xml>"""


RESPONSE_CUSTOMER_SERVICE_TMPL = u"""
	<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%d</CreateTime>
	<MsgType><![CDATA[transfer_customer_service]]></MsgType>
	</xml>"""

def get_text_response(from_user_name, to_user_name, content, token, user_profile):
	if len(content.strip()) == 0:
		return None

	timestamp = int(time.time())

	#向链接中添加sct
	if token:
		beg = 0
		pos = 0
		items = []
		while True:
			pos = content.find('href=', beg)
			if pos == -1:
				items.append(content[beg:])
				break

			pos += 6 #6 = len(href=")
			quote_char = content[pos-1] #获取引号，需要区分单、双引号
			quote_end_pos = content.find(quote_char, pos) #寻找href结束地址

			items.append(content[beg:pos])
			url = add_token_to_url(content[pos:quote_end_pos], token, user_profile)
			items.append(url)

			#准备下一次寻找
			beg = quote_end_pos
		content = ''.join(items).strip()

	return RESPONSE_TEXT_TMPL % (from_user_name, to_user_name, timestamp, content)

RESPONSE_CUSTOMER_SERVICE_TMPL = u"""
	<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%d</CreateTime>
	<MsgType><![CDATA[transfer_customer_service]]></MsgType>
	</xml>"""

def get_counstomer_service_text(fromusername, tousername):
	return RESPONSE_CUSTOMER_SERVICE_TMPL % (fromusername, tousername, int(time.time()))

RESPONSE_VOICE_TMPL = u"""
		<xml><tousername><![CDATA[%s]]></tousername>
		<fromusername><![CDATA[%s]]></fromusername>
		<createtime>%d</createtime>
		<msgtype><![CDATA[voice]]></msgtype>
		<mediaid><![CDATA[FWszzdATLEvQyS_t7EPrxImhHS8If4WuNtLs1KGokVIXpdxhq199RCp3lAEXuPH5]]></mediaid>
		<format><![CDATA[amr]]></format>
		<msgid>5937082633568649952</msgid>
		<recognition><![CDATA[ ]]></recognition>
		</xml>
		"""
def get_voice_request(to_user, from_user, content):
	timestamp = int(time.time())
	return RESPONSE_VOICE_TMPL % (to_user, from_user, timestamp)





REQUERST_TEST_EVENT_TMPL = u"""
		<xml>
		<ToUserName><![CDATA[%s]]></ToUserName>
		<FromUserName><![CDATA[%s]]></FromUserName>
		<CreateTime>%d</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[CLICK]]></Event>
		<EventKey><![CDATA[%s]]></EventKey>
		</xml>
		"""
def get_text_test_event_request(to_user, from_user, content):
	timestamp = int(time.time())
	return REQUERST_TEST_EVENT_TMPL % (to_user, from_user, timestamp, content)





REQUEST_IMAGE_MESSAGE_TEST_TMPL = u"""
	<xml><tousername><![CDATA[%s]]></tousername>
	<fromusername><![CDATA[%s]]></fromusername>
	<createtime>%d</createtime>
	<msgtype><![CDATA[image]]></msgtype>
	<picurl><![CDATA[http://mmbiz.qpic.cn/mmbiz/xhdgdktISRzrrib7keSrOfJPEvo76NdAyOj2fvmriaDLWXQYov13Eh0FLI7ESrDZl2XbvGyL5ESLy86p6HqTYOLw/0]]></picurl>
	<msgid>5938224064077240899</msgid>
	<mediaid><![CDATA[7YdZjcDMv3V34uZOEmBZwQuhAcpguERfOv8TCEFRLhJFeU-4FiQMM2_6HaBYkMZF]]></mediaid>
	</xml>
	"""
def get_image_message_test_request(to_user, from_user, content):
	timestamp = int(time.time())
	return REQUEST_IMAGE_MESSAGE_TEST_TMPL % (to_user, from_user, timestamp)


