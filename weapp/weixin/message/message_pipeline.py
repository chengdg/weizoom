# -*- coding: utf-8 -*-

__author__ = 'chuter'


from handler.weixin_message import *
from handler.message_handler import *

from handler.message_handle_context import *

from account.models import UserProfile
from core.exceptionutil import unicode_full_stack

from django.conf import settings

from watchdog.utils import watchdog_fatal, watchdog_info
from weixin.user.models import *
from weixin.message_util.WXBizMsgCrypt import WXBizMsgCrypt

from weixin.message import generator

"""
MessagePipeline即收到的消息的处理途径
MessagePipeline中通过组织其中的MessageHandler对消息依次进行处理

对任意一条消息，分三个阶段的处理：
1. 消息预处理
   该阶段，会使用含有pre_processing方法的所有MessageHandler进行依
   次处理，且不分MessageHandler的先后顺序
2. 消息处理
   该阶段，会使用含有handle方法的所有MessageHandler进行顺序处理，
   如果有一个MessageHandler正确处理，返回了有效结果则结束该阶段
   的处理
3. 消息后处理
   该阶段，会使用含有post_processing方法的所有MessageHandler进行依
   次处理，且不分MessageHandler的先后顺序

结构如下图所示：

			 —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— ——
			|                                                     |
		    | —— —— —— ——       —— —— —— ——          —— —— —— ——  | 
msg —— ——>  || bhandler1 | --> | bhandler2 | ... -> | bhandlerm | | —— ——
	        | —— —— —— ——       —— —— —— ——          —— —— —— ——  |      |
		    |                                                     |      |
		     —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— ——       |
                         —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— ——                                    
                        |
                        |
                       \ /
	           —— —— —— —— —— —— —— ——
	          |                       |
	          |     —— —— —— ——       |
	 ......   |    | handler1  |      |
	 .        |     —— —— —— ——       |
	 .        |                       |
	 .        |     —— —— —— ——       |
	 ......   |    | handler2  |      |
	 .        |     —— —— —— ——       |
	 .        |          .            |
	 ......   |          .            |
	 .        |          .            |
	 .        |     —— —— —— ——       |
	 ......   |    | handlern  |      |
	 |        |     —— —— —— ——       |
	 |        |                       |
	 |         —— —— —— —— —— —— —— ——
	 |
     | response
     |
	 |		 —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— ——
     |		|                                                     |
	 |	    | —— —— —— ——       —— —— —— ——          —— —— —— ——  | 
      ——>   || ahandler1 | --> | ahandler2 | ... -> | ahandlerk | | —— —— > response
	        | —— —— —— ——       —— —— —— ——          —— —— —— ——  | 
		    |                                                     | 
		     —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— ——  

示意图中的bhandler表示对消息进行预处理的handler
ahandler表示对消息进行后处理的handler

该设计和结构类似django中的MiddleWare的设计，只需要通过给定所需要配备的
handler的类路径信息(例如：weixin.handlers.KeywordHandler)，
settings.py中有默认的配置项DEFAULT_MSG_HANDLER_CLASSES
"""
class MessagePipeline(object):
	def __init__(self, handler_classes=None, haltonfailure=True):
		if None == handler_classes:
			if settings.IS_MESSAGE_OPTIMIZATION:
				handler_classes = settings.OPTIMIZATION_MSG_HANDLER_CLASSES
			else:
				handler_classes = settings.DEFAULT_MSG_HANDLER_CLASSES

		self.haltonfailure = haltonfailure

		self.pre_processing_handlers  = []
		self.handlers = []
		self.post_processing_handlers = []

		self._load_handlers(handler_classes)
	
		if len(self.handlers) == 0:
			raise ValueError('empty valid message handlers : ' + handler_classes.__str__())

	def _load_handlers(self, handler_classes):
		from django.core import exceptions
		from django.utils.importlib import import_module

		for handler_path in handler_classes:
			try:
				handler_module, handler_classname = handler_path.rsplit('.', 1)
			except ValueError:
				raise exceptions.ImproperlyConfigured('%s isn\'t a message handler module' % handler_path)
        
			try:
				module = import_module(handler_module)
			except ImportError, e:
				raise exceptions.ImproperlyConfigured('Error importing message handler %s: "%s"' % (handler_module, e))
          
			try:
				handler_class = getattr(module, handler_classname)
			except AttributeError:
				raise exceptions.ImproperlyConfigured('MessageHandler module "%s" does not define a "%s" class' % (handler_module, handler_class))
          
			try:
				handler_instance = handler_class()
			except:
				print "failed to create create instance for handler %s, cause:\n%s" % (handler_path, unicode_full_stack())
				if self.haltonfailure:
					raise ValueError("can\'t create instance for handler " + handler_path)
				else:
					continue
			
			if hasattr(handler_instance, 'handle'):
				self.handlers.append(handler_instance)

			if hasattr(handler_instance, 'pre_processing'):
				self.pre_processing_handlers.append(handler_instance)

			if hasattr(handler_instance, 'post_processing'):
				self.post_processing_handlers.append(handler_instance)

	def handle(self, request, webapp_id, old_process=True):
		try:
			if webapp_id:
				user_profile = UserProfile.objects.get(webapp_id=webapp_id)
			else:
				user_profile = None
		except:
			notify_msg = u"MessagePipeline，current_webapp_id:{}\n错误信息:{}".format(webapp_id, unicode_full_stack())
			watchdog_info(notify_msg)
			return None
		wxiz_msg_crypt = None
		is_from_simulator = False
		msg_signature = request.GET.get('msg_signature', None)
		timestamp = request.GET.get('timestamp', None)
		nonce = request.GET.get('nonce', None)
		encrypt_type = request.GET.get('encrypt_type', None)
		signature = request.GET.get('signature', None)
		component_info = None
		if old_process:
			if 'weizoom_test_data' in request.GET:
				xml_message = self._get_raw_message(request)
			else:
				xml_message = self._get_raw_message(request).decode('utf-8')
				if msg_signature and timestamp and nonce:
					weixin_mp_user = WeixinMpUser.get_weixin_mp_user(user_profile.user_id)
					if weixin_mp_user and weixin_mp_user.aeskey > AESKEY_NORMAL and weixin_mp_user.encode_aeskey:
						mp_user_access_token = WeixinMpUser.get_weixin_mp_user_access_token_by_mp_user(weixin_mp_user)
						if mp_user_access_token.app_id:
							wxiz_msg_crypt = WXBizMsgCrypt(user_profile.mp_token, weixin_mp_user.encode_aeskey, mp_user_access_token.app_id)
							_,xml_message = wxiz_msg_crypt.DecryptMsg(xml_message, msg_signature, timestamp, nonce)
							is_aeskey = True
		else:
			if 'weizoom_test_data' in request.GET:
				xml_message = self._get_raw_message(request)
			else:
				xml_message = self._get_raw_message(request).decode('utf-8')
				component_info = ComponentInfo.objects.filter(is_active=True)[0]
				wxiz_msg_crypt = WXBizMsgCrypt(component_info.token, component_info.ase_key, component_info.app_id)#"2950d602ffb613f47d7ec17d0a802b", "BPQSp7DFZSs1lz3EBEoIGe6RVCJCFTnGim2mzJw5W4I", "wx984abb2d00cc47b8")
				_,xml_message = wxiz_msg_crypt.DecryptMsg(xml_message, msg_signature, timestamp, nonce)

		if xml_message is None or len(xml_message) == 0:
			return None

		message = parse_weixin_message_from_xml(xml_message)
		
		if webapp_id != None:
			handling_context = MessageHandlingContext(message, xml_message, user_profile, request)

			#预处理
			self._pre_processing(handling_context, is_from_simulator)
			if not handling_context.should_process:
				return None

			prcoess_handler = None
			response_content = None
			for handler in self.handlers:
				process_handler = handler
				try:
					response_content = handler.handle(handling_context, is_from_simulator)

					if EMPTY_RESPONSE_CONTENT == response_content:
						response_content = None
						break

					if response_content:
						break
				except:
					self._handle_exception(handler, user_profile, xml_message)

					if self.haltonfailure:
						break

			#后处理
			self._post_processing(handling_context, process_handler, response_content, is_from_simulator)
		else:
			content	= 'SUCCESS'
			if message.toUserName ==  "gh_3c884a361561":
				if message.event:
					content = "%sfrom_callback" % (message.event)
				elif message.content.find('QUERY_AUTH_CODE') > -1:
					auth_code = message.content.split(":")[1]
					from core.wxapi.agent_weixin_api import WeixinApi, WeixinHttpClient
					weixin_http_client = WeixinHttpClient()
					weixin_api = WeixinApi(component_info.component_access_token, weixin_http_client)
					result = weixin_api.api_query_auth(component_info.app_id, auth_code)
					print '=======result----1:', result
					if result.has_key('authorization_info'):
						authorization_info = result['authorization_info']
						func_info_ids = []
						func_info = authorization_info['func_info']
						if isinstance(func_info, list):
							for funcscope_category in func_info:
								funcscope_category_id = funcscope_category.get('funcscope_category', None)
								if funcscope_category_id:
									func_info_ids.append(str(funcscope_category_id.get('id')))
						authorizer_appid = authorization_info['authorizer_appid']
						authorizer_access_token=authorization_info['authorizer_access_token']
						authorizer_refresh_token=authorization_info['authorizer_refresh_token']
						url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % authorizer_access_token
						post_json = '{ "touser":"%s", "msgtype":"text", "text": {"content":"%s_from_api" } }' % (message.fromUserName, auth_code)
						print '----0'
						print post_json
						print '---1'
						result = weixin_http_client.post(url, post_json)
						print result
						content = "%s_from_api" % auth_code
					else:
						print '---------------------Error----------------------'

				else:
					content = 'TESTCOMPONENT_MSG_TYPE_TEXT_callback'
			else:
				content	= 'SUCCESS'

			response_content = generator.get_text_request(message.fromUserName, message.toUserName, content)

		if response_content and wxiz_msg_crypt:
			_,response_content = wxiz_msg_crypt.EncryptMsg(response_content.encode('utf-8'), nonce, timestamp)
		return response_content



	def _pre_processing(self, handling_context, is_from_simulator):
		for pre_processing_handler in self.pre_processing_handlers:
			try:
				pre_processing_handler.pre_processing(handling_context, is_from_simulator)
				if not handling_context.should_process:
					return
			except:
				self._handle_exception(pre_processing_handler, \
						handling_context.user_profile, handling_context.xml_message)

	def _post_processing(self, handling_context, handler, response_content, is_from_simulator):
		for post_processing_handler in self.post_processing_handlers:
			try:
				post_processing_handler.post_processing(handling_context, handler, response_content, is_from_simulator)
			except:
				self._handle_exception(post_processing_handler, \
						handling_context.user_profile, handling_context.xml_message)

	def _get_raw_message(self, request):
		if 'weizoom_test_data' in request.GET:
			#通过模拟器来的数据
			return request.POST['weizoom_test_data']
		else:
			#通过微信来的数据
			if hasattr(request, 'raw_post_data'):
				return request.raw_post_data
			else:
				return request.body

	def _handle_exception(self, handler, user_profile, xml_message):
		assert (handler and user_profile)

		alert_message = u"处理消息失败，处理实现：{}\n所处理消息:\n{}\n异常信息:\n{}". \
				format(handler.__class__.__name__, xml_message, unicode_full_stack())

		watchdog_fatal(alert_message)

