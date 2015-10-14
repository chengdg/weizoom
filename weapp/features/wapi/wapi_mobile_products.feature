Feature: 测试WAPI的场景

Background: 安装完整测试数据
	Given jobs登录系统
	#商品
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
			"name": "东坡肘子",
			"category": "分类1,分类2,分类3",
			"physical_unit": "包",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"introduction": "东坡肘子的简介",
			"detail": "东坡肘子的详情",
			"remark": "东坡肘子的备注",
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
						"price": 11.12,
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"category": "分类1",
			"physical_unit": "盘",
			"price": 12.0,
			"weight": 5.5,
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"introduction": "叫花鸡的简介",
			"detail": "叫花鸡的详情",
			"shelve_type": "下架",
			"stock_type": "有限",
			"stocks": 3,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
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
			}
		}, {
			"name": "水晶虾仁",
			"category": "分类2,分类3",
			"physical_unit": "盘",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou3.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou3.jpg",
			"introduction": "水晶虾仁的简介",
			"detail": "水晶虾仁的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"红色 S": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"黄色 M": {
						"price": 9.1,
						"weight": 1.0,
						"stock_type": "无限"
					},
					"蓝色 M": {
						"price": 11.1,
						"weight": 1.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}, {
			"name": "莲藕排骨汤",
			"category": "分类3",
			"physical_unit": "盘",
			"thumbnails_url": "/standard_static/test_resource_img/tang1.jpg",
			"pic_url": "/standard_static/test_resource_img/tang1.jpg",
			"introduction": "莲藕排骨汤的简介",
			"detail": "莲藕排骨汤的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/tang1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 5.0
					}
				}
			}
		}, {
			"name": "冬荫功汤",
			"category": "分类3",
			"physical_unit": "盘",
			"thumbnails_url": "/standard_static/test_resource_img/tang2.jpg",
			"pic_url": "/standard_static/test_resource_img/tang2.jpg",
			"introduction": "冬荫功汤的简介",
			"detail": "冬荫功汤的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/tang2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 6.0
					}
				}
			}
		}, {
			"name": "松鼠桂鱼",
			"category": "分类3",
			"physical_unit": "盘",
			"thumbnails_url": "/standard_static/test_resource_img/yu3.jpg",
			"pic_url": "/standard_static/test_resource_img/yu3.jpg",
			"introduction": "松鼠桂鱼的简介",
			"detail": "松鼠桂鱼的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/yu3.jpg"
			}],
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"S": {
						"price": 6.0
					}, 
					"L": {
						"price": 8.0
					}, 
					"M": {
						"price": 7.0
					}
				}
			}
		}, {
			"name": "武昌鱼",
			"category": "",
			"physical_unit": "盘",
			"thumbnails_url": "/standard_static/test_resource_img/yu1.jpg",
			"pic_url": "/standard_static/test_resource_img/yu1.jpg",
			"introduction": "武昌鱼的简介",
			"detail": "武昌鱼的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/yu1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 11.0,
						"weight": 20,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}, {
			"name": "黄桥烧饼",
			"category": "",
			"physical_unit": "个",
			"thumbnails_url": "/standard_static/test_resource_img/mian1.jpg",
			"pic_url": "/standard_static/test_resource_img/mian1.jpg",
			"introduction": "黄桥烧饼的简介",
			"detail": "黄桥烧饼的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/mian1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 2.0
					}
				}
			}
		}, {
			"name": "热干面",
			"category": "",
			"physical_unit": "碗",
			"thumbnails_url": "/standard_static/test_resource_img/mian2.jpg",
			"pic_url": "/standard_static/test_resource_img/mian2.jpg",
			"introduction": "热干面的简介",
			"detail": "热干面的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/mian2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 1.5
					}
				}
			}
		}]	
		"""


@wapi
Scenario: 测试按类别获得商品列表的API

	When 访问WAPI:mall/products_by_category
		"""
		{
			"oid": "$owner_id(jobs)$",
			"category_id": "$category_id(分类1)$",
			"is_access_weizoom_mall": false
		}
		"""
	Then 获得WAPI结果
		"""
		{
		}
		"""


@wapi @wip.wapi
Scenario: 测试获取商品的API

	When 访问WAPI:mall/product
		"""
		{
			"id": "$product_id(东坡肘子)$"
		}
		"""
	Then 获得WAPI结果
		"""
		{
			"id": "$product_id(东坡肘子)$",
			"owner_id": "$owner_id(jobs)$",
			"name": "东坡肘子"
		}
		"""

@wapi
Scenario: 测试商品分类的接口
	# 获得分类列表

	When 访问WAPI:mall/products_categories
		"""
		{
			"oid": "$owner_id(jobs)$",
			"is_access_weizoom_mall": false
		}
		"""
	Then 获得WAPI列表结果
		"""
		[{
			"id": "$category_id(分类1)$",
			"name": "分类1"
		}, {
			"id": "$category_id(分类2)$",
			"name": "分类2"
		}, {
			"id": "$category_id(分类3)$",
			"name": "分类3"
		}]
		"""

	When 访问WAPI:mall/product_category
		"""
		{
			"id": "$category_id(分类1)$",
			"is_access_weizoom_mall": false
		}
		"""
	Then 获得WAPI结果
		"""
		{
			"product_count": 0,
			"oid": "$owner_id(jobs)$",
			"id": "$category_id(分类1)$",
			"name": "分类1"
		}
		"""

	When 访问WAPI:mall/product_category
		"""
		{
			"id": "$category_id(分类2)$",
			"is_access_weizoom_mall": false
		}
		"""
	Then 获得WAPI结果
		"""
		{
			"product_count": 0,
			"oid": "$owner_id(jobs)$",
			"id": "$category_id(分类2)$",
			"name": "分类2"
		}
		"""
