# __edit__ : "新新8.26"
Feature: 添加限时抢购商品到购物车中
	bill将各种商品放入购物车后，能浏览商品信息

"""
该feature中需要修改和补充,涉及到场景如下
限时抢购商品添加到购物车后,显示"限时抢购"标签样式,并且显示"商品已降阶*元"
1.设置限购数量,购物车数量大于限购数量,提示限购*件
2.设置限购数量,购物车数量大于库存,提示库存不足
3.设置限购数量,购物车数量大于库存大于限购数量,提示限购*件,库存不足
4.设置限购价格,购物车中显示限购价格
5.无规格限购商品添加到购物车中,浏览购物车
6.有规格限购同个商品添加到购物车中,浏览购物车
	#有规格限购时,分别添加到购物车,在购物车不进行限制,下单时,提示限购*件
7.商品设置起购件,购物车中始终提示至少购买*件
	#并且购物车数量小于起购数量时,减少数量按钮不可点击
8.商品设置起购件,购物车数量大于库存时,提示至少购买*件,库存不足
注,商品先创建限时抢购,再把商品价格改低于限时抢购价格,购物车中"商品已降阶*元"勿出现负数
9.商品先设置限购,再设置起购(小于限购数量),购物车数量大于起购数理大于限购数量,提示至少购买*件,限购*件
10.商品先设置限购,再设置起购(小于限购数量),购物车数量大于起购数理大于限购数量大于库存,提示至少购买*件,限购*件,库存不足
	#商品先设置限购,再设置起购(小于限购数量),再关闭起购购物车数量大于起购数理大于限购数量大于库存,提示至少购买*件,限购*件,库存不足
"""

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
			"price": 30
		}, {
			"name": "商品2",
			"price": 5
		}, {
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 7,
						"stock_type": "有限",
						"stocks": 2
					},
					"S": {
						"price": 8,
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
	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}, {
			"name": "商品2限时抢购",
			"start_date": "1天后",
			"end_date": "2天后",
			"products": ["商品2"],
			"promotion_price": 2.1
		}, {
			"name": "商品3限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品3"],
			"promotion_price": 3.1
		}, {
			"name": "商品4限时抢购",
			"start_date": "前天",
			"end_date": "昨天",
			"products": ["商品4"],
			"promotion_price": 4.1
		}]
		"""
	And bill关注jobs的公众号


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 放入多种参加限时抢购的商品到购物车，商品包括无规格，有规格，活动有效，活动无效
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品2",
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
			"total_product_count": 5,
			"total_price": 25.8,
			"product_groups": [{
				"promotion": {
					"type": "flash_sale",
					"result": {
						"saved_money": 18.5
					}
				},
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 1
				}]
			}, {
				"promotion": null,
				"products": [{
					"name": "商品2",
					"price": 5.0,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "flash_sale",
					"result": {
						"saved_money": 3.9
					}
				},
				"products": [{
					"name": "商品3",
					"model": "M",
					"price": 3.1,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "flash_sale",
					"result": {
						"saved_money": 4.9
					}
				},
				"products": [{
					"name": "商品3",
					"model": "S",
					"price": 3.1,
					"count": 2
				}]
			}]
		}
		"""