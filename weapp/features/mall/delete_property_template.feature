Feature: 删除图片分组
	Jobs通过管理系统在商城中删除图片分组

Background:
	Given jobs登录系统
	When jobs添加属性模板
		"""
		[{
			"name": "计算机模板",
			"properties": [{
				"name": "CPU",
				"description": "CPU描述"
			}, {
				"name": "内存",
				"description": "内存描述"
			}]
		}, {
			"name": "大米模板",
			"properties": [{
				"name": "产地",
				"description": "产地描述"
			}]
		}]
		"""
	Given bill登录系统
	When bill添加属性模板
		"""
		[{
			"name": "计算机模板",
			"properties": [{
				"name": "CPU",
				"description": "CPU描述"
			}, {
				"name": "内存",
				"description": "内存描述"
			}]
		}, {
			"name": "大米模板",
			"properties": [{
				"name": "产地",
				"description": "产地描述"
			}]
		}]
		"""

@mall @mall.product @mall.product_model @mall2
Scenario: 删除属性模板
	jobs删除属性模板后
	1. jobs的属性模板发生变化
	2. bill的属性模板不变
	
	Given jobs登录系统
	Then jobs能获取属性模板列表
		"""
		[{
			"name": "计算机模板"
		}, {
			"name": "大米模板"
		}]
		"""
	When jobs删除属性模板'计算机模板'
	Then jobs能获取属性模板列表
		"""
		[{
			"name": "大米模板"
		}]
		"""
	Given bill登录系统
	Then bill能获取属性模板列表
		"""
		[{
			"name": "计算机模板"
		}, {
			"name": "大米模板"
		}]
		"""
