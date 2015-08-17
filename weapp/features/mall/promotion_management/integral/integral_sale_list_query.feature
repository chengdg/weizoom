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
	When jobs批量添加商品
		|   name    |  code      |        category      |   status  |
		|   商品1   |            |    分类1             |   上架    |
		|   商品2   |  1234561   |    分类1,分类2       |   上架    |
		|   商品3   |  1234562   |    分类1,分类2,分类3 |   上架    |
		|   商品2   |  1234562   |                      |   上架    |
		|   商品4   |  1234563   |    分类2             |   上架    |
		|   商品5   |  1234564   |                      |   上架    |
	When jobs批量创建积分应用活动
		|    name    |  products        |   status  |  start_date  |   end_date  | is_permanant_active  | create_time |
		|积分应用6   | 商品2,1234561    |   未开始  |  明天        |3天后        |      false           | 今天        |
		|积分应用5   | 商品5,1234564    |   进行中  |              |             |      true            | 昨天        |
		|积分应用4   | 商品4,1234563    |   已结束  |  2015-08-01  |2015-08-05   |      false           | 2015-08-01  |
		|积分应用3   | 商品3,1234562    |   进行中  |  2015-07-10  |今天         |      false           | 2015-07-10  |
		|积分应用2   | 商品2,1234561    |   已结束  |  2015-06-10  |2015-08-10   |      false           | 2015-06-10  |
		|积分应用1   | 商品1            |   已结束  |  2015-05-10  |2015-07-25   |      false           | 2015-05-10  |

