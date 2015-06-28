@func:webapp.modules.mall.views.list_products
Feature: 在webapp中浏览商品
	bill能在webapp中看到jobs添加的"商品"

Background:
	Given jobs登录系统
	Given jobs已添加商品分类
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
						"market_price":20.0,
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
						"market_price":"",
						"weight": 6.0,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "商品3",
			"category": "",
			"physical_unit": "盘",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"introduction": "商品3的简介",
			"detail": "商品3的详情",
			"shelve_type": "上架",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"property": {},
				"models": {
					"standard": {
						"price": 12.0,
						"market_price":"",
						"weight": 6.0,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}]
		"""
	And bill关注jobs的公众号


@mall @mall.webapp @mall2 @zy_vp01
Scenario: 浏览商品
	jobs添加商品后
	1. bill能在webapp中看到jobs添加的商品
	2. 商品按添加顺序倒序排序

#	When bill访问jobs的webapp
#	And bill浏览jobs的webapp的'商品1'商品页
#	Then webapp页面标题为'商品1'
#	And bill获得webapp商品
#		"""
#		{
#			"name": "商品1",
#			"physical_unit": "包",
#			"thumbnails_url": "/standard_static/test_resource_img/hangzhou1.jpg",
#			"pic_url": "/standard_static/test_resource_img/hangzhou1.jpg",
#			"introduction": "商品1的简介",
#			"detail": "商品1的详情",
#			"remark": "商品1的备注",
#			"swipe_images": [{
#				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
#			}, {
#				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
#			}, {
#				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
#			}],
#			"model": {
#				"property": {},
#				"models": {
#					"standard": {
#						"price": 11.0,
#						"market_price":20.0,
#						"weight": 5.0,
#						"stock_type": "无限"
#					}
#				}
#			}
#		}
#		"""


	When bill访问jobs的webapp
	And bill浏览jobs的webapp的'全部'商品列表页
	Then webapp页面标题为'商品列表(全部)'
	And bill获得webapp商品列表
		"""
		[{
			"name": "商品3"
		}, {
			"name": "商品1"
		}]
		"""
