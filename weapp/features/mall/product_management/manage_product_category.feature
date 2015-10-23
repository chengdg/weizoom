# __author__ : "冯雪静"
#editor:王丽 2015.10.14
@func:webapp.modules.mall.views.update_productcategory
Feature: 管理商品分组列表
"""
	Manage Product Category
	Jobs能通过管理系统管理商城中的"商品分类列表"
	1.更新已存在的商品分类
	2.删除已存在的商品分类
	3.从分类中删除商品
	4.向分类中添加商品
	5.向分类中添加商品排序
"""

Background:
	Given jobs登录系统
	When jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	When jobs已添加商品
		#东坡肘子(有分类，上架，无限库存，多轮播图), 叫花鸡(无分类，下架，有限库存，单轮播图)
		"""
		[{
			"name": "东坡肘子",
			"status": "待售",
			"categories": "分类1,分类2",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"status": "待售",
			"categories": "分类1",
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}, {
			"name": "水晶虾仁",
			"status": "待售",
			"categories": "",
			"model": {
				"models": {
					"standard": {
						"price": 3.0
					}
				}
			}
		}]
		"""

@mall2 @product @group @ProductList  @mall @mall.product_category
Scenario:1 Jobs更新已存在的商品分类
	When jobs更新商品分类'分类1'为
		"""
		{
			"name": "分类1s"
		}
		"""
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1s"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""

@mall2 @product @group @ProductList  @mall @mall.product_category
Scenario:2 Jobs删除已存在的商品分类
	When jobs删除商品分类'分类2'
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类3"
		}]
		"""

@mall2 @product @group @ProductList  @mall.product_category @mall
Scenario:3 从分类中删除商品

	Given jobs登录系统
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1",
			"products": [{
				"name": "叫花鸡"
			}, {
				"name": "东坡肘子"
			}]
		}, {
			"name": "分类2",
			"products": [{
				"name": "东坡肘子"
			}]
		}, {
			"name": "分类3",
			"products": []
		}]
		"""
	When jobs从商品分类'分类1'中删除商品'东坡肘子'
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1",
			"products": [{
				"name": "叫花鸡"
			}]
		}, {
			"name": "分类2",
			"products": [{
				"name": "东坡肘子"
			}]
		}, {
			"name": "分类3",
			"products": []
		}]
		"""

@mall2 @product @group @ProductList  @mall.product_category @mall
Scenario:4 向分类中添加商品

	Given jobs登录系统
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1",
			"products": [{
				"name": "叫花鸡"
			}, {
				"name": "东坡肘子"
			}]
		}, {
			"name": "分类2",
			"products": [{
				"name": "东坡肘子"
			}]
		}, {
			"name": "分类3",
			"products": []
		}]
		"""
	Then jobs能获得商品分类'分类3'的可选商品集合为
		"""
		[{
			"name": "水晶虾仁",
			"display_price": 3.0,
			"status": "待售"
		}, {
			"name": "叫花鸡",
			"display_price": 12.0,
			"status": "待售"
		}, {
			"name": "东坡肘子",
			"display_price": 11.12,
			"status": "待售"
		}]
		"""
	And jobs能获得商品分类'分类2'的可选商品集合为
		"""
		[{
			"name": "水晶虾仁",
			"display_price": 3.0,
			"status": "待售"
		}, {
			"name": "叫花鸡",
			"display_price": 12.0,
			"status": "待售"
		}]
		"""
	And jobs能获得商品分类'分类1'的可选商品集合为
		"""
		[{
			"name": "水晶虾仁",
			"display_price": 3.0,
			"status": "待售"
		}]
		"""
	When jobs向商品分类'分类3'中添加商品
		"""
		[
			"东坡肘子",
			"叫花鸡",
			"水晶虾仁"
		]
		"""
	When jobs向商品分类'分类2'中添加商品
		"""
		[
			"水晶虾仁"
		]
		"""
	Then jobs能获得商品分类'分类3'的可选商品集合为
		"""
		[]
		"""
	And jobs能获得商品分类'分类2'的可选商品集合为
		"""
		[{
			"name": "叫花鸡",
			"display_price": 12.0,
			"status": "待售"
		}]
		"""
	And jobs能获得商品分类'分类1'的可选商品集合为
		"""
		[{
			"name": "水晶虾仁",
			"display_price": 3.0,
			"status": "待售"
		}]
		"""

