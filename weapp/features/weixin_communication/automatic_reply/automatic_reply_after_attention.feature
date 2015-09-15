# __author__ : "王丽"

Feature: 微信用户关注后系统自动回复
"""
	1.微信用户关注公众账号后，系统自动回复
		1）非系统会员，关注公众账号后，自动回复
		2）系统会员，取消关注之后，重新关注，自动回复
"""

Background:
	
	Given jobs登录系统

	When jobs已添加多图文
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

@mall2 @message @automaticReply 
Scenario: 1 关注后自动回复,文本类型
	When jobs添加关注自动回复规则
		"""
		[{
			"reply_content":"关注后自动回复内容1",
			"reply_type":"text"
		}]
		"""
	When bill关注jobs的公众号
	Then bill收到自动回复'关注后自动回复内容1'

@mall2 @message @automaticReply 
Scenario: 2 关注后自动回复,图文类型；会员关注后，获得自动回复，取消关注，再关注，仍然可以获得自动回复
	When jobs添加关注自动回复规则
		"""
		[{ 
			"reply_type":"text_picture",
			 "reply_content":"图文1"
		}]
		"""
	When bill关注jobs的公众号
	Then bill收到自动回复'图文1'
	
	When bill取消关注jobs的公众号
	When bill关注jobs的公众号
	Then bill收到自动回复'图文1'

