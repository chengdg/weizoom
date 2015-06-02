#coding:utf8
from __future__ import absolute_import

import os
import sys
import logging

# set the default Django settings module for the 'celery' program.
# if __name__=="__main__":
WEAPP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, WEAPP_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weapp.settings')
#os.environ['DJANGO_SETTINGS_MODULE'] = 'weapp.settings'
#SERVICES_DIR = os.path.abspath(os.path.join(os.getcwd(), '..'))
WEAPP_DIR = os.path.abspath(os.path.join(os.getcwd(), '..'))
print("WEAPP_DIR: {}".format(WEAPP_DIR))
sys.path.insert(0, WEAPP_DIR)
#for path in sys.path: print path

from weapp import settings
from celery import Celery
from celery.utils.log import get_logger

app = Celery('weapp')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
logging.info("init celery")
#app.config_from_object('django.conf:settings')
app.config_from_object('weapp.celeryconfig')
logging.info("loaded `celeryconfig`")
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks(lambda: settings.INSTALLED_TASKS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))




##################################################################################################
##################################################################################################
WEAPP_TASKS_PREFIX_LEN = len(os.path.realpath( os.path.join(settings.PROJECT_HOME,'..'))) + 1
celery_app  = app
task = celery_task = app.task
def celery_logger(name = None):
    if name:
        return get_logger(name)
    
    f = None
    if hasattr(sys, '_getframe'): 
        f = sys._getframe(1)
    else:
        try:
            raise Exception
        except:
            f = sys.exc_info()[2].tb_frame.f_back
    task = 'celery'
    if hasattr(f, "f_code"):
        co = f.f_code
        task = co.co_filename
        task = task[WEAPP_TASKS_PREFIX_LEN:task.rfind('.')].replace(os.sep,'.')
        task = '%s.%s' % (task, co.co_name)
    return get_logger(task)

