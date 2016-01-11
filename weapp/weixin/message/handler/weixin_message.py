# -*- coding: utf-8 -*-
"""@package weixin.message.weixin_message

定义了微信消息的类：

 * TextWeixinMessage
 * EventWeixinMessage
 * ImageWeixinMessage
 * LocationWeixinMessage
 * LinkWeixinMessage
 * VoiceWeixinMessage
"""

__author__ = 'chuter'

from BeautifulSoup import BeautifulSoup

class WeixinMessageTypes(object):
	def __init__(self):
		raise NotImplementedError

	TEXT = 'text'
	IMAGE = 'image'
	LOCATION = 'location'
	LINK = 'link'
	EVENT = 'event'
	VOICE = 'voice'


class ReveivedWeixinMessageFields(object):
	"""
	微信消息的字段
	"""
	def __init__(self):
		raise NotImplementedError

	# 所有类型消息都包含的属性
	ToUserName = 'ToUserName'
	FromUserName = 'FromUserName'
	CreateTime = 'CreateTime'
	MsgType = 'MsgType'
	MsgId = 'MsgId'
	Ticket = 'ticket'


class ReveivedTextWeixinMessageFields(ReveivedWeixinMessageFields):
	"""
	文本消息的字段
	"""
	def __init__(self):
		raise NotImplementedError

	# 文本消息独有的属性
	Content = 'Content'


class ReveivedEventWeixinMessageFields(ReveivedWeixinMessageFields):
	"""
	接收事件
	"""
	def __init__(self):
		raise NotImplementedError

	# 事件消息独有的属性
	Event = 'Event'
	EventKey = 'EventKey'


class ReveivedEventMassSendResultWeixinMessageFields(ReveivedEventWeixinMessageFields):
	def __init__(self):
		raise NotImplementedError

	# 事件消息独有的属性
	Status = 'status'
	TotalCount = 'totalcount'
	FilterCount = 'filtercount'
	SentCount = 'sentcount'
	ErrorCount = 'errorcount'


class ReveivedImageWeixinMessageFields(ReveivedWeixinMessageFields):
	def __init__(self):
		raise NotImplementedError

	# 图片消息独有的属性
	PicUrl = 'PicUrl'

class ReveivedLcationWeixinMessageFields(ReveivedWeixinMessageFields):
	def __init__(self):
		raise NotImplementedError	

	# 地理位置消息独有的属性
	Location_X = 'Location_X'
	Location_Y = 'Location_Y'
	Scale = 'Scale'
	Label = 'Label'

class ReveivedLinkWeixinMessageFields(ReveivedWeixinMessageFields):
	def __init__(self):
		raise NotImplementedError	

	# 链接消息独有的属性
	Title = 'Title'
	Description = 'Description'
	Url = 'Url'


class ReveivedVoiceWeixinMessageFields(ReveivedWeixinMessageFields):
	def __init__(self):
		raise NotImplementedError

	# 语音消息独有的属性
	MediaId = 'MediaId'
	Format = 'Format'
	Recognition = 'Recognition'


class WeixinMessageEvents(object):
	def __init__(self):
		raise NotImplementedError

	SUBSCRIBE = 'subscribe'
	UNSUBSCRIBE = 'unsubscribe'
	CLICK = 'CLICK'


