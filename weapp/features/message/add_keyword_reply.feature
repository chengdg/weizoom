Feature: 添加关键词自动回复

Background:
	Given jobs登录系统
	And jobs已添加单条图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容",
			"add_time":"2015-04-13 15:26:39"
		},{
			"title":"图文2",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"cover_in_the_text":"false",
			"summary":"单条图文2文本摘要",
			"content":"单条图文2文本内容",
			"add_time":"2015-04-13 16:26:39"
		},{
			"title":"图文3",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"cover_in_the_text":"false",
			"summary":"单条图文3文本摘要",
			"jump_url":"www.baidu.com",
			"add_time":"2015-04-13 17:26:39"
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
			#"summary":"单条图文4文本摘要",
			"content":"单条图文4文本内容",
			"sub": [{
				"title":"sub图文1",
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou2.jpg"
					}],
				"cover_in_the_text":"ture",
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
				"jump_url":"www.baidu.com"
			}]
		}]
		"""

Scenario: 1 正常添加关键词自动回复
	Jobs正常添加关键词自动回复 ，能获取他关键词自动回复

	Given jobs登录系统
	When jobs已添加关键词自动回复
		"""
		[{
			"rules_name":"规则1",
			"keyword": [{
				"keyword_name": "关键字1",
				"match": "equal"
			},{
				 "keyword_name": "关键字2",
				 "match": "like"
			},{
				 "keyword_name": "关键字3",
				 "match": "like"
			}],
			"keyword_reply": [{
				 "reply_content":"关键字回复内容1",
				 "reply_type":"text"
			},{
				 "reply_content":"关键字回复内容2",
				 "reply_type":"text"
			},{
				 "reply_content":"关键字回复内容3",
				 "reply_type":"text"
			}]
		},{
			"rules_name":"规则2",
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
		}]
		"""

	Then jobs能获取'规则1'
		"""
		{
			"rules_name":"规则1",
			"keyword": [{
				"keyword_name": "关键字1",
				"match": "equal"
			},{
				 "keyword_name": "关键字2",
				 "match": "like"
			},{
				 "keyword_name": "关键字3",
				 "match": "like"
			}],
			"keyword_reply": [{
				 "reply_content":"关键字回复内容1",
				 "reply_type":"text"
			},{
				 "reply_content":"关键字回复内容2",
				 "reply_type":"text"
			},{
				 "reply_content":"关键字回复内容3",
				 "reply_type":"text"
			}]
		}
		"""
	And jobs能获取'规则2'
		"""
		{
			"rules_name":"规则2",
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
		}
		"""


	And bill能获取关键词自动回复
		"""
		[]
		"""

Scenario: 2 异常添加关键词自动回复
	字数超出限制
	添加失败

