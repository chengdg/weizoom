Feature: 添加属性模板
	Jobs通过管理系统在商城中添加属性模板

Background:
	Given jobs登录系统

@mall @mall.product @mall.image_group @mall2
Scenario: 添加属性模板
	jobs添加属性模板后
	1. jobs能获取属性模板
	2. bill不能获取属性模板
	3. 多个图片分组按添加顺序排列

	When jobs添加属性模板
		"""
		{
			"name": "计算机模板",
			"properties": [{
				"name": "CPU",
				"description": "CPU描述"
			}, {
				"name": "内存",
				"description": "内存描述"
			}]
		}
		"""
	And jobs添加属性模板
		"""
		{
			"name": "大米模板",
			"properties": [{
				"name": "产地",
				"description": "产地描述"
			}]
		}
		"""
	Then jobs能获取属性模板列表
		"""
		[{
			"name": "计算机模板"
		}, {
			"name": "大米模板"
		}]
		"""
	And jobs能获取属性模板'计算机模板'
		"""
		{
			"properties": [{
				"name": "CPU",
				"description": "CPU描述"
			}, {
				"name": "内存",
				"description": "内存描述"
			}]
		}
		"""
	And jobs能获取属性模板'大米模板'
		"""
		{
			"properties": [{
				"name": "产地",
				"description": "产地描述"
			}]
		}
		"""
	Given bill登录系统
	Then bill能获取图片分组列表                        
		"""
		[]
		"""