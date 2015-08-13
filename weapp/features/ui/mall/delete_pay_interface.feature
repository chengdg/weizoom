@func:webapp.modules.mall.views.list_mall_settings
Feature:删除支付方式
	Jobs能通过管理系统删除"支付方式"

@ui @ui-mall @ui-mall.pay_interface
Scenario: 删除支付方式
	jobs删除支付方式后
	1. jobs的支付方式列表会受影响
	2. nokia的支付方式列表不会受影响

	Given jobs登录系统
	And jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"description": "我的支付宝",
			"is_active": "启用"
		}]
		"""
	Given nokia登录系统
	And nokia已添加支付方式
		"""
		[{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"description": "我的支付宝",
			"is_active": "启用"
		}]
		"""
	Given jobs登录系统:ui
	Then jobs能获得支付方式列表:ui
		"""
		[{
			"type": "微信支付",
			"is_active": true
		}, {
			"type": "货到付款",
			"is_active": true
		}, {
			"type": "支付宝",
			"is_active": true
		}]
		"""
	When jobs删除支付方式'我的支付宝':ui
	Then jobs能获得支付方式列表:ui
		"""
		[{
			"type": "微信支付",
			"is_active": true
		}, {
			"type": "货到付款",
			"is_active": true
		}]
		"""
	Given nokia登录系统:ui
	Then nokia能获得支付方式列表:ui
		"""
		[{
			"type": "微信支付",
			"is_active": true
		}, {
			"type": "货到付款",
			"is_active": true
		}, {
			"type": "支付宝",
			"is_active": true
		}]
		"""