class WeixinMessage(object):
	"""
	微信消息的类
	"""

	def __init__(self, messageSoup):
		"""
		根据BeautifulSoup解析的微信消息的soup创建WeixinMessage实例
		"""
		
		if None == messageSoup:
			raise ValueError('messageSoup can not be None')

		if type(messageSoup) != type(BeautifulSoup('dummy')):
			raise ValueError('messageSoup must be BeautifulSoup type')			

		self._check_message_validity(messageSoup)
		self.__message_fields_dict__ = {}

		self.msgType = messageSoup.msgtype.text
		self.toUserName = messageSoup.tousername.text
		self.fromUserName = messageSoup.fromusername.text
		self.createTime = messageSoup.createtime.text

		#如果消息经过转化，source标识了转过前的消息类型
		if hasattr(messageSoup, 'source') and messageSoup.source:
			self.source = messageSoup.source.text
		else:
			self.source = messageSoup.msgtype.text
		if hasattr(messageSoup, 'ticket') and messageSoup.ticket:
			self.ticket = messageSoup.ticket.text
		else:
			self.ticket = None

		if hasattr(messageSoup, 'event') and messageSoup.event:
			self.event = messageSoup.event.text
		else:
			self.event = None
	
		if hasattr(messageSoup, ReveivedEventMassSendResultWeixinMessageFields.Status) and messageSoup.status:
			self.status = messageSoup.status.text
		else:
			self.status = None

		if hasattr(messageSoup, ReveivedEventMassSendResultWeixinMessageFields.TotalCount) and messageSoup.totalcount:
			self.totalCount = messageSoup.totalcount.text
		else:
			self.totalCount = None

		if hasattr(messageSoup, ReveivedEventMassSendResultWeixinMessageFields.FilterCount) and messageSoup.filtercount:
			self.filterCount = messageSoup.filtercount.text
		else:
			self.filterCount = None

		if hasattr(messageSoup, ReveivedEventMassSendResultWeixinMessageFields.SentCount) and messageSoup.sentcount:
			self.sentCount = messageSoup.sentcount.text
		else:
			self.sentCount = None

		if hasattr(messageSoup, ReveivedEventMassSendResultWeixinMessageFields.ErrorCount) and messageSoup.errorcount:
			self.errorCount = messageSoup.errorcount.text
		else:
			self.errorCount = None

		if hasattr(messageSoup, 'msgid') and messageSoup.msgid:
			self.msgId = messageSoup.msgid.text
		else:
			self.msgId = None

		self.is_optimization_message = self.is_optimization_message()
		# if WeixinMessageTypes.EVENT != messageSoup.msgtype.text:
		# 	self.msgId = messageSoup.msgid.text
		# else:
		# 	self.msgId = None

	def _check_message_validity(self, messageSoup):
		assert (messageSoup)

		if not messageSoup.fromusername or not messageSoup.tousername \
				or not messageSoup.createtime or not  messageSoup.msgtype:
			raise ValueError('invalid weixin message:\n' + messageSoup.__str__())

		if WeixinMessageTypes.EVENT != messageSoup.msgtype.text:
			if not messageSoup.msgid:
				raise ValueError('invalid weixin message(no msgid):\n' + messageSoup.__str__())				


	def is_event_message(self):
		return WeixinMessageTypes.EVENT == self.msgType

	def is_voice_message(self):
		return WeixinMessageTypes.VOICE == self.msgType

	def is_text_message(self):
		return WeixinMessageTypes.TEXT == self.msgType

	def is_image_message(self):
		return WeixinMessageTypes.IMAGE == self.msgType

	def is_location_message(self):
		return WeixinMessageTypes.LOCATION == self.msgType

	def is_link_message(self):
		return WeixinMessageTypes.LINK == self.msgType

	def is_optimization_message(self):
		if self.is_event_message and self.event:
			if self.event.upper() == WeixinMessageEvents.CLICK:
				return True
			else:
				return False
		else:
			return True


class TextWeixinMessage(WeixinMessage):
	"""
	文本消息的类
	"""

	def __init__(self, messageSoup):
		super(TextWeixinMessage, self).__init__(messageSoup)

		self.content = messageSoup.content.text

	def _check_message_validity(self, messageSoup):
		assert (messageSoup)

		super(TextWeixinMessage, self)._check_message_validity(messageSoup)

		if None == messageSoup.content:
			raise ValueError('invalid weixin text message:\n' + messageSoup.__str__())

class EventWeixinMessage(WeixinMessage):
	"""
	事件消息的类
	"""

	def __init__(self, messageSoup):
		super(EventWeixinMessage, self).__init__(messageSoup)

		self.event = messageSoup.event.text
		self.eventKey = messageSoup.eventkey.text if messageSoup.eventkey else ''

	def _check_message_validity(self, messageSoup):
		assert (messageSoup)

		super(EventWeixinMessage, self)._check_message_validity(messageSoup)

		if None == messageSoup.event:
			raise ValueError('invalid weixin event message:\n' + messageSoup.__str__())


class ImageWeixinMessage(WeixinMessage):
	"""
	图片消息的类
	"""

	def __init__(self, messageSoup):
		super(ImageWeixinMessage, self).__init__(messageSoup)

		self.picUrl = messageSoup.picurl.text
		self.mediaId = messageSoup.mediaid.text

	def _check_message_validity(self, messageSoup):
		assert (messageSoup)

		super(ImageWeixinMessage, self)._check_message_validity(messageSoup)

		if None == messageSoup.picurl:
			raise ValueError('invalid weixin image message:\n' + messageSoup.__str__())


class LocationWeixinMessage(WeixinMessage):
	"""
	地点消息的类
	"""
	def __init__(self, messageSoup):
		super(LocationWeixinMessage, self).__init__(messageSoup)

		self.location_X = messageSoup.location_x.text
		self.location_Y = messageSoup.location_y.text
		self.scale = messageSoup.scale.text
		self.label = messageSoup.label.text

	def _check_message_validity(self, messageSoup):
		assert (messageSoup)

		super(LocationWeixinMessage, self)._check_message_validity(messageSoup)

		if None == messageSoup.location_x or None == messageSoup.location_y \
				or None == messageSoup.scale or None == messageSoup.label:
			raise ValueError('invalid weixin location message:\n' + messageSoup.__str__())


