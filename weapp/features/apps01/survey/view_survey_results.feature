#_author_:张三香 2015.11.13

Feature:用户调研-查看结果
	"""
	1、查看结果页面查询条件：
		【用户名】：支持模糊查询
		【调研时间】：按照用户参加调研的时间进行查询，开始时间和结束时间允许为空
	2、查看结果列表，按照调研时间倒序排列，每页最多显示10条数据

	"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建用户调研活动
		"""
		[{
			"title":"用户调研01",
			"sub_title":"所有模块",
			"content":"欢迎参加调研",
			"start_date":"5天前",
			"end_date":"2天后",
			"authority":"无需关注即可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"answer":
				{
					"title":"问答题",
					"is_required":"是"
				},
			"choose":
				[{
					"title":"选择题1",
					"single_or_multiple":"单选",
					"is_required":"是",
					"option":[{
							"options":"1"
						},{
							"options":"2"
						},{
							"options":"3"
					}]
				}],
			"quick":
				{
					"name":"false",
					"phone":"true",
					"email":"true",
					"item":[{
						"name":"填写项1",
						"is_required":"是"
					},{
						"name":"填写项2",
						"is_required":"否"
					}]
				},
			"upload_pic":
				{
					"title":"上传图片",
					"is_required":"是"
				}
		}]
		"""

	When bill关注jobs的公众号
	When tom关注jobs的公众号
	When tom1关注jobs的公众号
	When tom2关注jobs的公众号
	When tom2取消关注jobs的公众号

	When 微信用户批量参加jobs的用户调研活动
		| name       | member_name | survey_time | answer        |choose  |    quick                       | upload_pic |
		| 用户调研01 | bill        |2天前        |bill问答题内容 | 1      |bill,15111223344,1234@qq.com,11 | 1.jpg      |
		| 用户调研01 | tom         |昨天         |tom 问答题内容 | 2      |tom, 15211223344,2234@qq.com,22 | 2.jpg      |
		| 用户调研01 | tom1        |今天         |tom1问答题内容 | 1      |tom1,153211223344,3234@qq.com,33| 3.jpg      |
		| 用户调研01 | tom2        |今天         |tom2问答题内容 | 3      |tom2,15411223344,4234@qq.com,44 | 4.jpg      |

@apps @survey
Scenario:1 查看结果列表
	Given jobs登录系统
	Then jobs获得用户调研活动列表
		"""
		[{
			"name":"用户调研01",
			"parti_person_cnt":4,
			"prize_type":"优惠券",
			"start_date":"5天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions":["关闭","预览","统计","查看结果"]
		}]
		"""
	When jobs查看用户调研活动'用户调研01'
	Then jobs获得用户调研活动'用户调研01'的结果列表
		| member_name | survey_time |
		| tom2        |今天         |
		| tom1        |今天         |
		| tom         |昨天         |
		| bill        |2天前        |

@apps @survey
Scenario:2 查看结果列表查询
	Given jobs登录系统
	When jobs查看用户调研活动'用户调研01'
	Then jobs获得用户调研活动'用户调研01'的结果列表
		| member_name | survey_time |
		| tom2        |今天         |
		| tom1        |今天         |
		| tom         |昨天         |
		| bill        |2天前        |
	#空查询（默认查询）
		When jobs设置用户调研活动结果列表查询条件
			"""
			[]
			"""
		Then jobs获得用户调研活动'用户调研01'的结果列表
			| member_name | survey_time |
			| tom2        |今天         |
			| tom1        |今天         |
			| tom         |昨天         |
			| bill        |2天前        |

	#用户名查询
		#查询结果为空
			When jobs设置用户调研活动结果列表查询条件
				"""
				{
					"member_name":"abc"
				}
				"""
			Then jobs获得用户调研活动'用户调研01'的结果列表
				"""
				[]
				"""
		#模糊匹配
			When jobs设置用户调研活动结果列表查询条件
				"""
				{
					"member_name":"tom"
				}
				"""
			Then jobs获得用户调研活动'用户调研01'的结果列表
				| member_name | survey_time |
				| tom2        |今天         |
				| tom1        |今天         |
				| tom         |昨天         |
		#精确匹配
			When jobs设置用户调研活动结果列表查询条件
				"""
				{
					"member_name":"bill"
				}
				"""
			Then jobs获得用户调研活动'用户调研01'的结果列表
				| member_name | survey_time |
				| bill        |2天前        |

	#调研时间查询
		#查询结果为空
			When jobs设置用户调研活动结果列表查询条件
				"""
				{
					"survey_start_time":"3天前",
					"survey_end_time":"2天前"
				}
				"""
			Then jobs获得用户调研活动'用户调研01'的结果列表
				"""
				[]
				"""
		#开始时间非空，结束时间为空
			When jobs设置用户调研活动结果列表查询条件
				"""
				{
					"survey_start_time":"今天",
					"survey_end_time":""
				}
				"""
			Then jobs获得用户调研活动'用户调研01'的结果列表
				| member_name | survey_time |
				| tom2        |今天         |
				| tom1        |今天         |
		#开始时间为空，结束时间非空
			When jobs设置用户调研活动结果列表查询条件
				"""
				{
					"survey_start_time":"",
					"survey_end_time":"昨天"
				}
				"""
			Then jobs获得用户调研活动'用户调研01'的结果列表
				| member_name | survey_time |
				| tom         |昨天         |
				| bill        |2天前        |
		#开始时间和结束时间相等
			When jobs设置用户调研活动结果列表查询条件
				"""
				{
					"survey_start_time":"昨天",
					"survey_end_time":"昨天"
				}
				"""
			Then jobs获得用户调研活动'用户调研01'的结果列表
				| member_name | survey_time |
				| tom         |昨天         |

	#组合条件查询
		When jobs设置用户调研活动结果列表查询条件
			"""
			{
				"member_name":"bill",
				"survey_start_time":"3天前",
				"survey_end_time":"今天"
			}
			"""
		Then jobs获得用户调研活动'用户调研01'的结果列表
			| member_name | survey_time |
			| bill        |2天前        |

@apps @survey
Scenario:3 查看结果列表分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""
	When jobs查看用户调研活动'用户调研01'
	#Then jobs获得用户调研活动'用户调研01'的结果列表共'4'页

	When jobs访问微信抽奖活动'微信抽奖01'的结果列表第'1'页
	Then jobs获得用户调研活动'用户调研01'的结果列表
		| member_name | survey_time |
		| tom2        |今天         |

	When jobs访问微信抽奖活动'微信抽奖01'的结果列表下一页
	Then jobs获得用户调研活动'用户调研01'的结果列表
		| member_name | survey_time |
		| tom1        |今天         |

	When jobs访问微信抽奖活动'微信抽奖01'的结果列表'4'页
	Then jobs获得用户调研活动'用户调研01'的结果列表
		| member_name | survey_time |
		| bill        |2天前        |

	When jobs访问微信抽奖活动'微信抽奖01'的结果列表上一页
	Then jobs获得用户调研活动'用户调研01'的结果列表
		| member_name | survey_time |
		| tom         |昨天         |

@apps @survey
Scenario:4 访问用户的查看结果
	Given jobs登录系统
	When jobs查看用户调研活动'用户调研01'
	Then jobs获得用户调研活动'用户调研01'的结果列表
		| member_name | survey_time |
		| tom2        |今天         |
		| tom1        |今天         |
		| tom         |昨天         |
		| bill        |2天前        |
	When jobs访问用户'bill'的查看结果
	Then jobs获得用户'bill'的查看结果
		"""
		{
			"bill填写的内容":
				[{
					"问答题":"bill问答题内容"
				},{
					"选择题":"1"
				},{
					"姓名":"bill"
				},{
					"手机":"15111223344"
				},{
					"邮箱":"1234@qq.com"
				},{
					"填写项1":"11"
				},{
					"填写项2":""
				},{
					"上传图片":"1.jpg"
				}]
		}
		"""