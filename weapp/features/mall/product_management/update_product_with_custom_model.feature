@func:webapp.modules.mall.views.update_product
Feature: 更新商品规格
	Jobs通过管理系统在商城中添加"商品"后，能修改"商品规格"

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
Scenario: 重新添加商品规格
	Jobs添加无商品规格的商品后，能再次添加商品规格

	Given jobs已添加商品
		"""
		[{
			"name": "商品1",
			"model": {
				"models": {
					"standard": {
						"price": 11.0,
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	Then jobs能获取商品'商品1'
		"""
		{
			"is_enable_model": "不启用规格"
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


@mall @mall.product @mall.product_model @mall2
Scenario: 更新已有商品规格
	Jobs添加有商品规格的商品后，能更新商品规格

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
	When jobs更新商品'商品1'
		"""
		{
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.1,
						"weight": 3.2,
						"stock_type": "无限"
					},
					"红色 S": {
						"price": 1.0,
						"weight": 0.5,
						"stock_type": "无限"
					},
					"黑色 M": {
						"price": 1.0,
						"weight": 0.5,
						"stock_type": "无限"
					},
					"红色 M": {
						"price": 1.0,
						"weight": 0.5,
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
					"黑色 S": {
						"price": 10.1,
						"weight": 3.2,
						"stock_type": "无限"
					},
					"红色 S": {
						"price": 1.0,
						"weight": 0.5,
						"stock_type": "无限"
					},
					"黑色 M": {
						"price": 1.0,
						"weight": 0.5,
						"stock_type": "无限"
					},
					"红色 M": {
						"price": 1.0,
						"weight": 0.5,
						"stock_type": "无限"
					}
				}
			}
		}
		"""

@mall @mall.product @mall.product_model @mall2
Scenario: 修改商品的商品规格
	Jobs修改已添加的商品的商品规格

	Given jobs已添加商品
		"""
		[{
			"name": "商品1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}, {
			"name": "商品2",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色": {
						"price": 20.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}]
		"""
	When jobs更新商品'商品1'
		"""
		{
			"name": "商品1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"白色": {
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
					"白色": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}
		"""
	Then jobs能获取商品'商品2'
		"""
		{
			"name": "商品2",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色": {
						"price": 20.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}
		"""
