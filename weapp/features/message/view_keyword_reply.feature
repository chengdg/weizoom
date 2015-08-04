Feature:  浏览 查询 关键词自动回复 bc
	jobs能 浏览 查询关键词自动回复

Background:
	Given jobs登录系统
	And jobs已添加关键词自动回复
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
				"keyword_name": "关键字1",
				"match": "equal"
			}],
			"keyword_reply": [{
				 "reply_content":"关键字回复内容1",
				 "reply_type":"text"
			}]
		}]
		"""
	
	
	and jobs已分页设置
		"""
		[{
			"page_count":2
			
		}]
		"""

Scenario: 1 浏览关键词自动回复 
	1. jobs能看到按创建时间倒叙排列的列表信息
	2. jobs能分页查看列表信息
	
	When jobs浏览'关键词自动回复'
	Then jobs获得'关键词自动回复'列表
		"""
		[{
			"rules_name":"规则3",
			"keyword_name": "关键字1",
			"match": "equal",
			"reply_content":"关键字回复内容1"
		}, {
			"rules_name":"规则2",
			"keyword_name": "关键字21",
			"match": "equal",
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
		}]
		"""
	When jobs浏览'下一页'
	Then jobs获得'关键词自动回复'列表
		"""
		[{
			"rules_name":"规则1",
			"keyword_name": "关键字1",
			"match": "equal",
			"reply_content":"关键字回复内容1"
		}]
		"""
	When jobs浏览'上一页'
	Then jobs获得'关键词自动回复'列表
		"""
		[{
			"rules_name":"规则3",
			"keyword_name": "关键字1",
			"match": "equal",
			"reply_content":"关键字回复内容1"
		}, {
			"rules_name":"规则2",
			"keyword_name": "关键字21",
			"match": "equal",
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
		}]
		"""
Scenario: 2 浏览关键词自动回复 按关键词搜索结果
	
	
	When jobs搜索'关键字1'
	Then jobs获得'关键词自动回复'列表
		"""
		[ {
			"rules_name":"规则3",
			"keyword_name": "关键字1",
			"match": "equal",
			"reply_content":"关键字回复内容1"
		}, {
			"rules_name":"规则1",
			"keyword_name": "关键字1",
			"match": "equal",
			"reply_content":"关键字回复内容1"
		}]
		"""
	When jobs搜索'关键字2'
	Then jobs获得'图文管理'列表
		"""
		[ {
			"rules_name":"规则2",
			"keyword_name": "关键字21",
			"match": "equal",
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
		}]
		"""