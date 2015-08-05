# -*- coding: utf-8 -*-

__author__ = 'chuter'

import json

import api_settings
import weixin_error_codes as errorcodes

from core.jsonresponse import decode_json_str
from core.exceptionutil import unicode_full_stack
from utils.url_helper import complete_get_request_url
from core.weixin_media_saver import save_weixin_user_head_img

from watchdog.utils import watchdog_error

from weixin.user.access_token import update_access_token

"""
微信Api

微信平台针对认证后的服务号提供api接口，具体列表和文档登录微信公众
平台后点击左侧导航栏中服务下的我的服务可以看到

该模块对微信平台提供的api接口进行描述，便于在程序中进行微信api的访问
每一个api的调用该模块根据微信平台api的协议进行相应请求的组织，然后
通过weixin_http_client（默认使用WeixinHttpClient）进行实际请求返回处理结果

如果需要测试，给定weixin_http_client的stub或者mock的实现即可

目前提供的api接口有：

get_user_info
	获取用户基本信息
	文档参见http://mp.weixin.qq.com/wiki/index.php?title=%E8%8E%B7%E5%8F%96%E7%94%A8%E6%88%B7%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF

get_qrcode
	通过ticket换取二维码，返回二维码图片(jpg格式)内容
	文档参见http://mp.weixin.qq.com/wiki/index.php?title=%E7%94%9F%E6%88%90%E5%B8%A6%E5%8F%82%E6%95%B0%E7%9A%84%E4%BA%8C%E7%BB%B4%E7%A0%81

create_qrcode_ticket
	创建二维码ticket
	文档参见http://mp.weixin.qq.com/wiki/index.php?title=%E7%94%9F%E6%88%90%E5%B8%A6%E5%8F%82%E6%95%B0%E7%9A%84%E4%BA%8C%E7%BB%B4%E7%A0%81

send_custom_msg
	发送客服消息
	文档参见http://mp.weixin.qq.com/wiki/index.php?title=%E5%8F%91%E9%80%81%E5%AE%A2%E6%9C%8D%E6%B6%88%E6%81%AF

upload_media
	上传多媒体文件
	文档参见http://mp.weixin.qq.com/wiki/index.php?title=%E4%B8%8A%E4%BC%A0%E4%B8%8B%E8%BD%BD%E5%A4%9A%E5%AA%92%E4%BD%93%E6%96%87%E4%BB%B6

download_media
	下载多媒体文件
	文档参见http://mp.weixin.qq.com/wiki/index.php?title=%E4%B8%8A%E4%BC%A0%E4%B8%8B%E8%BD%BD%E5%A4%9A%E5%AA%92%E4%BD%93%E6%96%87%E4%BB%B6

create_customerized_menu
	创建自定义菜单
	文档参见http://mp.weixin.qq.com/wiki/index.php?title=%E8%87%AA%E5%AE%9A%E4%B9%89%E8%8F%9C%E5%8D%95%E5%88%9B%E5%BB%BA%E6%8E%A5%E5%8F%A3

create_customerized_menu
	删除自定义菜单
	文档参见http://mp.weixin.qq.com/wiki/index.php?title=%E8%87%AA%E5%AE%9A%E4%B9%89%E8%8F%9C%E5%8D%95%E5%88%A0%E9%99%A4%E6%8E%A5%E5%8F%A3

update_customerized_menu
	更新自定义菜单，微信没有提供更新接口
	实际操作是先调用删除再调用创建接口完成更新操作

每个接口调用如果发生异常会抛出WeixinApiError, 可通过该异常示例的
error_response属性来获取微信的api反馈信息，error_response包含的信息有：
errorcode: 错误代码
errmsg: 错误信息
detail: 异常详情

如果发现access_token失效则需要提供最新的access_token，重新获取WeixinApi实例
"""

class ObjectAttrWrapedInDict(dict):
	def __init__(self, src_dict):
		for key, value in src_dict.items():
			setattr(self, key, value)

	def __getattribute__(self, key):
		if not hasattr(self, key):
			return None

		return dict.__getattribute__(self, key)

import json

class WeixinApiResponse(object):

	def __init__(self, weixin_response):
		if type(weixin_response) != dict:
			self.response_json = self.__parse_response(weixin_response_text)
		else:
			self.response_json = weixin_response

		self.errcode = self.response_json.get('errcode', errorcodes.SUCCESS_CODE)
		self.errmsg = self.response_json.get('errmsg', '')

	def is_failed(self):
		return self.response_json.get('errcode', errorcodes.SUCCESS_CODE) != errorcodes.SUCCESS_CODE

	def get_errormsg_in_zh(self):
		return errorcodes.code2msg.get(self.errcode, self.errmsg)

	def __parse_response(self, response_text):
		response_text = response_text.strip()
		return decode_json_str(response_text)

