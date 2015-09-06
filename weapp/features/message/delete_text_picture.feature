Feature: 1298 编辑(删除) 图文消息 bc
	jobs能删除 图文消息

Background:
	Given jobs登录系统
	And jobs已添加单图文
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
			"jump_url":"www.baidu.com"
		}]
		"""
	And jobs已添加多图文
		"""
		[{
			"title":"图文4",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			#"summary":"单条图文4文本摘要",
			"content":"单条图文4文本内容",
			"sub": [{
				"title":"sub图文1",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou2.jpg"
					}],
				"cover_in_the_text":"true",
				#"summary":"sub单条图文1文本摘要",
				"content":"sub单条图文1文本内容"
			},{
				"title":"sub图文2",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
					}],
				"cover_in_the_text":"false",
				#"summary":"sub单条图文2文本摘要",
				"content":"sub单条图文2文本内容"
			},{
				"title":"sub图文3",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou4.jpg"
					}],
				"cover_in_the_text":"false",
				#"summary":"sub单条图文3文本摘要",
				"jump_url":"www.baidu.com"
			}]
		}]
		"""

Scenario:1 删除图文消息
	jobs添加单图文和多图文后
	1. jobs 删除1条图文消息 还有3条
	2. jobs又删除1条图文消息 还有2条

	When jobs已删除图文'图文4'
	Then jobs能获取图文管理列表
		"""
		[{
			title":"图文3"
		}, {
			"title":"图文2"
		}]
		"""
	When jobs已删除图文'图文3'
	Then jobs能获取图文管理列表
		"""
		[{
			"title":"图文2"
		}, {
			"title":"图文1"
		}]
		"""

# __author__ : "王丽"
Scenario:2 在按"图文名称"查询的查询结果下删除图文

	Given jobs登录系统

	When jobs设置图文列表的查询条件
		"""
		{
			"title":"图文3"
		}
		"""
	Then jobs能获取图文管理列表
		"""
		[{
			"title":"图文4"
		},{
			title":"图文3"
		}]
		"""
	When jobs已删除图文'图文3'
	Then jobs能获取图文管理列表
		"""
		[{
			"title":"图文4"
		}]
		"""
