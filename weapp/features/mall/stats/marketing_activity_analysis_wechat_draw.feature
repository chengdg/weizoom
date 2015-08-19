#_author_:张三香

Feature:营销活动分析-微信抽奖
"""
备注信息：

  1、微信抽奖活动分析列表按照活动结束时间倒序排列
  2、结果分析浮层中包含字段：
       A.参与会员数：参与该活动的新老会员总数  A=B+C
       B.新会员数：通过该活动新增的新会员数（活动期间，通过其他方式新增的会员不统计在内）
       C.老会员数：参与该活动的老会员数
"""

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
			"daily_play_count": 10,
			"detail": "测试2",
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
			"daily_play_count": 10,
			"detail": "测试2",
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
			"name":"微信抽奖03",
			"award_type": 0,
			"participate_num":0,
			"start_at": "2015-06-15",
			"end_at": "2025-06-15",
			"award_hour": 0,
			"daily_play_count": 10,
			"detail": "测试3",
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
	#And bill关注jobs的公众号
	#And tom关注jobs的公众号


@stats @wip.lottery
Scenario:1 '微信抽奖'营销活动参与次数和人数统计,参与传播和结果分析
# 建议改为：测试bill取消关注又再次关注
#营销活动分析-'微信抽奖'

	#a老会员和新会员参与抽奖 
	When bill关注jobs的公众号于'2015-05-16'
	And tom关注jobs的公众号于'2015-05-17'

	When 清空浏览器
	When mary1关注jobs的公众号于'2015-06-17'
	When mary1访问jobs的webapp
	When mary1把jobs的微站链接分享到朋友圈

	When 清空浏览器
	When mary2点击mary1分享链接
	When mary2关注jobs的公众号于'2015-06-17'
	When mary2访问jobs的webapp

	# 期望为推广扫码
	When mary3关注jobs的公众号于'2015-06-18'

	When 清空浏览器
	When mary4点击mary1分享链接
	When mary4关注jobs的公众号于'2015-06-19'
	When mary4访问jobs的webapp
	
	When 清空浏览器
	When mary5点击mary1分享链接
	When mary5关注jobs的公众号于'2015-06-19'
	When mary5访问jobs的webapp
	
	When 微信用户已参加'微信抽奖'营销活动
		| activity_name  | responsible_person | start_time          |end_time             |status  | participant |member_source   |direct_attention   |share_link_attention |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | bill 		|直接关注       |直接搜索jobs公众号 |                     |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | tom 	    |直接关注       |直接搜索jobs公众号 |                     |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | bill 		|直接关注       |直接搜索jobs公众号 |  tom,微信抽奖01    |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | jim 		|会员分享       |                   |  bill,微信抽奖01   |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | mary 		|会员分享       |                   |  tom,微信抽奖01    |
		| 微信抽奖01    | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | kate 		|会员分享       |                   |  bill,微信抽奖01   |
	
	Given jobs登录系统
	When 访问'微信抽奖'营销传播分析页面
	Then 获取'微信抽奖'营销传播分析数据
		|name           | manager           | parti_times | parti_person_cnt  | start_at            | end_at               | status   | status_text |
		| 微信抽奖01    | jobs              |        6    | 5                 | 2015-06-15 09:00:00 | 2025-06-30 09:00:00  | 1        | 已启动      |
		| 微信抽奖02    | jobs              |        0    | 0                 | 2015-06-15 08:00:00 | 2025-06-17 08:00:00  | 1        | 已启动      |
		| 微信抽奖03    | jobs              |        0    | 0                 | 2015-06-15 08:00:00 | 2025-06-15 08:00:00  | 1        | 已启动      |
	#参与传播	
	And 获得'微信抽奖'营销分析中'微信抽奖01'的'参与传播'信息
		"""
		{
			"children": [
				"bill",
				"tom",
				"jim",
				"kate",
				"mary"
			]
		}
		"""
	#结果分析
	And 获得'微信抽奖'营销分析中'微信抽奖01'的'结果分析'信息
		"""
		{
			"参与会员数": 5,
			"新会员数": 3,
			"老会员数": 2
		}
		"""

	#b取消关注-参与会员人数不减1，参与次数不减1
	# 疑问：取消关注应该影响抽奖结果？如果影响的话，在取消关注的部分，需要更新抽奖结果的数据
	When bill取消关注jobs的公众号
	Given jobs登录系统
	When 访问'微信抽奖'营销传播分析页面
	Then 获取'微信抽奖'营销传播分析数据
		# 原来: parti_times=6, parti_person_cnt=5
		|name           | manager           | parti_times | parti_person_cnt  | start_at            | end_at               | status   | status_text |
		| 微信抽奖01    | jobs              |        6    | 5                 | 2015-06-15 09:00:00 | 2025-06-30 09:00:00  | 1        | 已启动      |
		| 微信抽奖02    | jobs              |        0    | 0                 | 2015-06-15 08:00:00 | 2025-06-17 08:00:00  | 1        | 已启动      |
		| 微信抽奖03    | jobs              |        0    | 0                 | 2015-06-15 08:00:00 | 2025-06-15 08:00:00  | 1        | 已启动      |
	#参与传播
	And 获得'微信抽奖'营销分析中'微信抽奖01'的'参与传播'信息
		"""
		{
			"children": [
				"bill",
				"tom",
				"jim",
				"kate",
				"mary"
			]
		}
		"""
	And 获得'微信抽奖'营销分析中'微信抽奖01'的'结果分析'信息
		"""
		{
			"参与会员数": 5,
			"新会员数": 3,
			"老会员数": 2
		}
		"""

	#c取消关注->参加抽奖活动再关注，参与会员人数不加1，参与次数加1
	When bill参加抽奖活动'微信抽奖01'
	      #|date                 |activity_name  | responsible_person | start_time          |end_time             |status  | participant |member_souce   |direct_attention   |share_link_attension |
	      #|2015-06-16 10:10:00  |     | jobs               | 2015-06-15 09:00:00 | 2025-06-30 09:00:00 |已启动  | bill        |会员分享       |                   |  tom, 微信抽奖01    | 
	Given jobs登录系统
	When 访问'微信抽奖'营销传播分析页面
	Then 获取'微信抽奖'营销传播分析数据
		# 原来: parti_times=6, parti_person_cnt=5
		|name           | manager           | parti_times | parti_person_cnt  | start_at            | end_at               | status   | status_text |
		| 微信抽奖01    | jobs              |        7    | 5                 | 2015-06-15 09:00:00 | 2025-06-30 09:00:00  | 1        | 已启动      |
		| 微信抽奖02    | jobs              |        0    | 0                 | 2015-06-15 08:00:00 | 2025-06-17 08:00:00  | 1        | 已启动      |
		| 微信抽奖03    | jobs              |        0    | 0                 | 2015-06-15 08:00:00 | 2025-06-15 08:00:00  | 1        | 已启动      |
	#参与传播	
	And 获得'微信抽奖'营销分析中'微信抽奖01'的'参与传播'信息
		"""
		{
			"children": [
				"bill",
				"tom",
				"jim",
				"kate",
				"mary"
			]
		}
		"""
	#结果分析
	And 获得'微信抽奖'营销分析中'微信抽奖01'的'结果分析'信息
		"""
		{
			"参与会员数": 5,
			"新会员数": 3,
			"老会员数": 2
		}
		"""

	When mary取消关注jobs的公众号 
	When 微信用户已参加'微信抽奖'营销活动
		 |date                 |activity_name  | responsible_person | start_time          |end_time             |status  | participant |member_souce   |direct_attention   |share_link_attension |
		 |2015-06-16 11:00:00  | 微信抽奖02    | jobs               | 2015-06-15 08:00:00 | 2025-06-17 08:00:00 |已启动  | bill        |直接关注       |直接搜索jobs公众号 |                     |            
		 |2015-06-16 11:00:00  | 微信抽奖02    | jobs               | 2015-06-15 08:00:00 | 2025-06-17 08:00:00 |已启动  | tom         |直接关注       |直接搜索jobs公众号 |                     |  
		 |2015-06-16 11:10:00  | 微信抽奖02    | jobs               | 2015-06-15 09:00:00 | 2025-06-17 09:00:00 |已启动  | jim         |会员分享       |                   |  tom, 微信抽奖02    |
		 |2015-06-16 11:10:00  | 微信抽奖02    | jobs               | 2015-06-15 09:00:00 | 2025-06-17 09:00:00 |已启动  | mary       |会员分享       |                   |  tom, 微信抽奖02    |
	
	Given jobs登录系统
	When 访问'微信抽奖'营销传播分析页面
	Then 获取'微信抽奖'营销传播分析数据
		# 原来: parti_times=6, parti_person_cnt=5
		|name           | manager           | parti_times | parti_person_cnt  | start_at            | end_at               | status   | status_text |
		| 微信抽奖01    | jobs              |        7    | 5                 | 2015-06-15 09:00:00 | 2025-06-30 09:00:00  | 1        | 已启动      |
		| 微信抽奖02    | jobs              |        4    | 4                 | 2015-06-15 08:00:00 | 2025-06-17 08:00:00  | 1        | 已启动      |
		| 微信抽奖03    | jobs              |        0    | 0                 | 2015-06-15 08:00:00 | 2025-06-15 08:00:00  | 1        | 已启动      |
	#Then jobs获取'微信抽奖'营销活动分析列表
	#	|name           | manager           | parti_times | parti_person_cnt  | start_at            | end_at               | status   | status_text |
	#	| 微信抽奖01    | jobs              |        7    | 5                 | 2015-06-15 09:00:00 | 2025-06-30 09:00:00  | 1        | 已启动      |
	#		| 微信抽奖02    | jobs              |        4    | 4                 | 2015-06-15 08:00:00 | 2025-06-17 08:00:00  | 1        | 已启动      |
	#		| 微信抽奖03    | jobs              |        0    | 0                 | 2015-06-15 08:00:00 | 2025-06-15 08:00:00  | 1        | 已启动      |

	#参与传播
	#And 获得'微信抽奖'营销分析中'微信抽奖02'的'参与传播'信息
	#	"""
	#	{
	#		"children": [
	#			"bill",
	#			"tom",
	#			"jim",
	#			"mary"
	#		]
	#	}
	#	"""
	And 获得'微信抽奖'营销分析中'微信抽奖02'的'结果分析'信息
		"""
		{
			"参与会员数": 4,
			"新会员数": 0,
			"老会员数": 4
		}
		"""

    

