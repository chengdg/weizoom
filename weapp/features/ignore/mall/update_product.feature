#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
@func:webapp.modules.mall.views.update_product
Feature: Update Product
	Jobs能通过管理系统更新商品

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
				"models": {
					"standard": {
						"price": 12.0,
						"weight": 5.0,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}]	
		"""

@ui @ui-mall @ui-mall.product
Scenario: 更新商品
	Jobs添加一组商品后，能更改单个商品的所有字段的属性

	Given jobs登录系统:ui
	When jobs更新商品'商品1':ui
		"""
		{
			"name": "商品1*",
			"category": "分类2",
			"physical_unit": "包*",
			"thumbnails_url": "./test/imgs/hangzhou3.jpg",
			"pic_url": "./test/imgs/hangzhou3.jpg",
			"detail": "商品1*的详情",
			"remark": "商品1*的备注",
			"shelve_type": "下架",
			"model": {
				"models": {
					"standard": {
						"price": 111.0,
						"weight": 15.0,
						"stock_type": "有限",
						"stocks": 5
					}
				}
			}
		}	
		"""	
	Then jobs找不到商品'商品1'
	And jobs能获取商品'商品1*':ui
		"""
		{
			"name": "商品1*",
			"category": "分类2",
			"physical_unit": "包*",
			"detail": "商品1*的详情",
			"remark": "商品1*的备注",
			"shelve_type": "下架",
			"model": {
				"models": {
					"standard": {
						"price": 111.0,
						"weight": 15.0,
						"stock_type": "有限",
						"stocks": 5
					}
				}
			}
		}	
		"""
	And jobs能获取商品'商品2':ui
		"""
		{
			"name": "商品2",
			"category": "",
			"physical_unit": "盘",
			"detail": "商品2的详情",
			"shelve_type": "下架",
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"weight": 5.0,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}
		"""
	When jobs更新商品'商品1*':ui
		"""
		{
			"name": "商品1**",
			"category": ""
		}	
		"""
	Then jobs能获取商品'商品1**':ui
		"""
		{
			"name": "商品1**",
			"category": ""
		}	
		"""