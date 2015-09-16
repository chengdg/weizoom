# _author_ "师帅8.27"
Feature:在webapp中购买有会员折扣的商品
#1.购买单个会员价商品，会员在商品列表看到会员价，在详情页会看到原价及会员价
#2.购买多个会员价商品，在购物车显示会员价，在订单页显示会员价
#3.购买多个商品，包含会员价，分开计算
#4.购买多规格商品，参与会员价，单个规格按照会员价计算
#5.购买多个商品，包含一个商品的多个规格，参与会员价的商品按照会员价计算，没有参与会员价的商品原价计算
#6.购买会员价商品，详情页显示会员价，后台取消会员价，在订单页显示原价
#7.购买时，在订单页参与会员价，下单时，按照会员价计算

Blackground:
	Given jobs登陆系统
	And jobs已添加商品规格
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
			"name": "商品1",
			"is_member_product": "on",
			"price": 100.0
		}, {
			"name": "商品2",
			"is_member_product": "on",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 40.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 40.00,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品3",
			"is_member_product": "on",
			"price": 200
		}, {
			"name": "商品4",
			"is_member_product": "off",
			"price": 50
		}]
	"""
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		},{
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}]
		"""
	When bill关注jobs的公众号
	And bill2关注jobs的公众号
	And bill3关注jobs的公众号

	Given jobs登录系统
	When jobs更新"bill2"的会员等级
		"""
		{
			"name":"bill2",
			"member_rank":"铜牌会员"
		}
		"""
	When jobs更新"bill3"的会员等级
		"""
		{
			"name":"bill3",
			"member_rank":"银牌会员"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name":"bill3",
			"member_rank":"银牌会员"
		}, {
			"name":"bill2",
			"member_rank":"铜牌会员"
		}, {
			"name":"bill",
			"member_rank":"普通会员"
		}]
		"""

Scenario: 1 购买单个会员价商品，会员在商品列表看到会员价，在详情页会看到原价及会员价
	When bill购买jobs的商品
	"""
		[{
			"products": [{
				"name": "商品1",
				"price": 100.0
				"count": 1
			}]
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待支付",
			"final_price": 100.0
			"products": [{
				"name": "商品1",
				"price": 100.0,
				"count": 1
			}]
		}]
	"""
	When bill2购买jobs的商品
	"""
		[{
			"products": [{
				"name": "商品1",
				"price": 90.0
				"count": 1
			}]
		}]
	"""
	Then bill2成功创建订单
	"""
		[{
			"status": "待支付",
			"final_price": 90.0
			"products": [{
				"name": "商品1",
				"price": 90.0,
				"count": 1
			}]
		}]
	"""

Scenario: 2购买多个会员价商品，在购物车显示会员价，在订单页显示会员价
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品3",
			"count": 1
		}]
	"""
	When bill从购物车发起购买操作
	"""
		[{
			"totla_product_count": 2,
			"total_price": 300.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 100.0,
					"count": 1
				}, {
					"name": "商品3",
					"price": 200.0,
					"count": 1
				}]
			}]
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待支付",
			"final_price": 300.0
			"products": [{
				"name": "商品1",
				"price": 100.0,
				"count": 1
			}, {
				"name": "商品3",
				"price": 200.0,
				"count": 1
			}]
		}]
	"""
	When bill2访问jobs的webapp
	And bill2加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品3",
			"count": 1
		}]
	"""
	When bill2从购物车发起购买操作
	"""
		[{
			"totla_product_count": 2,
			"total_price": 270.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 90.0,
					"count": 1
				}, {
					"name": "商品3",
					"price": 180.0,
					"count": 1
				}]
			}]
		}]
	"""
	Then bill2成功创建订单
	"""
		[{
			"status": "待支付",
			"final_price": 270.0
			"products": [{
				"name": "商品1",
				"price": 90.0,
				"count": 1
			}, {
				"name": "商品3",
				"price": 180.0,
				"count": 1
			}]
		}]
	"""

