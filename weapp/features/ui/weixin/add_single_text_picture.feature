#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
Feature: 需求1290新建单条图文 jobs在系统中新建单条图文

@ui @senior @textPicture 
Scenario: 1 添加单条图文(js相关验证)
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
			"cover_in_the_text":"true",
			"summary_length":121,
			"content_length":20001
		}]
		"""

	Then jobs添加单条图文失败
@ui @senior @textPicture
Scenario: 2 添加单条图文(js相关验证)
	Jobs添加单条图文后
	标题为空，摘要为空，正文为空，没有插入一张图片
	添加失败

	Given jobs登录系统
	When jobs已添加单条图文
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
