#_author_:邓成龙 2016.04.13

Feature: 高级投票活动
	"""
	1.管理员删除用户提交的报名申请，列表中消失
		1.微信用户提交报名申请；
		2.报名详情中该微信用户提交高级投票申请状态为“待审核”；
		3.管理员删除该用户提交的申请；
		4.活动详情中的报名申请记录消失；
	2.管理员通过微信用户提交高级投票申请
	3.管理员通过微信用户提交高级投票申请
		1.根据票数不同获得的排名不同
		2.票数相同，谁先报名谁排在前面
	4.用户查看高级微信投票活动介绍
		微信用户进入高级投票主页
		微信用户查看"活动介绍"
	4.微信用户提交高级投票申请
		1.微信用户可以通过报名高级投票
		【名称】：必填项，高级投票活动的名称；
		【分组选择】：必填项，下拉框选择其中一个分组；
		【输入编号】：必填项，最多可输入16个字符；
		【输入详情】：必填项；

	5.微信用户搜索选手
		微信用户进入投票活动主页
		微信用户输入关键词搜索选手
		选手列表中展示名字包含关键词与编号包含关键词的选手信息，按照得票数由高到底排列
	5.微信用户查看排行信息
		微信用户进入高级投票主页
		微信用户点击“排行”链接进入排行页面
		查看排行榜列表
	6.查看三维数据
		微信用户进入高级投票主页
	7.微信用户给参与者投票
		1.微信用户提交报名申请；
		2.报名详情中管理员通过该用户提交的报名申请；
		3.参与者可以被投票；
	
	9.微信用户查看高级投票主页中的排行榜
		微信用户进入高级投票主页
	"""
Background:
	Given jobs登录系统
	When jobs新建微信高级投票活动
		"""
		[{
			"title":"微信高级投票-进行中",
			"groups":["初中组","高中组"],
			"rule": "高级投票规则",
			"desc":"高级投票活动介绍",
			"start_date":"2天前",
			"end_date":"2天后",
			"pic":"3.jpg"
		}]
		"""
	When jobs已添加单图文
		"""
		[{
			"title":"高级投票活动1单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"微信高级投票",
			"content":"微信高级投票",
			"jump_url":"微信高级投票-进行中"
		}]
		"""
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": 
				[{
					"keyword": "微信高级投票",
					"type": "equal"
				}],
			"keyword_reply": 
				[{
					"reply_content":"高级投票活动1单图文",
					"reply_type":"text_picture"
				}]
		}]
		"""

	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微信高级投票'
	Then bill收到自动回复'高级微信投票活动1单图文'
	When bill点击图文'高级微信投票活动1单图文'进入高级微信投票活动页面
	When bill参加高级投票报名活动
	"""
		{
			"headImg":"bill_head.jpg",
			"name":"bill",
			"group":["初中组"],
			"number":"003",	
			"details":"bill的产品好",
			"detail_pic":["pic1.jpg","pic2.jpg"]
		}
	"""
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微信高级投票'
	Then tom收到自动回复'高级微信投票活动1单图文'
	When tom点击图文'高级微信投票活动1单图文'进入高级微信投票活动页面
	When tom参加高级投票报名活动
	"""
		{
			"headImg":"tom_head.jpg",
			"name":"tom",
			"group":["初中组"],
			"number":"002",	
			"details":"tom的产品好",
			"detail_pic":["pic3.jpg","pic4.jpg"]
		}
	"""
	When zhouxun关注jobs的公众号
	When zhouxun访问jobs的webapp
	When zhouxun在微信中向jobs的公众号发送消息'微信高级投票'
	Then zhouxun收到自动回复'高级微信投票活动1单图文'
	When zhouxun点击图文'高级微信投票活动1单图文'进入高级微信投票活动页面
	When zhouxun参加高级投票报名活动
	"""
		{
			"headImg":"zhouxun_head.jpg",
			"name":"zhouxun",
			"group":["高中组"],
			"number":"003",	
			"details":"zhouxun的产品好",
			"detail_pic":["pic5.jpg","pic6.jpg"]
		}
	"""



@mall2 @apps @shvote @shvote_activity @yang
Scenario:1 管理员删除微信用户提交高级投票申请，列表中消失
	Given jobs登录系统
	When jobs于高级微信投票活动审核通过'bill'
	When jobs于高级微信投票活动删除'tom'
	Then jobs能获得报名详情列表
		"""
		[{
			"headImg":"bill_head.jpg",
			"player":"bill",
			"votes":0,
			"number":"001",
			"start_date":"今天",
			"status":"审核通过",
			"actions":["查看"]
		},{
			"headImg":"zhouxun_head.jpg",
			"player":"zhouxun",
			"votes":0,
			"number":"003",
			"start_date":"今天",
			"status":"待审核",
			"actions":["审核通过","删除","查看"]

		}]
		"""
	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票-进行中",
			"vote_count":0,
			"participant_count":2,
			"start_date":"2天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","报名详情","查看结果"]
		}]
		"""

