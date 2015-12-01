#_author_:张三香 2015.12.01

Feature:微信抽奖-查看结果

	"""
	1、查看结果页面查询条件：
		【用户名】：支持模糊查询
		【抽奖时间】：按照用户抽奖的时间进行查询，开始时间和结束时间允许为空
		【奖励类型】：下拉框显示，包括全部、积分、优惠券、实物和未中奖，默认显示'全部'，
		【领取状态】：下拉框显示，包括全部、未领取和已领取，默认显示'全部'
	2、查看结果列表，按照抽奖时间倒序排列，每页最多显示10条数据

	"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 10,
			"limit_counts": "不限",
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖01",
			"start_date":"3天前",
			"end_date":"5天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"不限",
			"win_rate":50%,
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":20,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts"30,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
		"""
	When bill关注jobs的公众号于"2015-10-01"
	When tom关注jobs的公众号于"2015-10-05"
	When tom1关注jobs的公众号
	When tom1取消关注jobs的公众号

	When 微信用户批量参加jobs的微信抽奖活动
		| name      |member_name| prize_grade | prize_name |lottery_time| receive_status |
		|微信抽奖01 |bill       | 一等奖      | 优惠1      |2天前       | 已领取         |
		|微信抽奖01 |bill       | 谢谢参与    | 谢谢参与   |昨天        | 已领取         |
		|微信抽奖01 |tom        | 二等奖      | 100积分    |今天        | 已领取         |
		|微信抽奖01 |bill       | 谢谢参与    | 谢谢参与   |今天        | 已领取         |
		|微信抽奖01 |tom1       | 一等奖      | 优惠1      |今天        | 已领取         |

@apps @lottery
Scenario:1 查看结果列表
	Given jobs登录系统
	Then jobs获得微信抽奖活动列表
		"""
		[{
			"name":"微信抽奖01",
			"part_num":5
		}]
		"""
	When jobs查看微信抽奖活动'微信抽奖01'
	Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
		| name      |member_name|mobile | prize_grade | prize_name |lottery_time| receive_status |actions|
		|微信抽奖01 |bill       |       | 一等奖      | 优惠1      |2天前       | 已领取         |       |
		|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |昨天        | 已领取         |       |
		|微信抽奖01 |tom        |       | 二等奖      | 100积分    |今天        | 已领取         |       |
		|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |今天        | 已领取         |       |
		|微信抽奖01 |tom1       |       | 一等奖      | 优惠1      |今天        | 已领取         |       |

