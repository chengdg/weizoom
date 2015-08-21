@func:webapp.modules.mall.views.update_product
Feature: 删除商品的商品规格
	Jobs通过管理系统在商城中添加"商品"后，能删除商品的"商品规格"

Background:
	Given jobs登录系统
	And jobs已添加商品规格
		'''
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"name": "白色",
				"image": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"name": "红色",
				"image": "/standard_static/test_resource_img/hangzhou3.jpg"
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
		'''


@mall @mall.product @mall.product_model @mall2
Scenario: 删除单条商品规格
	Jobs添加有商品规格的商品后
	1. 能删除一条商品规格

	Given jobs已添加商品
		"""
		[{
			"name": "商品1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 S": {
						"price": 9.1,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	Then jobs能获取商品'商品1'
		"""
		{
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 S": {
						"price": 9.1,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	When jobs删除商品'商品1'的商品规格'黑色 S'
	"""
	{
		"name": "商品1",
		"is_enable_model": "启用规格",
		"model": {
			"models": {
				"白色 S": {
					"price": 9.1,
					"weight": 1.0,
					"stock_type": "无限"
				}
			}
		}
	}
	"""
	Then jobs能获取商品'商品1'
		"""
		{
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"白色 S": {
						"price": 9.1,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		}
		"""


@mall @mall.product @mall.product_model @mall2
Scenario: 删除所有商品规格
	Jobs添加有商品规格的商品，删除所有商品规格，并添加标准规格数据
	1. jobs能获得的标准规格

	Given jobs已添加商品
		"""
		[{
			"name": "商品1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 S": {
						"price": 9.1,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	When jobs删除商品'商品1'的商品规格'黑色 S'
	"""
	{
		"name": "商品1",
		"is_enable_model": "启用规格",
		"model": {
			"models": {
				"白色 S": {
					"price": 9.1,
					"weight": 1.0,
					"stock_type": "无限"
				}
			}
		}
	}
	"""
	And jobs删除商品'商品1'的商品规格'白色 S'
	"""
	{
		"name": "商品1",
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
	Then jobs能获取商品'商品1'
		"""
		{
			"is_enable_model": "不启用规格",
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


@mall @mall.product @mall.product_model @mall2
Scenario: 禁用与启用商品规格
	Jobs添加有商品规格的商品后
	1. 能禁用商品规格
	2. 禁用后商品恢复标准规格

	Given jobs已添加商品
		"""
		[{
			"name": "商品1",
			"model":{
				"models": {
					"standard": {
						"price": 11.12,
						"weight": 5.0,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}]
		"""
	Then jobs能获取商品'商品1'
		"""
		{
			"is_enable_model": "不启用规格",
			"model":{
				"models": {
					"standard": {
						"price": 11.12,
						"weight": 5.0,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}
		"""
	When jobs更新商品'商品1'
		"""
		{
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}
		"""
	Then jobs能获取商品'商品1'
		"""
		{
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}
		"""
	When jobs更新商品'商品1'
		"""
		{
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 9.9,
						"weight": 1.0,
						"stock_type": "有限",
						"stocks": 1
					}
				}
			}
		}
		"""
	Then jobs能获取商品'商品1'
		"""
		{
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 9.9,
						"weight": 1.0,
						"stock_type": "有限",
						"stocks": 1
					}
				}
			}
		}
		"""
