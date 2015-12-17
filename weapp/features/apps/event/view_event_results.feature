#_author_:王丽 2015.12.03

Feature:活动报名-查看结果
	"""
	1、查看结果页面查询条件：
		【用户名】：会员昵称模糊查询
		【活动时间】：按照用户参加活动报名时间进行查询，开始时间和结束时间允许为空
	2、查看结果列表，按照报名时间倒序排列，每页最多显示10条数据
		【用户名】:会员的昵称和头像，非会员的显示为空
		【报名时间】：参与活动报名的时间，精确到时间
		【信息】：参与活动报名填写的信息项
	3、批量导出
		导出参与活动报名的结果
		填写项分单列导出
	"""

Background:
	Given jobs登录系统
	When jobs新建活动报名
		"""
		[{
			"title":"活动报名-无奖励",
			"subtitle":"活动报名-副标题-无奖励",
			"content":"内容描述-无奖励",
			"start_date":"5天前",
			"end_date":"2天后",
			"permission":"无需关注即可参与",
			"prize_type": "无奖励",
			"items_select":[{
						"item_name":"姓名",
						"is_selected":"true"
					},{
						"item_name":"手机",
						"is_selected":"true"
					},{
						"item_name":"邮箱",
						"is_selected":"true"
					},{
						"item_name":"QQ号",
						"is_selected":"true"
					},{
						"item_name":"职位",
						"is_selected":"false"
					},{
						"item_name":"住址",
						"is_selected":"false"
					}],
			"items_add":[{
						"item_name":"其他",
						"is_required":"false"
					}]
		}]
		"""

	#会员
		Given bill关注jobs的公众号
		When bill访问jobs的webapp

		Given tom关注jobs的公众号
		When tom访问jobs的webapp
		When tom取消关注jobs的公众号

	#无需关注即可参与
		#会员参与
			When 清空浏览器
			When bill参加活动报名'活动报名-无奖励'于'4天前'
				"""
				{
					"姓名":"bill",
					"手机":"15213265987",
					"邮箱":"123456@qq.com",
					"QQ号":"12345",
					"其他":""
				}
				"""
			Then bill获得提示"提交成功"
		#取消关注的会员参与
			When 清空浏览器
			When tom参加活动报名'活动报名-无奖励'于'3天前'
				"""
				{
					"姓名":"tom",
					"手机":"15213265987",
					"邮箱":"123456@qq.com",
					"QQ号":"12345",
					"其他":"其他"
				}
				"""
			Then tom获得提示"提交成功"
		#非会员参与
			When 清空浏览器
			When lily关注jobs的公众号
			When lily访问jobs的webapp
			When lily取消关注jobs的公众号
			When lily参加活动报名'活动报名-无奖励'于'2天前'
				"""
				{
					"姓名":"lily",
					"手机":"15213265987",
					"邮箱":"123456@qq.com",
					"QQ号":"12345",
					"其他":"其他"
				}
				"""
			Then lily获得提示"提交成功"
		#同以会员第二次参与同一活动报名
			When 清空浏览器
			When bill参加活动报名'活动报名-无奖励'于'4天前'
				"""
				{}
				"""
			Then bill获得提示"您已报名"

