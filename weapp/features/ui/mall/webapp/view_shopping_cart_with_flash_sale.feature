# __edit__ : "新新8.26"

Feature: 添加限时抢购商品到购物车中
	bill将各种商品放入购物车后，能浏览商品信息

"""
该feature中需要修改和补充,涉及到场景如下
限时抢购商品添加到购物车后,显示"限时抢购"标签样式,并且显示"商品已降阶*元"
1.设置限购数量,购物车数量大于限购数量,提示限购*件
2.设置限购数量(限购数量大于库存),购物车数量大于库存,提示库存不足
3.设置限购数量(限购数量小于库存),购物车数量大于库存,提示限购*件,库存不足
	#显示限时抢购价格，显示商品已降价*元
	#无规格限购商品添加到购物车中,浏览购物车
4.有规格限购同个商品添加到购物车中,浏览购物车
	#有规格限购时,分别添加到购物车,在购物车不进行限制,下单时,提示限购*件
5.商品设置起购件,购物车中始终提示至少购买*件
	#并且购物车数量小于起购数量时,减少数量按钮不可点击
6.商品设置起购件,购物车数量大于库存时,提示至少购买*件,库存不足
7.商品先创建限时抢购,再把商品价格改低于限时抢购价格,购物车中"商品已降阶*元"勿出现负数
8.商品先设置限购,再设置起购(小于限购数量),购物车数量大于起购数理大于限购数量,提示至少购买*件,限购*件
9.商品先设置限购,再设置起购(小于限购数量),购物车数量大于起购数理大于限购数量大于库存,提示至少购买*件,限购*件,库存不足
	#商品先设置限购,再设置起购(小于限购数量),再关闭起购购物车数量大于起购数理大于限购数量大于库存,提示至少购买*件,限购*件,库存不足
10.限购活动会员价添加到购物车中
11.放入多种参加限时抢购的商品到购物车，商品包括无规格，有规格，活动有效，活动无效
后续-添加：
	1.单规格商品限购两件，库存1，购物车起始数量4。购物车页面，调整数量为2，商品不可勾选；调整商品数量为1，商品可以勾选。
	2.单规格商品限购两件，库存3，购物车起始数量4。购物车页面，调整数量为2，商品可勾选
	
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
			"price": 5,
			"stock_type": "有限",
			"stocks": 1
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
			"purchase_count":2
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 3,
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
						"price": 100,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name": "商品6",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"S": {
						"price": 500,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		},{
			"name": "商品7",
			"price": 30
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
			"count_per_purchase": 2,
			"promotion_price": 2.1
		}, {
			"name": "商品3限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品3"],
			"count_per_purchase": 1,
			"promotion_price": 3.1
		}, {
			"name": "商品5限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品5"],
			"count_per_purchase": "",
			"promotion_price": 50
		}, {
			"name": "商品6限时抢购",
			"start_date": "前天",
			"end_date": "2天后",
			"products": ["商品6"],
			"count_per_purchase": 1,
			"promotion_price": 200
		},{
			"name": "商品7限时抢购",
			"start_date": "3天前",
			"end_date": "2天前",
			"products": ["商品7"],
			"count_per_purchase": 3,
			"promotion_price": 20
		}]
		"""
	And bill关注jobs的公众号




Scenario: 1 设置限购数量,购物车数量大于限购数量,提示限购*件

	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1
		}]
	"""
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1
		}]
	"""
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1
		}]
	"""
	Then bill能获得购物车:ui
	#显示限时抢购商品已降阶18.5元
	"""
		[{
			"type": "flash_sale",
			"name": "商品1",
			"count": 3
		}]
	"""
	Then jobs限购2件:ui
	When bill数量小于限购
	Then jobs无提示:ui

Scenario: 2 设置限购数量(限购数量大于库存),购物车数量大于库存,提示库存不足
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品2",
			"count": 1
		}]
	"""
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品2",
			"count": 1
		}]
	"""
	
	Then bill能获得购物车:ui
	#显示限时抢购商品已降阶2.9元
	"""
		[{
			"type": "flash_sale",
			"name": "商品2",
			"count": 2
		}]
	"""
	Then jobs库存不足:ui
	When bill点击数量小于库存
	Then jobs无提示:ui

Scenario: 3 设置限购数量(限购数量小于库存),购物车数量大于库存,提示限购*件,库存不足
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品6",
			"count": 1
		}]
	"""
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品6",
			"count": 1
		}]
	"""
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品6",
			"count": 1
		}]
	"""
	
	Then bill能获得购物车:ui
	#显示限时抢购商品已降阶300.0元
	"""
		[{
			"type": "flash_sale",
			"name": "商品6",
			"count": 3
		}]
	"""
	Then jobs限购1件:ui
	Then jobs库存不足:ui
	When bill点击数量小于库存
	Then jobs限购1件:ui

