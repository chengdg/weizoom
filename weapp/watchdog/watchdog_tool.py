#coding: utf8
"""@package services.service_util
命令行方式启动Celery task

**用法**：

	python services/send_task.py <service_name> <arg> [<arg> ...]

**说明**：

	<service_name> : 服务的名称。如果在@task中指定name，则为次名字；否则为函数的全名。

**用法举例**：

	>python services\send_task.py watchdog.send 100 "This is a message"
	service name: watchdog.send
	args: ['100', 'Hello,  world!']
	result: OK

"""

import os
import sys

#from celery.execute import send_task

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weapp.settings')

#from weapp import celeryconfig

#if celeryconfig.CELERY_ALWAYS_EAGER:
#	print("CELERY_ALWAYS_EAGER=True, use 'services.celery.send_task_test' instead")
#	from services.celery_util import send_task_test as send_task
#else:
#	from celery.execute import send_task
import weapp.settings

if __name__=="__main__":
	if len(sys.argv)<3:
		print("usage: {}  <code> <message>".format(sys.argv[0]))
		sys.exit(0)
	code = int(sys.argv[1])
	message = sys.argv[2]
	print("code: {}".format(code))
	print("message: {}".format(message))

	from weapp import celeryconfig
	celeryconfig.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

	from watchdog.tasks import send_watchdog
	result = send_watchdog.delay(code, message)
	print("result: {}".format(result.get(timeout=30)))
