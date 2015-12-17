# -*- coding: utf-8 -*-
__author__ = 'Administrator'
import requests
import json
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'}

# # get_order =requests.post("http://weapp.weizoom.com/openapi/auth",data={'username':'ceshi01','password':'weizoom'},headers=headers)
get_order =requests.post("http://weapp.weizoom.com/openapi/auth",data={'username':'ceshi01','password':'weizoom'},headers=headers)
print get_order.text

# {"access_token": "WZT10_ff3fdc78a066b087044396990ce2c3a0"}

# orders = requests.post("http://weapp.weizoom.com/openapi/order_info",data={"access_token": "WZT10_a8bcf60d2b4b6b35397eb2341ef94f09",'order_id':'20151208170349865'},headers=headers)
orders = requests.post("http://weapp.weizoom.com/openapi/order_list",data={"access_token": "WZT10_a8bcf60d2b4b6b35397eb2341ef94f09",'order_id':'20151217150256618','cur_page':1},headers=headers)

print orders.text
#
# orders = requests.post("http://dev.weapp.com/openapi/order_list",data={"access_token":"WZT10_f3518da15f89543e213d24ed0aa04b4f",
# 																			  'found_begin_time':'2015-12-05 1:00:17','found_end_time':'2015-12-12 14:37:17'
#  },headers=headers)
# #
# print len(json.loads(orders.text)['data'])
#
# orders = requests.post("http://dev.weapp.com/openapi/order_ship",data={"access_token":"WZT10_f3518da15f89543e213d24ed0aa04b4f",
# 																	   'order_id':'20151211102941784','logistics_number':'1212121212121',
# 																	   'logistics_name':'rufengda'
#  },headers=headers)
# #
# print orders.text