@func:webapp.modules.mall.views.update_product
Feature: 添加商品规格
	Jobs通过管理系统在商城中添加"商品"时，能指定"商品规格"

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


@mall2 @mall.product @mall.product_model
Scenario: 添加拥有单属性商品规格的商品
	Jobs添加拥有商品规格的商品后，能获取的商品信息中包含商品规格
	
	Given jobs登录系统
	And jobs已添加商品
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
		}]	
		"""
	Then jobs能获取商品'商品1'
		"""
		{
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
		}
		"""


@mall2 @mall.product @mall.product_model
Scenario: 添加拥有复合属性商品规格的商品
	Jobs添加拥有商品规格的商品后，能获取的商品信息中包含商品规格
	
	Given jobs登录系统
	And jobs已添加商品
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