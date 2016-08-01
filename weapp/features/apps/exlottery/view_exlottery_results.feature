#_author_:许韦 2016.08.01

Feature:专项抽奖-查看结果

	"""
	1、查看结果页面查询条件：
		【用户名】：支持模糊查询
		【抽奖时间】：按照用户抽奖的时间进行查询，开始时间和结束时间允许为空
		【奖品类型】：下拉框显示，包括全部、积分、优惠券、实物和未中奖，默认显示'全部'，
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
			"limit_counts": "无限",
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"share_intro":"百事专项抽奖活动",
			"desc":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"start_date":"2天前",
			"end_date":"2天后",
			"win_rate":"100%",
			"lottory_code_num":5,
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":1000
			},{
				"prize_grade":"二等奖",
				"prize_counts":0,
				"prize_type":"优惠券",
				"coupon":"优惠券1"
			},{
				"prize_grade":"三等奖",
				"prize_counts":0,
				"prize_type":"实物",
				"gift":"精美礼品"
			}]
		}]
		"""
	When bill关注jobs的公众号于'2015-10-01'
	When tom关注jobs的公众号于'2015-10-05'

	When 微信用户批量参加jobs的专项抽奖活动
		| name    |member_name|mobile      | prize_grade | prize_name |lottery_time| receive_status |
		|专项抽奖 |bill       |13758899565 | 一等奖      | 1000积分   |今天        | 已领取         |
		|专项抽奖 |bill       |13758899565 | 一等奖      | 1000积分   |昨天        | 已领取         |
		|专项抽奖 |tom        |13773373502 | 一等奖      | 1000积分   |昨天        | 已领取         |
		
		

@mall2 @apps @apps_egg @view_exlottery_results
Scenario:1 查看结果列表
	Given jobs登录系统
	Then jobs获得专项抽奖活动列表
	"""
		[{
			"name":"专项抽奖",
			"participant_count":3
		}]
	"""
	When jobs查看专项抽奖活动'专项抽奖'
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		|member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|bill       |13758899565  | 一等奖       | 1000积分     |今天        | 已领取      |       |
		|bill       |13758899565  | 一等奖       | 1000积分     |昨天        | 已领取      |       |
		|tom        |13773373502  | 一等奖       | 1000积分     |昨天        | 已领取      |       |
		
