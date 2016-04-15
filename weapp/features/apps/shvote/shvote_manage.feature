#_author_:许韦 2016.04.11

Feature: 新建微信高级投票活动
	"""
		用户通过参加微信高级投票活动帮助选手获得票数
		1.【标题】：必填项，高级投票活动的名称
		2.【投票规则】：必填项，最多可输入50个字符
			每天可投1次数
		3.【选手分组】：非必填项，添加可编辑组名
		4.【选手编号】：必填项，报名输入、自动生成2种方式
		5.【活动介绍】：必填项，不超过10000个字符
		6.【有效时间】：必填项，高级投票活动时间
		7.【活动权限】：分为无需关注即可参与、必须关注才可参与
		8.【活动奖励】：分为积分和优惠券奖励类型
		9.【活动图片】：活动背景图片
	"""


@mall2 @apps @shvote @add_shvote
Scenario:1 新建微信投票活动,无分组，活动未开始
	#选手分组-无分组
	#状态-未开始
	Given jobs登录系统
	When jobs新建高级微信投票活动
		"""
		[{
			"title":"微信高级投票-未开始",
			"groups":[],
			"rule": "高级投票规则",
			"desc":"高级投票活动介绍",
			"start_date":"2天后",
			"end_date":"3天后",
			"pic":"3.jpg"
		}]
		"""
	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票-未开始",
			"vote_count":0,
			"participant_count":0,
			"start_date":"2天后",
			"end_date":"3天后",
			"status":"未开始",
			"actions": ["删除","链接","预览","报名详情","查看结果"]
		}]
		"""
	When jobs编辑高级投票活动'微信高级投票-未开始'
		"""
		{
			"title":"微信高级投票-未开始",
			"groups":[],
			"desc":"高级投票活动介绍",
			"start_date":"今天",
			"end_date":"6天后",
			"pic":"3.jpg"
		}
		"""
	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票-未开始",
			"vote_count":0,
			"participant_count":0,
			"start_date":"今天",
			"end_date":"6天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","报名详情","查看结果"]
		}]
		"""

@mall2 @apps @shvote @add_shvote
Scenario:2 新建微信投票活动,活动已结束
	#选手分组-无分组
	#状态-已结束
	Given jobs登录系统
	When jobs新建高级微信投票活动
		"""
		[{
			"title":"微信高级投票-已结束",
			"groups":[],
			"desc":"高级投票活动介绍",
			"start_date":"2天前",
			"end_date":"昨天",
			"pic":"3.jpg"
		}]
		"""
	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票-已结束",
			"vote_count":0,
			"participant_count":0,
			"start_date":"2天前",
			"end_date":"昨天",
			"status":"已结束",
			"actions": ["删除","链接","预览","报名详情","查看结果"]
		}]
		"""

@mall2 @apps @shvote @add_shvote
Scenario:3 新建微信投票活动，多个分组，多个活动进行中
	#选手分组-多分组
	#状态-进行中
	Given jobs登录系统
	When jobs新建高级微信投票活动
		"""
		[{
			"title":"微信高级投票-进行中",
			"groups":["初中组"],
			"desc":"高级投票活动介绍",
			"start_date":"2天前",
			"end_date":"2天后",
			"pic":"3.jpg"
		},{
			"title":"微信高级投票-进行中",
			"groups":["高中组"],
			"desc":"高级投票活动介绍",
			"start_date":"2天前",
			"end_date":"2天后",
			"pic":"3.jpg"
		}]
		"""
	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票-进行中",
			"vote_count":0,
			"participant_count":0,
			"start_date":"2天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","报名详情","查看结果"]
		},{
			"name":"微信高级投票-进行中",
			"vote_count":0,
			"participant_count":0,
			"start_date":"2天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","报名详情","查看结果"]

		}]
		"""