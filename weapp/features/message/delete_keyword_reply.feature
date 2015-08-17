Feature: 删除关键词自动回复 bc
	jobs能删除 图文消息

Background:
	Given jobs登录系统
	And jobs已添加单条图文
		"""
		[{
			"rules_name":"规则1",
			"add_time":"2015-01-01 18:26:39",
			"keyword": [{
				"keyword_name": "关键字1",
				"match": "equal"
			}],
			"keyword_reply": [{
				 "reply_content":"关键字回复内容1",
				 "reply_type":"text"
			},{
				 "reply_content":"关键字回复内容111",
				 "reply_type":"text"
			}]
		},{
			"rules_name":"规则2",
			"add_time":"2015-01-02 18:26:39",
			"keyword": [{
				"keyword_name": "关键字21",
				"match": "equal"
			},{
				 "keyword_name": "关键字22",
				 "match": "like"
			}],
			"keyword_reply": [{
				 "reply_type":"text_picture",
				 "reply_content":[{
						"title":"图文1",
						"cover": [{
								"url": "/standard_static/test_resource_img/hangzhou1.jpg"
							}],
						"cover_in_the_text":"ture",
						"summary":"单条图文1文本摘要",
						"content":"单条图文1文本内容"
						}]
				 
			}]
		},{
			"rules_name":"规则3",
			"add_time":"2015-01-03 18:26:39",
			"keyword": [{
				"keyword_name": "关键字31",
				"match": "equal"
			}],
			"keyword_reply": [{
				 "reply_content":"关键字回复内容31",
				 "reply_type":"text"
			}]
		}]
		"""
	

Scenario: 1 删除单个关键字或删除单个回复
	至少要保留一个关键字，或一个关键字回复，否则无法成功
	
	When jobs已删除'关键词'_'关键字21'
	Then jobs获得'关键词自动回复'列表
		"""
		[{
			"rules_name":"规则3",
			"keyword_name": "关键字1",
			"match": "equal",
			"reply_content":"关键字回复内容1"
		}, {
			"rules_name":"规则2",
			"keyword_name": "关键字22",
			"match": "like",
			"reply_content":[{
						"title":"图文1",
						"cover": [{
								"url": "/standard_static/test_resource_img/hangzhou1.jpg"
							}],
						"cover_in_the_text":"ture",
						"summary":"单条图文1文本摘要",
						"content":"单条图文1文本内容"
						}]
		},{
			"rules_name":"规则1",
			"keyword_name": "关键字1",
			"match": "equal",
			"reply_content":"关键字回复内容1",
			"reply_content":"关键字回复内容111"
		}]
		"""
	When jobs已删除'自动回复'_'关键字回复内容111'
	Then jobs获得'关键词自动回复'列表
		"""
		[{
			"rules_name":"规则3",
			"keyword_name": "关键字1",
			"match": "equal",
			"reply_content":"关键字回复内容1"
		}, {
			"rules_name":"规则2",
			"keyword_name": "关键字22",
			"match": "like",
			"reply_content":[{
						"title":"图文1",
						"cover": [{
								"url": "/standard_static/test_resource_img/hangzhou1.jpg"
							}],
						"cover_in_the_text":"ture",
						"summary":"单条图文1文本摘要",
						"content":"单条图文1文本内容"
						}]
		},{
			"rules_name":"规则1",
			"keyword_name": "关键字1",
			"match": "equal",
			"reply_content":"关键字回复内容1",
		}]
		"""
	When jobs去删除'关键字1'
	Then jobs删除失败
	
	When jobs去删除'关键字回复内容1'
	Then jobs删除失败	

Scenario: 2 删除整条规则
	
	When jobs已删除'规则2'
	Then jobs获得'关键词自动回复'列表
		"""
		[{
			"rules_name":"规则3",
			"keyword_name": "关键字1",
			"match": "equal",
			"reply_content":"关键字回复内容1"
		},{
			"rules_name":"规则1",
			"keyword_name": "关键字1",
			"match": "equal",
			"reply_content":"关键字回复内容1",
			"reply_content":"关键字回复内容111"
		}]
		"""
	