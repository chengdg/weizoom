Feature: 1297 预览图文消息  bc
	jobs能 预览图文消息

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
		}]
		"""
	and jobs已添加多条图文
		"""
		[{
			"title":"图文4",,
			"add_time":"2015-04-13 18:26:39"
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"summary":"单条图文4文本摘要",
			"content":"单条图文4文本内容",
			"sub": [{
				"title":"sub图文1",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou2.jpg"
					}],
				"cover_in_the_text":"ture",
				"summary":"sub单条图文1文本摘要",
				"content":"sub单条图文1文本内容"
			},{
				"title":"sub图文2",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
					}],
				"cover_in_the_text":"false",
				"summary":"sub单条图文2文本摘要",
				"content":"sub单条图文2文本内容"
			},{
				"title":"sub图文3",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou4.jpg"
					}],
				"cover_in_the_text":"false",
				"summary":"sub单条图文3文本摘要",
				"jump_url":"www.baidu.com"
			}]
		}]
		"""
	

Scenario: 1 预览单图文信息
	jobs添加单图文和多图文后
	1. jobs查看'图文1'
	2. jobs能看到'图文1'的预览信息，包括 标题，创建时间，公众号信息，图片，内容
	
	When jobs预览'图文1'
	Then jobs获得'图文1'详情
		"""
		[{
			"title":"图文1",
			"add_time":"2015-04-13",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"content":"单条图文1文本内容",
			"infor":"公众号信息"
		}]
		"""
	
Scenario: 2 预览多图文信息
	jobs添加单图文和多图文后
	1. jobs查看'sub图文1'
	2. jobs能看到'sub图文1'的预览信息，包括 标题，创建时间，公众号信息，图片，内容
	
	When jobs预览'sub图文1'
	Then jobs获得'sub图文1'详情
		"""
		[{
			"title":"图文4",,
			"add_time":"2015-04-13 18:26:39"
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"summary":"单条图文4文本摘要",
			"content":"单条图文4文本内容",
			"sub": [{
				"title":"sub图文1",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou2.jpg"
					}],
				"cover_in_the_text":"ture",
				"summary":"sub单条图文1文本摘要",
				"content":"sub单条图文1文本内容"
			},{
				"title":"sub图文2",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
					}],
				"cover_in_the_text":"false",
				"summary":"sub单条图文2文本摘要",
				"content":"sub单条图文2文本内容"
			},{
				"title":"sub图文3",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou4.jpg"
					}],
				"cover_in_the_text":"false",
				"summary":"sub单条图文3文本摘要",
				"jump_url":"www.baidu.com"
			}]
		}]
		"""