Scenario: 3 购买多个商品，包含会员价，分开计算
	When bill2访问jobs的webapp
	And bill2加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 2
		}, {
			"name": "商品4",
			"count": 1
		}]
	"""
	When bill2从购物车发起购买操作
	"""
		[{
			"totla_product_count": 3,
			"total_price": 230.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 180.0,
					"count": 2
				}, {
					"name": "商品4",
					"price": 50.0,
					"count": 1
				}]
			}]
		}]
	"""
	Then bill2成功创建订单
	"""
		[{
			"status": "待支付",
			"final_price": 230.0
			"products": [{
				"name": "商品1",
				"price": 180.0,
				"count": 2
			}, {
				"name": "商品4",
				"price": 50.0,
				"count": 1
			}]
		}]
	"""


Scenario: 4 购买多规格商品，参与会员价，单个规格按照会员价计算
	When bill2访问jobs的webapp
	And bill2加入jobs的商品到购物车
	"""
		[{
			"name": "商品2",
			"count": 1,
			"model": "M"
		}, {
			"name": "商品4",
			"count": 2
		}]
	"""
	When bill2从购物车发起购买操作
	"""
		[{
			"totla_product_count": 3,
			"total_price": 136.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品2",
					"price": 36.0,
					"count": 1,
					"model": "M"
				}, {
					"name": "商品4",
					"price": 100.0,
					"count": 2
				}]
			}]
		}]
	"""
	Then bill2成功创建订单
	"""
		[{
			"status": "待支付",
			"final_price": 136.0
			"products": [{
				"name": "商品2",
				"price": 36.0,
				"count": 1,
				"model": "M"
			}, {
				"name": "商品4",
				"price": 100.0,
				"count": 2
			}]
		}]
	"""

Scenario: 5 购买多个商品，包含一个商品的多个规格，参与会员价的商品按照会员价计算，没有参与会员价的商品原价计算
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品2",
			"count": 1,
			"model": "M"
		}, {
			"name": "商品2",
			"count": 1,
			"model": "S"
		}, {
			"name": "商品4",
			"count": 1
		}]
	"""
	When bill从购物车发起购买操作
	"""
		[{
			"totla_product_count": 3,
			"total_price": 130.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品2",
					"price": 40.0,
					"count": 1,
					"model": "M"
				}, {
					"name": "商品2",
					"price": 40.0,
					"count": 1,
					"model": "S"
				}, {
					"name": "商品4",
					"price": 50,
					"count": 1
				}]
			}]
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待支付",
			"final_price": 130.0
			"products": [{
				"name": "商品2",
				"price": 40.0,
				"count": 1,
				"model": "M"
			}, {
				"name": "商品2",
				"price": 40.0,
				"count": 1,
				"model": "S"
			}, {
				"name": "商品4",
				"price": 50,
				"count": 1
			}]
		}]
	"""
	When bill2访问jobs的webapp
	And bill2加入jobs的商品到购物车
	"""
		[{
			"name": "商品2",
			"count": 1,
			"model": "M"
		}, {
			"name": "商品2",
			"count": 1,
			"model": "S"
		}, {
			"name": "商品4",
			"count": 1
		}]
	"""
	When bill2从购物车发起购买操作
	"""
		[{
			"totla_product_count": 3,
			"total_price": 122.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品2",
					"price": 36.0,
					"count": 1,
					"model": "M"
				}, {
					"name": "商品2",
					"price": 36.0,
					"count": 1,
					"model": "S"
				}, {
					"name": "商品4",
					"price": 50,
					"count": 1
				}]
			}]
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待支付",
			"final_price": 122.0
			"products": [{
				"name": "商品2",
				"price": 36.0,
				"count": 1,
				"model": "M"
			}, {
				"name": "商品2",
				"price": 36.0,
				"count": 1,
				"model": "S"
			}, {
				"name": "商品4",
				"price": 50,
				"count": 1
			}]
		}]
	"""

Scenario: 6 购买会员价商品，详情页显示会员价，后台取消会员价，在订单页显示原价
	When bill2访问jobs的webapp
	And bill2加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品2",
			"count": 1,
			"model": "M"
		}]
	"""
	When bill2从购物车发起购买操作
	"""
		[{
			"totla_product_count": 2,
			"total_price": 126.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 90.0,
					"count": 1
				}, {


					"name": "商品2",
					"price": 36.0,
					"count": 1,
					"model": "M"
				}]
			}]
		}]
	"""
	And jobs修改'商品1'
	"""
		[{
			"name": "商品1",
			"price": 100.0,
			"is_member_product": "off",
			
		}]
	"""
	Then bill2成功创建订单
	"""
		[{
			"status": "待支付",
			"final_price": 136.0
			"products": [{
				"name": "商品1",
				"price": 100.0,
				"count": 1
			}, {
				"name": "商品2",
				"price": 36.0,
				"count": 1,
				"model": "M"
			}]
		}]
	"""

Scenario: 7 购买时，在订单页参与会员价，下单时，按照会员价计算
	When bill2访问jobs的webapp
	And bill2加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品4",
			"count": 1
		}]
	"""
	When bill2从购物车发起购买操作
	"""
		[{
			"totla_product_count": 2,
			"total_price": 140.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 90.0,
					"count": 1
				}, {
					"name": "商品4",
					"price": 50.0,
					"count": 1
				}]
			}]
		}]
	"""
	And jobs修改'商品4'
	"""
		[{
			"name": "商品4",
			"price": 50.0,
			"is_member_product": "on"
		}]
	"""
	Then bill2成功创建订单
	"""
		[{
			"status": "待支付",
			"final_price": 135.0
			"products": [{
				"name": "商品1",
				"price": 90.0,
				"count": 1
			}, {
				"name": "商品4",
				"price": 45.0,
				"count": 1
			}]
		}]
	"""





