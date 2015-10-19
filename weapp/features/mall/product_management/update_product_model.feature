@func:webapp.modules.mall.views.list_mall_settings
#editor:张三香 2015.10.14

Feature: 更新商品规格
	Jobs通过管理系统在商城中更新供商品使用的"商品规格"

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

@mall2 @product @module   @mall @mall.product @mall.product_model
Scenario:1 更新商品规格信息
	Jobs更新商品规格后, 更新包括：
		1.增加规格属性值
		2.删除规格属性值
	更新后的结果:
		1. jobs能获得更新后的商品规格
		2. jobs能获得更新后的商品规格列表

	Given jobs登录系统
	When jobs更新商品规格'颜色'为
		"""
		{
			"name": "颜色*",
			"type": "文字"
		}
		"""
	And jobs更新商品规格'尺寸'为
		"""
		{
			"name": "尺寸*",
			"type": "图片",
			"add_values": [{
				"name": "L",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"delete_values": [{
				"name": "S"
			}]
		}
		"""
	Then jobs能获取商品规格列表
		"""
		[{
			"name": "颜色*",
			"type": "文字",
			"values": [{
				"name": "黑色"
			}, {
				"name": "白色"
			}]
		}, {
			"name": "尺寸*",
			"type": "图片",
			"values": [{
				"name": "M",
				"image": ""
			}, {
				"name": "L",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}]
		}]
		"""
	Given bill登录系统
	Then bill能获取商品规格列表
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

@mall2 @product @module   @mall @mall.product @mall.product_model
Scenario:2 删除商品规格值影响商品
	Jobs删除一条商品规格值后
	1. 删除后商品中规格不为空，直接去除这条规格值的组合规格
	2. 删除后商品中规格为空，商品转为“下架”状态

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
		}]
		"""
	Then jobs能获取商品'商品1'
		"""
		{
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
		}
		"""
	When jobs删除商品规格'颜色'的值'白色'
	Then jobs能获取商品'商品1'
		"""
		{
			"name": "商品1",
			"shelve_type": "下架",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 S": {},
					"黑色 M": {}
				}
			}
		}
		"""
	And jobs能获取商品'商品2'
		"""
		{
			"name": "商品2",
			"shelve_type": "下架"
		}
		"""
	#And jobs收到商品'商品2'的下架提示'因为该规格被删除，商品"商品2"已下架'
