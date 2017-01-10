# -*- coding: utf-8 -*-
import sys
import datetime
import copy
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

import json
from mall import models as mall_models
from eaglet.utils.resource_client import Resource

s=[]  ########TODO需要访问线上的order/orders接口拿到老的数据

def p_info(order):
    dd={}
    for delivery_item in order['delivery_items']:
        for product in delivery_item['products']:
            s=[]
            s.append([product['weight'],product['thumbnails_url'],product['product_model_name_texts']])
        dd[delivery_item['id']] = s
    return dd

info1 = []
info2 = []
n=0
for order in s:
    resp = Resource.use('gaia').get({
        'resource': 'order.order',
        'data': {
            'corp_id': '119',
            'id':order['id']
        }
    })
    n += 1
    order_old = resp['data']['order']
    info1 = p_info(order_old)
    info2 = p_info(order)
    for key,value in info1.items():
      print '=======key,value===========',key,value
      if info1[key] == info2[key]:
          print '========================',n
          print '========success=====success============success'
      else:
          print '========================',n
          print '========failed  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',order['id']
          break
