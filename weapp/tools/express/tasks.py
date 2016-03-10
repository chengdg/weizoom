# -*- coding: utf-8 -*-

__author__ = 'justing'
# from __future__ import absolute_import


from celery import task
from kdniao_express_callback import KdniaoCallbackHandle

    
@task(bind=True, max_retries=5)
def task_kdniao_callback(self, datas):
    #try:
    """
    接受从快递鸟推送的express消息
    """
    KdniaoCallbackHandle(datas).handle()

