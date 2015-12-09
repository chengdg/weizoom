__author__ = 'Administrator'
import requests
import json
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'}

# get_order =requests.post("http://red.weapp.weizzz.com/openapi/auth",data={'username':'malla','password':'test'},headers=headers)
get_order =requests.post("http://dev.weapp.com/openapi/auth",data={'username':'jobs','password':'test'},headers=headers)
print get_order.text

# {"access_token": "WZT10_ff3fdc78a066b087044396990ce2c3a0"}

orders = requests.post("http://red.weapp.weizzz.com/openapi/order_info",data={"access_token": "WZT10_ff3fdc78a066b087044396990ce2c3a0",'order_id':'20151208170349865'},headers=headers)

print orders.text

orders = requests.post("http://red.weapp.weizzz.com/openapi/order_list",data={"access_token":"WZT10_ff3fdc78a066b087044396990ce2c3a0",
																			  'found_begin_time':'2015-12-05 1:00:17','found_end_time':'2015-12-09 14:37:17'
},headers=headers)

print len(json.loads(orders.text)['data'])