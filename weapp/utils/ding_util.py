#coding=utf8

# 调用接口发送钉钉消息的工具 duhao

import requests, json

SECRET = '_WEIZOOM_DING_SECRET_'
def send_to_ding(text, cid):
	success = False
	if text and cid:
		url = 'http://weoa.weizzz.com:8081/wapi/ding/conversation/'
		params = {
			'cid': cid,
			'text': text,
			'secret': SECRET
		}
		response = requests.post(url, params)

		result = json.loads(response.text)
		if result['code'] == 200:
			success = True

	return success 
