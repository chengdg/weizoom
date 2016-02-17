#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
Feature: 在webapp中购买配送套餐
	bill能在webapp中购买jobs添加的"配送套餐"

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1"
		}]	
		"""
	And jobs已添加配送套餐
		"""
		[{
			"name": "套餐1",
			"product": "商品1",
			"type": "月",		
			"frequency": "1",
			"times": "3",
			"price": "2000",
			"original_price": "2900"
		}, {
			"name": "套餐2",
			"product": "商品1",
			"type": "周",
			"frequency": "1",
			"times": "3",
			"price": "1800",
			"original_price": "1900"
		}, {
			"name": "套餐3",
			"product": "商品1",
			"type": "日",
			"frequency": "3",
			"times": "3",
			"price": "1700",
			"original_price": "1900"
		}]
		"""


@mall @mall.webapp @market_tool @market_tool.delivery_plan
Scenario: 会员购买配送套餐
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill购买jobs的配送套餐
		"""
		{
			"name": "套餐1",
			"first_deliver_time": "今天",
			"ship_name": "bill",
			"ship_tel": "1312546586",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"ship_name": "bill",
			"ship_tel": "1312546586",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"final_price": 2000,
			"products": [{
				"name": "套餐1",
				"price": 2000
			}]
		}
		"""

@mall @mall.webapp @market_tool @market_tool.delivery_plan
Scenario: 非会员购买配送套餐
	When tom购买jobs的配送套餐
		"""
		{
			"name": "套餐1",
			"first_deliver_time": "今天",
			"ship_name": "bill",
			"ship_tel": "1312546586",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
	Then tom成功创建订单
		"""
		{
			"status": "待支付",
			"ship_name": "bill",
			"ship_tel": "1312546586",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"final_price": 2000,
			"products": [{
				"name": "套餐1",
				"price": 2000
			}]
		}
		"""

@mall @mall.webapp @market_tool @market_tool.delivery_plan
Scenario: 选择不同的配送时间
	bill购买套餐后
	1. bill能在webapp中的订单列表中看到订单配送时间

	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	#购买"月"套餐
	And bill购买jobs的配送套餐
		"""
		{
			"name": "套餐1",
			"first_deliver_time": "今天",
			"type": "月"
		}
		"""
	Then bill成功创建配送套餐订单
		"""
		{
			"delevery_date": ["今天", "今天+1月", "今天+2月"]
		}
		"""
	#购买"周"套餐
	When bill购买jobs的配送套餐
		"""
		{
			"name": "套餐2",
			"first_deliver_time": "今天",
			"type": "周"
		}
		"""
	Then bill成功创建配送套餐订单
		"""
		{
			"delevery_date": ["今天", "今天+1周", "今天+2周"]
		}
		"""
	#购买"日"套餐
	When bill购买jobs的配送套餐
		"""
		{
			"name": "套餐3",
			"first_deliver_time": "今天",
			"type": "日"
		}
		"""
	Then bill成功创建配送套餐订单
		"""
		{
			"delevery_date": ["今天", "今天+3天", "今天+6天"]
		}
		"""