# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from weixin.user.models import WeixinUser

PRIZE_CONTENT_FOR_NO_PRIZE_LEFT = u'非常抱歉，全部奖品已发放完。感谢您的参与！'
ENTER_GAME_WHEN_HAS_CMPLETED_GAME_RESPONSE_MESSAGE = u'您已经参与过答题，感谢您的参与'

#########################################################################
# QuestionInfo：问答信息
#########################################################################
class QuestionInfo(models.Model):
	owner = models.ForeignKey(User)
	start_patterns = models.CharField(max_length=1024) #匹配词，以英文空格' '分隔
	end_patterns = models.CharField(max_length=1024) #匹配词，以英文空格' '分隔
	finished_message = models.CharField(max_length=1024) #退出后的提示语
	statistics = models.IntegerField(default=0) # 参与人次
	time_limit = models.IntegerField(default=3) # 答题时间限制，默认3分钟
	is_active = models.BooleanField(default=True) #是否启用
	is_deleted = models.BooleanField(default=False) #是否删除
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'markettool_question_info'
		verbose_name = '问答'
		verbose_name_plural = '问答'


#########################################################################
# Problem：问题题目
#########################################################################
class Problem(models.Model):
	question_answer = models.ForeignKey(QuestionInfo)
	display_index = models.IntegerField(default=1)#显示的排序
	title = models.CharField(max_length=1024) #题目
	right_answer = models.CharField(max_length=1024) #正确答案, 以空格' '分割
	right_feedback = models.CharField(max_length=1024, default='')
	error_feedback = models.CharField(max_length=1024, default='')
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'markettool_question_problem'
		verbose_name = '问答题目'
		verbose_name_plural = '问答题目'


#########################################################################
# Prize：奖品
#########################################################################
class Prize(models.Model):
	question_answer = models.ForeignKey(QuestionInfo)
	right_count_min = models.IntegerField(default=0) #答对数量最小值
	right_count_max = models.IntegerField(default=0) #答对数量最大值
	content = models.CharField(max_length=2048) #奖品内容
	count = models.IntegerField(default=999999) #奖品数量

	class Meta(object):
		db_table = 'markettool_question_prize'
		verbose_name = '问答奖品'
		verbose_name_plural = '问答奖品'


#########################################################################
# MpQuestionStatics：用户的游戏状态
#########################################################################
STATUS_IN_GAME = 0
STATUS_NOT_IN_GAME = 1
STATUS_HAS_COMPLETED_GAME = 2
class WeixinUserStatus(models.Model):
    weixin_user = models.ForeignKey(WeixinUser, to_field='username', db_column='weixin_user_username')
    question_answer = models.ForeignKey(QuestionInfo)
    status = models.IntegerField(default=STATUS_NOT_IN_GAME) #游戏状态
    next_question_number = models.IntegerField(default=1) #下一道要回答的问题
    right_answer_count = models.IntegerField(default=0) #回答正确的题目的个数
    last_response_time = models.BigIntegerField() #最后一次响应的时间(毫秒)

    class Meta(object):
        db_table = 'markettool_question_status'
        verbose_name = '用户参与问答游戏状态'
        verbose_name_plural = '用户参与问答游戏状态'

#########################################################################
# CurrentWeixinUserStatus：用户当前状态
#########################################################################
class CurrentWeixinUserStatus(models.Model):
	weixin_user = models.ForeignKey(WeixinUser, to_field='username', db_column='weixin_user_username')
	question_answer = models.ForeignKey(QuestionInfo)
	status = models.IntegerField(default=STATUS_NOT_IN_GAME) #游戏状态

	class Meta(object):
		db_table = 'markettool_question_user_status'
		verbose_name = '用户当前状态'
		verbose_name_plural = '用户当前状态'