@mall2 @product @group @ProductList  @mall.product_category @mall
Scenario:5 向分类中添加商品排序
	jobs向分类中添加商品，可以进行排序
	1.在分类里，将待售商品放在最下面，只给在售商品排序，待售商品在排序列里没有输入框

	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name":"商品1",
			"price":9.0,
			"status":"在售"
		},{
			"name":"商品2",
			"price":9.9,
			"status":"在售"
		},{
			"name":"商品3",
			"price":9.99,
			"status":"在售"
		},{
			"name":"商品4",
			"price":11.0,
			"status":"在售"
		},{
			"name":"商品5",
			"price":13.0,
			"status":"在售"
		}]
		"""
	When jobs向商品分类'分类3'中添加商品
		"""
		[
			"东坡肘子",
			"叫花鸡",
			"水晶虾仁"
		]
		"""
	And jobs向商品分类'分类3'中添加商品
		"""
		[
			"商品1",
			"商品2",
			"商品3",
			"商品4",
			"商品5"
		]
		"""
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3",
			"products": [{
				"name": "商品5",
				"display_price": 13.0,
				"status": "在售",
				"display_index": 0
			}, {
				"name": "商品4",
				"display_price": 11.0,
				"status": "在售",
				"display_index": 0
			}, {
				"name": "商品3",
				"display_price": 9.99,
				"status": "在售",
				"display_index": 0
			}, {
				"name": "商品2",
				"display_price": 9.9,
				"status": "在售",
				"display_index": 0
			}, {
				"name": "商品1",
				"display_price": 9.0,
				"status": "在售",
				"display_index": 0
			}, {
				"name": "水晶虾仁",
				"display_price": 3.0,
				"status": "待售",
				"display_index": 0
			}, {
				"name": "叫花鸡",
				"display_price": 12.0,
				"status": "待售",
				"display_index": 0
			}, {
				"name": "东坡肘子",
				"display_price": 11.12,
				"status": "待售",
				"display_index": 0
			}]
		}]
		"""

	When bill关注jobs的公众号
	# 手机端只验证商品顺序
	When bill访问jobs的webapp
	And bill浏览jobs的webapp的'分类3'商品列表页
	Then bill获得webapp商品列表
		|   name   |
		|  商品5   |
		|  商品4   |
		|  商品3   |
		|  商品2   |
		|  商品1   |

	Given jobs登录系统
	When jobs更新分类'分类3'中商品'商品3'商品排序2
	And jobs更新分类'分类3'中商品'商品2'商品排序3
	And jobs更新分类'分类3'中商品'商品1'商品排序1

	#排序大于0，按照正序排列如：1,2,3,排序等于0按照加入分类时间排序
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3",
			"products": [{
				"name": "商品1",
				"display_price": 9.0,
				"status": "在售",
				"display_index": 1
			}, {
				"name": "商品3",
				"display_price": 9.99,
				"status": "在售",
				"display_index": 2
			}, {
				"name": "商品2",
				"display_price": 9.9,
				"status": "在售",
				"display_index": 3
			}, {
				"name": "商品5",
				"display_price": 13.0,
				"status": "在售",
				"display_index": 0
			}, {
				"name": "商品4",
				"display_price": 11.0,
				"status": "在售",
				"display_index": 0
			}, {
				"name": "水晶虾仁",
				"display_price": 3.0,
				"status": "待售",
				"display_index": 0
			}, {
				"name": "叫花鸡",
				"display_price": 12.0,
				"status": "待售",
				"display_index": 0
			}, {
				"name": "东坡肘子",
				"display_price": 11.12,
				"status": "待售",
				"display_index": 0
			}]
		}]
		"""

	# 手机端只验证商品顺序
	When bill访问jobs的webapp
	And bill浏览jobs的webapp的'分类3'商品列表页
	Then bill获得webapp商品列表
		|   name   |
		|  商品1   |
		|  商品3   |
		|  商品2   |
		|  商品5   |
		|  商品4   |

