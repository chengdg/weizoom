# -*- coding: utf-8 -*-

__author__ = 'chuter'


"""Unit tests for answer game process.

These tests make sure the message handling works as it should. """

if __name__ == '__main__':
	import sys
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from weixin.handler.handler_testutil import *
init_handler_test_env()

import time

from BeautifulSoup import BeautifulSoup

from weixin.handler.weixin_message import parse_weixin_message_from_xml
from weixin.handler.message_handler import *
from weixin.handler.message_handle_context import *

from answer_game import *

from account.models import *

from django.test import TestCase

class AnswerGameHandlerTest(TestCase):
	state = GameState()

	def testProcessNotTextMessage(self):
		#在非游戏状态处理非文本类消息时直接返回None, 且游戏状态始终是未进入游戏
		test_xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>123456789</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[CLICK]]></Event>
		<EventKey><![CDATA[__key__]]></EventKey>
		</xml>
		"""
		test_message = parse_weixin_message_from_xml(test_xml_message)
		context = createDummyMessageHandlingContext(test_message, test_xml_message)
		weixin_user_test = WeixinUser.objects.create(username='fromUser')

		#初始状态为未进入游戏
		self.assertEqual(STATUS_NOT_IN_GAME, self._get_cur_gamestatus_for_user(weixin_user_test))

		handler = AnswerGameHandler()
		self.assertEqual(None, handler.handle(context))
		self.assertEqual(STATUS_NOT_IN_GAME, self._get_cur_gamestatus_for_user(weixin_user_test))

		test_xml_message = """
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
		test_message = parse_weixin_message_from_xml(test_xml_message)
		context = createDummyMessageHandlingContext(test_message, test_xml_message)
		self.assertEqual(None, handler.handle(context))
		self.assertEqual(STATUS_NOT_IN_GAME, self._get_cur_gamestatus_for_user(weixin_user_test))

	def testNotInGameProcess(self):
		#清空信息
		QuestionInfo.objects.all().delete()
		Problem.objects.all().delete()
		CurrentWeixinUserStatus.objects.all().delete()
		WeixinUserStatus.objects.all().delete()

		context = self._create_dummy_context_for_text_message('fromUser', '--')
		weixin_user_test = WeixinUser.objects.create(username='fromUser')

		handler = AnswerGameHandler()

		#没有添加任何游戏信息的情况下，不进行任何处理
		self.assertEqual(None, handler.handle(context))

		#添加游戏信息
		answer_game = self._create_test_answer_game(getTestUserProfile().user, 's', 'e')
		self._create_game_question(answer_game, 'p1', 'a1')

		#但输入的关键词不是游戏启动关键词，不进行任何处理
		context = self._create_dummy_context_for_text_message('fromUser', 'ss')
		self.assertEqual(None, handler.handle(context))

		#此时当输入的关键词为启动游戏关键词's'，则状态转换为在游戏中
		#先确认初始时微信用户游戏状态信息和针对特定游戏的状态信息都为空
		self.assertEqual(None, self.state._get_weixin_user_cur_state_obj(weixin_user_test))
		self.assertEqual(None, self.state._get_user_state_for_game(weixin_user_test, answer_game))

		context = self._create_dummy_context_for_text_message('fromUser', 's')
		response_content = handler.handle(context)
		response_message_soup = self._parse_response_message_soup(response_content)
		self.assertEqual('p1', response_message_soup.content.text) #返回第一题的问题
		self.assertEqual(STATUS_IN_GAME, self.state._get_weixin_user_cur_state_obj(\
				weixin_user_test).status) #微信用户当前游戏状态为游戏中
		#微信用户在特定游戏的状态也为游戏中
		self.assertEqual(STATUS_IN_GAME, self.state._get_user_state_for_game(\
				weixin_user_test, answer_game).status)

		#如果微信用户已经完整的玩过一个与游戏，再输入该游戏的启动关键词不进入游戏，且进行相应反馈
		#先清空所有游戏状态
		CurrentWeixinUserStatus.objects.all().delete()
		WeixinUserStatus.objects.all().delete()

		#置微信用户针对特定游戏的状态为已完成
		WeixinUserStatus.objects.create(weixin_user=weixin_user_test, status=STATUS_HAS_COMPLETED_GAME, last_response_time=get_current_time_in_millis(), question_answer=answer_game)
		context = self._create_dummy_context_for_text_message('fromUser', 's')
		response_content = handler.handle(context)
		response_message_soup = self._parse_response_message_soup(response_content)
		self.assertEqual(ENTER_GAME_WHEN_HAS_CMPLETED_GAME_RESPONSE_MESSAGE, response_message_soup.content.text) #返回第一题的问题
		self.assertEqual(None, self.state._get_weixin_user_cur_state_obj(weixin_user_test)) #微信用户当前游戏状态信息为空
		#微信用户在特定游戏的状态仍未已经完成游戏
		self.assertEqual(STATUS_HAS_COMPLETED_GAME, self.state._get_user_state_for_game(\
				weixin_user_test, answer_game).status)

		#测试匹配启动关键词时不区分大小写
		#先清空所有游戏状态
		CurrentWeixinUserStatus.objects.all().delete()
		WeixinUserStatus.objects.all().delete()

		context = self._create_dummy_context_for_text_message('fromUser', 'S')
		response_content = handler.handle(context)
		response_message_soup = self._parse_response_message_soup(response_content)
		self.assertEqual('p1', response_message_soup.content.text) #返回第一题的问题
		self.assertEqual(STATUS_IN_GAME, self.state._get_weixin_user_cur_state_obj(\
				weixin_user_test).status) #微信用户当前游戏状态为游戏中
		#微信用户在特定游戏的状态也为游戏中
		self.assertEqual(STATUS_IN_GAME, self.state._get_user_state_for_game(\
				weixin_user_test, answer_game).status)

	def testInGameProcess(self):
		weixin_user_test = WeixinUser.objects.create(username='fromUser')
		handler = AnswerGameHandler()

		#清空信息
		QuestionInfo.objects.all().delete()
		Problem.objects.all().delete()
		CurrentWeixinUserStatus.objects.all().delete()
		WeixinUserStatus.objects.all().delete()

		#添加两个游戏信息
		QuestionInfo.objects.all().delete()
		Problem.objects.all().delete()

		answer_game_a = self._create_test_answer_game(getTestUserProfile().user, 'sa', 'ea')
		self._create_game_question(answer_game_a, 'pa', 'aa')

		answer_game_b = self._create_test_answer_game(getTestUserProfile().user, 'sb', 'eb')
		self._create_game_question(answer_game_b, 'pb', 'ab')

		#输入关键词，进入游戏a
		context = self._create_dummy_context_for_text_message('fromUser', 'sa')
		handler.handle(context)

		#游戏中输入退出关键词，状态转换为未进入游戏且返回每个游戏的退出提示语(测试时一律使用'finished')
		context = self._create_dummy_context_for_text_message('fromUser', 'ea')
		response_content = handler.handle(context)
		response_message_soup = self._parse_response_message_soup(response_content)
		self.assertEqual(answer_game_a.finished_message, response_message_soup.content.text)

		self.assertEqual(STATUS_NOT_IN_GAME, self.state._get_weixin_user_cur_state_obj(\
				weixin_user_test).status) #微信用户当前游戏状态为未进入游戏
		#微信用户在特定游戏的状态也为未进入游戏
		self.assertEqual(STATUS_NOT_IN_GAME, self.state._get_user_state_for_game(\
				weixin_user_test, answer_game_a).status)

		#输入关键词，进入游戏a
		context = self._create_dummy_context_for_text_message('fromUser', 'sa')
		handler.handle(context)

		#游戏中输入其它关键词都作为答案处理，包括其它游戏的启动关键词, 这样会正常结束游戏a
		context = self._create_dummy_context_for_text_message('fromUser', 'sb')
		response_content = handler.handle(context)
		response_message_soup = self._parse_response_message_soup(response_content)
		#只有一道题，那么会完成游戏，因为没有任何奖品，因此返回信息为PRIZE_CONTENT_FOR_NO_PRIZE_LEFT
		self.assertEqual(PRIZE_CONTENT_FOR_NO_PRIZE_LEFT, response_message_soup.content.text)

		self.assertEqual(STATUS_NOT_IN_GAME, self.state._get_weixin_user_cur_state_obj(\
				weixin_user_test).status) #微信用户当前游戏状态为未进入游戏
		#微信用户在特定游戏的状态为已完成游戏
		self.assertEqual(STATUS_HAS_COMPLETED_GAME, self.state._get_user_state_for_game(\
				weixin_user_test, answer_game_a).status)

		#游戏中输入超时，状态会转换为未进入游戏，且不进行其他任何处理
		WeixinUserStatus.objects.all().delete()

		answer_game_a.time_limit = 0
		answer_game_a.save() #一旦进入游戏a，始终会超时

		#输入关键词，进入游戏a
		context = self._create_dummy_context_for_text_message('fromUser', 'sa')
		handler.handle(context)

		#游戏交互超时
		context = self._create_dummy_context_for_text_message('fromUser', 'sb')
		time.sleep(0.1)
		self.assertEqual(None, handler.handle(context))
		
		self.assertEqual(STATUS_NOT_IN_GAME, self.state._get_weixin_user_cur_state_obj(\
				weixin_user_test).status) #微信用户当前游戏状态为未进入游戏
		#微信用户在特定游戏的状态也为未进入游戏
		self.assertEqual(STATUS_NOT_IN_GAME, self.state._get_user_state_for_game(\
				weixin_user_test, answer_game_a).status)

	def testNotTextMessageProcessInGameState(self):
		"""测试在游戏中时对非文本消息的处理
		"""

		#清空信息
		QuestionInfo.objects.all().delete()
		Problem.objects.all().delete()
		CurrentWeixinUserStatus.objects.all().delete()
		WeixinUserStatus.objects.all().delete()

		handler = AnswerGameHandler()
		weixin_user_test = WeixinUser.objects.create(username='fromUser')

		#添加游戏信息
		answer_game = self._create_test_answer_game(getTestUserProfile().user, 's', 'e')
		for i in xrange(2): #增加2道题
			self._create_game_question(answer_game, "p", "a")

		#验证在游戏过程中输入非文本消息，正确处理结果为作为错误答案处理
		
		#进入游戏
		context = self._create_dummy_context_for_text_message('fromUser', 's')
		handler.handle(context)

		#游戏中输入非文本类消息其它关键词都作为答案处理，返回信息中包括了错误答案反馈
		#且进入下一道题
		context = self._create_dummy_context_for_nottext_message('fromUser')
		response_content = handler.handle(context)
		response_message_soup = self._parse_response_message_soup(response_content)
		#返回答题错误反馈，且进入下一道题
		self.assertEqual("no\np", response_message_soup.content.text)

		#再次答题，完成全部答题
		context = self._create_dummy_context_for_nottext_message('fromUser')
		response_content = handler.handle(context)
		response_message_soup = self._parse_response_message_soup(response_content)
		#完成游戏，因为没有任何奖品，因此返回信息为PRIZE_CONTENT_FOR_NO_PRIZE_LEFT
		self.assertEqual(PRIZE_CONTENT_FOR_NO_PRIZE_LEFT, response_message_soup.content.text)

		self.assertEqual(STATUS_NOT_IN_GAME, self.state._get_weixin_user_cur_state_obj(\
				weixin_user_test).status) #微信用户当前游戏状态为未进入游戏
		#微信用户在特定游戏的状态为已完成游戏
		self.assertEqual(STATUS_HAS_COMPLETED_GAME, self.state._get_user_state_for_game(\
				weixin_user_test, answer_game).status)

	def testPrizeAwardding(self):
		"""测试奖品的颁发
		"""
		#清空信息
		QuestionInfo.objects.all().delete()
		Problem.objects.all().delete()
		CurrentWeixinUserStatus.objects.all().delete()
		WeixinUserStatus.objects.all().delete()

		handler = AnswerGameHandler()

		#添加游戏信息
		answer_game = self._create_test_answer_game(getTestUserProfile().user, 's', 'e')
		for i in xrange(5): #增加5道题
			self._create_game_question(answer_game, "p", "a")

		#添加奖品信息
		self._create_test_prize(answer_game, 5, 5, '一等奖', 1) #1等奖1个，答对5道题
		self._create_test_prize(answer_game, 2, 3, '二等奖', 3) #2等奖1个，答对2-3道题

		#创建6个微信用户
		weixin_user_a = WeixinUser.objects.create(username='usera')
		weixin_user_b = WeixinUser.objects.create(username='userb')
		weixin_user_c = WeixinUser.objects.create(username='userc')
		weixin_user_d = WeixinUser.objects.create(username='userd')
		weixin_user_e = WeixinUser.objects.create(username='usere')
		weixin_user_f = WeixinUser.objects.create(username='userf')

		#输入关键词，进入游戏答题
		context = self._create_dummy_context_for_text_message('usera', 's')
		handler.handle(context)

		#第一个用户答对4道题，拿到二等奖
		for i in xrange(4):
			context = self._create_dummy_context_for_text_message('usera', 'a')
			response_content = handler.handle(context)
			response_message_soup = self._parse_response_message_soup(response_content)
			#返回信息中都是返回正确反馈和下一道题的信息
			self.assertEqual("yes\np", response_message_soup.content.text)

		#答完最后一道题，获取奖品内容信息
		context = self._create_dummy_context_for_text_message('usera', 'sa')
		response_content = handler.handle(context)
		response_message_soup = self._parse_response_message_soup(response_content)
		self.assertEqual(u"二等奖", response_message_soup.content.text)
		self.assertEqual(4, self.state._get_user_state_for_game(weixin_user_a, answer_game).right_answer_count)

		#第二个用户答对5道题, 拿到一等奖
		context = self._create_dummy_context_for_text_message('userb', 's')
		handler.handle(context)

		for i in xrange(4):
			context = self._create_dummy_context_for_text_message('userb', 'a')
			handler.handle(context)

		#答完最后一道题，获取奖品内容信息
		context = self._create_dummy_context_for_text_message('userb', 'a')
		response_content = handler.handle(context)
		response_message_soup = self._parse_response_message_soup(response_content)
		self.assertEqual(u"一等奖", response_message_soup.content.text)
		self.assertEqual(5, self.state._get_user_state_for_game(weixin_user_b, answer_game).right_answer_count)

		#第三个用户答对5道题, 但是由于一等奖已经颁发完，只会获取到二等奖
		context = self._create_dummy_context_for_text_message('userc', 's')
		handler.handle(context)

		for i in xrange(4):
			context = self._create_dummy_context_for_text_message('userc', 'a')
			handler.handle(context)

		#答完最后一道题，获取奖品内容信息
		context = self._create_dummy_context_for_text_message('userc', 'a')
		response_content = handler.handle(context)
		response_message_soup = self._parse_response_message_soup(response_content)
		self.assertEqual(u"二等奖", response_message_soup.content.text)
		self.assertEqual(5, self.state._get_user_state_for_game(weixin_user_c, answer_game).right_answer_count)

		#第四个用户答对1道题, 由于答题数太少，拿不到任何奖项
		context = self._create_dummy_context_for_text_message('userd', 's')
		handler.handle(context)

		for i in xrange(4):
			context = self._create_dummy_context_for_text_message('userd', 'b')
			response_content = handler.handle(context)
			response_message_soup = self._parse_response_message_soup(response_content)
			#答错题，返回内容为错误反馈和下一道题目内容
			self.assertEqual("no\np", response_message_soup.content.text)

		#答完最后一道题，获取奖品内容信息
		context = self._create_dummy_context_for_text_message('userd', 'a')
		response_content = handler.handle(context)
		response_message_soup = self._parse_response_message_soup(response_content)
		self.assertEqual(PRIZE_CONTENT_FOR_NO_PRIZE_LEFT, response_message_soup.content.text)
		self.assertEqual(1, self.state._get_user_state_for_game(weixin_user_d, answer_game).right_answer_count)

		#第五个用户答对二道题, 拿到二等奖
		context = self._create_dummy_context_for_text_message('usere', 's')
		handler.handle(context)

		for i in xrange(2):
			context = self._create_dummy_context_for_text_message('usere', 'a')
			handler.handle(context)

		for i in xrange(3):
			context = self._create_dummy_context_for_text_message('usere', 'b')
			response_content = handler.handle(context)
			
		response_message_soup = self._parse_response_message_soup(response_content)
		self.assertEqual(u'二等奖', response_message_soup.content.text)
		self.assertEqual(2, self.state._get_user_state_for_game(weixin_user_e, answer_game).right_answer_count)

		#第六个用户答对四道题, 由于所有奖项都已颁发完，领取不到任何奖项
		context = self._create_dummy_context_for_text_message('userf', 's')
		handler.handle(context)

		for i in xrange(4):
			context = self._create_dummy_context_for_text_message('userf', 'a')
			handler.handle(context)

		#答完最后一道题，获取奖品内容信息
		context = self._create_dummy_context_for_text_message('userf', 'b')
		response_content = handler.handle(context)
		response_message_soup = self._parse_response_message_soup(response_content)
		self.assertEqual(PRIZE_CONTENT_FOR_NO_PRIZE_LEFT, response_message_soup.content.text)
		self.assertEqual(4, self.state._get_user_state_for_game(weixin_user_f, answer_game).right_answer_count)

	def testProcessingWithInactiveGame(self):
		"""测试在有游戏被删除或置为失效时的游戏互动处理
		"""
		#清空信息
		QuestionInfo.objects.all().delete()
		Problem.objects.all().delete()
		CurrentWeixinUserStatus.objects.all().delete()
		WeixinUserStatus.objects.all().delete()

		weixin_user_test = WeixinUser.objects.create(username='usera')
		handler = AnswerGameHandler()

		#添加游戏信息
		answer_game = self._create_test_answer_game(getTestUserProfile().user, 's', 'e')
		self._create_game_question(answer_game, "p", "a")

		#当游戏被置为失效时，无法进入游戏
		answer_game.is_active = False
		answer_game.save()

		context = self._create_dummy_context_for_text_message('usera', 's')
		self.assertEqual(None, handler.handle(context))

		#当游戏被删除时，也无法进入游戏
		answer_game.is_active = True
		answer_game.is_deleted = True
		answer_game.save()
		
		context = self._create_dummy_context_for_text_message('usera', 's')
		self.assertEqual(None, handler.handle(context))

		#当游戏有效时可正常进入
		answer_game.is_active = True
		answer_game.is_deleted = False
		answer_game.save()
		
		context = self._create_dummy_context_for_text_message('usera', 's')
		response_content = handler.handle(context)
		response_message_soup = self._parse_response_message_soup(response_content)
		#进入游侠，返回第一道题目
		self.assertEqual("p", response_message_soup.content.text)

	def _get_cur_gamestatus_for_user(self, weixin_user):
		user_status = CurrentWeixinUserStatus.objects.filter(weixin_user=weixin_user)
		if user_status.count() == 0:
			return STATUS_NOT_IN_GAME
		else:
			return user_status[0].status

	def _create_test_prize(self, answer_game, right_count_min, right_count_max, content, count):
		return Prize.objects.create(
			question_answer = answer_game,
			right_count_min = right_count_min,
			right_count_max = right_count_max,
			content = content,
			count = count
			)

	def _create_test_answer_game(self, user, start_patterns, end_patterns, time_limit=None):
		return QuestionInfo.objects.create(
			owner = user,
			start_patterns = start_patterns,
			end_patterns = end_patterns,
			finished_message = 'finished',
			time_limit = time_limit if time_limit else 3
			)

	def _create_game_question(self, answer_game, title, right_answer):
		return Problem.objects.create(
			question_answer = answer_game,
			title = title,
			right_answer = right_answer,
			right_feedback = 'yes',
			error_feedback = 'no',
			)

	def _create_dummy_context_for_text_message(self, fromUserName, text):
		test_xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[{}]]></FromUserName> 
		<CreateTime>1348831860</CreateTime>
		<MsgType><![CDATA[text]]></MsgType>
		<Content><![CDATA[{}]]></Content>
		<MsgId>1234567890123456</MsgId>
		</xml>
		""".format(fromUserName, text)

		test_message = parse_weixin_message_from_xml(test_xml_message)
		return createDummyMessageHandlingContext(test_message, test_xml_message)

	def _create_dummy_context_for_nottext_message(self, fromUserName):
		test_xml_message = """
		<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[{}]]></FromUserName>
		<CreateTime>1351776360</CreateTime>
		<MsgType><![CDATA[link]]></MsgType>
		<Title><![CDATA[公众平台官网链接]]></Title>
		<Description><![CDATA[公众平台官网链接]]></Description>
		<Url><![CDATA[url]]></Url>
		<MsgId>1234567890123456</MsgId>
		</xml> 
		""".format(fromUserName)

		test_message = parse_weixin_message_from_xml(test_xml_message)
		return createDummyMessageHandlingContext(test_message, test_xml_message)

	def _parse_response_message_soup(self, response_message_xml_str):
		return BeautifulSoup(response_message_xml_str)


if __name__ == '__main__':
	start_test_withdb()