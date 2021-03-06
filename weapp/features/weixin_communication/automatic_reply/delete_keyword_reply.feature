# __author__ : "王丽"

Feature: 删除关键词自动回复 bc
	jobs能删除 图文消息

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
			"title":"图文4",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"jump_url":"www.baidu.com",
			"content":"单条图文4文本内容"
		},{
			"title":"sub图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
				}],
			"cover_in_the_text":"true",
			"content":"sub单条图文1文本内容"
		},{
			"title":"sub图文2",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
			"cover_in_the_text":"false",
			"content":"sub单条图文2文本内容"
		},{
			"title":"sub图文3",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou4.jpg"
				}],
			"cover_in_the_text":"false",
			"content":"sub单条图文3文本内容",
			"jump_url":"www.baidu.com"
		}]
		"""

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
				 }]
		}]
		"""
	
@mall2 @message @automaticReply @senior @textPicture
Scenario: 1 删除单个关键字或删除单个回复
	至少要保留一个关键字，或一个关键字回复，否则无法成功
	
	#删除关键词自动回复规则中的关键词
	Given jobs登录系统
	When jobs编辑关键词自动回复规则'规则2'
		"""
		{
			"rules_name":"规则2",
			"keyword": [{
					"keyword": "关键字22",
					"type": "like"
				}],
			"keyword_reply": [{
				 "reply_type":"text_picture",
				 "reply_content":"图文4"
				 }]
		}
		"""
	Then jobs获得关键词自动回复列表
		"""
		[{
			"rules_name":"规则2",
			"keyword": [{
					"keyword": "关键字22",
					"type": "like"
				}],
			"keyword_reply": [{
					"reply_type":"text_picture",
					"reply_content":"图文4"
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

	#删除关键词自动回复规则中的回复内容	
	When jobs编辑关键词自动回复规则'规则1'
		"""
		{
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
					"reply_content":"关键字回复内容3",
					"reply_type":"text"
				}]
		}
		"""
	#When jobs删除回复内容'图文1'
	Then jobs获得关键词自动回复列表
		"""
		[{
			"rules_name":"规则2",
			"keyword": [{
					 "keyword": "关键字22",
					 "type": "like"
				}],
			"keyword_reply": [{
				"reply_type":"text_picture",
				"reply_content":"图文4"
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
					"reply_content":"关键字回复内容3",
					"reply_type":"text"
				}]
		}]
		"""
	
	#删除关键词自动回复规则中的唯一关键词，删除失败
	When jobs编辑关键词自动回复规则'规则2'
		"""
		{
			"rules_name":"规则2",
			"keyword": [{
					 "keyword": "",
					 "type": "like"
				}],
			"keyword_reply": [{
				"reply_type":"text_picture",
				"reply_content":"图文4"
				}]
		}
		"""
	Then jobs获得关键词自动回复列表
		"""
		[{
			"rules_name":"规则2",
			"keyword": [{
					 "keyword": "关键字22",
					 "type": "like"
				}],
			"keyword_reply": [{
				"reply_type":"text_picture",
				"reply_content":"图文4"
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
					"reply_content":"关键字回复内容3",
					"reply_type":"text"
				}]
		}]
		"""
	
	#删除关键词自动回复规则中的唯一回复内容，删除失败
	When jobs编辑关键词自动回复规则'规则2'
		"""
		{
			"rules_name":"规则2",
			"keyword": [{
					 "keyword": "关键字22",
					 "type": "like"
				}],
			"keyword_reply": [{
				"reply_type":"text_picture",
				"reply_content":""
				}]
		}
		"""	
	Then jobs获得关键词自动回复列表
		"""
		[{
			"rules_name":"规则2",
			"keyword": [{
					 "keyword": "关键字22",
					 "type": "like"
				}],
			"keyword_reply": [{
				"reply_type":"text_picture",
				"reply_content":"图文4"
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
					"reply_content":"关键字回复内容3",
					"reply_type":"text"
				}]
		}]
		"""

@mall2 @message @automaticReply @senior @textPicture
Scenario: 2 删除整条规则
	
	When jobs删除关键词自动回复规则'规则1'
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
				 }]
		}]
		"""
	