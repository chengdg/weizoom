#_author_:张三香

Feature: 营销分析中的“营销活动分析”
#jobs登录BI系统可以查看营销活动的名称、负责人、参与次数/人数、活动时间、活动状态和活动分析

Background:
	Given jobs登录系统
	And jobs已添加'微信抽奖'活动配置
		"""
		[{
			"id": 0,
			"name":"微信抽奖01",
			"award_type": 0,
			"participate_num":0,
			"start_at": "2015-06-15",
			"end_at": "2025-06-30",
			"award_hour": 0,
			"daily_play_count": 1,
			"detail": "<p>测试2<br/></p>",
			"expend_integral": 0,
			"no_prize_odd": 0,
			"not_win_desc": "谢谢参与",
			"prize_count|1": 1,
			"prize_name|1": "一等奖",
			"prize_odds|1": 100,
			"prize_source|1": 0,
			"prize_type|1": 1,
			"type": 0
		 },{
			"id": 0,
			"name":"微信抽奖02",
			"award_type": 0,
			"participate_num":0,
			"start_at": "2015-06-15",
			"end_at": "2025-06-17",
			"award_hour": 0,
			"daily_play_count": 1,
			"detail": "<p>测试2<br/></p>",
			"expend_integral": 0,
			"no_prize_odd": 0,
			"not_win_desc": "谢谢参与",
			"prize_count|1": 1,
			"prize_name|1": "一等奖",
			"prize_odds|1": 100,
			"prize_source|1": 0,
			"prize_type|1": 1,
			"type": 0
		 }]
		 """

	And jobs已添加'渠道扫码'营销活动
		"""
		[{
			"setting_id": 0,
			"name": "渠道扫码03",
			"prize_info": "{\"id\":-1, \"name\": \"non-prize\", \"type\": \"积分\"}",
			"reply_type": 0,
			"reply_material_id": 0,
			"re_old_member": 0,
			"grade_id": 16,
			"remark": "备注1"
		}, {
			"setting_id": 0,
			"name": "渠道扫码02",
			"prize_info": "{\"id\":-1, \"name\": \"non-prize\", \"type\": \"积分\"}",
			"reply_type": 0,
			"reply_material_id": 0,
			"re_old_member": 0,
			"grade_id": 16,
			"remark": "备注2"
		}, {
			"setting_id": 0,
			"name": "渠道扫码01",
			"prize_info": "{\"id\":-1, \"name\": \"non-prize\", \"type\": \"积分\"}",
			"reply_type": 0,
			"reply_material_id": 0,
			"re_old_member": 0,
			"grade_id": 16,
			"remark": "备注3"
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号
	And mary关注jobs的公众号
	And jim关注jobs的公众号
	And kate关注jobs的公众号
	And bob关注jobs的公众号

@mall2  @stats.marketing @wip.marketing1
Scenario: '微信抽奖'营销活动分析及分页
	Given jobs登录系统

	When 微信用户已参加'微信抽奖'营销活动
		|activity_name  | responsible_person | start_time          |end_time             |status  | participant |share_to       |member_source |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | bill        | tom,jim,kate  |         |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | bill        |  mary         |         |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | tom         |  mary         |         |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | mary        |               |bill     |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | tom         |  mary         |bill     |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | mary        |               |bill.tom |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | mary        |               |tom      |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | jim         |               |bill     |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | kate        |               |bill     |
		| 微信抽奖02    | jobs               | 2015-06-15 08:00:00 | 2025-06-17 08:00:00 |已启动  | bill        |               |         |
		| 微信抽奖02    | jobs               | 2015-06-15 08:00:00 | 2025-06-17 08:00:00 |已启动  | tom         |               |         | 

	Given jobs登录系统
	When 访问'微信抽奖'营销传播分析页面
	Then 获取'微信抽奖'营销传播分析数据
		|name  | manager | parti_times | parti_person_cnt | start_at           | end_at              | status   | status_text |
		| 微信抽奖01    | jobs              |        9 | 5                 | 2015-06-15 09:00:00 | 2025-06-30 09:00:00  | 1   | 已启动 |
		| 微信抽奖02    | jobs              |        2 | 2                 | 2015-06-15 08:00:00 | 2025-06-17 08:00:00  | 1   | 已启动 |


@ignore 
Scenario: '渠道扫码'营销活动分析及分页
	Given jobs登录系统
	Then jobs能看到的渠道扫码列表
		"""
		[{
			"name": "渠道扫码03",
			"remark": "备注1"
		}, {
			"name": "渠道扫码02",
			"remark": "备注2"
		}, {
			"name": "渠道扫码01",
			"remark": "备注3"
		}]
		"""

	When 微信用户已参加'渠道扫码'营销活动
		# bill1 --> tom, bill01 --> mary
		|activity_name  | responsible_person | authority |awards      |creat_time          | participant |share_to        |member_source |
		| 渠道扫码01    | jobs               | 是        | [优惠券]ss |2015-06-17 08:00:00 | bill        |                |         |
		| 渠道扫码01    | jobs               | 是        | [优惠券]ss |2015-06-17 08:00:00 | bill        | bill1          |         |
		| 渠道扫码01    | jobs               | 是        | [优惠券]ss |2015-06-17 08:00:00 | bob         |                |         |
		| 渠道扫码01    | jobs               | 是        | [优惠券]ss |2015-06-17 08:00:00 | tom         | bill01,bill,bob| bill    |
		| 渠道扫码01    | jobs               | 是        | [优惠券]ss |2015-06-17 08:00:00 | mary        |                | bill1   |
		| 渠道扫码01    | jobs               | 是        | [优惠券]ss |2015-06-17 08:00:00 | bill        |                | bill1   |
		| 渠道扫码01    | jobs               | 是        | [优惠券]ss |2015-06-17 08:00:00 | bob         |                | bill1   |
		| 渠道扫码02    | jobs               | 否        | [积分]20   |2015-06-18 08:00:00 | bill        |                |         |
		| 渠道扫码03    | jobs               | 是        | [积分]20   |2015-06-19 08:00:00 | bill        |                |         |
	
	Then 获取'渠道扫码'营销活动分析列表
		|name         | manager | parti_times | parti_person_cnt |  end_at  | status   | status_text |
		| 渠道扫码01  | jobs    |      7      | 4                |     -    |    1     |    已启动   |
		| 渠道扫码02  | jobs    |      1      | 1                |     -    |    1     |    已启动   |


@ignore 
Scenario: 一个用户扫描2个渠道二维码
	前提：已建立渠道扫码01和渠道扫码02（均设置已关注会员可参与）
	1、用户a扫"渠道扫码01"的二维码
	2、用户a再扫"渠道扫码02"的二维码

	Given jobs登录系统
	Then jobs能看到的渠道扫码列表
		"""
		[{
			"name": "渠道扫码03",
			"remark": "备注1"
		}, {
			"name": "渠道扫码02",
			"remark": "备注2"
		}, {
			"name": "渠道扫码01",
			"remark": "备注3"
		}]
		"""
	When bill通过扫描'渠道扫码01'二维码关注
	Then 获取'渠道扫码'营销活动分析列表
		|name           | manager | parti_times | parti_person_cnt | end_at | status | status_text |
		| 渠道扫码01    | jobs    |       1     | 1                |    -   |    1   | 已启动 |
		| 渠道扫码02    | jobs    |       0     | 0                |    -   |    1   | 已启动 |
	
	When bill通过扫描'渠道扫码02'二维码关注
	
	Then 获取'渠道扫码'营销活动分析列表
		|name        | manager | parti_times | parti_person_cnt | end_at | status | status_text |
		| 渠道扫码01 | jobs    |      1      | 1                |    -   | 1      | 已启动 |
		| 渠道扫码02 | jobs    |      0      | 0                |    -   | 1      | 已启动 |


@ignore 
Scenario: 【营销传播分析】同一用户多次扫同一个二维码时，参与次数不累加
	前提：已添加“渠道扫码01”
	1、用户a扫“渠道扫码01”；（参与次数/人数为：1/1）
	2、用户a再扫“渠道扫码01”；(参与次数/人数为：1/1)
	3、用户a取消关注后再扫“渠道扫码01”；(参与次数/人数为：1/1)

	Given jobs登录系统
	Then jobs能看到的渠道扫码列表
		"""
		[{
			"name": "渠道扫码03",
			"remark": "备注1"
		}, {
			"name": "渠道扫码02",
			"remark": "备注2"
		}, {
			"name": "渠道扫码01",
			"remark": "备注3"
		}]
		"""
	When bill通过扫描'渠道扫码01'二维码关注
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		|name  | manager | parti_times | parti_person_cnt |  end_at              | status   | status_text |
		| 渠道扫码01    | jobs              |        1 | 1                 |  -  | 1   | 已启动 |
		| 渠道扫码02    | jobs              |        0 | 0                 |  -  | 1   | 已启动 |

	When bill通过扫描'渠道扫码01'二维码关注
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		|name  | manager | parti_times | parti_person_cnt |  end_at              | status   | status_text |
		| 渠道扫码01    | jobs              |        2 | 1                 |  -  | 1   | 已启动 |
		| 渠道扫码02    | jobs              |        0 | 0                 |  -  | 1   | 已启动 |

	When bill取消关注jobs的公众号
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		|name  | manager | parti_times | parti_person_cnt |  end_at              | status   | status_text |
		| 渠道扫码01    | jobs              |        2 | 1                 |  -  | 1   | 已启动 |
		| 渠道扫码02    | jobs              |        0 | 0                 |  -  | 1   | 已启动 |

	Given bill关注jobs的公众号
	And jobs登录系统
	When bill通过扫描'渠道扫码01'二维码关注
	Then 获取'渠道扫码'营销活动分析列表
		|name  | manager | parti_times | parti_person_cnt |  end_at              | status   | status_text |
		| 渠道扫码01    | jobs              |        3 | 1                 |  -  | 1   | 已启动 |
		| 渠道扫码02    | jobs              |        0 | 0                 |  -  | 1   | 已启动 |



@ignore 
Scenario: 微信抽奖按照结束时间逆序展示

@ignore 
Scenario: 测试
	And jobs获取'微信抽奖01'的活动跟踪图
	 """
	 [{
	 "name":"微信抽奖01",
	 "children":
		[{
			 "name":"bill",
			 "children":
			 [{
				 "name":"tom",
				 "children":
					[{
					"name":"mary",
					"children":""
					}]
			 },{
				 "name":"jim",
				 "children":""
			 },{
				 "name":"kate",
				 "children":""
			 },{
				 "name":"mary",
				 "children":""
			 }]
		},{
			 "name":"tom",
			 "children":
			[{
				 "name":"mary",
				 "children":""
			}]
		}]
	 }]
	 """
	 And jobs获取'微信抽奖02'的活动跟踪图
	 """
	 [{
		 "name":"微信抽奖02",
		 "children":
		 [{
			"name":"bill",
			"children":""
		 },{
			"name":"tom",
			"children":""
		 }]
	 }]
	 """
	 
	#暂停-暂停'微信抽奖'营销活动'微信抽奖01'
	 When jobs已暂停'微信抽奖'营销活动'微信抽奖01'
	 """
	 [{
		"name":"微信抽奖01",
		 "type":"大转盘",
		 "participate_num":9,
		 "start_time":"2015-06-15 09:00:00",
		 "end_time":"2015-06-30 09:00:00",
		 "status":"已暂停",
		 "awards":
			[
				{"option":"谢谢参与"},
				{"option":"一等奖"},
				{"option":"二等奖"},
				{"option":"三等奖"}
			]
	 }]
	 """
	And jobs登录BI系统
	Then jobs获取'微信抽奖'营销活动分析列表
	 |activity_name  | responsible_person| participant_num/person_num |start_time           |end_time              |status   |
	 | 微信抽奖01    | jobs              |        9/5                 | 2015-06-15 09:00:00 | 2015-06-30 09:00:00  |已暂停   |           
	 | 微信抽奖02    | jobs              |        2/2                 | 2015-06-15 08:00:00 | 2015-06-17 08:00:00  |已启动   | 

	#已过期-2天后jobs登录BI系统、2015-06-17 08:00:00以后
	When jobs于'2015-06-18'登录BI系统
	Then 获取'微信抽奖'营销活动分析列表
	 |activity_name  | responsible_person| participant_num/person_num |start_time           |end_time              |status   |
	 | 微信抽奖01    | jobs              |        9/5                 | 2015-06-15 09:00:00 | 2015-06-30 09:00:00  |已暂停   |           
	 | 微信抽奖02    | jobs              |        2/2                 | 2015-06-15 08:00:00 | 2015-06-17 08:00:00  |已过期   | 
	 
	#删除-删除'微信抽奖'营销活动'微信抽奖02'(活动只能删除已过期的)
	When jobs已删除'微信抽奖'营销活动'微信抽奖02'
	And jobs登录BI系统
	Then jobs获取'微信抽奖'营销活动分析列表
		|activity_name  | responsible_person| participant_num/person_num |start_time           |end_time              |status   |
		| 微信抽奖01    | jobs              |        9/5                 | 2015-06-15 09:00:00 | 2015-06-30 09:00:00  |已暂停   |  

	#'微信抽奖'营销活动分页浏览、按照活动截止时间倒序排列、每页显示10条数据
	#jobs已添加10个'微信抽奖'营销活动（请开发同学在写step时，按下面的规则再加10条数据）
	When jobs已添加'微信抽奖'营销活动
		"""
		[{
		"name":"微信抽奖03",
		"type":"大转盘",
		"participate_num":0,
		"start_time":"2015-06-17 09:00:00",
		"end_time":"2015-06-29 09:00:00",
		"status":"已启动",
		"awards":
		 [
			{"option":"谢谢参与"},
			{"option":"一等奖"},
			{"option":"二等奖"},
			{"option":"三等奖"}
		 ]
		},{
		"name":"微信抽奖12",
		"type":"刮刮卡",
		"participate_num":0,
		"start_time":"2015-06-17 09:00:00",
		"end_time":"2015-06-20 09:00:00",
		"status":"已启动",
		"awards":
		 [
			{"option":"谢谢参与"},
			{"option":"一等奖"},
			{"option":"二等奖"},
			{"option":"三等奖"}
		 ]
		}]
		"""
	When jobs已设置分页条件
		"""
		{
		 "page_count":10
		}
		"""
	And jobs登录BI系统
	Then jobs获取'微信抽奖'营销活动分析列表
		|activity_name  | responsible_person| participant_num/person_num |start_time           |end_time              |status   |
		| 微信抽奖01    | jobs              |        9/5                 | 2015-06-15 09:00:00 | 2015-06-30 09:00:00  |已暂停   |
		| 微信抽奖03    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-29 09:00:00  |已启动   |
		| 微信抽奖04    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-28 09:00:00  |已启动   |
		| 微信抽奖05    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-27 09:00:00  |已启动   |
		| 微信抽奖06    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-26 09:00:00  |已启动   |
		| 微信抽奖07    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-25 09:00:00  |已启动   |
		| 微信抽奖08    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-24 09:00:00  |已启动   |
		| 微信抽奖09    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-23 09:00:00  |已启动   |
		| 微信抽奖10    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-22 09:00:00  |已启动   |
		| 微信抽奖11    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-21 09:00:00  |已启动   |
	And jobs获取显示共2页
	When jobs浏览'下一页'
	Then jobs获取'微信抽奖'营销活动分析列表
		|activity_name  | responsible_person| participant_num/person_num |start_time           |end_time              |status   |
		| 微信抽奖12    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-20 09:00:00  |已启动   |
	When jobs浏览'上一页'
	Then jobs获取'微信抽奖'营销活动分析列表
		|activity_name  | responsible_person| participant_num/person_num |start_time           |end_time              |status   |
		| 微信抽奖01    | jobs              |        9/5                 | 2015-06-15 09:00:00 | 2015-06-30 09:00:00  |已暂停   |
		| 微信抽奖03    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-29 09:00:00  |已启动   |
		| 微信抽奖04    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-28 09:00:00  |已启动   |
		| 微信抽奖05    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-27 09:00:00  |已启动   |
		| 微信抽奖06    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-26 09:00:00  |已启动   |
		| 微信抽奖07    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-25 09:00:00  |已启动   |
		| 微信抽奖08    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-24 09:00:00  |已启动   |
		| 微信抽奖09    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-23 09:00:00  |已启动   |
		| 微信抽奖10    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-22 09:00:00  |已启动   |
		| 微信抽奖11    | jobs              |        0/0                 | 2015-06-17 09:00:00 | 2015-06-21 09:00:00  |已启动   |


Scenario: 渠道扫码 
	When jobs登录BI系统
	#没有数据的字段在页面显示为--
	Then jobs获取'渠道扫码'营销活动分析列表
	|activity_name  | responsible_person| participant_num/person_num |start_time |end_time   |status   |
	| 渠道扫码03    | jobs              |        1/1                 | --        | --        |--       |
	| 渠道扫码02    | jobs              |        0/0                 | --        | --        |--       |
	| 渠道扫码01    | jobs              |        7/4                 | --        | --        |--       |
	And jobs获取'渠道扫码03'的活动跟踪图
		"""
		[{
		"name":"渠道扫码03",
		"children":
		[{
		 "name":"bill",
		 "children":""
		}]
		}]
		"""
	And jobs获取'渠道扫码02'的活动跟踪图
		"""
		[{
		"name":"渠道扫码02",
		"children":""
		}]
		"""
	And jobs获取'渠道扫码01'的活动跟踪图
		"""
		[{
		"name":"渠道扫码01",
		"children":
		[{
		"name":"bill",
		 "children":
			[{
			 "name":"bill1",
			 "children":
				{
				 "name":"bill01",
				 "children":""
				}
			},{
			 "name":"bob",
			 "children":""
			}]
		},{
		 "name":"bob",
		 "children":""
		}]
		}]  
		"""
	#'渠道扫码'营销活动分页浏览、每页显示10条数据
	#jobs已添加10个'渠道扫码'营销活动（请开发同学在写step时，按下面的规则再加10条数据）
	When jobs已添加'渠道扫码'营销活动
		"""
		[{
			"name":"渠道扫码13",
			"authority":"是",
			"creat_time":"2015-06-20 21:00:00",
			"awards":
			[{
				"type":"积分",
				"value":20
			}]    
		},{
			"name":"渠道扫码04",
			"authority":"是",
			"creat_time":"2015-06-20 08:00:00",
			"awards":
			[{
				"type":"无奖励",
				"value":""
			}]    
		}]
		"""
	When jobs已设置分页条件
		"""
		{
		"page_count":10
		}
		"""
	And jobs登录BI系统
	Then jobs获取'渠道扫码'营销活动分析列表
		|activity_name  | responsible_person| participant_num/person_num |start_time |end_time   |status   |
		| 渠道扫码13    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码12    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码11    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码10    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码09    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码08    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码07    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码06    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码05    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码04    | jobs              |        0/0                 | --        | --        |--       |
	And jobs获取显示共2页
	When job浏览'下一页'
	Then jobs获取'渠道扫码'营销活动分析列表
		|activity_name  | responsible_person| participant_num/person_num |start_time |end_time   |status   |
		| 渠道扫码03    | jobs              |        1/1                 | --        | --        |--       |
		| 渠道扫码02    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码01    | jobs              |        7/4                 | --        | --        |--       |
	When job浏览'上一页'
	Then jobs获取'渠道扫码'营销活动分析列表
		|activity_name  | responsible_person| participant_num/person_num |start_time |end_time   |status   |
		| 渠道扫码13    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码12    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码11    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码10    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码09    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码08    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码07    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码06    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码05    | jobs              |        0/0                 | --        | --        |--       |
		| 渠道扫码04    | jobs              |        0/0                 | --        | --        |--       |
