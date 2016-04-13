#_author_:许韦 2016.04.13

Feature: 用户查看高级微信投票活动介绍
	"""
		微信用户进入高级投票主页
		微信用户查看"活动介绍"
	"""
Background:
	Given jobs登录系统
	When jobs新建微信高级投票活动
		"""
		[{
			"title":"微信高级投票1",
			"group":[],
			"desc":"高级投票活动介绍",
			"start_date":"2天前",
			"end_date":"2天后",
			"pic":"1.jpg"
		}]
		"""
	When jobs已添加单图文
		"""
		[{
			"title":"高级投票活动1单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"微信高级投票",
			"content":"微信高级投票",
			"jump_url":"微信高级投票"
		}]
		"""
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": 
				[{
					"keyword": "微信高级投票",
					"type": "equal"
				}],
			"keyword_reply": 
				[{
					"reply_content":"微信高级投票",
					"reply_type":"text_picture"
				}]
		
		}]
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微信高级投票'
	Then bill收到自动回复'高级投票活动1单图文'
	When bill点击图文"高级投票活动1单图文"进入高级投票活动页面
	Then bill能获得微信高级投票活动介绍
		"""
		[{
			"title":"微信高级投票1",
			"start_date":"2天前",
			"end_date":"2天后",
			"desc":"高级投票活动介绍",
			"pic":"1.jpg"
		}]
		"""