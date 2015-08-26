@func:webapp.modules.mall.views.list_mall_settings
Feature:添加支付方式
	Jobs能通过管理系统添加"支付方式"

@ui @ui-mall @ui-mall.pay_interface
Scenario: 添加支付方式:微信支付
	Jobs添加"微信支付"后
	1. jobs能获取添加的微信支付
	2. bill不能获取jobs添加的微信支付

	Given jobs登录系统:ui
	When jobs添加支付方式:ui
		"""
		[{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用",
			"weixin_appid": "12345", 
			"weixin_partner_id": "22345", 
			"weixin_partner_key": "32345", 
			"weixin_sign": "42345"
		}]
		"""
	Then jobs能获得支付方式'我的微信支付':ui
		"""
		{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用",
			"weixin_appid": "12345", 
			"weixin_partner_id": "22345", 
			"weixin_partner_key": "32345", 
			"weixin_sign": "42345"
		}
		"""
	Given bill登录系统:ui
	Then bill能获得支付方式列表:ui
		"""
		[]
		"""


@ui @ui-mall @ui-mall.pay_interface
Scenario: 添加支付方式:支付宝支付
	Jobs添加"支付宝支付"后
	1. jobs能获取添加的支付宝支付
	2. bill不能获取jobs添加的支付宝支付

	Given jobs登录系统:ui
	When jobs添加支付方式:ui
		"""
		[{
			"type": "支付宝",
			"description": "我的支付宝",
			"is_active": "启用",
			"partner": "11", 
			"key": "21", 
			"ali_public_key": "31", 
			"private_key": "41",
			"seller_email": "a@a.com"
		}]
		"""
	Then jobs能获得支付方式'我的支付宝':ui
		"""
		{
			"type": "支付宝",
			"description": "我的支付宝",
			"is_active": "启用",
			"partner": "11", 
			"key": "21", 
			"ali_public_key": "31", 
			"private_key": "41",
			"seller_email": "a@a.com"
		}
		"""
	Given bill登录系统:ui
	Then bill能获得支付方式列表:ui
		"""
		[]
		"""


@ui @ui-mall @ui-mall.pay_interface
Scenario: 添加支付方式:货到付款
	Jobs添加"支付方式"后
	1. jobs能获取添加的支付方式
	2. bill不能获取jobs添加的支付方式

	Given jobs登录系统:ui
	When jobs添加支付方式:ui
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}]
		"""
	Then jobs能获得支付方式'我的货到付款':ui
		"""
		{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}
		"""
	Given bill登录系统:ui
	Then bill能获得支付方式列表:ui
		"""
		[]
		"""


@ui @ui-mall @ui-mall.pay_interface
Scenario: 添加多个支付方式
	Jobs添加多个"支付方式"后
	1. jobs能获取添加的支付方式列表
	2. 列表按添加顺序排列
	3. bill不能获取jobs添加的支付方式列表

	Given jobs登录系统
	And jobs已添加支付方式
		"""
		[{
			"type": "货到付款"
		}, {
			"type": "微信支付"
		}]
		"""
	Given jobs登录系统:ui
	Then jobs能获得支付方式列表:ui
		"""
		[{
			"type": "货到付款"
		}, {
			"type": "微信支付"
		}]
		"""
	Given bill登录系统:ui
	Then bill能获得支付方式列表:ui
		"""
		[]
		"""

@ui @ui-mall @ui-mall.pay_interface
Scenario: 添加支付方式的限制
	Jobs添加全部"支付方式"后
	1. jobs不能再添加支付方式
	2. bill还能再添加支付方式

	Given jobs登录系统
	And jobs登录系统:ui
	Then jobs"还能"添加其他支付方式:ui
	When jobs添加支付方式
		"""
		[{
			"type": "货到付款"
		}]
		"""
	Then jobs"还能"添加其他支付方式:ui
	When jobs添加支付方式
		"""
		[{
			"type": "微信支付"
		}]
		"""
	Then jobs"还能"添加其他支付方式:ui
	When jobs添加支付方式
		"""
		[{
			"type": "支付宝"
		}]
		"""
	Then jobs"不能"添加其他支付方式:ui
	Given bill登录系统:ui
	Then bill"还能"添加其他支付方式:ui