class LinkWeixinMessage(WeixinMessage):
	"""
	连接消息
	"""
	def __init__(self, messageSoup):
		super(LinkWeixinMessage, self).__init__(messageSoup)

		self.title = messageSoup.title.text
		self.description = messageSoup.description.text
		self.url = messageSoup.url.text

	def _check_message_validity(self, messageSoup):
		assert (messageSoup)

		super(LinkWeixinMessage, self)._check_message_validity(messageSoup)

		if None == messageSoup.url or None == messageSoup.title or None == messageSoup.description:
			raise ValueError('invalid weixin link message:\n' + messageSoup.__str__())


class VoiceWeixinMessage(WeixinMessage):
	"""
	语音消息的类
	"""
	def __init__(self, messageSoup):
		super(VoiceWeixinMessage, self).__init__(messageSoup)

		self.mediaId = messageSoup.mediaid.text
		self.format = messageSoup.format.text
		self.recognition = messageSoup.recognition.text

	def _check_message_validity(self, messageSoup):
		assert (messageSoup)

		super(VoiceWeixinMessage, self)._check_message_validity(messageSoup)

		if None == messageSoup.mediaid or None == messageSoup.format:
			raise ValueError('invalid weixin voice message:\n' + messageSoup.__str__())

DUMMY_TEXT_MSGID_TRANSED_FROM_EVENT = 'dummy_transfered_from_event'


def trans_to_text_message_from_event_message(eventWeixinMessage):
	"""
	trans_to_text_message_from_event_message把事件类型的消息转换成文本类型的消息，转换过程中，eventkey会作为转换后文本消息的内容。
	"""

	if None == eventWeixinMessage:
		raise ValueError('eventWeixinMessage can not be None')

	if type(eventWeixinMessage) != EventWeixinMessage:
		raise ValueError('eventWeixinMessage must be EventWeixinMessage type')

	xml_message = u"""
		<xml>
	 	<ToUserName><![CDATA[{}]]></ToUserName>
	 	<FromUserName><![CDATA[{}]]></FromUserName> 
	 	<CreateTime>{}</CreateTime>
	 	<MsgType><![CDATA[{}]]></MsgType>
	 	<Content><![CDATA[{}]]></Content>
	 	<MsgId>{}</MsgId>
	 	<Source>{}</Source>
	 	<Ticket>{}</Ticket>
	 	<Status>{}</Status>
	 	<TotalCount>{}</TotalCount>
	 	<FilterCount>{}</FilterCount>
	 	<SentCount>{}</SentCount>
	 	<ErrorCount>{}</ErrorCount>
	 	</xml>
		""" \
		.format(eventWeixinMessage.toUserName, 
				eventWeixinMessage.fromUserName, \
				eventWeixinMessage.createTime, 
				WeixinMessageTypes.TEXT, \
				eventWeixinMessage.eventKey, 
				#DUMMY_TEXT_MSGID_TRANSED_FROM_EVENT, 
				eventWeixinMessage.msgId,
				eventWeixinMessage.event,\
				eventWeixinMessage.ticket if eventWeixinMessage.ticket else '', \
				eventWeixinMessage.status if eventWeixinMessage.status else '', \
				eventWeixinMessage.totalCount if eventWeixinMessage.totalCount else '', \
				eventWeixinMessage.filterCount if eventWeixinMessage.filterCount else '', \
				eventWeixinMessage.sentCount if eventWeixinMessage.sentCount else '', \
				eventWeixinMessage.errorCount if eventWeixinMessage.errorCount else ''
				)

	return parse_weixin_message_from_xml(xml_message)

def parse_weixin_message_from_xml(xml_message):
	"""
	微信消息push过来之后的格式为xml格式的字符串，先使用
	BeautifulSoup对xml进行解析处理，之后根据消息类型创建对应的消息实例。
	"""
	
	if not xml_message:
		raise ValueError('xml_message can neither be None nor empty')

	messageSoup = BeautifulSoup(xml_message)
	
	if not messageSoup.msgtype:
		raise ValueError('invalid weixin message xml:\n' + xml_message)

	msgType = messageSoup.msgtype.text
	if WeixinMessageTypes.TEXT == msgType:
		return TextWeixinMessage(messageSoup)
	elif WeixinMessageTypes.EVENT == msgType:
		return EventWeixinMessage(messageSoup)
	elif WeixinMessageTypes.IMAGE == msgType:
		return ImageWeixinMessage(messageSoup)
	elif WeixinMessageTypes.VOICE == msgType:
		return VoiceWeixinMessage(messageSoup)
	elif WeixinMessageTypes.LOCATION == msgType:
		return LocationWeixinMessage(messageSoup)
	elif WeixinMessageTypes.LINK == msgType:
		return LinkWeixinMessage(messageSoup)
	else:
		raise ValueError("Not surpport the msgtype {} yet".format(msgType))
