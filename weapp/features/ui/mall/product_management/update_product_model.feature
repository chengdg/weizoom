#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
@func:webapp.modules.mall.views.list_mall_settings
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

@mall @mall.product @mall.product_model @drop_in_mall2 @ui
Scenario: 更新商品规格值影响商品
	Jobs更新一条商品规格值后
	1. 与该规格值关联的商品规格的名字发生变化

	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 S": {}
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
	When jobs更新商品规格'尺寸'为
		"""
		{
			"name": "尺寸",
			"type": "文字",
			"add_values": [{
				"name": "S*"
			}],
			"delete_values": [{
				"name": "S"
			}]
		}
		"""
	Then jobs能获取商品'商品1'
		"""
		{
			"name": "商品1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 S*": {}
				}
			}
		}
		"""
	And jobs能获取商品'商品2'
		"""
		{
			"name": "商品2",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"白色 S*": {}
				}
			}
		}
		"""


