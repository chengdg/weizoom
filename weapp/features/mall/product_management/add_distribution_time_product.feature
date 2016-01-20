#_author_:王丽 2016.01.20

Feature: 添加具有配送时间新商品
"""
	Add Product
	Jobs能通过管理系统在商城中添加"商品"，商品可以配置“配送时间”是否开启此配置项
"""

@product @addProduct
Scenario:1 添加'配送时间'配置的商品
	Jobs添加商品后，能获取他添加的商品

	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "红烧肉",
			"category": "",
			"price": 12.0,
			"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"introduction": "红烧肉的简介",
			"detail": "红烧肉的详情",
			"shelve_type": "上架",
			"stock_type": "有限",
			"stocks": 3,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"weight": 5.5,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			},
			"postage": "免运费",
			"distribution_time":"on"
		}]
		"""
	Then jobs能获取商品'红烧肉'
		"""
		{
			"name": "红烧肉",
			"category": "",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"detail": "红烧肉的详情",
			"shelve_type": "上架",
			"stock_type": "有限",
			"stocks": 3,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"weight": 5.5,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			},
			"pay_interfaces":[{
				"type": "在线支付"
			},{
				"type": "货到付款"
			}],
			"postage": "免运费",
			"distribution_time":"on"
		}
		"""
