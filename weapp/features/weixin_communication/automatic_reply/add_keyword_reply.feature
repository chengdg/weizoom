# __author__ : "王丽"

Feature: 添加关键词自动回复

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
		},{
			"title":"图文2",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"cover_in_the_text":"false",
			"summary":"单条图文2文本摘要",
			"content":"单条图文2文本内容"
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
			"jump_url":"www.baidu.com",
			"summary":"单条图文4文本摘要",
			"content":"单条图文4文本内容"
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
				"url": "/standard_static/test_resource_img/hangzhou4.jpg"
				}],
			"cover_in_the_text":"false",
			"summary":"sub单条图文3文本摘要",
			"content":"sub单条图文3文本内容",
			"jump_url":"www.baidu.com"
		}]
		"""

@message @automaticReply @senior @textPicture @mall2 
Scenario: 1 正常添加关键词自动回复
	Jobs正常添加关键词自动回复 ，能获取他关键词自动回复

	Given jobs登录系统
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": [{
					"keyword": "关键字1",
					"type": "equal"
				},{
					 "keyword": "关键字2",
					 "type": "like"
				},{
					 "keyword": "关键字3",
					 "type": "like"
				}],
			"keyword_reply": [{
					 "reply_content":"关键字回复内容1",
					 "reply_type":"text"
				},{
					 "reply_content":"图文1",
					 "reply_type":"text_picture"
				},{
					 "reply_content":"关键字回复内容3",
					 "reply_type":"text"
				}]
		},{
			"rules_name":"规则2",
			"keyword": [{
					"keyword": "关键字21",
					"type": "equal"
					},{
					 "keyword": "关键字22",
					 "type": "like"
				}],
			"keyword_reply": [{
				 	"reply_type":"text_picture",
				 	"reply_content":"图文4"
				 	},{
					 "reply_content":"图文2",
					 "reply_type":"text_picture"
				}]
		}]
		"""

	Then jobs获得关键词自动回复列表
		"""
		[{
			"rules_name":"规则2",
			"keyword": [{
					"keyword": "关键字21",
					"type": "equal"
				},{
					"keyword": "关键字22",
					"type": "like"
				}],
			"keyword_reply": [{
				 "reply_type":"text_picture",
				 "reply_content":"图文4"
				 },{
					"reply_content":"图文2",
					"reply_type":"text_picture"
				}]
		},{
			"rules_name":"规则1",
			"keyword": [{
					"keyword": "关键字1",
					"type": "equal"
				},{
					"keyword": "关键字2",
					"type": "like"
				},{
					"keyword": "关键字3",
					"type": "like"
				}],
			"keyword_reply": [{
					"reply_content":"关键字回复内容1",
					"reply_type":"text"
				},{
					"reply_content":"图文1",
					"reply_type":"text_picture"
				},{
					"reply_content":"关键字回复内容3",
					"reply_type":"text"
				}]
		}]
		"""

	Given bill登录系统
	Then bill获得关键词自动回复列表
		"""
		[]
		"""

@message @automaticReply @senior @textPicture @mall2
Scenario: 2 发送关键词，可以获得正确的回复
	
	Given jobs登录系统
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": [{
					"keyword": "关键字1",
					"type": "equal"
				},{
					 "keyword": "关键字2",
					 "type": "like"
				},{
					 "keyword": "关键字3",
					 "type": "like"
				}],
			"keyword_reply": [{
					 "reply_content":"关键字回复内容1",
					 "reply_type":"text"
				}]
		},{
			"rules_name":"规则2",
			"keyword": [{
					"keyword": "关键字21",
					"type": "equal"
				},{
					 "keyword": "关键22",
					 "type": "like"
				}],
			"keyword_reply": [{
				 "reply_type":"text_picture",
				 "reply_content":"图文4"
				 }]
		}]
		"""
	When 清空浏览器
	When bill关注jobs的公众号
	When bill在微信中向jobs的公众号发送消息'关键字1'
	Then bill收到自动回复'关键字回复内容1'

	When bill在微信中向jobs的公众号发送消息'关键22模糊匹配'
	Then bill收到自动回复'图文4'

	When bill在微信中向jobs的公众号发送消息'关键字21精确匹配'
	Then bill收到自动回复' '
