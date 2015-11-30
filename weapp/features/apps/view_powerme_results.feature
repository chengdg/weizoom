#_author_:张三香 2015.11.25

Feature:查看微助力活动
	"""
		1.分页：每页展示10条数据

		2.排序：按照助力值由高到低排序，相同助力值，按照参与时间正序排序

		3.批量导出：导出所有参与活动人员信息，按照排名先后导出，即列表展示规则

		4.查询条件：用户名和参与时间,用户名支持模糊查询

	"""

Background:
	Given jobs登录系统
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		},{
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}]
		"""
	When jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1"
		}
		"""
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码1",
			"create_time": "2015-10-10 10:20:30",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "分组1",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "感谢您的的参与，为好友助力成功！"
		}]
		"""
	When jobs新建微助力活动
		"""
		[{
			"name":"微助力活动1",
			"start_date":"3天前",
			"end_date":"10天后",
			"is_show_countdown":"true",
			"desc":"微助力活动描述1",
			"reply":"微助力1",
			"qr_code":"带参数二维码1",
			"share_pic":"1.jpg",
			"background_pic":"2.jpg",
			"background_color":"冬日暖阳",
			"rules":"获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式"
		},{
			"name":"微助力活动2",
			"start_date":"今天",
			"end_date":"3天后",
			"is_show_countdown":"false",
			"desc":"微助力活动描述2",
			"reply":"微助力2",
			"qr_code":"",
			"share_pic":"3.jpg",
			"background_pic":"4.jpg",
			"background_color":"热带橙色",
			"rules":"按上按上打算四大的撒的撒<br />撒打算的撒的撒大声地<br />按上打算打算<br />阿萨德按上打"
		}]
		"""
	When jobs已添加单图文
		"""
		[{
			"title":"微助力1单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容",
			"jump_url":"微助力-微助力活动1"
		},{
			"title":"微助力2单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文2文本摘要",
			"content":"单条图文2文本内容",
			"jump_url":"微助力-微助力活动2"
		}]
		"""
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": [{
					"keyword": "微助力1",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"微助力1单图文",
					"reply_type":"text_picture"
				}]
		},{
			"rules_name":"规则2",
			"keyword": [{
					"keyword": "微助力2",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"微助力2单图文",
					"reply_type":"text_picture"
				}]
		}]
		"""

	When bill关注jobs的公众号
	And tom关注jobs的公众号
	And tom1关注jobs的公众号
	And tom2关注jobs的公众号

	When 微信用户批量参加jobs的微助力活动
		| member_name | powerme_value | parti_time |  name      |
		| tom1        |     4         | 3天前      | 微助力活动1 |
		| bill        |     10        | 昨天       | 微助力活动1 |
		| tom         |     8         | 今天       | 微助力活动1 |
		| tom2        |     4         | 今天       | 微助力活动1 |
		| bill        |     2         | 今天       | 微助力活动2 |

@apps @apps_powerme @apps_powerme_backend @view_powerme_results @kuki1
Scenario:1 查看结果
	Given jobs登录系统
	When jobs查看微助力活动'微助力活动1'
	Then jobs获得微助力活动'微助力活动1'的结果列表
		| rank | member_name | powerme_value | parti_time |
		|  1   | bill        |     10        | 昨天       |
		|  2   | tom         |     8         | 今天       |
		|  3   | tom1        |     4         | 3天前      |
		|  4   | tom2        |     4         | 今天       |

@apps @apps_powerme @apps_powerme_backend @view_powerme_results
Scenario:2 查看结果页面的查询
	Given jobs登录系统
	When jobs查看微助力活动'微助力活动1'
	When jobs设置微助力活动结果列表查询条件
		"""
		{}
		"""
	Then jobs获得微助力活动'微助力活动1'的结果列表
		| rank | member_name | powerme_value | parti_time |
		|  1   | bill        |     10        | 昨天       |
		|  2   | tom         |     8         | 今天       |
		|  3   | tom1        |     4         | 3天前      |
		|  4   | tom2        |     4         | 今天       |
	#用户名查询
		#精确匹配
			When jobs设置微助力活动结果列表查询条件
				"""
				{
					"member_name":"bill"
				}
				"""
			Then jobs获得微助力活动'微助力活动1'的结果列表
				| rank | member_name | powerme_value | parti_time |
				|  1   | bill        |     10        | 昨天       |
		#模糊查询
			When jobs设置微助力活动结果列表查询条件
				"""
				{
					"member_name":"tom"
				}
				"""
			Then jobs获得微助力活动'微助力活动1'的结果列表
				| rank | member_name | powerme_value | parti_time |
				|  1   | tom         |     8         | 今天       |
				|  2   | tom1        |     4         | 3天前      |
				|  3   | tom2        |     4         | 今天       |

	#参与时间查询
		#开始时间非空，结束时间为空
			When jobs设置微助力活动结果列表查询条件
				"""
				{
					"parti_start_time":"昨天",
					"parti_end_time":""
				}
				"""
			Then jobs获得微助力活动'微助力活动1'的结果列表
				| rank | member_name | powerme_value | parti_time |
				|  1   | bill        |     10        | 昨天       |
				|  2   | tom         |     8         | 今天       |
				|  3   | tom1        |     4         | 3天前      |
				|  4   | tom2        |     4         | 今天       |

		#开始时间为空，结束时间非空
			When jobs设置微助力活动结果列表查询条件
				"""
				{
					"parti_start_time":"",
					"parti_start_time":"今天"
				}
				"""
			Then jobs获得微助力活动'微助力活动1'的结果列表
				| rank | member_name | powerme_value | parti_time |
				|  1   | bill        |     10        | 昨天       |
				|  2   | tom         |     8         | 今天       |
				|  3   | tom1        |     4         | 3天前      |
				|  4   | tom2        |     4         | 今天       |

		#开始时间和结束时间相等
			When jobs设置微助力活动结果列表查询条件
				"""
				{
					"parti_start_time":"今天",
					"parti_end_time":"今天"
				}
				"""
			Then jobs获得微助力活动'微助力活动1'的结果列表
				| rank | member_name | powerme_value | parti_time |
				|  1   | tom         |     8         | 今天       |
				|  2   | tom2        |     4         | 今天       |

		#开始时间和结束时间不相等
			When jobs设置微助力活动结果列表查询条件
				"""
				{
					"parti_start_time":"3天前",
					"parti_start_time":"昨天"
				}
				"""
			Then jobs获得微助力活动'微助力活动1'的结果列表
				| rank | member_name | powerme_value | parti_time |
				|  1   | bill        |     10        | 昨天       |
				|  2   | tom1        |     4         | 今天      |

	#组合条件查询
		When jobs设置微助力活动结果列表查询条件
			"""
			{
				"member_name":"tom2"
				"parti_start_time":"昨天",
				"parti_start_time":"今天"
			}
			"""
		Then jobs获得微助力活动'微助力活动1'的结果列表
				| rank | member_name | powerme_value | parti_time |
				|  1   | tom2        |     4         | 今天       |

@apps @apps_powerme @apps_powerme_backend @view_powerme_results
Scenario:3 查看结果页面的批量导出
	Given jobs登录系统
	When jobs查看微助力活动'微助力活动1'
	When jobs批量导出微助力活动'微助力活动1'的结果
	Then jobs获得微助力活动'微助力活动1'的批量导出结果信息
		| rank | member_name | powerme_value | parti_time |
		|  1   | bill        |     10        | 昨天       |
		|  2   | tom         |     8         | 今天       |
		|  3   | tom1        |     4         | 3天前      |
		|  4   | tom2        |     4         | 今天       |