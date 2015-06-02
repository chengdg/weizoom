# -*- coding: utf-8 -*-

__author__ = 'chuter'

from weixin.handler.keyword_handler import *
from question.models import *

from account.models import get_token_for

from core.dateutil import get_current_time_in_millis

from weixin.message import generator

"""
处理在交互环境中玩答题游戏的相关消息

系统中每个用户可配置多个答题游戏，每个游戏有一个启动关键词
和关闭关键词，答题游戏有以下2种状态：
1. 未进入答题游戏
2. 正在答题

初始状态为1
状态转换描述如下：

    关键词为启动游戏关键词且该微信用户还没有完成过答题
1 ------------------------------------------------------> 2
    
          退出关键词
2 -------------------------------> 1

            超时
2 -------------------------------> 1

        答完最后一道题
2 -------------------------------> 1


在1状态，如果输入为启动游戏关键词但是该微信用户已经完成过答题，
那么直接返回反馈信息

在2状态输入非退出关键词都被认为是当前题目的答案

在2状态时收到关键词但是游戏已经超时，那么修改状态不进行反馈

在2状态时答完所有的题，那么修改状态为未进入游戏

在该处理过程中，假设发送消息的微信用户在我们系统中已经存在

"""

class GameState(object):
	def _get_weixin_user_state_for_question(self):
		pass

	def _get_weixin_user_cur_state_obj(self, from_weixin_user):
		try:
			return CurrentWeixinUserStatus.objects.get(weixin_user=from_weixin_user)
		except: 
			return None

	def _get_question_info_match_start_keyword(self, message, user):
		lower_keyword = message.content.lower()
		if not lower_keyword:
			return None

		question_infos = QuestionInfo.objects.filter(owner=user, is_deleted=0, is_active=1)
		for question_info in question_infos:
			if question_info.start_patterns.lower().strip() == lower_keyword.strip():
				#遇到第一个匹配的就返回不需要继续匹配，因为同一用户游戏之间启动关键词决不存在重复
				return question_info
		return None

	########################################################################
	# _get_user_state_for_game: 获取用户针对某一个答题游戏的当前所处状态信息
	# 如果CurrentWeixinUserStatus对应的记录不存在，返回None(未进入该游戏)
	########################################################################
	def _get_user_state_for_game(self, from_weixin_user, question_info):
		user_state_for_specific_games = WeixinUserStatus.objects.filter(weixin_user=from_weixin_user, question_answer=question_info)
		return user_state_for_specific_games[0] if user_state_for_specific_games else None

	def _update_weixin_user_cur_state(self, from_weixin_user, new_state, question_info=None):
		cur_state_obj = self._get_weixin_user_cur_state_obj(from_weixin_user)
		if cur_state_obj:
			if question_info:
				cur_state_obj.question_answer = question_info
			cur_state_obj.status = new_state
			cur_state_obj.save()
			return cur_state_obj
		else:
			return CurrentWeixinUserStatus.objects.create(weixin_user=from_weixin_user, status=new_state, question_answer=question_info)

	def _get_question_count(self, question_info):
		return Problem.objects.filter(question_answer=question_info).count()

	def _get_question(self, question_index, question_info):
		questions = Problem.objects.filter(question_answer=question_info)
		try:
			return questions.order_by('display_index')[question_index-1]
		except:
			questions.order_by('display_index')[0]

	########################################################################
	# _get_prize: 获取获奖信息
	#
	# 首先根据正确答题数目判断获几等奖，假设应该获1等奖：
	# 	a. 如果该奖项已发放完，根据区间获取下一等奖：
	#		1. 如果下一等奖也已发放完，那么继续获取下下一级奖，直到
	#          还没有发放完的奖项作为该用户的奖品；如果全部发放完，
	#          返回PRIZE_CONTENT_FOR_NO_PRIZE_LEFT
	#	b. 否则直接返回1等奖所设置的获奖内容信息
	########################################################################
	def _get_prize(self, right_answer_count, question_info):
		prizes = Prize.objects.filter(question_answer=question_info).order_by('right_count_max')

		if 0 == len(prizes): #没有奖品
			return None

		if prizes[0].right_count_min > right_answer_count: #分数太低，没有奖品
			return None
		target_prize_index = len(prizes) - 1
		for index, prize in enumerate(prizes):
			if prize.right_count_max >= right_answer_count:
				target_prize_index = index
				break

		for index in xrange(target_prize_index, -1, -1):
			if prizes[index].right_count_min > right_answer_count:
				continue

			if prizes[index].count > 0:
				return prizes[index]

		return None

	########################################################################
	# _handle_keyword_in_game: 处理问答游戏中的输入
	#
	# 首先判断输入，如果是启动游戏关键词返回第一题信息且更新下一道题的序号；
	# 否则，输入为正在回答的问题的答案，那么先判断是否为最后一题：
	#	a. 如果是，那么计算得奖结果返回相应信息且更新当前状态为STATUS_HAS_COMPLETED_GAME；
	#	b. 否则判断答题结果正确与否，返回相应反馈信息和下一道题且更新下一道题序号
	#	   和正确答题个数（计算奖品使用）
	########################################################################
	def _handle_keyword_in_game(self, user_profile, message, from_weixin_user, question_info, is_from_simulator, is_at_begin=False):
		response_content = None

		user_state_for_specific_game = self._get_user_state_for_game(from_weixin_user, question_info)

		assert (user_state_for_specific_game) #只有在游戏中才会进入到该方法，在游戏中该信息一定不为空

		next_question_index = user_state_for_specific_game.next_question_number

		if is_at_begin:
			first_question = self._get_question(1, question_info)
			response_content = first_question.title
		else:
			answer = message.content
			lower_answer = answer.lower()
			question = self._get_question(next_question_index, question_info)
			is_answer_right = (lower_answer == question.right_answer.lower())

			if is_answer_right:
				user_state_for_specific_game.right_answer_count += 1

			if self._get_question_count(question_info) == next_question_index:
				user_state_for_specific_game.status = STATUS_HAS_COMPLETED_GAME

				#完成游戏，更新当前微信用户的游戏状态信息为未进入游戏状态
				ss = self._update_weixin_user_cur_state(from_weixin_user, STATUS_NOT_IN_GAME)

				#TODO 是否需要对奖品的获取和更改进行加锁??
				prize = self._get_prize(user_state_for_specific_game.right_answer_count, question_info)
			
				if prize:
					from django.db import connection, transaction
					cursor = connection.cursor()
					cursor.execute('update markettool_question_prize set count=count-1 where id =' + str(prize.id))
					transaction.commit_unless_managed()
					response_content = prize.content
				else:
					response_content = PRIZE_CONTENT_FOR_NO_PRIZE_LEFT
			else:
				response_content = question.right_feedback if is_answer_right else question.error_feedback

				next_question_index += 1
				next_question = self._get_question(next_question_index, question_info)
				
				if response_content:
					response_content = "%s\n%s" % (response_content, next_question.title)
				else:
					response_content = next_question.title
		
		#更新当前微信用户正在玩的游戏状态信息
		user_state_for_specific_game.next_question_number = next_question_index
		user_state_for_specific_game.last_response_time = get_current_time_in_millis()
		user_state_for_specific_game.save()

		return self._build_response_to_weixin_user(user_profile, message, from_weixin_user, response_content, is_from_simulator)

	def _increase_game_participants_count(self, question_info):
		from django.db import connection, transaction
		cursor = connection.cursor()
		cursor.execute('update markettool_question_info set statistics=statistics+1 where id =' + str(question_info.id))
		transaction.commit_unless_managed()

	########################################################################
	# _reset_weixin_user_status_for_specific_game: 重置WeixinUserStatus：
	#
	# 重置正确答题个数，下道题序号等信息
	########################################################################
	def _reset_weixin_user_status_for_specific_game(self, user_state_for_specific_game, question_info=None, status=None, last_response_time=None):
		user_state_for_specific_game.right_answer_count = 0
		user_state_for_specific_game.next_question_number = 1
		if question_info:
			user_state_for_specific_game.question_answer = question_info
		if status != None:
			user_state_for_specific_game.status = status 
		if last_response_time != None:
			user_state_for_specific_game.last_response_time = last_response_time
		user_state_for_specific_game.save()	

	def _get_token_for_weixin_user(self, user_profile, weixin_user, is_from_simulator):
		if is_from_simulator:
			if 'develop' == settings.MODE:
				token = get_token_for(user_profile.webapp_id, weixin_user.username)
			else:
				token = ''
		else:
			token = get_token_for(user_profile.webapp_id, weixin_user.username)

		return token

	def _build_response_to_weixin_user(self, user_profile, message, from_weixin_user, response_text, is_from_simulator):
		token = self._get_token_for_weixin_user(user_profile, from_weixin_user, is_from_simulator)
		response = generator.get_text_response(from_weixin_user.username, message.toUserName, response_text, token, user_profile)
		return response

