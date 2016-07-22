# -*- coding: utf-8 -*-

import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

from apps import send_task

"""
测试模版消息队列
前提: 配置好并开启“拼团成功通知”模版
测试环境：nj
"""

if __name__ == '__main__':
	send_task('services.weixin_template_service.task.service_template_message', {
		'user_id': 8,
		'reason': u'测试-weapp',
		'event_type': 1,
		'member_id': 86,
		'url': 'http://www.baidu.com',
		'items': {
			'keyword1': u'呵呵嗒-weapp',
			'keyword2': '9182499182409124'
		}
	})