@apps @lottery
Scenario:2 查看结果列表查询
	Given jobs登录系统
	When jobs查看微信抽奖活动'微信抽奖01'
	Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
		| name      |member_name|mobile | prize_grade | prize_name |lottery_time| receive_status |actions|
		|微信抽奖01 |tom1       |       | 一等奖      | 优惠1      |今天        | 已领取         |       |
		|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |今天        | 已领取         |       |
		|微信抽奖01 |tom        |       | 二等奖      | 100积分    |今天        | 已领取         |       |
		|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |昨天        | 已领取         |       |
		|微信抽奖01 |bill       |       | 一等奖      | 优惠1      |2天前       | 已领取         |       |
	#空查询（默认查询）
		When jobs设置微信抽奖活动结果列表查询条件
			"""
			[]
			"""
		Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
			| name      |member_name|mobile | prize_grade | prize_name |lottery_time| receive_status |actions|
			|微信抽奖01 |tom1       |       | 一等奖      | 优惠1      |今天        | 已领取         |       |
			|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |今天        | 已领取         |       |
			|微信抽奖01 |tom        |       | 二等奖      | 100积分    |今天        | 已领取         |       |
			|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |昨天        | 已领取         |       |
			|微信抽奖01 |bill       |       | 一等奖      | 优惠1      |2天前       | 已领取         |       |

	#用户名查询
		#查询结果为空
			When jobs设置微信抽奖活动结果列表查询条件
				"""
				{
					"member_name":"abc"
				}
				"""
			Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
				"""
				[]
				"""

		#模糊匹配
			When jobs设置微信抽奖活动结果列表查询条件
				"""
				{
					"member_name":"tom"
				}
				"""
			Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
				| name      |member_name|mobile | prize_grade | prize_name |lottery_time| receive_status |actions|
				|微信抽奖01 |tom1       |       | 一等奖      | 优惠1      |今天        | 已领取         |       |
				|微信抽奖01 |tom        |       | 二等奖      | 100积分    |今天        | 已领取         |       |

		#精确匹配
			When jobs设置微信抽奖活动结果列表查询条件
				"""
				{
					"member_name":"bill"
				}
				"""
			Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
				| name      |member_name|mobile | prize_grade | prize_name |lottery_time| receive_status |actions|
				|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |今天        | 已领取         |       |
				|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |昨天        | 已领取         |       |
				|微信抽奖01 |bill       |       | 一等奖      | 优惠1      |2天前       | 已领取         |       |

	#抽奖时间查询
		#查询结果为空
			When jobs设置微信抽奖活动结果列表查询条件
				"""
				{
					"start_date":"5天前",
					"end_date":"3天前"
				}
				"""
			Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
				"""
				[]
				"""

		#开始时间为空，结束时间非空
			When jobs设置微信抽奖活动结果列表查询条件
				"""
				{
					"start_date":"",
					"end_date":"昨天"
				}
				"""
			Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
				| name      |member_name|mobile | prize_grade | prize_name |lottery_time| receive_status |actions|
				|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |昨天        | 已领取         |       |
				|微信抽奖01 |bill       |       | 一等奖      | 优惠1      |2天前       | 已领取         |       |

		#开始时间非空，结束时间为空
			When jobs设置微信抽奖活动结果列表查询条件
				"""
				{
					"start_date":"昨天",
					"end_date":""
				}
				"""
			Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
				| name      |member_name|mobile | prize_grade | prize_name |lottery_time| receive_status |actions|
				|微信抽奖01 |tom1       |       | 一等奖      | 优惠1      |今天        | 已领取         |       |
				|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |今天        | 已领取         |       |
				|微信抽奖01 |tom        |       | 二等奖      | 100积分    |今天        | 已领取         |       |
				|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |昨天        | 已领取         |       |

		#开始时间和结束时间非空
			When jobs设置微信抽奖活动结果列表查询条件
				"""
				{
					"start_date":"昨天",
					"end_date":"今天"
				}
				"""
			Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
				| name      |member_name|mobile | prize_grade | prize_name |lottery_time| receive_status |actions|
				|微信抽奖01 |tom1       |       | 一等奖      | 优惠1      |今天        | 已领取         |       |
				|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |今天        | 已领取         |       |
				|微信抽奖01 |tom        |       | 二等奖      | 100积分    |今天        | 已领取         |       |
				|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |昨天        | 已领取         |       |

		#开始时间和结束时间相等
			When jobs设置微信抽奖活动结果列表查询条件
				"""
				{
					"start_date":"今天",
					"end_date":"今天"
				}
				"""
			Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
				| name      |member_name|mobile | prize_grade | prize_name |lottery_time| receive_status |actions|
				|微信抽奖01 |tom1       |       | 一等奖      | 优惠1      |今天        | 已领取         |       |
				|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |今天        | 已领取         |       |
				|微信抽奖01 |tom        |       | 二等奖      | 100积分    |今天        | 已领取         |       |

	#奖品类型查询
		When jobs设置微信抽奖活动结果列表查询条件
			"""
			{
				"prize_type":"优惠券"
			}
			"""
		Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
			| name      |member_name|mobile | prize_grade | prize_name |lottery_time| receive_status |actions|
			|微信抽奖01 |bill       |       | 一等奖      | 优惠1      |2天前       | 已领取         |       |
			|微信抽奖01 |tom1       |       | 一等奖      | 优惠1      |今天        | 已领取         |       |

		When jobs设置微信抽奖活动结果列表查询条件
			"""
			{
				"prize_type":"未中奖"
			}
			"""
		Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
			| name      |member_name|mobile | prize_grade | prize_name |lottery_time| receive_status |actions|
			|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |昨天        | 已领取         |       |
			|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |今天        | 已领取         |       |

	#领取状态查询
		When jobs设置微信抽奖活动结果列表查询条件
			"""
			{
				"receive_status":"已领取"
			}
			"""
		Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
			| name      |member_name|mobile | prize_grade | prize_name |lottery_time| receive_status |actions|
			|微信抽奖01 |tom1       |       | 一等奖      | 优惠1      |今天        | 已领取         |       |
			|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |今天        | 已领取         |       |
			|微信抽奖01 |tom        |       | 二等奖      | 100积分    |今天        | 已领取         |       |
			|微信抽奖01 |bill       |       | 谢谢参与    | 谢谢参与   |昨天        | 已领取         |       |
			|微信抽奖01 |bill       |       | 一等奖      | 优惠1      |2天前       | 已领取         |       |

	#组合条件查询
		When jobs设置微信抽奖活动结果列表查询条件
			"""
			{
				"member_name":"bill",
				"start_date":"3天前",
				"end_date":"今天",
				"prize_type":"优惠券"
				"receive_status":"已领取"
			}
			"""
		Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
			| name      |member_name|mobile | prize_grade | prize_name |lottery_time| receive_status |actions|
			|微信抽奖01 |bill       |       | 一等奖      | 优惠1      |2天前       | 已领取         |       |

@apps @lottery
Scenario:3 查看结果列表分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""
	When jobs查看微信抽奖活动'微信抽奖01'
	#Then jobs获得微信抽奖活动'微信抽奖01'的结果列表共'3'页

	When jobs访问微信抽奖活动'微信抽奖01'的结果列表第'1'页
	Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
		| name      |member_name| prize_grade | prize_name |lottery_time| receive_status |
		|微信抽奖01 |tom1       | 一等奖      | 优惠1      |今天        | 已领取         |
		|微信抽奖01 |bill       | 谢谢参与    | 谢谢参与   |今天        | 已领取         |

	When jobs访问微信抽奖活动'微信抽奖01'的结果列表下一页
	Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
		|微信抽奖01 |tom        | 二等奖      | 100积分    |今天        | 已领取         |
		|微信抽奖01 |bill       | 谢谢参与    | 谢谢参与   |昨天        | 已领取         |

	When jobs访问微信抽奖活动'微信抽奖01'的结果列表第'3'页
	Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
		|微信抽奖01 |bill       | 一等奖      | 优惠1      |2天前       | 已领取         |

	When jobs访问微信抽奖活动'微信抽奖01'的结果列表上一页
	Then jobs获得微信抽奖活动'微信抽奖01'的结果列表
		|微信抽奖01 |tom        | 二等奖      | 100积分    |今天        | 已领取         |
		|微信抽奖01 |bill       | 谢谢参与    | 谢谢参与   |昨天        | 已领取         |

@apps @lottery
Scenario:4 批量导出
	Given jobs登录系统
	When jobs查看微信抽奖活动'微信抽奖01'
	Then jobs能批量导出微信抽奖活动'微信抽奖01'的结果列表