@mall2 @apps_event @apps_event_backend @view_event_results
Scenario:1 活动参与结果列表-查询
	Given jobs登录系统

	#默认条件查询
		When jobs查看活动报名'活动报名-无奖励'
		When jobs设置活动报名结果列表查询条件
			"""
			{
				"name":"",
				"start_date":"",
				"end_date":""
			}
			"""
		Then jobs获得活动报名'活动报名-无奖励'结果列表
			"""
			[{
				"name":"lily",
				"date":"2天前",
				"info":{
						"姓名":"lily",
						"手机":"15213265987",
						"邮箱":"123456@qq.com",
						"QQ号":"12345",
						"其他":"其他"
					}
			},{
				"name":"tom",
				"date":"3天前",
				"info":{
						"姓名":"tom",
						"手机":"15213265987",
						"邮箱":"123456@qq.com",
						"QQ号":"12345",
						"其他":"其他"
					}
			},{
				"name":"bill",
				"date":"4天前",
				"info":{
						"姓名":"bill",
						"手机":"15213265987",
						"邮箱":"123456@qq.com",
						"QQ号":"12345",
						"其他":""
					}
			}]
			"""

	#按"用户名"查询
		#模糊匹配
		When jobs设置活动报名结果列表查询条件
			"""
			{
				"name":"o",
				"start_date":"",
				"end_date":""
			}
			"""
		Then jobs获得活动报名'活动报名-无奖励'结果列表
			"""
			[{
				"name":"tom",
				"date":"3天前",
				"info":{
						"姓名":"tom",
						"手机":"15213265987",
						"邮箱":"123456@qq.com",
						"QQ号":"12345",
						"其他":"其他"
					}
			}]
			"""

		#完全匹配
		When jobs设置活动报名结果列表查询条件
			"""
			{
				"name":"bill",
				"start_date":"",
				"end_date":""
			}
			"""
		Then jobs获得活动报名'活动报名-无奖励'结果列表
			"""
			[{
				"name":"bill",
				"date":"4天前",
				"info":{
						"姓名":"bill",
						"手机":"15213265987",
						"邮箱":"123456@qq.com",
						"QQ号":"12345",
						"其他":""
					}
			}]
			"""
		#查询结果为空 这个有问题，待验证
		When jobs设置活动报名结果列表查询条件
			"""
			{
				"name":"v",
				"start_date":"",
				"end_date":""
			}
			"""
		Then jobs获得活动报名'活动报名-无奖励'结果列表
			"""
			[]
			"""

	#按"报名时间"查询
		#开始时间不为空，结束时间为空，查询开始时间之后所有的
			When jobs设置活动报名结果列表查询条件
				"""
				{
					"name":"",
					"start_date":"3天前",
					"end_date":""
				}
				"""
			Then jobs获得活动报名'活动报名-无奖励'结果列表
				"""
				[{
					"name":"lily",
					"date":"2天前",
					"info":{
							"姓名":"lily",
							"手机":"15213265987",
							"邮箱":"123456@qq.com",
							"QQ号":"12345",
							"其他":"其他"
						}
				},{
					"name":"tom",
					"date":"3天前",
					"info":{
							"姓名":"tom",
							"手机":"15213265987",
							"邮箱":"123456@qq.com",
							"QQ号":"12345",
							"其他":"其他"
						}
				}]
				"""
		#开始时间为空，结束时间不为空，查询结束时间之前所有的
			When jobs设置活动报名结果列表查询条件
				"""
				{
					"name":"",
					"start_date":"",
					"end_date":"3天前"
				}
				"""
			Then jobs获得活动报名'活动报名-无奖励'结果列表
				"""
				[{
					"name":"bill",
					"date":"4天前",
					"info":{
							"姓名":"bill",
							"手机":"15213265987",
							"邮箱":"123456@qq.com",
							"QQ号":"12345",
							"其他":""
						}
				}]
				"""
		#开始时间不为空，结束时间不为空，查询查询时间区间内的数据
			When jobs设置活动报名结果列表查询条件
				"""
				{
					"name":"",
					"start_date":"3天前",
					"end_date":"2天前"
				}
				"""
			Then jobs获得活动报名'活动报名-无奖励'结果列表
				"""
				[{
					"name":"tom",
					"date":"3天前",
					"info":{
							"姓名":"tom",
							"手机":"15213265987",
							"邮箱":"123456@qq.com",
							"QQ号":"12345",
							"其他":"其他"
						}
				}]
				"""
		#查询结果为空
			When jobs设置活动报名结果列表查询条件
				"""
				{
					"name":"",
					"start_date":"6天前",
					"end_date":"5天前"
				}
				"""
			Then jobs获得活动报名'活动报名-无奖励'结果列表
				"""
				[]
				"""

	#混合查询
		When jobs设置活动报名结果列表查询条件
			"""
			{
				"name":"i",
				"start_date":"4天前",
				"end_date":"3天前"
			}
			"""
		Then jobs获得活动报名'活动报名-无奖励'结果列表
			"""
			[{
				"name":"bill",
				"date":"4天前",
				"info":{
						"姓名":"bill",
						"手机":"15213265987",
						"邮箱":"123456@qq.com",
						"QQ号":"12345",
						"其他":""
					}
			}]
			"""

@mall2 @apps_event @apps_event_backend @view_event_results
Scenario:2 活动参与结果列表-分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""
	When jobs访问活动报名'活动报名-无奖励'的结果列表第'1'页

	Then jobs获得活动报名'活动报名-无奖励'结果列表
		"""
		[{
			"name":"lily",
			"date":"2天前",
			"info":{
					"姓名":"lily",
					"手机":"15213265987",
					"邮箱":"123456@qq.com",
					"QQ号":"12345",
					"其他":"其他"
				}
		}]
		"""
	When jobs访问活动报名'活动报名-无奖励'的结果列表下一页
	Then jobs获得活动报名'活动报名-无奖励'结果列表
		"""
		[{
			"name":"tom",
			"date":"3天前",
			"info":{
					"姓名":"tom",
					"手机":"15213265987",
					"邮箱":"123456@qq.com",
					"QQ号":"12345",
					"其他":"其他"
				}
		}]
		"""
	When jobs访问活动报名'活动报名-无奖励'的结果列表第'3'页
	Then jobs获得活动报名'活动报名-无奖励'结果列表
		"""
		[{
			"name":"bill",
			"date":"4天前",
			"info":{
					"姓名":"bill",
					"手机":"15213265987",
					"邮箱":"123456@qq.com",
					"QQ号":"12345",
					"其他":""
				}
		}]
		"""
	When jobs访问活动报名'活动报名-无奖励'的结果列表上一页
	Then jobs获得活动报名'活动报名-无奖励'结果列表
		"""
		[{
			"name":"tom",
			"date":"3天前",
			"info":{
					"姓名":"tom",
					"手机":"15213265987",
					"邮箱":"123456@qq.com",
					"QQ号":"12345",
					"其他":"其他"
				}
		}]
		"""


