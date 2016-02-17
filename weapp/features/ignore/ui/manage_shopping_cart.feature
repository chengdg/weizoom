#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
Feature: 添加参加满减活动的商品到购物车后，浏览购物车中的商品

Background:
	Given jobs登录系统
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
			"price": 50
		}, {
			"name": "商品2",
			"price": 5
		}, {
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 20,
						"stock_type": "有限",
						"stocks": 2
					},
					"S": {
						"price": 30,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品4",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 9,
						"stock_type": "无限"
					}
				}   
			}
		}, {
			"name": "商品5",
			"price": 1
		}]	
		"""
	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}]
		"""
	When jobs创建满减活动
		"""
		[{
			"name": "商品3满减",
			"start_date": "今天",
			"end_date": "2天后",
			"products": ["商品3", "商品2"],
			"price_threshold": 70.0,
			"cut_money": 10.0,
			"is_enable_cycle_mode": true
		}]
		"""
	Given jobs已添加支付方式
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
	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址



@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 从购物车删除商品后，重新计算价格、数量等信息
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 2
		}, {
			"name": "商品2",
			"count": 14
		}, {
			"name": "商品3",
			"model": {
				"models":{
					"M": {
						"count": 2
					}
				}
			}
		}, {
			"name": "商品3",
			"model": {
				"models":{
					"S": {
						"count": 2
					}
				}
			}
		}, {
			"name": "商品5",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 21,
			"total_price": 174,
			"product_groups": [{
				"promotion": {
					"type": "flash_sale",
					"result": {
						"saved_money": 38.5
					}
				},
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 2
				}]
			}, {
				"promotion": {
					"type": "price_cut",
					"result": {
						"price": 140,
						"cut_money": 20,
						"subtotal": 150.0
					}
				},
				"products": [{
					"name": "商品2",
					"price": 5.0,
					"count": 14
				}, {
					"name": "商品3",
					"model": "M",
					"price": 20.0,
					"count": 2
				}, {
					"name": "商品3",
					"model": "S",
					"price": 30.0,
					"count": 2
				}]
			}, {
				"promotion": null,
				"products": [{
					"name": "商品5",
					"price": 1.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill从购物车中删除商品'商品2':ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 7,
			"total_price": 114,
			"product_groups": [{
				"promotion": {
					"type": "flash_sale",
					"result": {
						"saved_money": 38.5
					}
				},
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 2
				}]
			}, {
				"promotion": {
					"type": "price_cut",
					"result": {
						"price": 70,
						"cut_money": 10,
						"subtotal": 90.0
					}
				},
				"products": [{
					"name": "商品3",
					"model": "M",
					"price": 20.0,
					"count": 2
				}, {
					"name": "商品3",
					"model": "S",
					"price": 30.0,
					"count": 2
				}]
			}, {
				"promotion": null,
				"products": [{
					"name": "商品5",
					"price": 1.0,
					"count": 1
				}]
			}]
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 对商品的选择影响价格、数量
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 2
		}, {
			"name": "商品2",
			"count": 14
		}, {
			"name": "商品3",
			"model": {
				"models":{
					"M": {
						"count": 2
					}
				}
			}
		}, {
			"name": "商品3",
			"model": {
				"models":{
					"S": {
						"count": 2
					}
				}
			}
		}, {
			"name": "商品5",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 21,
			"total_price": 174,
			"product_groups": [{
				"promotion": {
					"type": "flash_sale",
					"result": {
						"saved_money": 38.5
					}
				},
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 2
				}]
			}, {
				"promotion": {
					"type": "price_cut",
					"result": {
						"price": 140,
						"cut_money": 20,
						"subtotal": 150.0
					}
				},
				"products": [{
					"name": "商品2",
					"price": 5.0,
					"count": 14
				}, {
					"name": "商品3",
					"model": "M",
					"price": 20.0,
					"count": 2
				}, {
					"name": "商品3",
					"model": "S",
					"price": 30.0,
					"count": 2
				}]
			}, {
				"promotion": null,
				"products": [{
					"name": "商品5",
					"price": 1.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill取消对购物车中商品'商品2'的选中:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 7,
			"total_price": 114,
			"product_groups": [{
				"promotion": {
					"type": "flash_sale",
					"result": {
						"saved_money": 38.5
					}
				},
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 2
				}]
			}, {
				"promotion": {
					"type": "price_cut",
					"result": {
						"price": 70,
						"cut_money": 10,
						"subtotal": 90.0
					}
				},
				"products": [{
					"name": "商品2",
					"price": 5.0,
					"count": 14
				}, {
					"name": "商品3",
					"model": "M",
					"price": 20.0,
					"count": 2
				}, {
					"name": "商品3",
					"model": "S",
					"price": 30.0,
					"count": 2
				}]
			}, {
				"promotion": null,
				"products": [{
					"name": "商品5",
					"price": 1.0,
					"count": 1
				}]
			}]
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 购买行为影响购物车
	1. 从购物车进入编辑订单页面，不下单，回到购物车页面，购物车信息不变
	2. 下单后，购物车中被选中的商品消失
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品3",
			"model": {
				"models":{
					"M": {
						"count": 1
					}
				}
			}
		}, {
			"name": "商品3",
			"model": {
				"models":{
					"S": {
						"count": 2
					}
				}
			}
		}]
		"""
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 4,
			"total_price": 81.5,
			"product_groups": [{
				"promotion": {
					"type": "flash_sale",
					"result": {
						"saved_money": 38.5
					}
				},
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "price_cut",
					"result": {
						"price": 70,
						"cut_money": 10,
						"subtotal": 70.0
					}
				},
				"products": [{
					"name": "商品3",
					"model": "M",
					"price": 20.0,
					"count": 1
				}, {
					"name": "商品3",
					"model": "S",
					"price": 30.0,
					"count": 2
				}]
			}]
		}
		"""
	When bill从购物车发起购买操作:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 4,
			"total_price": 81.5,
			"product_groups": [{
				"promotion": {
					"type": "flash_sale",
					"result": {
						"saved_money": 38.5
					}
				},
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "price_cut",
					"result": {
						"price": 70,
						"cut_money": 10,
						"subtotal": 70.0
					}
				},
				"products": [{
					"name": "商品3",
					"model": "M",
					"price": 20.0,
					"count": 1
				}, {
					"name": "商品3",
					"model": "S",
					"price": 30.0,
					"count": 2
				}]
			}]
		}
		"""
	#第二次下单，进行购买，购物车变化
	When bill取消对购物车中商品'商品1'的选中:ui
	When bill从购物车发起购买操作:ui
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 1,
			"total_price": 11.5,
			"product_groups": [{
				"promotion": {
					"type": "flash_sale",
					"result": {
						"saved_money": 38.5
					}
				},
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 1
				}]
			}]
		}
		"""