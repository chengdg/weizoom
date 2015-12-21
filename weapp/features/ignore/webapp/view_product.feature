# __author__ : "冯雪静"
@func:webapp.modules.mall.views.list_products
Feature: 在webapp中浏览商品
	bill能在webapp中看到jobs添加的"商品"
	"""
	准备数据：1.商品分类，2.商品规格，3.会员等级，4.商品，5.限时抢购活动，6.会员
	1.浏览商品
	2.浏览商品列表
	3.浏览商品分类
	"""

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
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}]
		"""
	Given jobs已添加商品
	#商品1：开起了会员价，多规格，商品2：是限时抢购商品，商品3：普通商品
		"""
		[{
			"name": "商品1",
			"promotion_title": "促销的东坡肘子",
			"categories": "分类1,分类2,分类3",
			"detail": "东坡肘子的详情",
			"status": "在售",
			"is_member_product": "on",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 S": {
						"price": 20.00,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 S": {
						"price": 10.00,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品2",
			"category": "分类1",
			"detail": "叫花鸡的详情",
			"status": "在售",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}, {
			"name": "商品3",
			"category": "",
			"detail": "叫花鸡的详情",
			"status": "在售",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.00,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品4",
			"category": "",
			"detail": "叫花鸡的详情",
			"status": "待售",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 15.00,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品2限时抢购",
			"promotion_title":"限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name":"商品2",
			"member_grade": "铜牌会员",
			"count_per_purchase": 1,
			"promotion_price": 50.00,
			"limit_period": 1
		}]
		"""
	Given bill关注jobs的公众号
	And tom关注jobs的公众号
	Given jobs登录系统
	When jobs更新'bill'的会员等级
		"""
		{
			"name": "bill",
			"member_rank": "铜牌会员"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "普通会员"
		}, {
			"name": "bill",
			"member_rank": "铜牌会员"
		}]
		"""


@product @ui
Scenario: 1 浏览商品
	jobs添加商品后
	1. bill能在webapp中看到jobs添加的商品
	2. tom能在webapp中看到jobs添加的商品

	When bill访问jobs的webapp
	And bill浏览jobs的webapp的'商品1'商品页
	#享受会员价的会员能获取商品原价和会员价
	Then webapp页面标题为'商品1'
	And bill获得webapp商品
		"""
		{
			"name": "商品1",
			"promotion_title": "促销的东坡肘子",
			"detail": "东坡肘子的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"model": {
				"models": {
					"黑色 S": {
						"price": 20.00,
						"member_price": 18.00,
						"stocks": 3
					},
					"白色 S": {
						"price": 10.00,
						"member_price": 9.00
					}
				}
			}
		}
		"""
	When bill浏览jobs的webapp的'商品2'商品页
	#享受限时抢购的会员获取的是限时抢购价
	Then webapp页面标题为'商品2'
	And bill获得webapp商品
		"""
		{
			"name": "商品2",
			"detail": "限时抢购",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 50.00,
						"stocks": 3
					}
				}
			}
		}
		"""
	When bill浏览jobs的webapp的'商品3'商品页
	Then webapp页面标题为'商品3'
	And bill获得webapp商品
		"""
		{
			"name": "商品3",
			"detail": "叫花鸡的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.00
					}
				}
			}
		}
		"""
	When tom访问jobs的webapp
	And tom浏览jobs的webapp的'商品1'商品页
	Then webapp页面标题为'商品1'
	And tom获得webapp商品
		"""
		{
			"name": "商品1",
			"promotion_title": "促销的东坡肘子",
			"detail": "东坡肘子的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"model": {
				"models": {
					"黑色 S": {
						"price": 20.00,
						"stocks": 3
					},
					"白色 S": {
						"price": 10.00
					}
				}
			}
		}
		"""
	When tom浏览jobs的webapp的'商品2'商品页
	Then webapp页面标题为'商品2'
	And tom获得webapp商品
		"""
		{
			"name": "商品2",
			"detail": "叫花鸡的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stocks": 3
					}
				}
			}
		}
		"""
	When tom浏览jobs的webapp的'商品3'商品页
	Then webapp页面标题为'商品3'
	And tom获得webapp商品
		"""
		{
			"name": "商品3",
			"detail": "叫花鸡的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.00
					}
				}
			}
		}
		"""


@product @ui
Scenario: 2 浏览商品列表
	jobs添加商品后
	1. bill获得webapp商品列表，商品按添加顺序倒序排序
	2. tom获得webapp商品列表，商品按添加顺序倒序排序

	When bill访问jobs的webapp
	And bill浏览jobs的webapp的'全部'商品列表页
	#有会员价的会员获取商品列表时是会员价
	#享受限时抢购的会员获取商品列表是限时抢购价
	Then webapp页面标题为'商品列表'
	And bill获得webapp商品列表
		"""
		[{
			"name": "商品3",
			"price": 12.00
		}, {
			"name": "商品2",
			"price": 50.00
		}, {
			"name": "商品1",
			"price": 9.00
		}]
		"""
	When tom访问jobs的webapp
	And tom浏览jobs的webapp的'全部'商品列表页
	Then webapp页面标题为'商品列表'
	And tom获得webapp商品列表
		"""
		[{
			"name": "商品3",
			"price": 12.00
		}, {
			"name": "商品2",
			"price": 100.00
		}, {
			"name": "商品1",
			"price": 10.00
		}]
		"""


@product @ui
Scenario: 3 浏览商品分类
	jobs添加商品后
	1. bill获得webapp商品列表，商品按添加顺序倒序排序
	2. tom获得webapp商品列表，商品按添加顺序倒序排序

	When bill访问jobs的webapp
	And bill浏览jobs的webapp的'分类1'商品列表页
	Then webapp页面标题为'商品列表'
	And bill获得webapp商品列表
		"""
		[{
			"name": "商品2",
			"price": 50.00
		}, {
			"name": "商品1",
			"price": 9.00
		}]
		"""
	When tom访问jobs的webapp
	And tom浏览jobs的webapp的'分类1'商品列表页
	Then webapp页面标题为'商品列表'
	And tom获得webapp商品列表
		"""
		[{
			"name": "商品2",
			"price": 100.00
		}, {
			"name": "商品1",
			"price": 10.00
		}]
		"""