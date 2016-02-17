#watcher:zhangsanxiang@weizoom.com,benchi@weizoom.com
#_author_：张三香

Feature:积分应用活动的查询
	Jobs能对积分应用活动列表进行查询

Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		},{
			"name": "分类2"
		},{
			"name": "分类3"
		},{
			"name": "分类4"
		}]
		"""
	When jobs已添加商品
		|   name    |  bar_code      |        category      | shelve_type  |
		|   商品1   |            |    分类1             |   上架       |
		|   商品2   |  1234561   |    分类1,分类2       |   上架       |
		|   商品3   |  1234562   |    分类1,分类2,分类3 |   上架       |
		|   商品4   |  1234563   |    分类2             |   上架       |
		|   商品5   |  1234564   |                      |   上架       |
		#|   商品6   |  1234562   |                      |   上架       |
	When jobs创建积分应用活动
		|    name    |  product_name   |   status  |  start_date  |   end_date  | is_permanant_active  | created_at |
		|积分应用1   | 商品1    |   已结束  |  2015-05-10  |2015-05-25   |      false           | 2015-05-10  |
		|积分应用2   | 商品2    |   已结束  |  2015-06-10  |2015-08-10   |      false           | 2015-06-10  |
		|积分应用3   | 商品3    |   进行中  |  2015-07-10  |明天          |      false           | 2015-07-10  |
		|积分应用4   | 商品4    |   已结束  |  2015-08-01  |2015-08-05   |      false           | 2015-08-01  |
		|积分应用5   | 商品5    |   进行中  |              |             |      true            | 昨天        |
		|积分应用6   | 商品2    |   未开始  |  明天        |3天后        |      false           | 今天        |

@mall2 @promotionIntegral @integral
Scenario: 积分应用活动列表查询
	#空查询（默认查询）
		When jobs设置查询条件
			"""
			{
				"product_name":"",
				"bar_code":"",
				"status":"全部",
				"start_date":"",
				"end_date":""
			}
			"""
		Then jobs获取积分应用活动列表
			|    name    |product_name|bar_code|   status  |  start_date  |   end_date  | is_permanant_active  | created_at |
			|积分应用6   | 商品2 |1234561    |   未开始  |  明天        |3天后        |      false           | 今天        |
			|积分应用5   | 商品5 |1234564    |   进行中  |             |            |      true            | 昨天        |
			|积分应用4   | 商品4 |1234563    |   已结束  |  2015-08-01  |2015-08-05   |      false           | 2015-08-01  |
			|积分应用3   | 商品3 |1234562    |   进行中  |  2015-07-10  |明天          |      false           | 2015-07-10  |
			|积分应用2   | 商品2 |1234561    |   已结束  |  2015-06-10  |2015-08-10   |      false           | 2015-06-10  |
			|积分应用1   | 商品1 |          |   已结束  |  2015-05-10  |2015-05-25   |      false           | 2015-05-10  |
	#商品名称
		#完全匹配
			When jobs设置查询条件
				"""
				{
					"product_name":"商品2",
					"bar_code":"",
					"status":"全部",
					"start_date":"",
					"end_date":""
				}
				"""
			Then jobs获取积分应用活动列表
				|    name    |  product_name|bar_code|   status  |  start_date  |   end_date  | is_permanant_active  | created_at |
				|积分应用6   | 商品2 |1234561    |   未开始  |  明天        |3天后        |      false           | 今天        |
				|积分应用2   | 商品2 |1234561    |   已结束  |  2015-06-10  |2015-08-10   |      false           | 2015-06-10  |

		#部分匹配
			When jobs设置查询条件
				"""
				{
					"product_name":"商品",
					"bar_code":"",
					"status":"全部",
					"start_date":"",
					"end_date":""
				}
				"""
			Then jobs获取积分应用活动列表
				|    name    |  product_name|bar_code     |   status  |  start_date  |   end_date  | is_permanant_active  | created_at |
				|积分应用6   | 商品2 |1234561    |   未开始  |  明天        |3天后        |      false           | 今天        |
				|积分应用5   | 商品5 |1234564    |   进行中  |              |             |      true            | 昨天        |
				|积分应用4   | 商品4 |1234563    |   已结束  |  2015-08-01  |2015-08-05   |      false           | 2015-08-01  |
				|积分应用3   | 商品3 |1234562    |   进行中  |  2015-07-10  |明天         |      false           | 2015-07-10  |
				|积分应用2   | 商品2 |1234561    |   已结束  |  2015-06-10  |2015-08-10   |      false           | 2015-06-10  |
				|积分应用1   | 商品1 |           |   已结束  |  2015-05-10  |2015-05-25   |      false           | 2015-05-10  |

		#查询结果为空
			When jobs设置查询条件
				"""
				{
					"product_name":"商 品",
					"bar_code":"",
					"status":"全部",
					"start_date":"",
					"end_date":""
				}
				"""
			Then jobs获取积分应用活动列表
				|    name    |  product_name|bar_code     |   status  |  start_date  |   end_date  | is_permanant_active  | created_at |

	#商品条码
		#完全匹配
			When jobs设置查询条件
				"""
				{
					"product_name":"",
					"bar_code":"1234564",
					"status":"全部",
					"start_date":"",
					"end_date":""
				}
				"""
			Then jobs获取积分应用活动列表
				|    name    |  product_name|bar_code     |   status  |  start_date  |   end_date  | is_permanant_active  | created_at |
				|积分应用5   | 商品5 |1234564    |   进行中  |              |             |      true            | 昨天        |

		#查询结果为空
			When jobs设置查询条件
				"""
				{
					"product_name":"",
					"bar_code":"1234",
					"status":"全部",
					"start_date":"",
					"end_date":""
				}
				"""
			Then jobs获取积分应用活动列表
				|    name    |  product_name|bar_code     |   status  |  start_date  |   end_date  | is_permanant_active  | created_at |

	#活动时间
		#查询条件校验
		#	When jobs设置查询条件
		#		"""
		#		{
		#			"product_name":"",
		#			"bar_code":"",
		#			"status":"全部",
		#			"start_date":"2015-05-10",
		#			"end_date":""
		#		}
		#		"""
		#	Then jobs获得系统提示"请输入结束日期"

		#	When jobs设置查询条件
		#		"""
		#		{
		#			"product_name":"",
		#			"bar_code":"",
		#			"status":"全部",
		#			"start_date":"",
		#			"end_date":"2015-08-10"
		#		}
		#		"""
		#	Then jobs获得系统提示"请输入开始日期"

		#查询活动时间
			When jobs设置查询条件
				"""
				{
					"product_name":"",
					"bar_code":"",
					"status":"全部",
					"start_date":"2015-05-01",
					"end_date":"2015-06-11"
				}
				"""
			Then jobs获取积分应用活动列表
				|    name    |  product_name|bar_code     |   status  |  start_date  |   end_date  | is_permanant_active  | created_at |
				|积分应用1   | 商品1 |           |   已结束  |  2015-05-10  |2015-05-25   |      false           | 2015-05-10  |

			When jobs设置查询条件
				"""
				{
					"product_name":"",
					"bar_code":"",
					"status":"全部",
					"start_date":"2015-06-10",
					"end_date":"明天"
				}
				"""
			Then jobs获取积分应用活动列表
				|    name    |  product_name|bar_code     |   status  |  start_date  |   end_date  | is_permanant_active  | created_at |
				|积分应用4   | 商品4 |1234563    |   已结束  |  2015-08-01  |2015-08-05   |      false           | 2015-08-01  |
				|积分应用3   | 商品3 |1234562    |   进行中  |  2015-07-10  |明天         |      false           | 2015-07-10  |
				|积分应用2   | 商品2 |1234561    |   已结束  |  2015-06-10  |2015-08-10   |      false           | 2015-06-10  |
				#|积分应用6   | 商品2 |1234561    |   未开始  |  明天        |3天后        |      false           | 今天        |
				#|积分应用5   | 商品5 |1234564    |   进行中  |              |             |      true            | 昨天        |
				
		#查询结果为空
			When jobs设置查询条件
				"""
				{
					"product_name":"",
					"bar_code":"",
					"status":"全部",
					"start_date":"2015-06-12",
					"end_date":"2015-08-11"
				}
				"""
			Then jobs获取积分应用活动列表
				|    name    |  product_name|bar_code     |   status  |  start_date  |   end_date  | is_permanant_active  | created_at |
				|积分应用4   | 商品4 |1234563    |   已结束  |  2015-08-01  |2015-08-05   |      false           | 2015-08-01  |

	#促销状态
			When jobs设置查询条件
				"""
				{
					"product_name":"",
					"bar_code":"",
					"status":"进行中",
					"start_date":"",
					"end_date":""
				}
				"""
			Then jobs获取积分应用活动列表
				|    name    |  product_name|bar_code     |   status  |  start_date  |   end_date  | is_permanant_active  | created_at |
				|积分应用5   | 商品5 |1234564    |   进行中  |              |             |      true            | 昨天        |
				|积分应用3   | 商品3 |1234562    |   进行中  |  2015-07-10  |明天         |      false           | 2015-07-10  |

	#组合查询
			When jobs设置查询条件
				"""
				{
					"product_name":"商品4",
					"bar_code":"1234563",
					"status":"全部",
					"start_date":"2015-08-01",
					"end_date":"2015-08-05"
				}
				"""
			Then jobs获取积分应用活动列表
				|    name    |  product_name|bar_code     |   status  |  start_date  |   end_date  | is_permanant_active  | created_at |
				|积分应用4   | 商品4 |1234563    |   已结束  |  2015-08-01  |2015-08-05   |      false           | 2015-08-01  |