@mall2 @apps @apps_egg @view_exlottery_results
Scenario:2 查看结果列表查询
	Given jobs登录系统
	When jobs查看专项抽奖活动'专项抽奖'
	#空查询（默认查询）
	When jobs设置专项抽奖活动结果列表查询条件
		"""
		{}
		"""
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		|member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|bill       |13758899565  | 一等奖       | 1000积分     |今天        | 已领取      |       |
		|bill       |13758899565  | 一等奖       | 1000积分     |昨天        | 已领取      |       |
		|tom        |13773373502  | 一等奖       | 1000积分     |昨天        | 已领取      |       |

	#用户名查询
		#查询结果为空
	When jobs设置专项抽奖活动结果列表查询条件
		"""
		{
			"member_name":"abc"
		}
		"""
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		"""
		[]
		"""

		#模糊匹配
	When jobs设置专项抽奖活动结果列表查询条件
		"""
		{
			"member_name":"t"
		}
		"""
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
	    |member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|tom        |13773373502  | 一等奖       | 1000积分     |昨天        | 已领取      |       |

		#精确匹配
	When jobs设置专项抽奖活动结果列表查询条件
		"""
		{
			"member_name":"bill"
		}
		"""
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		|member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|bill       |13758899565  | 一等奖       | 1000积分     |今天        | 已领取      |       |
		|bill       |13758899565  | 一等奖       | 1000积分     |昨天        | 已领取      |       |

	#抽奖时间查询
		#查询结果为空
	When jobs设置专项抽奖活动结果列表查询条件
		"""
		{
			"lottery_start_time":"5天前",
			"lottery_end_time":"3天前"
		}
		"""
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		"""
		[]
		"""

		#开始时间为空，结束时间非空
	When jobs设置专项抽奖活动结果列表查询条件
		"""
		{
			"lottery_start_time":"",
			"lottery_end_time":"昨天"
		}
		"""
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		|member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|bill       |13758899565  | 一等奖       | 1000积分     |昨天        | 已领取      |       |
		|tom        |13773373502  | 一等奖       | 1000积分     |昨天        | 已领取      |       |

		#开始时间非空，结束时间为空
	When jobs设置专项抽奖活动结果列表查询条件
		"""
		{
			"lottery_start_time":"昨天",
			"lottery_end_time":""
		}
		"""
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		|member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|bill       |13758899565  | 一等奖       | 1000积分     |今天        | 已领取      |       |
		|bill       |13758899565  | 一等奖       | 1000积分     |昨天        | 已领取      |       |
		|tom        |13773373502  | 一等奖       | 1000积分     |昨天        | 已领取      |       |

		#开始时间和结束时间非空
	When jobs设置专项抽奖活动结果列表查询条件
		"""
		{
			"lottery_start_time":"昨天",
			"lottery_end_time":"今天"
		}
		"""
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		|member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|bill       |13758899565  | 一等奖       | 1000积分     |今天        | 已领取      |       |
		|bill       |13758899565  | 一等奖       | 1000积分     |昨天        | 已领取      |       |
		|tom        |13773373502  | 一等奖       | 1000积分     |昨天        | 已领取      |       |

		#开始时间和结束时间相等
	When jobs设置专项抽奖活动结果列表查询条件
		"""
		{
			"lottery_start_time":"今天",
			"lottery_end_time":"今天"
		}
		"""
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		|member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|bill       |13758899565  | 一等奖       | 1000积分     |今天        | 已领取      |       |

	#奖品类型查询
	When jobs设置专项抽奖活动结果列表查询条件
		"""
		{
			"prize_type":"优惠券"
		}
		"""
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		"""
		[]
		"""
	When jobs设置专项抽奖活动结果列表查询条件
		"""
		{
			"prize_type":"未中奖"
		}
		"""
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		"""
		[]
		"""

	#领取状态查询
	When jobs设置专项抽奖活动结果列表查询条件
		"""
		{
			"receive_status":"已领取"
		}
		"""
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		|member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|bill       |13758899565  | 一等奖       | 1000积分     |今天        | 已领取      |       |
		|bill       |13758899565  | 一等奖       | 1000积分     |昨天        | 已领取      |       |
		|tom        |13773373502  | 一等奖       | 1000积分     |昨天        | 已领取      |       |


	#组合条件查询
	When jobs设置专项抽奖活动结果列表查询条件
		"""
		{
			"member_name":"bill",
			"lottery_start_time":"3天前",
			"lottery_end_time":"今天",
			"prize_type":"积分",
			"receive_status":"已领取"
		}
		"""
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		|member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|bill       |13758899565  | 一等奖       | 1000积分     |今天        | 已领取      |       |
		|bill       |13758899565  | 一等奖       | 1000积分     |昨天        | 已领取      |       |

@mall2 @apps @apps_egg @view_exlottery_results
Scenario:3 查看结果列表分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""
	When jobs查看专项抽奖活动'专项抽奖'
	#Then jobs获得专项抽奖活动'专项抽奖'的结果列表共'3'页

	When jobs访问专项抽奖活动'专项抽奖'的结果列表第'1'页
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		|member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|bill       |13758899565  | 一等奖       | 1000积分     |今天        | 已领取      |       |

	When jobs访问专项抽奖活动'专项抽奖'的结果列表下一页
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		|member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|bill       |13758899565  | 一等奖       | 1000积分     |昨天        | 已领取      |       |

	When jobs访问专项抽奖活动'专项抽奖'的结果列表第'3'页
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		|member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|tom        |13773373502  | 一等奖       | 1000积分     |昨天        | 已领取      |       |

	When jobs访问专项抽奖活动'专项抽奖'的结果列表上一页
	Then jobs获得专项抽奖活动'专项抽奖'的结果列表
		|member_name|mobile       | prize_grade | prize_name |lottery_time| receive_status |actions|
		|bill       |13758899565  | 一等奖       | 1000积分     |昨天        | 已领取      |       |