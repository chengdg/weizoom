#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
@func:webapp.modules.mall.views.list_mall_settings
Feature: 添加商品规格
	Jobs通过管理系统在商城中添加供商品使用的"商品规格"

Background:
	Given jobs登录系统:ui

@ui @ui-mall @ui-mall.product @ui-mall.product_model
Scenario: 添加商品规格
	Jobs添加商品规格后
	1. jobs能获取商品规格
	2. jobs的商品规格列表按创建顺序正序排列
	3. bill不能获取商品规格

	When jobs添加商品规格:ui
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "./test/imgs/hangzhou1.jpg"
			}, {
				"name": "白色",
				"image": "./test/imgs/hangzhou2.jpg"
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
	Then jobs能获取商品规格列表:ui
		"""
		[{
			"name": "颜色",
			"content": "黑色, 白色"
		}, {
			"name": "尺寸",
			"content": "M, S"
		}]
		"""
	And jobs能获取商品规格'颜色':ui
		"""
		{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "valid"
			}, {
				"name": "白色",
				"image": "valid"
			}]
		}
		"""
	And jobs能获取商品规格'尺寸':ui
		"""
		{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M",
				"image": null
			}, {
				"name": "S",
				"image": null
			}]
		}
		"""
	Given bill登录系统:ui
	Then bill能获取商品规格列表:ui
		"""
		[]
		"""