@mall2 @apps @shvote @shvote_activity
Scenario:2 没有有微信用户报名参与活动和有微信用户报名参与活动，但是均未通过审核
	Given jobs登录系统
	When jobs于高级微信投票活动删除'bill'
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微信高级投票'
	Then bill收到自动回复'高级投票活动1单图文'
	When bill点击图文'高级投票活动1单图文'进入高级微信投票活动页面
	When bill参加高级投票报名活动
	Then bill获得微信高级投票活动排行榜列表
		"""
		[]
		"""

@mall2 @apps @shvote @shvote_activity
Scenario:3 微信用户报名参与活动并通过审核在活动主页的显示
	#其中考虑到没有通过审核的用户不在列表中展示
	#多分组：高中组、初中组
	#审核通过的用户

	Given jobs登录系统
	When jobs于高级微信投票活动审核通过'bill'
	When jobs于高级微信投票活动审核通过'tom'
	When jobs于高级微信投票活动审核通过'zhouxun'
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微信高级投票'
	Then tom收到自动回复'高级投票活动1单图文'
	When tom点击图文'高级投票活动1单图文'进入高级微信投票活动页面
	Then tom获得微信高级投票活动主页内容
		"""
		{"初中组":
			[{
				"group":"初中组",
				"number":"003",
				"player":"bill",
				"votes":0
			},{
				"groups":"初中组",
				"number":"002",
				"player":"tom",
				"votes":0
			}],
		"高中组":
			[{
				"group":"高中组",
				"number":"001",
				"player":"zhouxun",
				"votes":0
			}]
		}
		"""

@mall2 @apps @shvote @shvote_activity
Scenario:4 微信用户浏览高级投票活动主页，获得三维数据
	#背景里已经有的三个报名投票的人就是三个浏览人数
	#多增加一个人为其中的选手投票，三维数据的变化
	#删除选手三维数据变化
	Given jobs登录系统
	When jobs于高级微信投票活动审核通过'bill'
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微信高级投票'
	Then bill收到自动回复'高级投票活动1单图文'
	When bill点击图文'高级投票活动1单图文'进入高级微信投票活动页面
	Then bill获得微信高级投票活动'微信高级投票-进行中'主页的内容
		"""
		{
			"total_participanted_count":3,
			"total_voted_count":0,
			"total_visits":3,
			"end_date":"2天后"
		}
		"""
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微信高级投票'
	Then tom收到自动回复'高级投票活动1单图文'
	When tom点击图文'高级投票活动1单图文'进入高级微信投票活动页面
	When tom在高级投票中为'bill'投票
	Then tom获得微信高级投票活动'微信高级投票-进行中'主页的内容
		"""
		{
			"total_participanted_count":3,
			"total_voted_count":1,
			"total_visits":4,
			"end_date":"2天后"
		}
		"""
	When jobs于高级微信投票活动删除'tom'
	When zhouxun关注jobs的公众号
	When zhouxun访问jobs的webapp
	When zhouxun在微信中向jobs的公众号发送消息'微信高级投票'
	Then zhouxun收到自动回复'高级投票活动1单图文'
	When zhouxun点击图文'高级投票活动1单图文'进入高级微信投票活动页面
	When zhouxun在高级投票中为'bill'投票
	Then zhouxun获得微信高级投票活动'微信高级投票-进行中'主页的内容
		"""
		{
			"total_participanted_count":2,
			"total_voted_count":2,
			"total_visits":5,
			"end_date":"2天后"
		}
		"""