Scenario: 4 有规格限购同个商品添加到购物车中,浏览购物车
	#有规格限购时,分别添加到购物车,在购物车不进行限制,下单时,提示限购*件
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品3",
			"model": {
				"models":{
					"M": {
						"count": 1
					}
				}
			}
		}]
	"""
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品3",
			"model": {
				"models":{
					"S": {
						"count": 1
					}
				}
			}
		}]
	"""		
	Then bill能获得购物车:ui
	#显示限时抢购商品已降阶300.0元
	"""
		[{
			"type": "flash_sale",
			"name": "商品3",
			"model": "M",
			"count": 1
		},{
			"type": "flash_sale",
			"name": "商品3",
			"model": "S",
			"count": 1
		}]
	"""

Scenario: 5 商品设置起购件(购物车数量小于库存时),购物车中始终提示至少购买*件
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品4",
			"model": {
				"models":{
					"M": {
						"count": 1
					}
				}
			}
		}]
	"""
	
	Then bill能获得购物车:ui
	
	"""
		[{
			"type": "起购商品",
			"name": "商品4",
			"model": "M",
			"count": 2
		}]
	"""
	Then jobs至少购买2件:ui
	When bill点击数量大于库存
	#库存为3,点击+按钮时提示
	Then jobs至少购买2件:ui
	Then jobs库存不足:ui


Scenario: 6 商品设置起购件(购物车数量大于库存时),提示至少购买*件,库存不足
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品4",
			"model": {
				"models":{
					"M": {
						"count": 2
					}
				}
			}
		}]
	"""
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品4",
			"model": {
				"models":{
					"M": {
						"count": 2
					}
				}
			}
		}]
	"""
	
	Then bill能获得购物车:ui
	
	"""
		[{
			"type": "起购商品",
			"name": "商品4",
			"model": "M",
			"count": 4
		}]
	"""
	Then jobs至少购买2件:ui
	Then jobs库存不足:ui
	When bill点击数量小于库存
	#点击数量2件,小于库存时提示
	Then jobs至少购买2件:ui

Scenario: 7 商品先创建限时抢购,再把商品价格改低于限时抢购价格,购物车中"商品已降阶*元"出现负数
	#产品暂不处理这种情况
	
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品5",
			"model": {
				"models":{
					"S": {
						"count": 2
					}
				}
			}
		}]
	"""
	
	Then bill能获得购物车:ui
	
	"""
		[{
			"type": "flash_sale",
			"commodity_markdown":50
			"name": "商品5",
			"model": "S",
			"count": 2
		}]
	"""
	When jobs修改商品
	"""
	[{
			"name": "商品5",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"S": {
						"price": 20,
						"stock_type": "无限"
					}
				}
			}
		}]
	"""
	Then bill能获得购物车:ui
	
	"""
		[{
			"type": "flash_sale",
			"commodity_markdown":-30
			"name": "商品5",
			"model": "S",
			"count": 2
		}]
	"""

Scenario: 8 商品先设置限购,再设置起购(小于限购数量),购物车数量大于起购数理大于限购数量,提示至少购买*件,限购*件
	When jobs修改商品
	"""
	[{
			"name": "商品1",
			"price": 30,
			"purchase_count":1
		}]
	"""
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1					
		}]
	"""

	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1		
		}]
	"""
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1		
		}]
	"""

	Then bill能获得购物车:ui
	
	"""
		[{
			"type": "flash_sale",
			"name": "商品1",
			"count": 3
		}]
	"""
	Then bill至少购买1件:ui
	Then bill限购2件:ui

Scenario: 9 商品先设置限购,再设置起购(小于限购数量),购物车数量大于起购数理大于限购数量大于库存,提示至少购买*件,限购*件,库存不足

	When jobs修改商品
	"""
	[{
			"name": "商品1",
			"price": 30,
			"purchase_count":1
			"stock_type": "有限",
			"stocks": 2
		}]
	"""
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1					
		}]
	"""

	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1		
		}]
	"""
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1		
		}]
	"""

	Then bill能获得购物车:ui
	
	"""
		[{
			"type": "flash_sale",
			"name": "商品1",
			"count": 3
		}]
	"""
	Then bill至少购买1件:ui
	Then bill限购2件:ui
	Then bill库存不足:ui

Scenario: 10 限购活动会员价添加到购物车中

	Given jobs登录系统
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}]
		"""
	
	When jobs更新"bill"的会员等级
		"""
		{
			"name": "bill",
			"member_rank": "铜牌会员"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "",
			"member_rank": "普通会员"
		}, {
			"name": "bill",
			"member_rank": "铜牌会员"
		}]
		"""
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
	"""
		[{
			"name": "商品1",
			"count": 1					
		}]
	"""

	Then bill能获得购物车:ui
	
	"""
		[{
			"type": "flash_sale",
			"name": "商品1",
			"count": 1
		}]
	"""
Scenario: 11 放入多种参加限时抢购的商品到购物车，商品包括无规格，有规格，活动有效，活动无效
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品7",
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
						"count": 1
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
			"product_groups": [{
				"promotion": {
					"type": "flash_sale",
					"result": {
						"saved_money": 11.5
					}
				},
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "",
					"result": {
						"saved_money": 30
					}
				},
				"products": [{
					"name": "商品7",
					"price": 30,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "flash_sale",
					"result": {
						"saved_money": 3.1
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
						"saved_money": 3.1
					}
				},
				"products": [{
					"name": "商品3",
					"model": "S",
					"price": 3.1,
					"count": 1
				}]
			}]
		}
		"""


