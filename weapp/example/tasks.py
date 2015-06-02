#coding: utf8
"""@package example.tasks
Celery task函数示例

调用示例：

首先启动celery服务（确保celeryconfig.py中的`CELERY_ALWAYS_EAGER=False`）：
```
$ start_celery.sh
```

然后进入manage shell并执行：
```
$ python manage.py shell
>>> from example.tasks import example_task
>>> result = example_task.delay("hello, world")
>>> result.state
u'SUCCESS'
>>> result.get(timeout=1)
u'hello, world'
```

"""

from weapp.celery import celery_logger, celery_task as task
@task
def example_task(msg):
	info= celery_logger().info
	info("message: {},   REQ:%s".format(msg))
	return msg


@task(bind=True)
def example_bind_task(self, msg):
	info= celery_logger().info
	log = self.app.log.get_default_logger()
	info("message: {},   REQ:%s".format(msg))
	return msg