@func:webapp.modules.mall.views.list_products
Feature: 添加商品到购物车中
	bill能在webapp中将jobs添加的"商品"放入购物车

Background:
	Given jobs登录系统
	And jobs已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "红色",
				"image": "/standard_static/test_resource_img/icon_color/icon_1.png"
			}, {
				"name": "黄色",
				"image": "/standard_static/test_resource_img/icon_color/icon_5.png"
			}, {
				"name": "蓝色",
				"image": "/standard_static/test_resource_img/icon_color/icon_9.png"
			}]
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}, {
				"name": "L"
			}]
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 3
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
	And bill关注jobs的公众号
	And tom关注jobs的公众号


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 放入单个商品到购物车
	jobs添加商品后
	1. bill能在webapp中将jobs添加的商品放入购物车
	2. 多次放入同一个商品不会增加购物车中商品的条数
	3. tom的购物车不受bill操作的影响
	
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1"
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 1,
			"total_price": 3.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 3,
					"count": 1
				}]
			}]
		}
		"""
	When bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1",
			"count": 2
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 3,
			"total_price": 9.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 3,
					"count": 3
				}]
			}]
		}
		"""
	When tom访问jobs的webapp:ui
	Then tom能获得购物车:ui
		"""
		{
			"total_product_count": 0,
			"total_price": 0.0,
			"product_groups": []
		}
		"""	


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 放入多个商品到购物车
	jobs添加商品后
	1. bill能在webapp中将jobs添加的商品放入购物车
	2. 多次放入不同商品会增加购物车中商品的条数
	
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1"
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 1,
			"total_price": 3.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 3,
					"count": 1
				}]
			}]
		}
		"""
	When bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品2"
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 2,
			"total_price": 8.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 3,
					"count": 1
				}]
			}, {
				"promotion": null,
				"products": [{
					"name": "商品2",
					"price": 5,
					"count": 1
				}]
			}]
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 放入同一种商品的不同规格到购物车
	jobs添加商品后
	1. 商品的不同规格会增加购物车中商品的条数
	
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品3",
			"model": "红色 S",
			"count": 1
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 1,
			"total_price": 10.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品3",
					"model": "红色 S",
					"price": 10.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品3",
			"model": "黄色 M",
			"count": 2
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 3,
			"total_price": 28.2,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品3",
					"model": "红色 S",
					"price": 10,
					"count": 1
				}]
			}, {
				"promotion": null,
				"products": [{
					"name": "商品3",
					"model": "黄色 M",
					"price": 9.1,
					"count": 2
				}]
			}]
		}
		"""


# _author_ "师帅8.26"补充
Scenario:3 商品添加到购物车后，后台对商品进行上下架管理
	bill在webapp中将jobs的商品加入到购物车后，jobs对此商品进行删除操作
	1.bill查看jobs的webapp购物车，此商品已无效
	2.不影响购物车的其他商品

	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品2",
			"count": 1
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 2,
			"total_price": 8,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 3,
					"count": 1
				}]
			}, {
				"promotion": null,
				"products": [{
					"name": "商品2",
					"price": 5,
					"count": 1
				}]
			}]
		}
		"""
	Given jobs登录系统:ui
	When jobs-下架商品'商品1':ui
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 1,
			"total_price": 5,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品2",
					"price": 5,
					"count": 1
				}]
			}, {
				"promotion": null,
				"invalid_products": [{
					"name": "商品1",
					"price": 3,
					"count": 1
				}]
			}]
		}
		"""
	Given jobs登录系统:ui
	When jobs将商品'商品2'放入回收站:ui
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 0,
			"total_price": 0,
			"product_groups": [{
				"promotion": null,
				"invalid_products": [{
					"name": "商品2",
					"price": 5,
					"count": 1
				}]
			}, {
				"promotion": null,
				"invalid_products": [{
					"name": "商品1",
					"price": 3,
					"count": 1
				}]
			}]
		}
		"""
	Given jobs登录系统:ui
	When jobs-上架商品'商品1':ui
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 1,
			"total_price": 3,
			"product_groups": [{
				"promotion": null,
				"iproducts": [{
					"name": "商品1",
					"price": 3,
					"count": 1
				}]
			}, {
				"promotion": null,
				"invalid_products": [{
					"name": "商品2",
					"price": 5,
					"count": 1
				}]
			}]
		}
		"""

