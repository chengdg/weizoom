# -*- coding: utf-8 -*-

__author__ = 'jiangzhe'

import hashlib, urllib2, json, time, random, string

from django.core.cache import cache
from django.http import HttpResponse

from weixin.user import access_token

def config(request):
	"""
	生成微信JS的config签名部分，供页面js嵌入
	使用【订阅号：加洛桃红】获取ticket，支持域名weapp.com,weizzz.com
	
	使用的js接口如下:
	
	  * onMenuShareAppMessage
	  * onMenuShareTimeline
	  * onMenuShareQQ
	  * previewImage
	  * hideOptionMenu
	  * showOptionMenu
	  * chooseImage

	@see http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html
	"""
	# 获取 加洛桃红(测试账号) 的ticket
	jsapi_ticket = cache.get('wxjs_ticket')
	#appId = 'wx25bbc5642d3cb78c'
	appId = 'wx4f43465ddfc20077'
	if not jsapi_ticket:
		# 获取 加洛桃红(测试账号) 的token

		#appSecret = '4dfc131ac1b61fcba81db7142d400387'
		appSecret = 'd4cdbf24a90c57b5e2592e1e2c174b45'
		token, expires_span, other = access_token.get_new_access_token(appId, appSecret)
		#print 'get new token ',token

		get_ticket_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi'
		ticket_response = json.loads(urllib2.urlopen(get_ticket_url % token).read())
		jsapi_ticket = ticket_response['ticket']
		#print 'get new ticket', jsapi_ticket
		cache.set('wxjs_ticket', jsapi_ticket, 7200)

	# 制作签名
	noncestr = string.join(random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcba',16)).replace(' ', '')
	timestamp = str(time.time())
	redirect_url = request.GET['path']
	# print redirect_url
	sha1_str = 'jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s' % (jsapi_ticket, noncestr, timestamp, redirect_url)
	signature = hashlib.sha1(sha1_str).hexdigest()
	result = "wx.config({"+\
      "debug: false,"+\
      "appId: '%s',"+\
      "timestamp: %s,"+\
      "nonceStr: '%s',"+\
      "signature: '%s',"+\
      "jsApiList: ["+\
      	"'onMenuShareAppMessage','onMenuShareTimeline','onMenuShareQQ','previewImage','hideOptionMenu','showOptionMenu','chooseImage',"+\
      "]"+\
    "});"
	response = HttpResponse(result % (appId, timestamp, noncestr, signature), content_type='application/x-javascript')
	return response

def renovate(request):
	"""
	记录微信JS注册失败的原因，删除ticket，下次页面调用时从新获取
	"""
	print 'wexin js renovate', request.GET['errMsg']
	cache.delete('wxjs_ticket')
	return HttpResponse('1', content_type='text/html')