class WeixinApiError(Exception):
	def __init__(self, weixin_error_response):
		self.error_response = weixin_error_response

	def __unicode__(self):
		return u"errcode:{}\nerrmsg:{}\ndetail:{}".format(
			self.error_response.errcode,
			self.error_response.errmsg,
			self.error_response.detail
			)

	def __str__(self):
		return self.__unicode__().encode('utf-8')

"""
微信Api提供的微信用户基本信息，包括以下属性：
subscribe : 用户是否订阅该公众号标识，值为0时，代表此用户没有关注该公众号，拉取不到其余信息
openid : 用户的标识，对当前公众号唯一
nickname : 昵称
sex : 用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
city : 用户所在城市
province : 用户所在省份
language : 用户的语言，简体中文为zh_CN
headimgurl : 用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表640*640正方形头像），用户没有头像时该项为空
subscribe_time : 用户关注时间，为时间戳。如果用户曾多次关注，则取最后关注时间

假设现在持有与具体实例绑定的标识符userinfo
直接使用userinfo.openid获取对应的用户标识等属性
如果所获取的属性不存在那么会得到None
"""
class WeixinUserInfo(ObjectAttrWrapedInDict):
	def __init__(self, src_dict):
		super(WeixinUserInfo, self).__init__(src_dict)

"""
微信Api提供的二维码Ticket信息，包括以下属性：
ticket: 获取的二维码ticket，凭借此ticket可以在有效时间内换取二维码
expire_seconds: 二维码的有效时间，以秒为单位。最大不超过1800
"""
class QrcodeTicket(ObjectAttrWrapedInDict):
	TEMPORARY = 'QR_SCENE'
	PERMANENT = 'QR_LIMIT_SCENE'

	MAX_EXPIRE_SECONDS = 1800

	def __init__(self, src_dict):
		super(QrcodeTicket, self).__init__(src_dict)

"""
微信Api错误信息，包含以下属性：
errorcode : 错误代码，全部错误代码请参见weixin_error_codes
errmsg : 错误信息
detail : 异常堆栈
"""
class WeixinErrorResponse(ObjectAttrWrapedInDict):
	def __init__(self, src_dict):
		super(WeixinErrorResponse, self).__init__(src_dict)

		if not hasattr(self, 'detail'):
			self.detail = ''


def build_system_exception_response():
	response_dict = {}
	response_dict['errcode'] = errorcodes.SYSTEM_ERROR_CODE
	response_dict['errmsg'] = errorcodes.code2msg[errorcodes.SYSTEM_ERROR_CODE]
	response_dict['detail'] = unicode_full_stack()
	return WeixinErrorResponse(response_dict)

from custom_message import build_custom_message_json_str
from weixin.user.models import inactive_mpuser_access_token

head_img_saver = save_weixin_user_head_img

