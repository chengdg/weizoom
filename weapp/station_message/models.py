# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from django.db import models
from django.db.models import signals

MODULES = {
    'DATA': 0,
    'WEIBO': 1,
    'WEIXIN': 2,
    'WEAPP': 3,
    'COMPASS':4
}

class Message(models.Model):
    modules = models.IntegerField(default=MODULES['DATA']) #选择模块
    message_type = models.BooleanField(default=True) #默认消息中心
    title = models.CharField(max_length=128)#标题名
    file_url = models.CharField(max_length=256) #上传文件地址
    content = models.TextField()#内容
    file_type = models.BooleanField(default=True) #上传类型(默认word)
    created_at = models.DateTimeField(auto_now_add=True) #添加时间
    owner = models.ForeignKey(User)

    class Meta(object):
        db_table = 'message_message'
        verbose_name = '系统消息'
        verbose_name_plural = '系统消息'

class UserHasMessage(models.Model):
    user = models.ForeignKey(User)
    message = models.ForeignKey(Message)
    is_read = models.BooleanField(default=False)
    message_type = models.BooleanField(default=True)

    class Meta(object):
        db_table = 'message_user_has_message'
        verbose_name = '用户－系统消息'
        verbose_name_plural = '用户－系统消息'

class MessageAttachment(models.Model):
    """
    消息附件
    """
    # 消息id Message
    message = models.ForeignKey(Message)
    file_type = models.CharField(max_length=26)  # 文档类型
    file_name = models.CharField(max_length=1024)  # 原始文件名
    path = models.CharField(max_length=1024, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        db_table = 'message_attachment'

def add_relation_to_user(instance, created, **kwords):
    """
    新增message后触发
    :param instance: Message
    :param created: boolean
    :param kwords: other args
    """
    if created:
        created_list = []
        for user in User.objects.exclude(id=1):
            created_list.append(UserHasMessage(
                user = user,
                message = instance,
                message_type = instance.message_type
            ))
        UserHasMessage.objects.bulk_create(created_list)

#signals
signals.post_save.connect(add_relation_to_user, sender=Message, dispatch_uid='user_message.add_relation')

