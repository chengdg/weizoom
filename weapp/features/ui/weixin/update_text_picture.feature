Feature: 需求1298编辑图文消息 jobs在系统中编辑图文消息
	
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
		}]
		"""
	And jobs已添加多图文
		"""
		[{
			"title":"图文2",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
				}],
			"cover_in_the_text":"true",
			"summary":"单条图文2文本摘要",
			"content":"单条图文2文本内容"
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
				"url": "/standard_static/test_resource_img/wufan1.jpg"
				}],
			"cover_in_the_text":"false",
			"summary":"sub单条图文3文本摘要",
			"jump_url":"www.baidu.com",
			"content":"sub单条图文3文本内容"
		}]
		"""

@ui @senior @textPicture
Scenario: 1 编辑单条图文(js校验) 
	Jobs编辑单条图文后
	标题超出30字以内，摘要超出120字以内，正文超出2万字以内，插入一张图片
	添加失败

	Given jobs登录系统
	When jobs已编辑单条图文
		"""
		[{
			"title_length":31,
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary_length":121,
			"content_length":20001
		}]
		"""
	 
	Then jobs添加单条图文失败

@ui @senior @textPicture		
Scenario: 2 编辑单条图文(js校验) 
	Jobs添加单条图文后
	标题为空，摘要为空，正文为空，没有插入一张图片
	添加失败

	Given jobs登录系统
	When jobs已编辑单条图文
		"""
		[{
			"title":null,
			"cover": null,
			"cover_in_the_text":"true",
			"summary":null,
			"content":null
		}]
		"""
	 
	Then jobs添加单条图文失败

