Feature: 浏览 查询图文列表
"""
	jobs能 浏览 查询图文列表
"""

Background:
	Given jobs登录系统
	When jobs已添加单图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容"
		},{
			"title":"图文2",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"cover_in_the_text":"false",
			"summary":"单条图文2文本摘要",
			"content":"单条图文2文本内容"
		},{
			"title":"图文3",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"cover_in_the_text":"false",
			"summary":"单条图文3文本摘要",
			"content":"单条图文3文本内容",
			"jump_url":"www.baidu.com"
		},{
			"title":"图文4",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou4.jpg"
			}],
			"cover_in_the_text":"false",
			"summary":"单条图文4文本摘要",
			"content":"单条图文4文本内容",
			"jump_url":"www.baidu.com"
		}]
		"""
	And jobs已添加多图文
		"""
		[{
			"title":"图文5",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
				}],
			"cover_in_the_text":"true",
			"summary":"单条图文5文本摘要",
			"content":"单条图文5文本内容"
		},{
			"title":"sub图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
				}],
			"cover_in_the_text":"true",
			"summary":"sub单条图文1文本摘要",
			"content":"sub单条图文1文本内容"
		},{
			"title":"sub图文2",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
			"cover_in_the_text":"false",
			"summary":"sub单条图文2文本摘要",
			"content":"sub单条图文2文本内容"
		},{
			"title":"sub图文3",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou4.jpg"
				}],
			"cover_in_the_text":"false",
			"summary":"sub单条图文3文本摘要",
			"jump_url":"www.baidu.com"
		}]
		"""

Scenario: 1 浏览图文列表，分页
	jobs添加单图文和多图文后
	1. jobs能看到按创建时间倒叙排列的图文列表
	2. jobs能分页查看图文列表

	Given jobs登录系统

	And jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""
	When jobs浏览图文管理
	When jobs浏览图文管理列表第1页
	Then jobs能获取图文管理列表 
		"""
		[{
			"title":"图文1"
		},{
			"title":"图文2"
		}]
		"""
	When jobs浏览图文管理列表下一页
	Then jobs能获取图文管理列表
		"""
		[{
			"title":"图文3"
		},{
			"title":"图文4"
		}]
		"""
	When jobs浏览图文管理列表第3页
	Then jobs能获取图文管理列表
		"""
		[{
			"title":"图文5"
		}]
		"""
	When jobs浏览图文管理列表上一页
	Then jobs能获取图文管理列表
		"""
		[{
			"title":"图文3"
		},{
			"title":"图文4"
		}]
		"""

Scenario: 2 浏览图文列表 按标题搜索结果
	jobs添加单图文和多图文后
	1. jobs能看到按创建时间倒叙排列的图文列表
	2. jobs能根据标题的部分匹配来搜索图文列表
	注意：#图文5，中包括sub图文1的子图文#

	#查询标题多图文的子图文标题也在查询范围内，返回的是整个多图文
		When jobs设置图文列表查询条件
			"""
			{
				"title":"图文3"
			}
			"""
		Then jobs能获取图文管理列表
			"""
			[ {
				"title":"图文3"
			},{
				"title":"图文5"
			}]
			"""
	#完全匹配查询
		When jobs设置图文列表查询条件
			"""
			{
				"title":"sub图文1"
			}
			"""
		Then jobs能获取图文管理列表
			"""
			[{
				"title":"图文5"
			}]
			"""
	#空条件查询
		When jobs设置图文列表查询条件
			"""
			{
				"title":""
			}
			"""
		Then jobs能获取图文管理列表
		"""
		[{
			"title":"图文1"
		},{
			"title":"图文2"
		},{
			"title":"图文3"
		},{
			"title":"图文4"
		},{
			"title":"图文5"
		}]
		"""
