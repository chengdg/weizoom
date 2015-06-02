# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

class QQRequestParams(object):
	"""
	qq登陆请求中的参数定义
	"""
	def __init__(self):
		raise NotImplementedError

	SIGN = 'sign'


	# 必须 	授权类型，此值固定为“code”
	RESPONSE_TYPE='response_type'

	# 必须 	申请QQ登录成功后，分配给应用的appid
	CLIENT_ID='client_id'

	# 必须 	成功授权后的回调地址，必须是注册appid时填写的主域名下的地址，
	# 建议设置为网站首页或网站的用户中心。注意需要将url进行URLEncode。
	REDIRECT_URI='redirect_uri'

	# 必须 	client端的状态值。用于第三方应用防止CSRF攻击，成功授权后回调时会原样带回。
	# 请务必严格按照流程检查用户与state参数状态的绑定。
	STATE='state'

	# 可选 	请求用户授权时向用户显示的可进行授权的列表。
	# 例如：scope=get_user_info,list_album,upload_pic,do_like
	SCOPE='scope'


	# 必须 	授权类型，在本步骤中，此值为“authorization_code”。
	GRANT_TYPE='grant_type'

	# 必须 	申请QQ登录成功后，分配给网站的appid。
	CLIENT_SECRET='client_secret'

	# 必须 	上一步返回的authorization code。注意此code会在10分钟内过期.
	CODE='code'

