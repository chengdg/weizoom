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
			"subtitle":"所有模块",
			"content":"欢迎参加调研",
			"start_date":"5天前",
			"end_date":"2天后",
			"permission":"无需关注即可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"answer":
				[{
					"title":"问答题",
					"is_required":"是"
				}],
			"choose":
				[{
					"title":"选择题1",
					"type":"单选",
					"is_required":"是",
					"option":[{
							"options":"1"
						},{
							"options":"2"
						},{
							"options":"3"
					}]
				}],
			"participate_info":
				[{
					"items_select":
						[{
							"item_name":"姓名",
							"is_selected":"false"
						},{
							"item_name":"手机",
							"is_selected":"true"
						},{
							"item_name":"邮箱",
							"is_selected":"true"
						},{
							"item_name":"QQ",
							"is_selected":"false"
						},{
							"item_name":"职位",
							"is_selected":"false"
						},{
							"item_name":"住址",
							"is_selected":"false"
						}],
					"item_add":
						[{
							"item_name":"填写项1",
							"is_required":"是"
						},{
							"item_name":"填写项2",
							"is_required":"否"
						}]
				}],
			"upload_pic":
				[{
					"title":"上传图片",
					"is_required":"是"
				}]
		}]
		"""

	When bill关注jobs的公众号
	When tom关注jobs的公众号
	When tom1关注jobs的公众号
	When tom2关注jobs的公众号
	When tom2取消关注jobs的公众号

	When bill参加jobs的用户调研活动"用户调研01"于"2天前"
		"""
		{
			"问答题":
				[{
					"title":"问答题",
					"value":"bill问答题内容"
				}],
			"选择题":
				[{
					"title":"选择题1",
					"value":[{
							"title":"1",
							"type":"单选",
							"isSelect":"是"
						},{
							"title":"2",
							"type":"单选",
							"isSelect":"否"
						},{
							"title":"3",
							"type":"单选",
							"isSelect":"否"
						}]
				}],
			"快捷模块":
				[{
					"value":{
						"姓名":"bill",
						"手机":"15111223344",
						"邮箱":"1234@qq.com",
						"填写项1":"11"
					}
				}],
			"上传图片":
				[{
					"title":"上传图片",
					"value":"1.jpg"
				}]
		}
		"""
	When tom参加jobs的用户调研活动"用户调研01"于"昨天"
		"""
		{
			"问答题":
				[{
					"title":"问答题",
					"value":"tom问答题内容"
				}],
			"选择题":
				[{
					"title":"选择题1",
					"value":[{
							"title":"1",
							"type":"单选",
							"isSelect":"否"
						},{
							"title":"2",
							"type":"单选",
							"isSelect":"是"
						},{
							"title":"3",
							"type":"单选",
							"isSelect":"否"
						}]
				}],
			"快捷模块":
				[{
					"value":{
						"姓名":"tom",
						"手机":"15211223344",
						"邮箱":"2234@qq.com",
						"填写项1":"22"
					}
				}],
			"上传图片":
				[{
					"title":"上传图片",
					"value":"2.jpg"
				}]
		}
		"""
	When tom1参加jobs的用户调研活动"用户调研01"于"今天"
		"""
		{
			"问答题":
				[{
					"title":"问答题",
					"value":"tom1问答题内容"
				}],
			"选择题":
				[{
					"title":"选择题1",
					"value":[{
							"title":"1",
							"type":"单选",
							"isSelect":"是"
						},{
							"title":"2",
							"type":"单选",
							"isSelect":"否"
						},{
							"title":"3",
							"type":"单选",
							"isSelect":"否"
						}]
				}],
			"快捷模块":
				[{
					"value":{
						"姓名":"tom1",
						"手机":"153211223344",
						"邮箱":"3234@qq.com",
						"填写项1":"33"
					}
				}],
			"上传图片":
				[{
					"title":"上传图片",
					"value":"3.jpg"
				}]
		}
		"""
	When tom2参加jobs的用户调研活动"用户调研01"于"今天"
		"""
		{
			"问答题":
				[{
					"title":"问答题",
					"value":"tom2问答题内容"
				}],
			"选择题":
				[{
					"title":"选择题1",
					"value":[{
							"title":"1",
							"type":"单选",
							"isSelect":"否"
						},{
							"title":"2",
							"type":"单选",
							"isSelect":"否"
						},{
							"title":"3",
							"type":"单选",
							"isSelect":"是"
						}]
				}],
			"快捷模块":
				[{
					"value":{
						"姓名":"tom2",
						"手机":"15411223344",
						"邮箱":"4234@qq.com",
						"填写项1":"44"
					}
				}],
			"上传图片":
				[{
					"title":"上传图片",
					"value":"4.jpg"
				}]
		}
		"""

@mall2 @apps @survey @view_survey_results
Scenario:1 查看结果列表
	Given jobs登录系统
	Then jobs获得用户调研活动列表
		"""
		[{
			"name":"用户调研01",
			"participant_count":4,
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

@mall2 @apps @survey
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

@mall2 @apps @survey @view_survey_results
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

@mall2 @apps @survey
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