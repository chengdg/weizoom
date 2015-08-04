@func:webapp.modules.mall.views.list_mall_settings
Feature: 删除商品规格
	Jobs通过管理系统在商城中删除供商品使用的"商品规格"

Background:
	Given jobs登录系统
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
	And bill登录系统
	And bill已添加商品规格
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

@ui @ui-mall @ui-mall.product @ui-mall.product_model
Scenario: 删除商品规格
	Jobs更新商品规格后
	1. jobs不能能获得删除后的商品规格
	2. jobs能获得更新后的商品规格列表
	
	Given jobs登录系统:ui
	When jobs删除商品规格'颜色':ui
	Then jobs能获取商品规格列表:ui
		"""
		[{
			"name": "尺寸",
			"content": "M, S"
		}]	
		"""
	Given bill登录系统:ui
	Then bill能获取商品规格列表:ui
		"""
		[{
			"name": "颜色",
			"content": "黑色, 白色"
		}, {
			"name": "尺寸",
			"content": "M, S"
		}]
		"""

@ui @ui-mall @ui-mall.product @ui-mall.product_model
Scenario: 删除商品规格影响商品
	Jobs删除一条商品规格后
	1. 使用该商品规格的商品转为“下架”状态
	2. 没有使用该商品规格的商品保持不变

	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 S": {},
					"白色 S": {},
					"黑色 M": {},
					"白色 M": {}
				}
			}
		}, {
			"name": "商品2",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"白色 S": {}
				}
			}
		}, {
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"S": {}
				}
			}
		}]	
		"""
	Given jobs登录系统:ui
	When jobs删除商品规格'颜色':ui
	Then jobs能获取商品'商品1':ui
		"""
		{
			"name": "商品1",
			"is_enable_model": "不启用规格",
			"shelve_type": "下架"
		}	
		"""
	And jobs能获取商品'商品2':ui
		"""
		{
			"name": "商品2",
			"is_enable_model": "不启用规格",
			"shelve_type": "下架"
		}	
		"""
	And jobs能获取商品'商品3':ui
		"""
		{
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"S": {}
				}
			}
		}
		"""
	#And jobs收到商品'商品2'的下架提示'因为该规格被删除，商品"商品1，商品2"已下架'