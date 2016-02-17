#watcher:benchi@weizoom.com
# __edit__ : "benchi"
# 满减活动现在系统中已经关闭，故该feathure的各个场景先设置为@ignore，不再执行，等需要时再开启
Feature: 添加参与满减活动的商品到购物车中

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
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"S": {
						"price": 10,
						"stock_type": "无限"
					}
				}
			}
		}]	
		"""
	When jobs创建满减活动
		"""
		[{
			"name": "商品1满减",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"price_threshold": 100.0,
			"cut_money": 10.5
		}, {
			"name": "商品3满减",
			"start_date": "今天",
			"end_date": "2天后",
			"products": ["商品3", "商品2"],
			"price_threshold": 70.0,
			"cut_money": 10.0,
			"is_enable_cycle_mode": true
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号


@ignore @mall2 @mall.webapp @mall.webapp.shopping_cart
Scenario: 1购买单个满减商品，不满足价格阈值
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}]
		"""
	Then bill能获得购物车
		"""
		{
			"product_groups": [{
				"promotion": null,
				"can_use_promotion": false,
				"products": [{
					"name": "商品1",
					"price": 50.0,
					"count": 1
				}]
			}]
		}
		"""


@ignore @mall2 @mall.webapp @mall.webapp.shopping_cart
Scenario: 2购买满减活动中的部分商品，金额等于满足价格阈值，不执行循环满减
	商品2是"商品3满减"中的其中一个商品，测试部分商品累计金额满足满减的场景
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品2",
			"count": 14
		}]
		"""
	Then bill能获得购物车
		"""
		{
			"product_groups": [{
				"promotion": {
					"type": "price_cut",
					"result": {
						"subtotal": 60.0
					}
				},
				"can_use_promotion": true,
				"products": [{
					"name": "商品2",
					"price": 5.0,
					"count": 14
				}]
			}]
		}
		"""

@ignore @mall2 @mall.webapp @mall.webapp.shopping_cart
Scenario: 3购买满减活动中的全部商品，金额大于满足价格阈值，并满足循环满减条件
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
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
		}]
		"""
	Then bill能获得购物车
		"""
		{
			"product_groups": [{
				"promotion": {
					"type": "price_cut",
					"result": {
						"subtotal": 150.0
					}
				},
				"can_use_promotion": true,
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
			}]
		}
		"""