Scenario:4 商品添加到购物车后，后台对商品规格进行修改
	bill在webapp中将jobs的商品加入到购物车后，jobs将此商品的商品规格进行修改
	1.bill查看jobs的webapp购物车，此商品已无效
	2.bill可以清空无效商品

	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
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
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 2,
			"total_price": 15
			"product_groups": [{
				"products": [{
					"name": "商品3",
					"price": 7,
					"count": 1,
					"model": "M"
				}, {
					"name": "商品3",
					"price": 8,
					"count": 1,
					"model": "S"
				}]
			}],
			"invalid_products": []
		}
		"""
	#更改规格M的库存为0
	Given jobs登录系统:ui
	When jobs更新商品'商品3':ui
		"""
		{
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 7,
						"stock_type": "有限",
						"stocks": 0
					},
					"S": {
						"price": 8,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	Then jobs能获取商品'商品3':ui
		"""
		{
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 7,
						"stock_type": "有限",
						"stocks": 0
					},
					"S": {
						"price": 8,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 1,
			"total_price": 8,
			"product_groups": [{
				"products": [{
					"name": "商品3",
					"price": 8,
					"count": 1,
					"model": "S"
				}]
			}],
			"invalid_products": [{
				"name": "商品3",
				"price": 7,
				"count": 1,
				"model": "M"
			}]
		}
		"""
	#删除规格S
	When bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品5",
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
		"""
		{
			"total_product_count": 2,
			"total_price": 18,
			"product_groups": [{
				"products": [{
					"name": "商品3",
					"price": 8,
					"count": 1,
					"model": "S"
				}, {
					"name": "商品5",
					"price": 10,
					"count": 1,
					"model": "S"
				}]
			}],
			"invalid_products": [{
				"name": "商品3",
				"price": 7,
				"count": 1,
				"model": "M"
			}]
		}
		"""
	Given jobs登录系统:ui
	When jobs删除商品规格'尺寸'的值'S':ui
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 0,
			"total_price": 0,
			"product_groups": [],
			"invalid_products": [{
				"name": "商品3",
				"price": 7,
				"count": 1,
				"model": "M"
			}, {
				"name": "商品3",
				"price": 8,
				"count": 1
			}, {
				"name": "商品5",
				"price": 10,
				"count": 1
			}]
		}
		"""
	#商品4的规格从custom model变为standard model
	When bill加入jobs的商品到购物车:ui
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
		{
			"total_product_count": 1,
			"total_price": 8,
			"product_groups": [{
				"products": [{
					"name": "商品4",
					"price": 9,
					"count": 1,
					"model": "M"
				}]
			}],
			"invalid_products": [{
				"name": "商品3",
				"price": 7,
				"count": 1,
				"model": "M"
			}, {
				"name": "商品3",
				"price": 8,
				"count": 1
			}, {
				"name": "商品5",
				"price": 10,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统:ui
	When jobs更新商品'商品4':ui
		"""
		{
			"name": "商品4",
			"model": {
				"models":{
					"standard": {
						"price": 9.5
					}
				}
			}
		}
		"""
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"product_groups": [],
			"invalid_products": [{
				"name": "商品3",
				"price": 7,
				"count": 1
			}, {
				"name": "商品3",
				"price": 8,
				"count": 1
			}, {
				"name": "商品5",
				"price": 10,
				"count": 1
			}, {
				"name": "商品4",
				"price": 9,
				"count": 1
			}]
		}
		"""
	When bill从购物车中删除商品:ui
		"""
		["商品3", "商品5", "商品4"]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"product_groups": [],
			"invalid_products": []
		}
		"""
	#商品1的规格从standard model到custom model
	When bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1"
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"product_groups": [{
				"products": [{
					"name": "商品1",
					"price": 3,
					"count": 1
				}]
			}],
			"invalid_products": []
		}
		"""
	Given jobs登录系统:ui
	When jobs更新商品'商品1':ui
		"""
		{
			"name": "商品1",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 9.5,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}
		"""
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"product_groups": [],
			"invalid_products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""

Scenario: 5 商品添加到购物车后，进行删除
	bill加入jobs的商品到购物车后
	1.可以对购物车的商品进行删除

	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品2",
			"count": 1
		}, {
			"name": "商品4",
			"model": {
				"models":{
					"M": {
						"count": 3
					}
				}   
			}
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 5,
			"total_price": 35,
			"product_groups": [{
				"products": [{
					"name": "商品1"
				}, {
					"name": "商品2"
				}, {
					"name": "商品4"
				}]
			}],
			"invalid_products": []
		}
		"""
	When bill从购物车中删除商品:ui
		"""
		["商品1", "商品2"]
		""" 
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 3,
			"total_price": 27,
			"product_groups": [{
				"products": [{
					"name": "商品4"
				}]
			}],
			"invalid_products": []
		}
		"""

Scenario:6 商品添加到购物车后，后台对商品的价格，库存进行修改（库存数量不为0）
	bill在webapp中将jobs的商品加入到购物车后，jobs将此商品的商品规格进行修改
	1.bill查看jobs的webapp购物车，此商品有效，价格与库存为更改后的值

	
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
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
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 2,
			"total_price": 15,
			"product_groups": [{
				"products": [{
					"name": "商品3",
					"price": 7,
					"count": 1,
					"model": "M"
				}, {
					"name": "商品3",
					"price": 8,
					"count": 1,
					"model": "S"
				}]
			}],
			"invalid_products": []
		}
		"""
	#更改规格M的库存为3 S的价格为10
	Given jobs登录系统:ui
	When jobs更新商品'商品3':ui
		"""
		{
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 7,
						"stock_type": "有限",
						"stocks": 3
					},
					"S": {
						"price": 10,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	Then jobs能获取商品'商品3':ui
		"""
		{
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 7,
						"stock_type": "有限",
						"stocks": 3
					},
					"S": {
						"price": 10,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 2,
			"total_price": 17,
			"product_groups": [{
				"products": [{
					"name": "商品3",
					"price": 7,
					"count": 1,
					"model": "M",
					"stocks": 3
				}, {
					"name": "商品3",
					"price": 10,
					"count": 1,
					"model": "S"
				}]
			}],
			"invalid_products": []
		}
		"""

#1.将商品添加至购物车，商品参加限时抢购
#2.将商品添加至购物车，商品参加买赠活动
#3.将商品添加至购物车，商品参与会员价和积分活动


#根据bug_6565-补充.雪静
Scenario: 7 把商品加入购物车后，更改商品为起购商品
	bill把jobs的商品加入购物车后，jobs更改此商品为起购商品
	1.bill查看购物车此商品数量和总计

	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}]
		"""
	Given jobs登录系统
	When jobs更新商品'商品1'
		"""
		{
			"name": "商品1",
			"purchase_count": 3,
			"price": 3
		}
		"""
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 3,
			"total_price": 9.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 3,
					"count": 3
				}]
			}]
		}
		"""
	Then bill能获得提示信息"至少购买3件":ui