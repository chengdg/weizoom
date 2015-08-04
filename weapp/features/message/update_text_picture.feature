Feature: 需求1298编辑图文消息 jobs在系统中编辑图文消息
	
Background:
	Given jobs登录系统
	And jobs已添加单条图文
		"""
		[{
			"title":"图文1",
			"add_time":"2015-04-13 15:26:39",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容"
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
			"content":"单条图文4文本内容",
			"sub": [{
				"title":"sub图文1",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou2.jpg"
					}],
				"cover_in_the_text":"ture",
				"content":"sub单条图文1文本内容"
			},{
				"title":"sub图文2",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
					}],
				"cover_in_the_text":"false",
				"content":"sub单条图文2文本内容"
			},{
				"title":"sub图文3",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou4.jpg"
					}],
				"cover_in_the_text":"false",
				"jump_url":"www.baidu.com"
			}]
		}]
		"""
	

Scenario: 1 编辑多条图文 
	
	Given jobs登录系统
	When jobs已编辑多条图文
		"""
		[{
			"title":"图文1修改",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"content":"单条图文1文本内容修改",
			"sub": [{
				"title":"sub图文1",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou2.jpg"
					}],
				"cover_in_the_text":"ture",
				"content":"sub单条图文1文本内容修改"
			},{
				"title":"sub图文2",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
					}],
				"cover_in_the_text":"false",
				"content":"sub单条图文2文本内容修改"
			},{
				"title":"sub图文3",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou4.jpg"
					}],
				"cover_in_the_text":"false",
				"jump_url":"www.sohu.com"
			}]
		}]
		"""
	 
	Then jobs能获取多条'图文1修改'
		"""
		{
			"title":"图文1修改",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"content":"单条图文1文本内容修改",
			"sub": [{
				"title":"sub图文1",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou2.jpg"
					}],
				"cover_in_the_text":"ture",
				"content":"sub单条图文1文本内容修改"
			},{
				"title":"sub图文2",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
					}],
				"cover_in_the_text":"false",
				"content":"sub单条图文2文本内容修改"
			},{
				"title":"sub图文3",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou4.jpg"
					}],
				"cover_in_the_text":"false",
				"jump_url":"www.sohu.com"
			}]
		}
		"""
	
	And bill能获取多条图文
		"""
		[]
		"""

Scenario: 2 编辑单条图文 
	Jobs编辑单条图文后，能获取他编辑的单条图文
	标题30字以内，摘要120字以内，正文2万字以内，插入一张图片

	Given jobs登录系统
	When jobs已编辑单条图文
		"""
		[{
			"title":"图文1修改",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"summary":"单条图文1文本摘要修改",
			"content":"单条图文1文本内容修改"
		}]
		"""
	Then jobs能获取'图文1修改'
		"""
		{
			"title":"图文1修改",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"summary":"单条图文1文本摘要修改",
			"content":"单条图文1文本内容修改"
		}
		"""
	And bill能获取单条图文
		"""
		[]
		"""

Scenario: 3 编辑单条图文 
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
			"cover_in_the_text":"ture",
			"summary_length":121,
			"content_length":20001
		}]
		"""
	 
	Then jobs添加单条图文失败
		
Scenario: 4 编辑单条图文 
	Jobs添加单条图文后
	标题为空，摘要为空，正文为空，没有插入一张图片
	添加失败

	Given jobs登录系统
	When jobs已编辑单条图文
		"""
		[{
			"title":null,
			"cover": null,
			"cover_in_the_text":"ture",
			"summary":null,
			"content":null
		}]
		"""
	 
	Then jobs添加单条图文失败	