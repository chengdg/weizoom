#_author_:张三香
#editor:王丽 2015.10.13

Feature:在售商品管理-查看商品规格详情
"""
	#说明：
		#针对线上bug4372补充feature
		#bug4372描述：[商品管理]-[在售商品管理]规格弹窗中规格名称不显示问题
			没有输入任何筛选条件,查看规格正常,可以查看到该商品的规格弹窗中的规格名称
			当输入了筛选商品名称后,查看规格,规格名称不显示了
"""

Background:
	Given jobs登录系统
	And jobs已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"name": "白色",
				"image": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}, {
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
			"name": "无规格",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "有限",
						"stocks": 1
					}
				}
			}
		},{
			"name": "商品1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 M": {
						"price": 11.0,
						"weight": 1.0,
						"stock_type": "有限",
						"stocks": 11,
						"user_code":"101010"
					},
					"白色 M": {
						"price": 11.0,
						"weight": 1.0,
						"stock_type": "无限"
					},
					"黑色 S": {
						"price": 11.0,
						"weight": 1.0,
						"stock_type": "有限",
						"stocks": 11
					},
					"白色 S": {
						"price": 11.0,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name": "商品2",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色": {
						"price": 12.0,
						"weight": 1.0,
						"stock_type": "有限",
						"stocks": 12
					},
					"白色": {
						"price": 12.0,
						"weight": 1.0,
						"stock_type": "有限",
						"stocks": 12
					}
				}
			}
		}]
		"""

@mall2 @product @saleingProduct @online_bug
Scenario:1 不设置查询条件,查看商品规格详情
	Given jobs登录系统
	When jobs设置商品查询条件
		"""
		{}
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name":"商品2",
			"price":12.00
		},{
			"name":"商品1",
			"price":11.00
		},{
			"name":"无规格",
			"price":10.00
		}]
		"""
	And jobs能获取商品规格详情'商品2'
		| 颜色 | 价格(元) | 库存 | 商品编码 |
		| 黑色 | 12       | 12   |          |
		| 白色 | 12       | 12   |          |
	And jobs能获取商品规格详情'商品1'
		| 颜色 | 尺寸  | 价格(元) | 库存   | 商品编码 |
		| 黑色 |  M    |  11      | 11     | 101010   |
		| 白色 |  M    |  11      | 无限   |          |
		| 黑色 |  S    |  11      | 11     |          |
		| 白色 |  S    |  11      | 无限   |          |

@mall2 @product @saleingProduct @online_bug
Scenario:2 设置查询条件,查看商品规格详情
	Given jobs登录系统
	#商品名称
		When jobs设置商品查询条件
			"""
			{
				"name":"商品"
			}
			"""
		Then jobs能获得'在售'商品列表
			"""
			[{
				"name":"商品2",
				"price":12.00
			},{
				"name":"商品1",
				"price":11.00
			}]
			"""
		And jobs能获取商品规格详情'商品2'
			| 颜色 | 价格(元) | 库存 | 商品编码 |
			| 黑色 | 12       | 12   |          |
			| 白色 | 12       | 12   |          |
		And jobs能获取商品规格详情'商品1'
			| 颜色 | 尺寸  | 价格(元) | 库存   | 商品编码 |
			| 黑色 |  M    |  11      | 11     | 101010   |
			| 白色 |  M    |  11      | 无限   |          |
			| 黑色 |  S    |  11      | 11     |          |
			| 白色 |  S    |  11      | 无限   |          |

	#商品库存
		When jobs设置商品查询条件
			"""
			{
				"lowStocks":12,
				"highStocks":12
			}
			"""
		Then jobs能获得'在售'商品列表
			"""
			[{
				"name":"商品2",
				"price":12.00
			}]
			"""
		And jobs能获取商品规格详情'商品2'
			| 颜色 | 价格(元) | 库存 | 商品编码 |
			| 黑色 | 12       | 12   |          |
			| 白色 | 12       | 12   |          |
	#商品价格
		When jobs设置商品查询条件
			"""
			{
				"lowPrice":11,
				"highPrice":11
			}
			"""
		Then jobs能获得'在售'商品列表
			"""
			[{
				"name":"商品1",
				"price":11.00
			}]
			"""
		And jobs能获取商品规格详情'商品1'
			| 颜色 | 尺寸  | 价格(元) | 库存   | 商品编码 |
			| 黑色 |  M    |  11      | 11     | 101010   |
			| 白色 |  M    |  11      | 无限   |          |
			| 黑色 |  S    |  11      | 11     |          |
			| 白色 |  S    |  11      | 无限   |          |
