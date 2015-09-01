#_author_:张三香

Feature:商品销量与订单量的比较
"""
	#说明：
		#针对线上bug3967补充feature
		#bug3967描述：【窝夫小子】商品的订单量大于商品总销量
			已完成的订单数量应该等于或者小于商品销量
		#订单支付完成（待发货、已发货、已完成）后,商品销量才变化
"""

Background:
	Given jobs登录系统
	When jobs添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用",
			"weixin_appid": "12345", 
			"weixin_partner_id": "22345", 
			"weixin_partner_key": "32345", 
			"weixin_sign": "42345"
		},{
			"type": "支付宝",
			"description": "我的支付宝支付",
			"is_active": "启用"
		}]
		"""
	Given jobs已添加商品规格
		"""
		[{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name":"商品1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"M": {},
					"S": {}
				}
			}
		},{
			"name": "商品2",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 12.0.,
						"weight": 1.0,
						"stock_type": "有限",
						"stocks": 12
					}
				}
			}
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号
	And marry关注jobs的公众号

@product @sales  @online_bug 
Scenario: 1 订单量等于商品销量
	Given jobs登录系统
	#待发货订单（bill购买商品1,数量1）
		When bill访问jobs的webapp
		And bill购买jobs的商品
			"""
				{
					"products": [{
						"name": "商品1",
						"model": "M",
						"count": 1
					}]
				}
			"""
		When bill使用支付方式'货到付款'进行支付

	#已发货订单（tom购买商品1,数量1）
		When tom访问jobs的webapp
		And tom购买jobs的商品
			"""
				{
					"products": [{
						"name": "商品1",
						"model": "S",
						"count": 1
					}]
				}
			"""
		When tom使用支付方式'微信支付'进行支付
		Given jobs登录系统
		When jobs对最新订单进行发货

	#已完成订单（marry购买商品1,数量1）
		When marry访问jobs的webapp
		And marry购买jobs的商品
			"""
				{
					"products": [{
						"name": "商品1",
						"model": "M",
						"count": 1
					}]
				}
			"""
		When marry使用支付方式'支付宝'进行支付
		Given jobs登录系统
		When jobs对最新订单进行发货
		When jobs'完成'最新订单
	Then jobs能获取商品'商品1'
		"""
			{
				"name":"商品1",
				"sales":3
			}
		"""
	When jobs根据给定条件查询订单
		"""
		{
			"product_name": "商品1"
		}
		"""
	Then jobs能获得筛选结果
		"""
			{
				"results": 3
			}
		"""

@product @sales  @online_bug 
Scenario: 2 订单量小于商品销量
	Given jobs登录系统
	#bill只购买商品1,数量1
		When bill访问jobs的webapp
		And bill购买jobs的商品
			"""
				{
					"products": [{
						"name": "商品1",
						"model": "M",
						"count": 1
					}]
				}
			"""
		When bill使用支付方式'货到付款'进行支付
		Given jobs登录系统
		When jobs对最新订单进行发货
		When jobs'完成'最新订单
	#tom只购买商品1,数量2
		When tom访问jobs的webapp
		And tom购买jobs的商品
			"""
				{
					"products": [{
						"name": "商品1",
						"model": "M",
						"count": 1
					},{
						"name": "商品1",
						"model": "S",
						"count": 1
					}]
				}
			"""
		When tom使用支付方式'微信支付'进行支付
		Given jobs登录系统
		When jobs对最新订单进行发货
		When jobs'完成'最新订单
	#marry购买2种商品（商品1,2 商品2,1）
		When marry访问jobs的webapp
		And marry购买jobs的商品
			"""
				{
					"products": [{
						"name": "商品1",
						"model": "M",
						"count": 2
					},{
						"name": "商品2",
						"count": 1
					}]
				}
			"""
		When marry使用支付方式'微信支付'进行支付
		Given jobs登录系统
		When jobs对最新订单进行发货
		When jobs'完成'最新订单
	Then jobs能获取商品'商品1'
		"""
			{
				"name":"商品1",
				"sales":5
			}
		"""
	When jobs根据给定条件查询订单
		"""
		{
			"product_name": "商品1",
			"order_status": "已完成"
		}
		"""
	Then jobs能获得筛选结果
		"""
			{
				"results": 3
			}
		"""