@promotionIntegral @integral
Scenario: 积分应用活动列表查询
	#空查询（默认查询）
		When jobs设置查询条件
			"""
			[{
				"pro_name":"",
				"pro_code":"",
				"status":"全部",
				"start_date":"",
				"end_date":""
			}]
			"""
		Then jobs获取积分应用活动列表
			|    name    |  products        |   status  |  start_date  |   end_date  | is_permanant_active  | create_time |
			|积分应用6   | 商品2,1234561    |   未开始  |  明天        |3天后        |      false           | 今天        |
			|积分应用5   | 商品5,1234564    |   进行中  |              |             |      true            | 昨天        |
			|积分应用4   | 商品4,1234563    |   已结束  |  2015-08-01  |2015-08-05   |      false           | 2015-08-01  |
			|积分应用3   | 商品3,1234562    |   进行中  |  2015-07-10  |今天         |      false           | 2015-07-10  |
			|积分应用2   | 商品2,1234561    |   已结束  |  2015-06-10  |2015-08-10   |      false           | 2015-06-10  |
			|积分应用1   | 商品1            |   已结束  |  2015-05-10  |2015-05-25   |      false           | 2015-05-10  |
	#商品名称
		#完全匹配
			When jobs设置查询条件
				"""
				[{
					"pro_name":"商品2",
					"pro_code":"",
					"status":"全部",
					"start_date":"",
					"end_date":""
				}]
				"""
			Then jobs获取积分应用活动列表
				|    name    |  products        |   status  |  start_date  |   end_date  | is_permanant_active  | create_time |
				|积分应用6   | 商品2,1234561    |   未开始  |  明天        |3天后        |      false           | 今天        |
				|积分应用2   | 商品2,1234561    |   已结束  |  2015-06-10  |2015-08-10   |      false           | 2015-06-10  |

		#部分匹配
			When jobs设置查询条件
				"""
				[{
					"pro_name":"商品",
					"pro_code":"",
					"status":"全部",
					"start_date":"",
					"end_date":""
				}]
				"""
			Then jobs获取积分应用活动列表
				|    name    |  products        |   status  |  start_date  |   end_date  | is_permanant_active  | create_time |
				|积分应用6   | 商品2,1234561    |   未开始  |  明天        |3天后        |      false           | 今天        |
				|积分应用5   | 商品5,1234564    |   进行中  |              |             |      true            | 昨天        |
				|积分应用4   | 商品4,1234563    |   已结束  |  2015-08-01  |2015-08-05   |      false           | 2015-08-01  |
				|积分应用3   | 商品3,1234562    |   进行中  |  2015-07-10  |今天         |      false           | 2015-07-10  |
				|积分应用2   | 商品2,1234561    |   已结束  |  2015-06-10  |2015-08-10   |      false           | 2015-06-10  |
				|积分应用1   | 商品1            |   已结束  |  2015-05-10  |2015-07-25   |      false           | 2015-05-10  |

		#查询结果为空
			When jobs设置查询条件
				"""
				[{
					"pro_name":"商 品",
					"pro_code":"",
					"status":"全部",
					"start_date":"",
					"end_date":""
				}]
				"""
			Then jobs获取积分应用活动列表
				|    name    |  products        |   status  |  start_date  |   end_date  | is_permanant_active  | create_time |

	#商品条码
		#完全匹配
			When jobs设置查询条件
				"""
				[{
					"pro_name":"",
					"pro_code":"1234564",
					"status":"全部",
					"start_date":"",
					"end_date":""
				}]
				"""
			Then jobs获取积分应用活动列表
				|    name    |  products        |   status  |  start_date  |   end_date  | is_permanant_active  | create_time |
				|积分应用5   | 商品5,1234564    |   进行中  |              |             |      true            | 昨天        |

		#查询结果为空
			When jobs设置查询条件
				"""
				[{
					"pro_name":"",
					"pro_code":"1234",
					"status":"全部",
					"start_date":"",
					"end_date":""
				}]
				"""
			Then jobs获取积分应用活动列表
				|    name    |  products        |   status  |  start_date  |   end_date  | is_permanant_active  | create_time |

	#活动时间
		#查询条件校验
			When jobs设置查询条件
				"""
				[{
					"pro_name":"",
					"pro_code":"",
					"status":"全部",
					"start_date":"2015-05-10",
					"end_date":""
				}]
				"""
			Then jobs获得系统提示"请输入结束日期"

			When jobs设置查询条件
				"""
				[{
					"pro_name":"",
					"pro_code":"",
					"status":"全部",
					"start_date":"",
					"end_date":"2015-08-10"
				}]
				"""
			Then jobs获得系统提示"请输入开始日期"

		#查询活动时间
			When jobs设置查询条件
				"""
				[{
					"pro_name":"",
					"pro_code":"",
					"status":"全部",
					"start_date":"2015-05-01",
					"end_date":"2015-06-11"
				}]
				"""
			Then jobs获取积分应用活动列表
				|    name    |  products        |   status  |  start_date  |   end_date  | is_permanant_active  | create_time |
				|积分应用1   | 商品1            |   已结束  |  2015-05-10  |2015-05-25   |      false           | 2015-05-10  |

			When jobs设置查询条件
				"""
				[{
					"pro_name":"",
					"pro_code":"",
					"status":"全部",
					"start_date":"2015-06-10",
					"end_date":"今天"
				}]
				"""
			Then jobs获取积分应用活动列表
				|    name    |  products        |   status  |  start_date  |   end_date  | is_permanant_active  | create_time |
				|积分应用6   | 商品2,1234561    |   未开始  |  明天        |3天后        |      false           | 今天        |
				|积分应用5   | 商品5,1234564    |   进行中  |              |             |      true            | 昨天        |
				|积分应用4   | 商品4,1234563    |   已结束  |  2015-08-01  |2015-08-05   |      false           | 2015-08-01  |
				|积分应用3   | 商品3,1234562    |   进行中  |  2015-07-10  |今天         |      false           | 2015-07-10  |
				|积分应用2   | 商品2,1234561    |   已结束  |  2015-06-10  |2015-08-10   |      false           | 2015-06-10  |

		#查询结果为空
			When jobs设置查询条件
				"""
				[{
					"pro_name":"",
					"pro_code":"",
					"status":"全部",
					"start_date":"2015-06-12",
					"end_date":"2015-08-11"
				}]
				"""
			Then jobs获取积分应用活动列表
				|    name    |  products        |   status  |  start_date  |   end_date  | is_permanant_active  | create_time |

	#促销状态
			When jobs设置查询条件
				"""
				[{
					"pro_name":"",
					"pro_code":"",
					"status":"进行中",
					"start_date":"",
					"end_date":""
				}]
				"""
			Then jobs获取积分应用活动列表
				|    name    |  products        |   status  |  start_date  |   end_date  | is_permanant_active  | create_time |
				|积分应用5   | 商品5,1234564    |   进行中  |              |             |      true            | 昨天        |
				|积分应用3   | 商品3,1234562    |   进行中  |  2015-07-10  |今天         |      false           | 2015-07-10  |

	#组合查询
			When jobs设置查询条件
				"""
				[{
					"pro_name":"商品4",
					"pro_code":"1234563",
					"status":"全部",
					"start_date":"2015-08-01",
					"end_date":"2015-08-05"
				}]
				"""
			Then jobs获取积分应用活动列表
				|    name    |  products        |   status  |  start_date  |   end_date  | is_permanant_active  | create_time |
				|积分应用4   | 商品4,1234563    |   已结束  |  2015-08-01  |2015-08-05   |      false           | 2015-08-01  |
