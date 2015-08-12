@func:webapp.modules.mall.views.list_mall_settings
Feature: 添加商品规格
	Jobs通过管理系统在商城中添加供商品使用的"商品规格"

Background:
	Given jobs登录系统

@mall @mall.product @mall.product_model @drop_in_mall2 @zy_apm01 @mall2
Scenario: 添加商品规格
	Jobs添加商品规格后
	1. jobs能获取商品规格
	2. bill不能获取商品规格

	Given jobs已添加商品规格
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
	Then jobs能获取商品规格'颜色'
		"""
		{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"name": "白色",
				"image": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}
		"""
	And jobs能获取商品规格'尺寸'
		"""
		{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}
		"""
	Given bill登录系统
	Then bill能获取商品规格列表
		"""
		[]
		"""


@mall @mall.product @mall.product_model @mall2
Scenario: 添加多个商品规格后，获取商品规格列表
	Jobs添加多个商品规格后
	1. jobs能获取商品规格列表
	2. 商品规格列表按创建顺序正序排列

	When jobs已添加商品规格
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
	Then jobs能获取商品规格列表
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
	Given bill登录系统
	Then bill能获取商品规格列表
		"""
		[]
		"""
