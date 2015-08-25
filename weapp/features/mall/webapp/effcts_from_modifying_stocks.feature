
#_author_:张三香

Feature:后台商品列表修改库存，对手机端的商品的影响
	#说明：
		#针对线上"bug3918"补充feature
		#bug3918-功能问题【商品管理】-商品列表，修改库存不管用，手机端还是显示原来的
		#当手机端商品显示'已售罄'后，后台商品列表修改库存后，手机端商品不再显示'已售罄'

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号

@product @online_bug
Scenario: 手机端商品显示已售罄,后台修改库存为有数量后,手机端不再显示已售罄

	#商品由有库存变为已售罄
		Given jobs登录系统
		Then jobs能获取商品'商品1'
			"""
			{
				"name": "商品1",
				"model": {
					"models": {
						"standard": {
							"price": 100.00,
							"stock_type": "有限",
							"stocks": 2
						}
					}
				}
			}
			"""

		When bill访问jobs的webapp
		When bill购买jobs的商品
			"""
			[{
				"products": [{
					"name": "商品1",
					"count": 2
				}]
			}]
			"""
		Then bill成功创建订单
			"""
			{
				"status": "待支付",
				"final_price": 200.00,
				"products": [{
					"name": "商品1",
					"price": 100.00,
					"count": 2
				}]
			}
			"""

		Given jobs登录系统
		Then jobs能获取商品'商品1'
			"""
			{
				"name": "商品1",
				"model": {
					"models": {
						"standard": {
							"price": 100.00,
							"stock_type": "有限",
							"stocks": 0
						}
					}
				}
			}
			"""

		When bill访问jobs的webapp
		And bill浏览jobs的webapp的'全部'商品列表页
		Then bill获得webapp商品列表
			"""
			[{
				"name": "商品1",
				"price":100.00
			}]
			"""
		When bill浏览jobs的webapp的'商品1'商品页
		Then webapp页面标题为'商品1'
		And bill获得系统提示信息'商品已售罄,非常抱歉'

	#后台修改库存，商品由已售罄变为有库存
		Given jobs登录系统
		When jobs更新商品'商品1'
			"""
				{
					"name": "商品1",
					"model": {
						"models": {
							"standard": {
								"price": 100.00,
								"stock_type": "有限",
								"stocks": 10
							}
						}
					}
				}
			"""
		Then jobs能获取商品'商品1'
			"""
				{
					"name": "商品1",
					"model": {
						"models": {
							"standard": {
								"price": 100.00,
								"stock_type": "有限",
								"stocks": 10
							}
						}
					}
				}
			"""

		When bill访问jobs的webapp
		And bill浏览jobs的webapp的'全部'商品列表页
		Then bill获得webapp商品列表
			"""
			[{
				"name": "商品1",
				"price":100.00
			}]
			"""
		When bill浏览jobs的webapp的'商品1'商品页
		Then webapp页面标题为'商品1'
		#不再提示'商品已售罄,非常抱歉'