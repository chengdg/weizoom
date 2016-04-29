#_author_:张三香 2015.11.13

Feature: 新建用户调研活动
	#修改备注：原来的'快捷模块'名称改成'参与人信息'

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
		When jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2"
		}
		"""

@mall2 @apps @survey @add_survey
Scenario:1 新建用户调研活动,添加'问答'模块,无奖励
	Given jobs登录系统
	When jobs新建用户调研活动
		"""
		[{
			"title":"问答用户调研",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"明天",
			"end_date":"2天后",
			"permission":"无需关注即可参与",
			"prize_type":"无奖励",
			"member_group":"分组1",
			"answer":
				[{
					"title":"问答题1",
					"is_required":"是"
				},{
					"title":"问答题2",
					"is_required":"否"
				}]
		}]
		"""
	Then jobs获得用户调研活动列表
		"""
		[{
			"name":"问答用户调研",
			"participant_count":0,
			"prize_type":"无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["链接","预览","统计","查看结果"]
		}]
		"""

@mall2 @apps @survey @add_survey
Scenario:2 新建用户调研活动,添加'选择题'模块,积分奖励
	Given jobs登录系统
	When jobs新建用户调研活动
		"""
		[{
			"title":"选择题用户调研",
			"subtitle":"用户调研2",
			"content":"欢迎参加调研",
			"start_date":"今天",
			"end_date":"2天后",
			"permission":"必须关注才可参与",
			"prize_type":"积分",
			"integral": 10,
			"member_group":"分组1",
			"choose":
				[{
					"title":"选择题1",
					"type":"单选",
					"is_required":"是",
					"option":[{
							"options":"1"
						},{
							"options":"2"
						},{
							"options":"3"
						}]
				},{
					"title":"选择题2",
					"type":"多选",
					"is_required":"否",
					"option":[{
							"options":"选项A"
						},{
							"options":"选项B"
						},{
							"options":"选项C"
						}]
				}]
		}]
		"""
	Then jobs获得用户调研活动列表
		"""
		[{
			"name":"选择题用户调研",
			"participant_count":0,
			"prize_type":"积分",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","统计","查看结果"]
		}]
		"""

@mall2 @apps @survey @add_survey
Scenario:3 新建用户调研活动,添加'参与人信息'模块,优惠券奖励
	Given jobs登录系统
	When jobs新建用户调研活动
		"""
		[{
			"title":"参与人信息模块用户调研",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"今天",
			"end_date":"2天后",
			"permission":"无需关注即可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"member_group":"分组1",
			"participate_info":
				[{
					"items_select":
						[{
							"item_name":"姓名",
							"is_selected":"false"
						},{
							"item_name":"手机",
							"is_selected":"true"
						},{
							"item_name":"邮箱",
							"is_selected":"true"
						},{
							"item_name":"QQ",
							"is_selected":"false"
						},{
							"item_name":"职位",
							"is_selected":"false"
						},{
							"item_name":"住址",
							"is_selected":"false"
						}],
					"items_add":
						[{
							"item_name":"填写项1",
							"is_required":"是"
						},{
							"item_name":"填写项2",
							"is_required":"否"
						},{
							"item_name":"填写项3",
							"is_required":"否"
						}]
				}]
		}]
		"""
	Then jobs获得用户调研活动列表
		"""
		[{
			"name":"参与人信息模块用户调研",
			"participant_count":0,
			"prize_type":"优惠券",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions":["关闭","链接","预览","统计","查看结果"]
		}]
		"""

@mall2 @apps @survey @add_survey
Scenario:4 新建用户调研活动,添加'上传图片'模块,无需关注即可参与
	Given jobs登录系统
	When jobs新建用户调研活动
		"""
		[{
			"title":"上传图片用户调研",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"今天",
			"end_date":"2天后",
			"permission":"无需关注即可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"member_group":"分组1",
			"upload_pic":
				[{
					"title":"上传图片",
					"is_required":"是"
				}]
		}]
		"""
	Then jobs获得用户调研活动列表
		"""
		[{
			"name":"上传图片用户调研",
			"participant_count":0,
			"prize_type":"优惠券",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions":["关闭","链接","预览","统计","查看结果"]
		}]
		"""

@mall2 @apps @survey @add_survey
Scenario:5 新建用户调研活动,添加所有模块,必须关注才可参与
	Given jobs登录系统
	When jobs新建用户调研活动
		"""
		[{
			"title":"所有模块用户调研",
			"subtitle":"所有模块",
			"content":"欢迎参加调研",
			"start_date":"今天",
			"end_date":"2天后",
			"permission":"必须关注才可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"member_group":"分组1",
			"answer":
				[{
					"title":"问答题",
					"is_required":"是"
				}],
			"choose":
				[{
					"title":"选择题1",
					"type":"单选",
					"is_required":"是",
					"option":[{
							"options":"1"
						},{
							"options":"2"
						},{
							"options":"3"
					}]
				}],
			"participate_info":
				[{
					"items_select":
					[{
						"item_name":"姓名",
						"is_selected":"false"
					},{
						"item_name":"手机",
						"is_selected":"true"
					},{
						"item_name":"邮箱",
						"is_selected":"true"
					},{
						"item_name":"QQ",
						"is_selected":"false"
					},{
						"item_name":"职位",
						"is_selected":"false"
					},{
						"item_name":"住址",
						"is_selected":"false"
					}],
					"items_add":[{
						"item_name":"填写项1",
						"is_required":"是"
					},{
						"item_name":"填写项2",
						"is_required":"否"
					}]
				}],
			"upload_pic":
				[{
					"title":"上传图片1",
					"is_required":"是"
				},{
					"title":"上传图片2",
					"is_required":"否"
				}]
		}]
		"""
	Then jobs获得用户调研活动列表
		"""
		[{
			"name":"所有模块用户调研",
			"participant_count":0,
			"prize_type":"优惠券",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions":["关闭","链接","预览","统计","查看结果"]
		}]
		"""
