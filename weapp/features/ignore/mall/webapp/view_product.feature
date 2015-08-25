@func:webapp.modules.mall.views.list_products
Feature: 在webapp中浏览商品
	bill能在webapp中看到jobs添加的"商品"

Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"category": "分类1",
			"physical_unit": "包",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"introduction": "商品1的简介",
			"detail": "商品1的详情",
			"remark": "商品1的备注",
			"shelve_type": "上架",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"model": {
				"property": {},
				"models": {
					"standard": {
						"price": 11.0,
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品2",
			"category": "",
			"physical_unit": "盘",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"introduction": "商品2的简介",
			"detail": "商品2的详情",
			"shelve_type": "下架",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"property": {},
				"models": {
					"standard": {
						"price": 12.0,
						"weight": 6.0,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}]	
		"""
	And bill关注jobs的公众号


@ui @ui-mall @ui-mall.webapp
Scenario: 浏览标准规格商品
	jobs添加商品后
	1. bill能在webapp中看到jobs添加的商品

	When bill访问jobs的webapp:ui
	And bill浏览jobs的webapp的'商品1'商品页:ui
	Then webapp页面标题为'商品1':ui
	And bill获得webapp商品:ui
		"""
		{
			"name": "商品1",
			"detail": "商品1的详情",
			"price": 11.0,
			"market_price": 11.0,
			"weight": 5.0,
			"stocks": "无限",
			"postage_config_name": "免运费"
		}
		"""


@ui @ui-mall @ui-mall.webapp
Scenario: 运费为免运费时，浏览商品库存信息，调整商品数量
	jobs添加商品后
	1. bill能调整商品数量
	2. bill调整商品数量时，重量，价格，运费有相应的变化
	
	When bill访问jobs的webapp:ui
	And bill浏览jobs的webapp的'商品1'商品页:ui
	Then bill获得webapp商品:ui
		"""
		{
			"name": "商品1",
			"detail": "商品1的详情",
			"price": 11.0,
			"market_price": 11.0,
			"weight": 5.0,
			"stocks": "无限",
			"postage_config_name": "免运费"
		}
		"""
	Given jobs登录系统:ui
	When jobs更新商品'商品1':ui
	"""
	{
		"name": "商品1",
		"model": {
			"models": {
				"standard": {
					"stock_type": "有限",
					"stocks": 3,
					"price": 11.0,
					"weight": 5.0
				}
			}
		}
	}	
	"""
	When bill访问jobs的webapp:ui
	And bill浏览jobs的webapp的'商品1'商品页:ui
	Then bill获得webapp商品:ui
		"""
		{
			"name": "商品1",
			"detail": "商品1的详情",
			"price": 11.0,
			"purchase_price": 11.0,
			"market_price": 11.0,
			"weight": 5.0,
			"stocks": "3包",
			"postage_config_name": "免运费"
		}
		"""
	When bill增加购买'2'个webapp商品:ui
	Then bill获得webapp商品的购买数量为'3':ui
	Then bill获得webapp商品:ui
		"""
		{
			"purchase_price": 33.0,
			"weight": 15.0
		}
		"""
	When bill减少购买'1'个webapp商品:ui
	Then bill获得webapp商品的购买数量为'2':ui
	Then bill获得webapp商品:ui
		"""
		{
			"purchase_price": 22.0,
			"weight": 10.0
		}
		"""
	When bill减少购买'3'个webapp商品:ui
	Then bill获得webapp商品的购买数量为'1':ui
	When bill增加购买'10'个webapp商品:ui
	Then bill获得webapp商品的购买数量为'3':ui


@ui @ui-mall @ui-mall.webapp
Scenario: 运费不为免运费时，调整商品数量
	jobs添加商品后
	1. bill能调整商品数量
	2. bill调整商品数量时，重量，价格，运费有相应的变化
	
	Given jobs登录系统
	And jobs已添加运费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":5,
			"first_weight_price":15.00,
			"added_weight":2,
			"added_weight_price":5.50
		}]
		"""
	When jobs选择'顺丰'运费配置
	When bill访问jobs的webapp:ui
	And bill浏览jobs的webapp的'商品1'商品页:ui
	Then bill获得webapp商品:ui
		"""
		{
			"name": "商品1",
			"detail": "商品1的详情",
			"price": 11.0,
			"purchase_price": 11.0,
			"market_price": 11.0,
			"weight": 5.0,
			"postage": 15.0,
			"stocks": "无限",
			"postage_config_name": "顺丰"
		}
		"""
	When bill增加购买'1'个webapp商品:ui
	Then bill获得webapp商品:ui
		"""
		{
			"price": 11.0,
			"purchase_price": 22.0,
			"weight": 10.0,
			"postage": 31.5,
			"postage_config_name": "顺丰"
		}
		"""
	When bill减少购买'1'个webapp商品:ui
	Then bill获得webapp商品:ui
		"""
		{
			"price": 11.0,
			"purchase_price": 11.0,
			"weight": 5.0,
			"postage": 15.0,
			"postage_config_name": "顺丰"
		}
		"""