class NotInGameState(GameState):
	"""
	未进入游戏状态，该状态下：
	如果输入某个游戏的启动关键词且没有完整的玩过该游戏，那么状态转换为游戏状态并返回反馈信息
	其它输入不进行任何处理
	"""
	def process_input_in_cur_state(self, user_profile, message, from_weixin_user, is_from_simulator):
		#如果不是文本类型的消息，不进行任何处理
		if not message.is_text_message():
			return None

		cur_game = self._get_question_info_match_start_keyword(message, user_profile.user)	
		if not cur_game: #没有任何一个问题的启动关键词与输入匹配，那么不进行任何处理
			return None

		#进入游戏
		#首先获取当前微信用户针对匹配到的游戏的状态
		user_state_for_specific_game = self._get_user_state_for_game(from_weixin_user, cur_game)

		if user_state_for_specific_game == None: #还没有对应的状态信息，则新增
			user_state_for_specific_game = WeixinUserStatus.objects.create(weixin_user=from_weixin_user, status=STATUS_IN_GAME, last_response_time=get_current_time_in_millis(), question_answer=cur_game)
		else:
			if STATUS_HAS_COMPLETED_GAME == user_state_for_specific_game.status:
				#如果当前微信用户之前已经完整的玩过该游戏，那么进行相应的反馈
				if cur_game and cur_game.is_deleted == 0 and cur_game.is_active == 1:
					#如果对应的游戏没被删除并且还有效才进行反馈
					return self._build_response_to_weixin_user(user_profile, message, from_weixin_user, ENTER_GAME_WHEN_HAS_CMPLETED_GAME_RESPONSE_MESSAGE, is_from_simulator)
				else:
					#否则不进行任何处理
					return None

			#初始化当前用户针对匹配的具体游戏的状态
			self._reset_weixin_user_status_for_specific_game(user_state_for_specific_game, cur_game, STATUS_IN_GAME, get_current_time_in_millis())

		#更改当前微信用户当前的游戏状态
		self._update_weixin_user_cur_state(from_weixin_user, STATUS_IN_GAME, cur_game)
		
		#然后更新游戏的参与人数
		if not is_from_simulator: #模拟器中的数据不进行参与计数
			self._increase_game_participants_count(cur_game)

		#进行答题处理
		return self._handle_keyword_in_game(user_profile, message, from_weixin_user, cur_game, is_from_simulator, True)

