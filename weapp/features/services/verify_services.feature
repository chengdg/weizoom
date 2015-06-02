@func:services.service_manager
Feature: 验证services

Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"model": {
				"models": {
					"standard": {
						"price": 9.9,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		},{
			"name": "商品2",
			"model": {
				"models": {
					"standard": {
						"price": 10,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		}]	
		"""
	
	And jobs已添加支付方式
		"""
		[{
			"type":"货到付款"
		}]
		"""
	And bill关注jobs的公众号

@wip.victor @mall2 
Scenario: 测试订单发货时会发消息给'post_save_order_service'

	Given jobs登录系统
	Then jobs获得未读订单提示数量为0
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"customer_message": "bill购买'商品1'"
		}
		"""
	Then jobs获得未读订单提示数量为1