class WeixinApi(object):
	def __init__(self, mpuser_access_token, weixin_http_client):
		if mpuser_access_token is None or mpuser_access_token.access_token is None:
			raise ValueError(u'缺少授权信息')

		# mpuser = mpuser_access_token.mpuser
		# if not mpuser.is_service or not mpuser.is_certified:
		# 	raise ValueError(u'只有授权过的服务号才可以使用Api')

		# if not mpuser_access_token.is_active:
		# 	raise ValueError(u'授权已经过期')

		self.mpuser_access_token = mpuser_access_token
		self.weixin_http_client = weixin_http_client

	def get_user_info(self, openid, is_retry=False):
		param_dict = {'openid':openid}
		request_url = self._complete_weixin_api_get_request_url('cgi-bin/user/info', param_dict)

		try:
			api_response = self.weixin_http_client.get(request_url)
		except:
			self._raise_system_error(u'获取用户基本信息')

		if self._is_error_response(api_response):
			if self._is_error_dueto_access_token(api_response):
				if is_retry:
					self._raise_request_error(api_response, u'获取用户基本信息')
				else:
					#如果由于access_token的问题，那么先更新access_token后重试
					if (update_access_token(self.mpuser_access_token)):
						return get_user_info(openid, True)
					else:
						self._raise_request_error(api_response, u'获取用户基本信息')
			else:
				self._raise_request_error(api_response, u'获取用户基本信息')

		user_info = WeixinUserInfo(api_response)

		#保存微信用户头像，使用本地地址
		if hasattr(user_info, 'headimgurl'):
			head_img_url = head_img_saver(user_info.headimgurl)
			if head_img_url:
				user_info.headimgurl = head_img_url
			else:
				user_info.headimgurl = ''
		else:
			user_info.headimgurl = ''

		return user_info

	#获取二维码图片，返回字节流，如果ticket非法返回None
	#该方法供后台代码使用，如果是前端代码可直接使用ticket在js中访问微信获取
	def get_qrcode(self, ticket):
		if ticket is None or len(ticket) == 0:
			return None

		url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={}".format(ticket)

		weixin_response = None
		try:
			weixin_response = urllib2.urlopen(url)
			return weixin_response.read()
		except:
			self._raise_system_error(u'获取带参数的二维码')
		finally:
			if weixin_response:
				try:
					weixin_response.close()
				except:
					pass

	def __should_change_to_delete_request(menu_json_str):
		if menu_json_str is None:
			return True

		if isinstance(menu_json_str, dict):
			menu_json_str = menu_json_str.__str__()

		try:
			menu_json_str = re.sub('\\s+', '', menu_json_str)
			return menu_json_str == '{}'
		except:
			return False

	def create_customerized_menu(self, menu_json, is_retry=False):
		if self.__should_change_to_delete_request(menu_json):
			return self.delete_customerized_menu()

		if isinstance(menu_json, str):
			try:
				menu_json = json.loads(menu_json)
			except:
				self._raise_system_error(u'自定义菜单数据格式错误')

		request_url = self._complete_weixin_api_get_request_url('cgi-bin/menu/create', {})

		try:
			api_response = self.weixin_http_client.post(request_url, menu_json)
		except:
			self._raise_system_error(u'创建自定义菜单')

		if self._is_error_response(api_response):
			if self._is_error_dueto_access_token(api_response):
				if is_retry:
					self._raise_request_error(api_response, u'创建自定义菜单')
				else:
					#如果由于access_token的问题，那么先更新access_token后重试
					if (update_access_token(self.mpuser_access_token)):
						return create_customerized_menu(menu_json, True)
					else:
						self._raise_request_error(api_response, u'创建自定义菜单')
			else:
				self._raise_request_error(api_response, u'创建自定义菜单')

		return True

	def delete_customerized_menu(self, is_retry=False):
		request_url = self._complete_weixin_api_get_request_url('cgi-bin/menu/delete', {})

		try:
			api_response = self.weixin_http_client.get(request_url)
		except:
			self._raise_system_error(u'删除自定义菜单')

		if self._is_error_response(api_response):
			if self._is_error_dueto_access_token(api_response):
				if is_retry:
					self._raise_request_error(api_response, u'删除自定义菜单')
				else:
					#如果由于access_token的问题，那么先更新access_token后重试
					if (update_access_token(self.mpuser_access_token)):
						return delete_customerized_menu(True)
					else:
						self._raise_request_error(api_response, u'删除自定义菜单')
			else:
				self._raise_request_error(api_response, u'删除自定义菜单')

		return True

	def update_customerized_menu(self, menu_json):
		if self.__should_change_to_delete_request(menu_json):
			return self.delete_customerized_menu()

		self.delete_customerized_menu()
		return self.create_customerized_menu(menu_json)

	#创建二维码ticket
	#scene_id为定义的二维码所使用的场景值ID，临时二维码时为32位非0整型，
	#永久二维码时最大值为1000（目前参数只支持1--100000）
	#ticket_type为二维码类型，默认为临时类型
	def create_qrcode_ticket(self, scene_id, ticket_type=QrcodeTicket.TEMPORARY, is_retry=False):
		post_param_json_str = '{"expire_seconds": %d, "action_name": "%s", "action_info": {"scene": {"scene_id": %d}}}'%(
			QrcodeTicket.MAX_EXPIRE_SECONDS, ticket_type, scene_id)

		post_param_json = decode_json_str(post_param_json_str)

		request_url = self._complete_weixin_api_get_request_url('cgi-bin/qrcode/create', {})

		try:
			api_response = self.weixin_http_client.post(request_url, post_param_json)
		except:
			self._raise_system_error(u'创建带参数的二维码')

		if self._is_error_response(api_response):
			if self._is_error_dueto_access_token(api_response):
				if is_retry:
					self._raise_request_error(api_response, u'创建带参数的二维码')
				else:
					#如果由于access_token的问题，那么先更新access_token后重试
					if (update_access_token(self.mpuser_access_token)):
						return create_qrcode_ticket(scene_id, ticket_type, True)
					else:
						self._raise_request_error(api_response, u'创建带参数的二维码')
			else:
				self._raise_request_error(api_response, u'创建带参数的二维码')

		return QrcodeTicket(api_response)

	def send_custom_msg(self, sendto_openid, custom_msg):
		post_param_json_str = None

		try:
			post_param_json_str = build_custom_message_json_str(sendto_openid, custom_msg)
		except:
			self._raise_system_error(u'创建要发送的客服消息')

		if post_param_json_str is None:
			self._raise_system_error(u'要发送的客服消息为None')

		post_param_json = decode_json_str(post_param_json_str)
		request_url = self._complete_weixin_api_get_request_url('cgi-bin/message/custom/send', {})

		try:
			api_response = self.weixin_http_client.post(request_url, post_param_json)
		except:
			self._raise_system_error(u"发送客服消息:\n{}".format(post_param_json_str))

		if self._is_error_response(api_response):
			self._raise_request_error(api_response, u"发送客服消息:\n{}".format(post_param_json_str))

		return api_response

	def upload_media(self):
		pass

	def download_media(self):
		pass

	def _notify_api_request_error(self, apierror, api_name=''):
		notify_msg = u"微信api调用失败，api:{}\n错误信息:{}".format(api_name, apierror.__unicode__())
		watchdog_error(notify_msg)

	def _raise_request_error(self, response, api_name=''):
		error_response = WeixinErrorResponse(response)

		if error_response.errcode in (errorcodes.ILLEGAL_ACCESS_TOKEN_CODE,
			errorcodes.ACCESS_TOKEN_EXPIRED_CODE, errorcodes.INVALID_ACCESS_TOKEN_CODE):
			inactive_mpuser_access_token(self.mpuser_access_token)

		apierror = WeixinApiError(error_response)

		self._notify_api_request_error(apierror, api_name)

		raise apierror

	def _raise_system_error(self, api_name=''):
		system_error_response = build_system_exception_response()
		apierror = WeixinApiError(system_error_response)

		self._notify_api_request_error(apierror, api_name)

		raise apierror

	def _is_error_response(self, response):
		if type(response) == dict:
			return response.get('errcode', errorcodes.SUCCESS_CODE) != errorcodes.SUCCESS_CODE
		else:
			return False

	def _is_error_dueto_access_token(self, response):
		if type(response) == dict:
			return response.get('errcode', errorcodes.SUCCESS_CODE) in (errorcodes.ILLEGAL_ACCESS_TOKEN_CODE,
				errorcodes.ACCESS_TOKEN_EXPIRED_CODE, errorcodes.INVALID_ACCESS_TOKEN_CODE)
		else:
			return False


	def _complete_weixin_api_get_request_url(self, path, param_dict={}):
		if param_dict is None:
			param_dict = {}

		if not param_dict.has_key('access_token'):
			param_dict['access_token'] = self.mpuser_access_token.access_token

		return complete_get_request_url(
			api_settings.WEIXIN_API_PROTOCAL,
			api_settings.WEIXIN_API_DOMAIN,
			path,
			param_dict
			)

