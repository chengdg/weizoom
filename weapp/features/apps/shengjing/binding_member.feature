@func:apps.shengjing.binding_member
Feature:盛景定制化会员中心绑定手机号
	
	
@apps.shengjing.binding_member @ignore
Scenario: 绑定会员信息
	1、微信营销系统会员A进入绑定页面，输入手机号15501289932会对应验证码，进入绑定信息页面，绑定成功后进入个人信息页面

	2、微信营销系统会员B进入绑定页面，输入手机号15501289931会对应验证码，进入个人信息页面

	Given bill配置绑定成功后给好友增加积分
		"""
			{
				"interal": "10"
			}
		"""

	Given 手机号15501289932是胜景会员，手机号15501289931不是胜景会员

	Given bill拥有会员A和B,并且A是B的上级节点
	
	When bill的会员A和B访问绑定信息页面时输入以下内容
		"""
			{
			"member_a":{
				"number": "15501289931",
				"captcha": "12345"
				},
			"member_b":{
				"number": "15501289911",
				"captcha": "12345"
				}
			}

		"""
	Then bill可以得到的绑定信息
		"""
			{
			"a":{
				"number": "15501289931",
				"captcha": "12345",
				"is_student":"1"
				},
			"b":{
				"number": "15501289911",
				"captcha": "12345",
				"is_student":"0"
				}
			}			
		"""
	When bill会员B进入绑定个人信息页面,输入以下信息
		"""
			{
				"name": "bert",
				"position": "程序员",
				"company": "北京微众文化传媒有限公司"
			}			
		"""


	