@mall2 @apps @shvote @shvote_activity 
Scenario:5 微信用户可以给参与者投票
	#用户可以对参与者进行投票
	#该用户再次对参与者进行投票，无法进行第二次投票，获取到的是原来的数据
	#获得相同票数的选手在活动主页的排行榜显示排名情况和单独页面的排行榜（即有序号的排行榜）
	#不同用户获得票数不同的排名
	#不同用户获得票数相同的排名，谁先报名谁排在第一位
	#不同的人为同一个选手进行投票票数会加1
	Given jobs登录系统
	When jobs于高级微信投票活动审核通过'bill'
	When jobs于高级微信投票活动审核通过'tom'
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微信高级投票'
	Then tom收到自动回复'高级投票活动1单图文'
	When tom点击图文'高级投票活动1单图文'进入高级微信投票活动页面
	When tom在高级投票中为'bill'投票
	Then tom获得微信高级投票活动主页排行榜列表
	"""
		[{
			"number":"001",
			"name":"bill",
			"votes":1
		},{
			"number":"002",
			"name":"tom",
			"votes":0
		},{
			"number":"003",
			"name":"zhouxun",
			"votes":0
		}]
	"""
	Then tom获得微信高级投票活动单独页面排行榜
		"""
		[{
			"number":"001",
			"name":"bill",
			"votes":1
		},{
			"number":"002",
			"name":"tom",
			"votes":1
		},{
			"number":"003",
			"name":"zhouxun",
			"votes":1
		}]
		"""
	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票-进行中",
			"total_voted_count":1,
			"total_participanted_count":2,
			"start_date":"2天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["删除","链接","预览","报名详情","查看结果"]
		}]
		"""
	When tom在高级投票中为'bill'投票
	Then tom获得微信高级投票活动主页排行榜列表
	"""
		[{
			"number":"001",
			"name":"bill",
			"votes":1
		},{
			"number":"002",
			"name":"tom",
			"votes":1
		},{
			"number":"003",
			"name":"zhouxun",
			"votes":1
		}]
	"""

	Then tom获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票-进行中",
			"total_voted_count":1,
			"total_participant_count":2,
			"start_date":"2天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","报名详情","查看结果"]
		}]
		"""
	When zhouxun关注jobs的公众号
	When zhouxun访问jobs的webapp
	When zhouxun在微信中向jobs的公众号发送消息'微信高级投票'
	Then zhouxun收到自动回复'高级投票活动1单图文'
	When zhouxun点击图文'高级投票活动1单图文'进入高级微信投票活动页面
	When zhouxun在高级投票中为'tom'投票
	Then zhouxun获得微信高级投票活动主页排行榜列表
	"""
		[{
			"number":"001",
			"name":"bill",
			"votes":1
		},{
			"number":"002",
			"name":"tom",
			"votes":1
		},{
			"number":"003",
			"name":"zhouxun",
			"votes":1
		}]
	"""
	Then zhouxun获得微信高级投票活动单独页面排行榜
		"""
		[{
			"groups":"初中组",
			"ranking":1,
			"number":"002",
			"player":"bill",
			"votes":1
		},{
			"groups":"初中组",
			"ranking":2,
			"number":"002",
			"player":"tom",
			"votes":1
		}]
		"""


	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票-进行中",
			"total_vote_count":2,
			"total_participant_count":2,
			"start_date":"2天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","报名详情","查看结果"]
		}]
		"""
	When mayun关注jobs的公众号
	When mayun访问jobs的webapp
	When mayun在微信中向jobs的公众号发送消息'微信高级投票'
	Then mayun收到自动回复'高级投票活动1单图文'
	When mayun点击图文'高级投票活动1单图文'进入高级微信投票活动页面
	When mayun在高级投票中为'bill'投票
	Then mayun获得微信高级投票活动主页排行榜列表
	"""
		[{
			"number":"001",
			"name":"bill",
			"votes":2
		},{
			"number":"002",
			"name":"tom",
			"votes":1
		}]
	"""


	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票-进行中",
			"total_vote_count":3,
			"total_participant_count":2,
			"start_date":"2天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","报名详情","查看结果"]
		}]
		"""



@mall2 @apps @shvote @shvote_activity
Scenario:6 微信用户搜索选手
		#精确搜索
		#模糊搜索
		#不相关用户的搜索
	Given jobs登录系统
	When jobs于高级微信投票活动审核通过'bill'
	When jobs于高级微信投票活动审核通过'tom'
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微信高级投票'
	Then tom收到自动回复'高级投票活动1单图文'
	When tom点击图文'高级投票活动1单图文'进入高级微信投票活动页面
	When tom搜索选手'bill'
	Then tom获得微信高级投票活动主页排行榜列表
	"""
		[{
			"number":"001",
			"name":"bill",
			"votes":0
		}]
	"""

	When tom搜索选手'u'
	"""
		[{
			"number":"001",
			"name":"zhouxun",
			"votes":0

		}]
	"""
	When tom搜索选手'bigs'
	Then tom获得微信高级投票活动排行榜列表
	"""
		[]
	"""


@mall2 @apps @shvote @shvote_activity
Scenario:7 管理员查看选手详情
	Given jobs登录系统
	When jobs于高级微信投票活动审核通过"bill"
	Then jobs获得'bill'的详情
		"""
		[{
			"player":"bill",
			"number":"001",
			"votes":0,
			"detail":"123456789"
		}]
		"""
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微信高级投票'
	Then tom收到自动回复'高级投票活动1单图文'
	When tom点击图文'高级投票活动1单图文'进入高级微信投票活动页面
	When tom在高级投票中为'bill'投票
	Then tom获得'bill'的详情
		"""
		[{
			"player":"bill",
			"number":"001",
			"votes":1,
			"detail":"123456789"
		}]
		"""
