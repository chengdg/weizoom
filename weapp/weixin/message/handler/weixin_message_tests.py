# -*- coding: utf-8 -*-

"""Unit tests for weixin message parsing.

These tests make sure the parsing works as it should. """

import unittest

from weixin_message import *

class WeixinMessageTest(unittest.TestCase):
	def assertMessageEquals(self, message, msgType, toUserName, fromUserName, createTime, msgId):
		self.assertEqual(msgType, message.msgType)
		self.assertEqual(toUserName, message.toUserName)
		self.assertEqual(fromUserName, message.fromUserName)
		self.assertEqual(createTime, message.createTime)
		self.assertEqual(msgId, message.msgId)

	def assertTextMessageEquals(self, message, content):
		self.assertTrue(type(message) == TextWeixinMessage, u'消息类型不正确')
		self.assertEqual(content, message.content)

	def assertEventMessageEquals(self, message, eventType, eventKey):
		self.assertTrue(type(message) == EventWeixinMessage, u'消息类型不正确')
		self.assertEqual(eventType, message.event)	
		self.assertEqual(eventKey, message.eventKey)

	def assertImageMessageEquals(self, message, picUrl):
		self.assertTrue(type(message) == ImageWeixinMessage, u'消息类型不正确')
		self.assertEqual(picUrl, message.picUrl)	

	def assertLocationMessageEquals(self, message, location_X, location_Y, scale, label):
		self.assertTrue(type(message) == LocationWeixinMessage, u'消息类型不正确')
		self.assertEqual(location_X, message.location_X)
		self.assertEqual(location_Y, message.location_Y)
		self.assertEqual(scale, message.scale)
		self.assertEqual(label, message.label)

	def assertLinkMessageEquals(self, message, title, description, url):
		self.assertTrue(type(message) == LinkWeixinMessage, u'消息类型不正确')
		self.assertEqual(title, message.title)
		self.assertEqual(description, message.description)
		self.assertEqual(url, message.url)

	def assertVoiceMessageEquals(self, message, mediaId, format, recognition):
		self.assertTrue(type(message) == VoiceWeixinMessage, u'消息类型不正确')
		self.assertEqual(mediaId, message.mediaId)
		self.assertEqual(format, message.format)
		self.assertEqual(recognition, message.recognition)

class WinxinMessageCreateTestForInvalidFormant(WeixinMessageTest):
	"""测试对输入非法时的解析行为"""

	def setUp(self):
		self.to_user_name_xml_node = '<ToUserName><![CDATA[toUser]]></ToUserName>'
		self.from_user_name_xml_node = '<FromUserName><![CDATA[fromUser]]></FromUserName>'
		self.create_time_xml_node = '<CreateTime>1348831860</CreateTime>'
		self.msg_type_xml_node = '<MsgType><![CDATA[text]]></MsgType>'
		self.content_type_xml_node = '<Content><![CDATA[this is a test]]></Content>'
		self.msg_id_xml_node = '<MsgId>1234567890123456</MsgId>'

	def testParseFromNotXMl(self):
		try:
			parse_weixin_message_from_xml(None)
			self.fail()
		except ValueError:
			self.assertTrue(True)

		try:
			parse_weixin_message_from_xml('not xml')
			self.fail()
		except ValueError:
			self.assertTrue(True)

	def testParseFromXmlMessageMissToUserNameField(self):
		xml_message = """
		<xml>
		 {}
		 {}
		 {}
		 {}
		 {}
		 </xml>
		""".format(self.from_user_name_xml_node, self.create_time_xml_node, \
			self.msg_type_xml_node, self.content_type_xml_node, self.msg_id_xml_node)

		try:
			parse_weixin_message_from_xml(xml_message)
			self.fail()
		except ValueError:
			self.assertTrue(True)
		
	def testParseFromXmlMessageMissFromUserNameField(self):
		xml_message = """
		<xml>
		 {}
		 {}
		 {}
		 {}
		 {}
		 </xml>
		""".format(self.to_user_name_xml_node, self.create_time_xml_node, \
			self.msg_type_xml_node, self.content_type_xml_node, self.msg_id_xml_node)

		try:
			parse_weixin_message_from_xml(xml_message)
			self.fail()
		except ValueError:
			self.assertTrue(True)

	def testParseFromXmlMessageMissCreateTimeField(self):
		xml_message = """
		<xml>
		 {}
		 {}
		 {}
		 {}
		 {}
		 </xml>
		""".format(self.to_user_name_xml_node, self.from_user_name_xml_node, \
			self.msg_type_xml_node, self.content_type_xml_node, self.msg_id_xml_node)

		try:
			parse_weixin_message_from_xml(xml_message)
			self.fail()
		except ValueError:
			self.assertTrue(True)

	def testParseFromXmlMessageMissMsgTypeField(self):
		xml_message = """
		<xml>
		 {}
		 {}
		 {}
		 {}
		 {}
		 </xml>
		""".format(self.to_user_name_xml_node, self.from_user_name_xml_node, \
			self.create_time_xml_node, self.content_type_xml_node, self.msg_id_xml_node)

		try:
			parse_weixin_message_from_xml(xml_message)
			self.fail()
		except ValueError:
			self.assertTrue(True)

	def testParseFromXmlMessageMissMsgIdField(self):
		xml_message = """
		<xml>
		 {}
		 {}
		 {}
		 {}
		 {}
		 </xml>
		""".format(self.to_user_name_xml_node, self.from_user_name_xml_node, \
			self.create_time_xml_node, self.content_type_xml_node, self.msg_id_xml_node)

		try:
			parse_weixin_message_from_xml(xml_message)
			self.fail()
		except ValueError:
			self.assertTrue(True)

