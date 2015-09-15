# __author__ : "王丽"

Feature:  浏览 查询 关键词自动回复 bc
	jobs能 浏览 查询关键词自动回复

Background:
	Given jobs登录系统
	When jobs已添加单图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容"
		}]
		"""
	and jobs已添加多图文
		"""
		[{
			"title":"图文4",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"jump_url":"www.baidu.com",
			"summary":"单条图文4文本摘要",
			"content":"单条图文4文本内容"
		},{
			"title":"sub图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
				}],
			"cover_in_the_text":"ture",
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
		},{
			"rules_name":"规则3",
			"keyword": [{
					"keyword": "关键字4",
					"type": "equal"
				},{
					"keyword": "关键字5",
					"type": "like"
				}],
			"keyword_reply": [{
				 "reply_type":"text_picture",
				 "reply_content":"图文4"
				 }]
		}]
		"""

@message @automaticReply @senior @textPicture
Scenario: 1 浏览关键词自动回复列表，分页
	1. jobs能看到按创建顺序倒叙排列的列表
	2. jobs能分页查看列表信息
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""

	When jobs访问关键词自动回复规则列表
	Then jobs获得关键词自动回复规则列表显示共3页

	When jobs访问关键词自动回复规则列表第1页
	Then jobs获得关键词自动回复列表
		"""
		[{
			"rules_name":"规则3",
			"keyword": [{
					"keyword": "关键字4",
					"type": "equal"
				},{
					"keyword": "关键字5",
					"type": "like"
				}],
			"keyword_reply": [{
				 "reply_type":"text_picture",
				 "reply_content":"图文4"
				 }]
		}]
		"""
	When jobs浏览'下一页'
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
	When jobs浏览'上一页'
	Then jobs获得关键词自动回复列表
		"""
		[{
			"rules_name":"规则3",
			"keyword": [{
					"keyword": "关键字4",
					"type": "equal"
				},{
					"keyword": "关键字5",
					"type": "like"
				}],
			"keyword_reply": [{
				 "reply_type":"text_picture",
				 "reply_content":"图文4"
				 }]
		}]
		"""

@message @automaticReply @senior @textPicture
Scenario: 2 浏览关键词自动回复 按关键词搜索结果

	#空条件查询，查询出所有关键词自动回复规则
	When jobs设置关键词搜索条件
		"""
		{
			"keyword":""
		}
		"""
	Then jobs获得关键词自动回复列表
		"""
		[{
			"rules_name":"规则3",
			"keyword": [{
					"keyword": "关键字4",
					"type": "equal"
				},{
					"keyword": "关键字5",
					"type": "like"
				}],
			"keyword_reply": [{
				 "reply_type":"text_picture",
				 "reply_content":"图文4"
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

	#模糊匹配查询，只要有一个关键词满足条件即可
	When jobs设置关键词搜索条件
		"""
		{
			"keyword":"1"
		}
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


	When jobs设置关键词搜索条件
		"""
		{
			"keyword":"关键字5"
		}
		"""
	Then jobs获得关键词自动回复列表
		"""
		[{
			"rules_name":"规则3",
			"keyword": [{
					"keyword": "关键字4",
					"type": "equal"
				},{
					"keyword": "关键字5",
					"type": "like"
				}],
			"keyword_reply": [{
				 "reply_type":"text_picture",
				 "reply_content":"图文4"
				 }]
		}]
		"""

	#查询结果为空
	When jobs设置关键词搜索条件
		"""
		{
			"keyword":"77"
		}
		"""
	Then jobs获得关键词自动回复列表
		"""
		[]
		"""