Scenario:2 '微信抽奖'营销活动分析列表及分页
    #列表按照活动结束倒序排列
    #有翻页，每页显示10条数据
     Given jobs登录系统
     When jobs已设置分页条件
		"""
		{
			"page_count":1
		}
		"""
	 Then jobs获取'微信抽奖'营销活动分析列表
		|name  | manager | parti_times | parti_person_cnt | start_at           | end_at              | status   | status_text |
		| 微信抽奖01    | jobs              |        0 | 0                 | 2015-06-15 09:00:00 | 2025-06-30 09:00:00  | 1   | 已启动 |
	 And jobs获取显示共3页	
	 When jobs浏览'下一页'
	 Then jobs获取'微信抽奖'营销活动分析列表
		|name  | manager | parti_times | parti_person_cnt | start_at           | end_at              | status   | status_text |
		| 微信抽奖02    | jobs              |        0 | 0                 | 2015-06-15 08:00:00 | 2025-06-17 08:00:00  | 1   | 已启动 |	
     When jobs浏览'第3页'  
	 Then jobs获取'微信抽奖'营销活动分析列表
		|name  | manager | parti_times | parti_person_cnt | start_at           | end_at              | status   | status_text |
		| 微信抽奖03    | jobs              |        0 | 0                 | 2015-06-15 08:00:00 | 2025-06-15 08:00:00  | 1   | 已启动 |
	 When jobs浏览'上一页'
	 Then jobs获取'微信抽奖'营销活动分析列表
		|name  | manager | parti_times | parti_person_cnt | start_at           | end_at              | status   | status_text |
		| 微信抽奖02    | jobs              |        0 | 0                 | 2015-06-15 08:00:00 | 2025-06-17 08:00:00  | 1   | 已启动 |	
        