class TextWeixinMessageCreateTest(WeixinMessageTest):
	"""测试对文本消息的创建"""

	def setUp(self):
		self.xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName> 
		<CreateTime>1348831860</CreateTime>
		<MsgType><![CDATA[text]]></MsgType>
		<Content><![CDATA[this is a test]]></Content>
		<MsgId>1234567890123456</MsgId>
		</xml>
		"""

	def testTextMessageCreate(self):
		text_message = parse_weixin_message_from_xml(self.xml_message)
		self.assertMessageEquals(text_message, 'text', 'toUser', 'fromUser', '1348831860', '1234567890123456')
		self.assertTextMessageEquals(text_message, 'this is a test')

class EventWeixinMessageCreateTest(WeixinMessageTest):
	"""测试对事件消息的创建，事件消息中没有msgId信息"""

	def setUp(self):
		self.xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>123456789</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[EVENT]]></Event>
		<EventKey><![CDATA[EVENTKEY]]></EventKey>
		</xml>
		"""

	def testEventMessageCreate(self):
		event_message = parse_weixin_message_from_xml(self.xml_message)
		self.assertMessageEquals(event_message, 'event', 'toUser', 'fromUser', '123456789', None)
		self.assertEventMessageEquals(event_message, 'EVENT', 'EVENTKEY')

class ImageWeixinMessageCreateTest(WeixinMessageTest):
	"""测试对事件消息的创建，事件消息中没有msgId信息"""

	def setUp(self):
		self.xml_message = """
		<xml>
 		<ToUserName><![CDATA[toUser]]></ToUserName>
 		<FromUserName><![CDATA[fromUser]]></FromUserName>
 		<CreateTime>1348831860</CreateTime>
 		<MsgType><![CDATA[image]]></MsgType>
 		<PicUrl><![CDATA[this is a url]]></PicUrl>
 		<MsgId>1234567890123456</MsgId>
 		</xml>
		"""

	def testImageMessageCreate(self):
		image_message = parse_weixin_message_from_xml(self.xml_message)
		self.assertMessageEquals(image_message, 'image', 'toUser', 'fromUser', '1348831860', '1234567890123456')
		self.assertImageMessageEquals(image_message, 'this is a url')

class LocationWeixinMessageCreateTest(WeixinMessageTest):
	"""测试对地理位置消息的创建"""

	def setUp(self):
		self.xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>1351776360</CreateTime>
		<MsgType><![CDATA[location]]></MsgType>
		<Location_X>23.134521</Location_X>
		<Location_Y>113.358803</Location_Y>
		<Scale>20</Scale>
		<Label><![CDATA[位置信息]]></Label>
		<MsgId>1234567890123456</MsgId>
		</xml>
		"""

	def testLocationMessageCreate(self):
		location_message = parse_weixin_message_from_xml(self.xml_message)
		self.assertMessageEquals(location_message, 'location', 'toUser', 'fromUser', '1351776360', '1234567890123456')
		self.assertLocationMessageEquals(location_message, '23.134521', '113.358803', '20', u'位置信息')

class LinkWeixinMessageCreateTest(WeixinMessageTest):
	"""测试对链接消息的创建"""

	def setUp(self):
		self.xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>1351776360</CreateTime>
		<MsgType><![CDATA[link]]></MsgType>
		<Title><![CDATA[公众平台官网链接]]></Title>
		<Description><![CDATA[公众平台官网链接]]></Description>
		<Url><![CDATA[url]]></Url>
		<MsgId>1234567890123456</MsgId>
		</xml> 
		"""

	def testLinkMessageCreate(self):
		link_message = parse_weixin_message_from_xml(self.xml_message)
		self.assertMessageEquals(link_message, 'link', 'toUser', 'fromUser', '1351776360', '1234567890123456')
		self.assertLinkMessageEquals(link_message, u'公众平台官网链接', u'公众平台官网链接', 'url')

class VoiceWeixinMessageCreateTest(WeixinMessageTest):
	"""测试对语音消息的创建"""

	def setUp(self):
		self.xml_message = """
		<xml>
	    <ToUserName><![CDATA[toUser]]></ToUserName>
	    <FromUserName><![CDATA[fromUser]]></FromUserName>                                 
		<CreateTime>1351776360</CreateTime>
	    <MsgType><![CDATA[voice]]></MsgType>
	    <MediaId><![CDATA[abcdef]]></MediaId>
	    <Format><![CDATA[amr]]></Format>
	    <MsgId>1234567890123456</MsgId>
	    <Recognition><![CDATA[]]></Recognition>
		</xml>
		"""

	def testVoiceMessageCreate(self):
		voice_message = parse_weixin_message_from_xml(self.xml_message)
		self.assertMessageEquals(voice_message, 'voice', 'toUser', 'fromUser', '1351776360', '1234567890123456')
		self.assertVoiceMessageEquals(voice_message, 'abcdef', 'amr', None)

class MessageTranslateTest(WeixinMessageTest):
	"""测试消息之间的转换，只可以从事件消息转换为文本消息"""

	def testEventMessageTransToTextMessage(self):
		xml_message = """
		<xml><ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>123456789</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[CLICK]]></Event>
		<EventKey><![CDATA[__key__]]></EventKey>
		</xml>
		"""

		event_message = parse_weixin_message_from_xml(xml_message)
		text_message = trans_to_text_message_from_event_message(event_message)
		self.assertMessageEquals(text_message, 'text', 'toUser', 'fromUser', '123456789', DUMMY_TEXT_MSGID_TRANSED_FROM_EVENT)
		self.assertTextMessageEquals(text_message, '__key__')

if __name__ == '__main__':
    unittest.main()