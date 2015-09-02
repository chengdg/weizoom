# __author__ : "冯雪静"
@func:webapp.modules.mall.views.list_mall_settings
Feature:更新支付方式
	Jobs能通过管理系统更新"支付方式"
	"""
	1.更新支付方式,微信支付
	2.更新支付方式,货到付款
	3.更新支付方式,支付宝
	4.切换启用/停用状态
	"""

@mall2 @mall.pay_interface @wip.pi1
Scenario: 1 更新支付方式:微信支付
	Jobs更新"微信支付"后
	1. jobs能获取更新后的微信支付
	2. nokia的微信支付不受影响

	Given jobs登录系统
	When jobs添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用",
			"version": "v2",
			"weixin_appid": "12345",
			"weixin_partner_id": "22345",
			"weixin_partner_key": "32345",
			"weixin_sign": "42345"
		}]
		"""
	Then jobs能获得支付方式
		"""
		{
			"type": "微信支付",
			"is_active": "启用",
			"version": "v2",
			"weixin_appid": "12345",
			"weixin_partner_id": "22345",
			"weixin_partner_key": "32345",
			"weixin_sign": "42345"
		}
		"""
	Given nokia登录系统
	When nokia添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用",
			"version": "v2",
			"weixin_appid": "1",
			"weixin_partner_id": "2",
			"weixin_partner_key": "3",
			"weixin_sign": "4"
		}]
		"""
	Given jobs登录系统
	When jobs更新支付方式'微信支付'
		"""
		{
			"type": "微信支付",
			"version": "v3",
			"weixin_appid": "123450",
			"app_secret": "223450",
			"mch_id": "323450",
			"api_key": "423450"
		}
		"""
	Then jobs能获得支付方式
		"""
		{
			"type": "微信支付",
			"is_active": "启用",
			"version": "v3",
			"weixin_appid": "123450",
			"app_secret": "223450",
			"mch_id": "323450",
			"api_key": "423450"
		}
		"""
	Given nokia登录系统
	Then nokia能获得支付方式
		"""
		{
			"type": "微信支付",
			"is_active": "启用",
			"version": "v2",
			"weixin_appid": "1",
			"weixin_partner_id": "2",
			"weixin_partner_key": "3",
			"weixin_sign": "4"
		}
		"""

@mall2 @mall.pay_interface
Scenario: 2 更新支付方式:货到付款
	Jobs更新"货到付款"后
	1. jobs能获取更新后的货到付款
	2. nokia的货到付款不受影响

	Given jobs登录系统
	When jobs添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	Then jobs能获得支付方式
		"""
		{
			"type": "货到付款",
			"is_active": "启用"
		}
		"""
	Given nokia登录系统
	When nokia添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	Given jobs登录系统
	When jobs更新支付方式'货到付款'
		"""
		{
			"type": "货到付款",
			"is_active": "停用"
		}
		"""
	Then jobs能获得支付方式
		"""
		{
			"type": "货到付款",
			"is_active": "停用"
		}
		"""
	Given nokia登录系统
	Then nokia能获得支付方式
		"""
		{
			"type": "货到付款",
			"is_active": "启用"
		}
		"""


@mall2 @mall @mall.pay_interface
Scenario: 3 更新支付方式:支付宝
	Jobs更新"支付宝"后
	1. jobs能获取更新后的支付宝
	2. nokia的支付宝不受影响

	Given jobs登录系统
	When jobs添加支付方式
		"""
		[{
			"type": "支付宝",
			"is_active": "启用",
			"partner": "11",
			"key": "21",
			"ali_public_key": "31",
			"private_key": "41",
			"seller_email": "a@a.com"
		}]
		"""
	Then jobs能获得支付方式
		"""
		{
			"type": "支付宝",
			"is_active": "启用",
			"partner": "11",
			"key": "21",
			"ali_public_key": "31",
			"private_key": "41",
			"seller_email": "a@a.com"
		}
		"""
	Given nokia登录系统
	When nokia添加支付方式
		"""
		[{
			"type": "支付宝",
			"is_active": "启用",
			"partner": "10",
			"key": "20",
			"ali_public_key": "30",
			"private_key": "40",
			"seller_email": "a@a.com"
		}]
		"""
	Given jobs登录系统
	When jobs更新支付方式'支付宝'
		"""
		{
			"type": "支付宝",
			"partner": "110", 
			"key": "210", 
			"ali_public_key": "310", 
			"private_key": "410",
			"seller_email": "b@b.com"
		}
		"""
	Then jobs能获得支付方式
		"""
		{
			"type": "支付宝",
			"is_active": "启用",
			"partner": "110", 
			"key": "210", 
			"ali_public_key": "310", 
			"private_key": "410",
			"seller_email": "b@b.com"
		}
		"""
	Given nokia登录系统
	Then nokia能获得支付方式
		"""
		{
			"type": "支付宝",
			"is_active": "启用",
			"partner": "10", 
			"key": "20", 
			"ali_public_key": "30", 
			"private_key": "40",
			"seller_email": "a@a.com"
		}
		"""


@mall2 @mall @mall.pay_interface
Scenario: 4 切换启用/停用状态
	jobs切换支付方式的启用/停用状态后，会影响webapp中"支付方式列表页面"的显示

	Given jobs登录系统
	And jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"is_active": "启用"
		}]
		"""
	Then jobs能获得支付方式列表
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"is_active": "启用"
		}]
		"""
	When jobs'停用'支付方式'微信支付'
	When jobs'停用'支付方式'支付宝'
	When jobs'停用'支付方式'货到付款'
	Then jobs能获得支付方式列表
		"""
		[{
			"type": "微信支付",
			"is_active": "停用"
		}, {
			"type": "货到付款",
			"is_active": "停用"
		}, {
			"type": "支付宝",
			"is_active": "停用"
		}]
		"""