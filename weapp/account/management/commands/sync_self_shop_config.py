# -*- coding: utf-8 -*-

import json
import requests
import MySQLdb

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group


from account.models import UserProfile, AccountDivideInfo
from mall.models import *

class Command(BaseCommand):
    help = "update account_type from fans"
    args = ''

    def handle(self, *args, **options):
        """
        处理所有自营平台配置
        """
        conn= MySQLdb.connect(
            host='127.0.0.1',
            port = 3306,
            user='panda',
            passwd='weizoom',
            db ='panda',
            charset="utf8"
            )
        cur = conn.cursor()
        #获取所有零售返点类型的panda用户
        cur.execute(u"select * from self_shop_self_shops")
        rows = cur.fetchall()
        for row in rows:
            #获取自营平台的id或者username
            account = row[2]
            if account.isdigit():
                if User.objects.filter(id=account):
                    user = User.objects.get(id=account)
            else:
                if User.objects.filter(username=account):
                    user = User.objects.get(username=account)

            if user:
                #更新panda中对应weapp自营平台的方式统一成user_id
                cur.execute("update self_shop_self_shops set weapp_user_id = '%d' where weapp_user_id ='%s'" % (user.id, account))
                conn.commit()
                #创建配置，如果配置不存在
                if AccountDivideInfo.objects.filter(user_id=user.id).count() <= 0:
                    AccountDivideInfo.objects.create(user_id=user.id)


            


