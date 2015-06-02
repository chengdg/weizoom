Feature: 配送套餐后台订单管理
		 需要已管理员权限运行(修改系统时间)

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
			"type": "日",		
			"frequency": "3",
			"times": "3",
			"price": "2000",
			"original_price": "2900"
		}]
		"""
	And jobs已添加了支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}]
		"""

@mall @mall.order @mall.order.manager @market_tool.delivery_plan
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
	Given jobs登录系统
	Then jobs通过后台管理系统可以看到配送套餐订单列表
		"""
		[{
			"status": "待支付",
			"price": 2000,
			"buyer": "bill",
			"products":[{
				"product_name": "套餐1",
				"count": 1,
				"total_price": "2000.00"
			}]
		}]
		"""
	And jobs成功创建配送套餐订单
		"""
		{
			"delevery_date": ["今天", "今天+3天", "今天+6天"]
		}
		"""