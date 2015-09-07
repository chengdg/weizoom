Feature: 需求1290新建单条图文 jobs在系统中新建单条图文

@mall2 @senior @textPicture @wll
Scenario: 1 添加单条图文
	Jobs添加单条图文后，能获取他添加单条图文
	标题30字以内，摘要120字以内，正文2万字以内，插入一张图片

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
		}]
		"""

	Then jobs能获取图文'图文1'
		"""
		{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容"
		}
		"""
	And jobs能获取图文'图文2'
		"""
		{
			"title":"图文2",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"cover_in_the_text":"false",
			"summary":"单条图文2文本摘要",
			"content":"单条图文2文本内容"
		}
		"""

	And jobs能获取图文'图文3'
		"""
		{
			"title":"图文3",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"cover_in_the_text":"false",
			"summary":"单条图文3文本摘要",
			"content":"单条图文3文本内容",
			"jump_url":"www.baidu.com"
		}
		"""
	Given bill登录系统
	Then bill能获取图文管理列表
		"""
		[]
		"""
@ignore
Scenario: 2 添加单条图文(js相关验证)
	Jobs添加单条图文后
	标题超出30字以内，摘要超出120字以内，正文超出2万字以内，插入一张图片
	添加失败

	Given jobs登录系统
	When jobs已添加单条图文
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
@ignore
Scenario: 3 添加单条图文(js相关验证)
	Jobs添加单条图文后
	标题为空，摘要为空，正文为空，没有插入一张图片
	添加失败

	Given jobs登录系统
	When jobs已添加单条图文
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
