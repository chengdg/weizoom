# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals
from django.conf import settings
from django.db.models import F
from datetime import datetime, timedelta

from core import dateutil
from modules.member.models import *
from account.models import *


#===============================================================================
# TestGame: 趣味测试
#===============================================================================
class TestGame(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=256)
    background_pic_url = models.CharField(max_length=256, null=True)
    is_non_member = models.BooleanField(default=False)
    award_prize_info = models.TextField(default='{"id":-1,"name":"non-prize","type":"无奖励"}', verbose_name=u'奖品信息')
    created_at = models.DateTimeField(auto_now_add=True) #创建时间
    
    class Meta(object):
        db_table = 'market_tool_test_game'
        verbose_name = '趣味测试'
        verbose_name_plural = '趣味测试'
        ordering = ['-id']
        
    @property
    def joined_users(self):
        webapp_user_ids = [value.webapp_user_id for value in TestGameRecord.objects.filter(test_game=self)]
        return list(WebAppUser.objects.filter(id__in=webapp_user_ids))

    @property
    def joined_user_count(self):
        return TestGameRecord.objects.filter(test_game=self).values("webapp_user_id").distinct().count()  
        
        
#===============================================================================
# TestGameQuestion: 趣味测试题目
#===============================================================================
class TestGameQuestion(models.Model):
    test_game = models.ForeignKey(TestGame)
    name = models.CharField(max_length=256)
    display_index = models.IntegerField(default=1) #显示的排序
    created_at = models.DateTimeField(auto_now_add=True) #创建时间
    
    class Meta(object):
        db_table = 'market_tool_test_game_question'
        verbose_name = '趣味测试题目'
        verbose_name_plural = '趣味测试题目'
        ordering = ['display_index']
    

#===============================================================================
# TestGameQuestionAnswer: 趣味测试题目选项
#===============================================================================
class TestGameQuestionAnswer(models.Model):
    test_game_question = models.ForeignKey(TestGameQuestion)
    name = models.CharField(max_length=256)
    score = models.IntegerField(default=0)
    display_index = models.CharField(max_length=256, default="A") #显示的排序
    created_at = models.DateTimeField(auto_now_add=True) #创建时间
    
    class Meta(object):
        db_table = 'market_tool_test_game_question_answer'
        verbose_name = '趣味测试题目选项'
        verbose_name_plural = '趣味测试题目选项'
        ordering = ['display_index']
        
        
#===============================================================================
# TestGameResult: 趣味测试结果
#===============================================================================
class TestGameResult(models.Model):
    test_game = models.ForeignKey(TestGame)
    section = models.CharField(max_length=256) #取值区间
    content = models.CharField(max_length=500) #结果内容
    title = models.CharField(max_length=500) #结果标题
    display_index = models.IntegerField(default=1) #显示的排序
    created_at = models.DateTimeField(auto_now_add=True) #创建时间
    
    class Meta(object):
        db_table = 'market_tool_test_game_result'
        verbose_name = '趣味测试结果'
        verbose_name_plural = '趣味测试结果'
        ordering = ['display_index']
        
        
#===============================================================================
# TestGameRecord: 参加测试记录
#===============================================================================
class TestGameRecord(models.Model):
    test_game = models.ForeignKey(TestGame)
    webapp_user_id = models.IntegerField(default=-1)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True) #创建时间
    
    class Meta(object):
        db_table = 'market_tool_test_game_record'
        verbose_name = '参加测试记录'
        verbose_name_plural = '参加测试记录'
    