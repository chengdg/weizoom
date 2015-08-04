Feature: 1298 编辑(删除) 图文消息 bc
	jobs能删除 图文消息

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
				"title":"sub图文1",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou2.jpg"
					}],
				"cover_in_the_text":"ture",
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
	and jobs已分页设置
		"""
		[{
			"page_count":2

		}]
		"""

Scenario: 删除图文消息
	jobs添加单图文和多图文后
	1. jobs 删除1条图文消息 还有3条
	2. jobs又删除1条图文消息 还有2条

	When jobs已删除'图文4'
	Then jobs获得'图文管理'列表
		"""
		[{
			title":"图文3",
			"add_time":"2015-04-13 17:26:39",
			"the_last_send_time":""
		}, {
			"title":"图文2",
			"add_time":"2015-04-13 16:26:39",
			"the_last_send_time":"2015-04-14 16:26:39"
		}]
		"""
	When jobs已删除'图文3'
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
