#_author_:邓成龙 2016.4.14
Feature: 管理员增加选手
	"""
		管理员创建选手
	"""

Background:
	Given jobs登录系统
	When jobs新建微信高级投票活动
	"""
		[{
			"title":"新建微信高级投票活动",
			"groups":[],
			"daily_vote":3
			"rule":"高级投票规则",
			"desc":"高级投票活动介绍",
			"start_date":"今天",
			"end_date":"2天后",
			"pic":"1.jpg"
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
			"actions":["查看"]
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