class InGameState(GameState):
	"""
	正在游戏中状态，该状态下:
	如果输入该游戏的退出关键词，那么状态转换为未进入游戏状态并返回反馈信息
	离上次输入时间超出设定的超时时间，那么状态转换为未进入游戏状态且不进行任何其他处理
	其它任何关键词或其他类型消息都作为当前题目的答案进行处理，并返回相应的反馈信息
	"""
	def process_input_in_cur_state(self, user_profile, message, from_weixin_user, is_from_simulator):
		cur_state_obj = self._get_weixin_user_cur_state_obj(from_weixin_user)
		cur_game = cur_state_obj.question_answer
		user_state_for_specific_game = self._get_user_state_for_game(from_weixin_user, cur_game)

 		assert (user_state_for_specific_game) #已经在游戏中，针对特定游戏的状态肯定已经存在

		#首先根据设定的游戏超时时间看是否已经超时
		if (get_current_time_in_millis() - user_state_for_specific_game.last_response_time) > cur_game.time_limit*60*1000:
			#如果超时，那么更改当前微信用户的游戏状态以及针对特定游戏的状态
			#不进行其他任何处理
			self._update_weixin_user_cur_state(from_weixin_user, STATUS_NOT_IN_GAME)
			self._reset_weixin_user_status_for_specific_game(user_state_for_specific_game, status=STATUS_NOT_IN_GAME, last_response_time=get_current_time_in_millis())
			return None
 
		if not message.is_text_message(): #如果不是文本类型的消息，把消息的文本内容置为
		                                  #一个不可能存在的字符串，这样下面代码会作为错误答案来处理
			message.content = ''


		if cur_game.end_patterns.lower() == message.content.lower(): 
			#为当前游戏的退出关键词，那么退出游戏且返回相应的反馈信息
			#进行状态的更新以标识退出游戏
			self._update_weixin_user_cur_state(from_weixin_user, STATUS_NOT_IN_GAME)
			self._reset_weixin_user_status_for_specific_game(user_state_for_specific_game, status=STATUS_NOT_IN_GAME, last_response_time=get_current_time_in_millis())		
			return self._build_response_to_weixin_user(user_profile, message, from_weixin_user, cur_game.finished_message, is_from_simulator)

		#进行答题处理
		return self._handle_keyword_in_game(user_profile, message, from_weixin_user, cur_game, is_from_simulator)

class AnswerGameHandler(KeywordHandler):
	state_value_2_state_ins = {
		STATUS_NOT_IN_GAME : NotInGameState(),
		STATUS_IN_GAME : InGameState()
	}

	def handle(self, context, is_from_simulator=False):
		message = context.message
		user_profile = context.user_profile
		
		from_weixin_user = self._get_from_weixin_user(message)
		cur_state = self._get_user_cur_state(user_profile.user, from_weixin_user)
		return cur_state.process_input_in_cur_state(user_profile, message, from_weixin_user, is_from_simulator)

	def _get_user_cur_state(self, user, from_weixin_user):
		try:
			cur_state_obj = CurrentWeixinUserStatus.objects.get(weixin_user=from_weixin_user)
			return self.state_value_2_state_ins[cur_state_obj.status]
		except: #不存在或者数据库操作异常都作为未进入游戏状态处理
			return self.state_value_2_state_ins[STATUS_NOT_IN_GAME]

	def _handle_keyword(self, context, from_weixin_user, is_from_simulator):
		user_profile = context.user_profile
		message = context.message
		
		cur_state = self._get_user_cur_state(user_profile.user, from_weixin_user)
		return cur_state.process_input_in_cur_state(user_profile, message, from_weixin_user, is_from_simulator)