"""
进行微信平台Http请求的客户端
返回结果格式为json格式，

错误信息示例为：
{
	errcode : 42001,
	errmsg : "access_token expired",
	detail : "详细的异常堆栈"
}

正确信息针对具体api，例如对于获取用户信息api返回结果：
{
    "subscribe": 1,
    "openid": "o6_bmjrPTlm6_2sgVt7hMZOPfL2M",
    "nickname": "Band",
    "sex": 1,
    "language": "zh_CN",
    "city": "广州",
    "province": "广东",
    "country": "中国",
    "headimgurl":    "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
   "subscribe_time": 1382694957
}

详情请参见微信平台官方Api接口文档

可通过weixin_error_codes获取每个错误代码对应的详细的中文说明文字
"""
import json
import urllib2
class WeixinHttpClient(object):
	def __init__(self):
		super(WeixinHttpClient, self).__init__()

	def get(self, url):
		weixin_response = urllib2.urlopen(url)

		try:
			return self._parse_response(weixin_response.read().decode('utf-8'))
		finally:
			if weixin_response:
				try:
					weixin_response.close()
				except:
					pass

	def post(self, url, post_param_json):
		req = urllib2.Request(url)
		opener = urllib2.build_opener()

		weixin_response = opener.open(req, json.dumps(post_param_json, ensure_ascii=False).encode('utf-8'))

		try:
			return self._parse_response(weixin_response.read().decode('utf-8'))
		finally:
			if weixin_response:
				try:
					weixin_response.close()
				except:
					pass

	def upload(self, url, upload_str_data):
		pass

	def download(self, url):
		pass

	def _parse_response(self, response_text):
		response_text = response_text.strip()

		if response_text.startswith(u'{') and response_text.endswith(u'}'):
			try:
				return decode_json_str(response_text)
			except:
				return response_text
		else:
			return response_text