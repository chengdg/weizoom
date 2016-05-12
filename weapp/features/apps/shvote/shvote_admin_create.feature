#_author_:邓成龙 2016.4.14
Feature: 管理员增加选手，管理员对选手编号进行搜索
	"""
		1.管理员创建选手
		2.管理员对选手编号进行搜索迷糊搜索
	"""

Background:
	Given jobs登录系统
	When jobs新建微信高级投票活动
	"""
		[{
			"title":"新建微信高级投票活动",
			"groups":["初中组"],
			"daily_vote":3,
			"rule":"高级投票规则",
			"desc":"高级投票活动介绍",
			"start_date":"今天",
			"end_date":"2天后",
			"pic":"1.jpg"
		}]
	"""

	When jobs已添加单图文
		"""
		[{
			"title":"高级微信投票活动1单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"微信高级投票",
			"content":"微信高级投票",
			"jump_url":"新建微信高级投票活动"
		}]
		"""
	And jobs已添加关键词自动回复规则
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
					"reply_content":"高级微信投票活动1单图文",
					"reply_type":"text_picture"
				}]
		}]
		"""
@mall2 @apps @shvote @shvote_admin_create
Scenario:1.管理员创建选手
	Given jobs登录系统
	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"新建微信高级投票活动",
			"total_voted_count":0,
			"total_participanted_count":0,
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","报名详情","查看结果"]
		}]
		"""
	When jobs在"新建微信高级投票活动"高级投票活动后台创建选手
	"""
		{
			"icon":"bill_head.jpg",
			"name":"bill",
			"group":"初中组",
			"serial_number":"001",
			"details":"bill的产品好",
			"pics":["pic1.jpg","pic2.jpg"]
		}
	"""
	Then jobs能获得报名详情列表
	"""
		[{	"headImg":"bill_head.jpg",
			"player":"bill",
			"votes":0,
			"number":"001",
			"start_date":"今天",
			"status":"审核通过",
			"actions":["查看","删除"]
		}]
	"""
	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"新建微信高级投票活动",
			"total_voted_count":0,
			"total_participanted_count":"1",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","报名详情","查看结果"]
		}]
		"""


@mall2 @apps @shvote @shvote_admin_create
Scenario:2 管理员搜索选手
		#精确搜索
		#模糊搜索
		#不相关用户的搜索
	Given jobs登录系统
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微信高级投票'
	Then bill收到自动回复'高级微信投票活动1单图文'
	When bill点击图文'高级微信投票活动1单图文'进入高级微信投票活动页面
	And bill参加高级投票报名活动
		"""
			{
				"icon":"bill_head.jpg",
				"name":"bill",
				"group":"初中组",
				"serial_number":"001",
				"details":"bill的产品好",
				"pics":["pic1.jpg","pic2.jpg"]
			}
		"""
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	And tom在微信中向jobs的公众号发送消息'微信高级投票'
	Then tom收到自动回复'高级微信投票活动1单图文'
	When tom点击图文'高级微信投票活动1单图文'进入高级微信投票活动页面
	And tom参加高级投票报名活动
		"""
			{
				"icon":"tom_head.jpg",
				"name":"tom",
				"group":"初中组",
				"serial_number":"002",
				"details":"tom的产品好",
				"pics":["pic3.jpg","pic4.jpg"]
			}
		"""
	Given jobs登录系统
	When jobs在"新建微信高级投票活动"高级投票活动后台创建选手
		"""
			{
				"icon":"zhouxun_head.jpg",
				"name":"zhouxun",
				"group":"初中组",
				"serial_number":"013",
				"details":"zhouxun的产品好",
				"pics":["pic5.jpg","pic6.jpg"]
			}
		"""

	Given jobs登录系统
	When jobs于高级微信投票活动审核通过'bill'

	#模糊搜索
	When jobs设置高级投票报名详情查询条件
		"""
			{
				"serial_number":"00"
			}
		"""
	Then jobs能获得报名详情列表
		"""
			[{
				"headImg":"tom_head.jpg",
				"player":"tom",
				"votes":0,
				"number":"002",
				"start_date":"今天",
				"status":"待审核",
				"actions":["审核通过","查看","删除"]
			},{
				"headImg":"bill_head.jpg",
				"player":"bill",
				"votes":0,
				"number":"001",
				"start_date":"今天",
				"status":"审核通过",
				"actions":["查看","删除"]
			}]
		"""

	#精确用户搜索
	When jobs设置高级投票报名详情查询条件
		"""
			{
				"serial_number":"013"
			}
		"""

	Then jobs能获得报名详情列表
		"""
			[{
				"headImg":"zhouxun_head.jpg",
				"player":"zhouxun",
				"votes":0,
				"number":"013",
				"start_date":"今天",
				"status":"审核通过",
				"actions":["查看","删除"]
			}]
		"""

	#不相关用户的搜索
	When jobs设置高级投票报名详情查询条件
		"""
			{
				"serial_number":"005"
			}
		"""

	Then jobs能获得报名详情列表
		"""
			[]
		"""


@mall2 @apps @shvote @shvote_admin_create @kuki
Scenario:3 管理员删除选手，审核通过和未通过的都可以删除
	Given jobs登录系统
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微信高级投票'
	Then bill收到自动回复'高级微信投票活动1单图文'
	When bill点击图文'高级微信投票活动1单图文'进入高级微信投票活动页面
	And bill参加高级投票报名活动
		"""
			{
				"icon":"bill_head.jpg",
				"name":"bill",
				"group":"初中组",
				"serial_number":"001",
				"details":"bill的产品好",
				"pics":["pic1.jpg","pic2.jpg"]
			}
		"""
	When 清空浏览器
	And tom关注jobs的公众号
	And tom访问jobs的webapp
	And tom在微信中向jobs的公众号发送消息'微信高级投票'
	Then tom收到自动回复'高级微信投票活动1单图文'
	When tom点击图文'高级微信投票活动1单图文'进入高级微信投票活动页面
	And tom参加高级投票报名活动
		"""
			{
				"icon":"tom_head.jpg",
				"name":"tom",
				"group":"初中组",
				"serial_number":"002",
				"details":"tom的产品好",
				"pics":["pic3.jpg","pic4.jpg"]
			}
		"""
	Given jobs登录系统
	When jobs在"新建微信高级投票活动"高级投票活动后台创建选手
		"""
			{
				"icon":"zhouxun_head.jpg",
				"name":"zhouxun",
				"group":"初中组",
				"serial_number":"003",
				"details":"zhouxun的产品好",
				"pics":["pic5.jpg","pic6.jpg"]
			}
		"""

	Given jobs登录系统
	When jobs于高级微信投票活动审核通过'bill'


	#删除审核通过的用户
	When jobs于高级微信投票活动删除'bill'


	#删除未审核通过的用户
	And jobs于高级微信投票活动删除'tom'
	Then jobs能获得报名详情列表
		"""
			[{	"headImg":"zhouxun_head.jpg",
				"player":"zhouxun",
				"votes":0,
				"number":"003",
				"start_date":"今天",
				"status":"审核通过",
				"actions":["查看","删除"]
			}]
		"""

@mall2 @apps @shvote @shvote_admin_create
Scenario:4 微信用户不能重复报名参与高级投票活动,编号也不能重复
	Given jobs登录系统
	When bill关注jobs的公众号
	And bill访问jobs的webapp
	And bill在微信中向jobs的公众号发送消息'微信高级投票'
	Then bill收到自动回复'高级微信投票活动1单图文'
	When bill点击图文'高级微信投票活动1单图文'进入高级微信投票活动页面
	And bill参加高级投票报名活动
		"""
			{
				"icon":"bill_head.jpg",
				"name":"bill",
				"group":"初中组",
				"serial_number":"001",
				"details":"bill的产品好",
				"pics":["pic1.jpg","pic2.jpg"]
			}
		"""

	#重复提交报名信息
	And bill参加高级投票报名活动
		"""
			{
				"icon":"bill_head.jpg",
				"name":"bill",
				"group":"初中组",
				"serial_number":"002",
				"details":"bill的产品好",
				"pics":["pic3.jpg","pic4.jpg"]
			}
		"""
	Given jobs登录系统
	When jobs在"新建微信高级投票活动"高级投票活动后台创建选手
		"""
			{
				"icon":"zhouxun_head.jpg",
				"name":"zhouxun",
				"group":"初中组",
				"serial_number":"003",
				"details":"zhouxun的产品好",
				"pics":["pic5.jpg","pic6.jpg"]
			}
		"""
	And jobs在"新建微信高级投票活动"高级投票活动后台创建选手
		"""
			{
				"icon":"zhouxun_head.jpg",
				"name":"zhouxun",
				"group":"初中组",
				"serial_number":"003",
				"details":"zhouxun的产品好",
				"pics":["pic7.jpg","pic8.jpg"]
			}
		"""	

	Then jobs能获得报名详情列表
		"""
			[{
				"headImg":"bill_head.jpg",
				"player":"bill",
				"votes":0,
				"number":"001",
				"start_date":"今天",
				"status":"待审核",
				"actions":["审核通过","查看","删除"]
			},{
				"headImg":"zhouxun_head.jpg",
				"player":"zhouxun",
				"votes":0,
				"number":"003",
				"start_date":"今天",
				"status":"审核通过",
				"actions":["查看","删除"]
			}]
		"""