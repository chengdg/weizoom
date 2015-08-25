Feature: 1296 浏览 查询图文列表 bc
	jobs能 浏览 查询图文列表

Background:
	Given jobs登录系统
	And jobs已添加单条图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容",
			"add_time":"2015-04-13 15:26:39"
		},{
			"title":"图文2",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"cover_in_the_text":"false",
			"summary":"单条图文2文本摘要",
			"content":"单条图文2文本内容",
			"add_time":"2015-04-13 16:26:39"
		},{
			"title":"图文3",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"cover_in_the_text":"false",
			"summary":"单条图文3文本摘要",
			"jump_url":"www.baidu.com",
			"add_time":"2015-04-13 17:26:39"
		}]
		"""
	And jobs已添加多条图文
		"""
		[{
			"title":"图文4",,
			"add_time":"2015-04-13 18:26:39"
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			#"summary":"单条图文4文本摘要",
			"content":"单条图文4文本内容",
			"sub": [{
				"title":"sub图文1",
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou2.jpg"
					}],
				"cover_in_the_text":"ture",
				#"summary":"sub单条图文1文本摘要",
				"content":"sub单条图文1文本内容"
			},{
				"title":"sub图文2",
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
					}],
				"cover_in_the_text":"false",
				#"summary":"sub单条图文2文本摘要",
				"content":"sub单条图文2文本内容"
			},{
				"title":"sub图文3",
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou4.jpg"
					}],
				"cover_in_the_text":"false",
				#"summary":"sub单条图文3文本摘要",
				"jump_url":"www.baidu.com"
			}]
		}]
		"""
	And jobs已发送图文
		"""
		[{
			"title":"图文1",
			"add_time":"2015-04-13 15:26:39",
			"the_last_send_time":"2015-04-14 15:26:39"
		}, {
			"title":"图文2",
			"add_time":"2015-04-13 16:26:39",
			"the_last_send_time":"2015-04-14 16:26:39"
		}, {
			"title":"图文3",
			"add_time":"2015-04-13 17:26:39",
			"the_last_send_time":""
		}, {
			"title":"图文4",
			"add_time":"2015-04-13 18:26:39",
			"the_last_send_time":"2015-04-14 11:26:39"
		}]
		"""
	And jobs已分页设置
		"""
		[{
			"page_count":2

		}]
		"""

Scenario: 1 浏览图文列表
	jobs添加单图文和多图文后
	1. jobs能看到按创建时间倒叙排列的图文列表
	2. jobs能分页查看图文列表

	When jobs浏览'图文管理'
	Then jobs获得'图文管理'列表
		"""
		[{
			"title":"图文4",
			"add_time":"2015-04-13 18:26:39",
			"the_last_send_time":"2015-04-14 11:26:39"
		}, {
			"title":"图文3",
			"add_time":"2015-04-13 17:26:39",
			"the_last_send_time":""
		}]
		"""
	When jobs浏览'下一页'
	Then jobs获得'图文管理'列表
		"""
		[{
			"title":"图文2",
			"add_time":"2015-04-13 16:26:39",
			"the_last_send_time":"2015-04-14 16:26:39"
		}, {
			"title":"图文1",
			"add_time":"2015-04-13 15:26:39",
			"the_last_send_time":"2015-04-14 15:26:39"
		}]
		"""
	When jobs浏览'上一页'
	Then jobs获得'图文管理'列表
		"""
		[{
			"title":"图文4",
			"add_time":"2015-04-13 18:26:39",
			"the_last_send_time":"2015-04-14 11:26:39"
		}, {
			"title":"图文3",
			"add_time":"2015-04-13 17:26:39",
			"the_last_send_time":""
		}]
		"""

Scenario: 2 浏览图文列表 按标题搜索结果
	jobs添加单图文和多图文后
	1. jobs能看到按创建时间倒叙排列的图文列表
	2. jobs能根据标题的部分匹配来搜索图文列表
	注意：#图文4，中包括sub图文1的子图文#

	When jobs搜索'图文1'
	Then jobs获得'图文管理'列表
		"""
		[ {
			"title":"图文4",
			"add_time":"2015-04-13 18:26:39",
			"the_last_send_time":"2015-04-14 11:26:39"
		}, {
			"title":"图文1",
			"add_time":"2015-04-13 15:26:39",
			"the_last_send_time":"2015-04-14 15:26:39"
		}]
		"""
	When jobs搜索'sub图文1'
	Then jobs获得'图文管理'列表
		"""
		[ {
			"title":"图文4",
			"add_time":"2015-04-13 18:26:39",
			"the_last_send_time":"2015-04-14 11:26:39"
		}]
		"""