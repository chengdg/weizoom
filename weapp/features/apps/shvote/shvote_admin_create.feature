#_author_:邓成龙 2016.4.14
Feature: 管理员增加选手
	"""
		管理员创建选手
	"""

Background:
	Given jobs登录系统
	When jobs新建高级投票活动
	#新建高级微信投票活动,无分组
	"""
		[{
			"title":"新建微信高级投票活动",
			"groups":[],
			"rule":"高级投票规则",,
			"desc":"高级投票活动介绍",
			"start_date":"今天",
			"end_date":"2天后",
			"pic":"1.jpg"
		}]
	"""
@mall2 @apps @shvote @shvote_admin_create @yang33
Scenario:1.管理员创建选手
	When jobs登录系统
	When jobs于"新建微信高级投票活动"高级投票活动后台创建选手
	"""
		{
			"headImg":"head.jpg",
			"name":"bill",
			"group":["初中组"],
			"number":"001",
			"details":"bill的产品好",
			"detail_pic":["pic1.jpg","pic2.jpg"]
		}
	"""
	Then jobs能获得报名详情列表
	"""
		[{	"headImg":"head.jpg",
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
			"name":"微信高级投票",
			"vote_count":1,
			"participant_count":"1",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["删除","链接","预览","报名详情","查看结果"]
		}]
		"""
