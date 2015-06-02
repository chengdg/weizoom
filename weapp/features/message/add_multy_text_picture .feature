Feature: 需求1291新建多条图文 jobs在系统中新建多条图文
	
#Background:
#	Given jobs登录系统
	

#@mall @mall.product @after_rebuild
Scenario: 1 添加多条图文 
	Jobs添加多条图文后，能获取他添加多条图文
	标题30字以内，摘要120字以内，正文2万字以内，插入一张图片

	Given jobs登录系统
	When jobs已添加多条图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容",
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
	 
	Then jobs能获取多条'图文1'
		"""
		{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容",
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
		}
		"""
	
	And bill能获取多条图文
		"""
		[]
		"""

