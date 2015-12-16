#_author_:张三香 2015.11.13

Feature:手机端用户参加用户调研活动
	"""
		1、活动权限：无需关注即可参与和必须关注才可参与
		2、针对某调研活动，在活动有效时间内用户只能参加一次
		3、优惠券奖励：添加每人限领1张的优惠券时，若会员参加活动前已经领取过该优惠券，则参加活动不再获得奖励
	"""
@apps @survey
Scenario:1 参加调研活动,无需关注即可参与
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
	When jobs新建用户调研活动
		"""
		[{
			"title":"用户调研01",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"今天",
			"end_date":"2天后",
			"authority":"无需关注即可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"answer":
				{
					"title":"问答题",
					"is_required":"是"
				}
		}]
		"""

	When bill关注jobs的公众号
	When bill访问jobs的webapp

	#会员bill可参与
		When bill参加jobs的用户调研活动'用户调研01'
			"""
			{
				"问答题":"bill填写内容"
			}
			"""

		When bill把jobs的用户调研活动'用户调研01'的活动链接分享到朋友圈

	#非会员tom可参与
		When tom点击bill分享的用户调研活动'用户调研01'的活动链接
		When tom参加jobs的用户调研活动'用户调研01'
			"""
			{
				"问答题":"tom填写内容"
			}
			"""
		#Then tom获得信息提示'您获得了一张优惠券<br />赶紧去个人中心查看吧'

	#取消关注会员marry可参与
		When marry关注jobs的公众号
		When marry访问jobs的webapp
		When marry取消关注jobs的公众号

		When marry点击bill分享的用户调研活动'用户调研01'的活动链接
		When marry参加jobs的用户调研活动'用户调研01'
			"""
			{
				"问答题":"marry填写内容"
			}
			"""
		#Then marry获得信息提示'您获得了一张优惠券<br />赶紧去个人中心查看吧'

		Given jobs登录系统
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"用户调研01",
				"parti_person_cnt":3,
				"prize_type":"优惠券"
			}]
			"""

@apps @survey
Scenario:2 参加调研活动,必须关注才可参与
	Given jobs登录系统
	When jobs新建用户调研活动
		"""
		[{
			"title":"用户调研02",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"今天",
			"end_date":"2天后",
			"authority":"必须关注才可参与",
			"prize_type":"积分",
			"integral":100,
			"choose":
				[{
					"title":"选择题1",
					"single_or_multiple":"单选",
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
					"single_or_multiple":"多选",
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

	When bill关注jobs的公众号
	When bill访问jobs的webapp

	#会员bill可参加
		When bill参加jobs的用户调研活动'用户调研02'
			"""
			[{
				"选择题1":"1"
			},{
				"选择题2":"选项B"
			}]
			"""

		When bill把jobs的用户调研活动'用户调研02'的活动链接分享到朋友圈

	#非会员tom参加，点击【提交】按钮时弹出jobs的公众号二维码
		When tom点击bill分享的用户调研活动'用户调研02'的活动链接
		When tom参加jobs的用户调研活动'用户调研02'
			"""
			[{
				"选择题1":"2"
			},{
				"选择题2":"选项A"
			}]
			"""
		#Then tom获得jobs的公众号二维码图片

	#取消关注会员marry参加，点击【提交】按钮时弹出jobs的公众号二维码
		When marry关注jobs的公众号
		When marry访问jobs的webapp
		When marry取消关注jobs的公众号

		When marry点击bill分享的用户调研活动'用户调研02'的活动链接
		When marry参加jobs的用户调研活动'用户调研02'
			"""
			[{
				"选择题1":"3"
			},{
				"选择题2":"选项A"
			}]
			"""
		#Then marry获得jobs的公众号二维码图片

		Given jobs登录系统
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"用户调研02",
				"parti_person_cnt":1,
				"prize_type":"积分"
			}]
			"""

@apps @survey
Scenario:3 参加调研活动,活动奖励的校验
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
	When jobs新建用户调研活动
		"""
		[{
			"title":"积分用户调研",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"今天",
			"end_date":"2天后",
			"authority":"无需关注即可参与",
			"prize_type":"积分",
			"integral":100,
			"choose":
				[{
					"title":"选择题1",
					"single_or_multiple":"单选",
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
					"single_or_multiple":"多选",
					"is_required":"否",
					"option":[{
							"options":"选项A"
						},{
							"options":"选项B"
						},{
							"options":"选项C"
						}]
				}]
		},{
			"title":"优惠券用户调研01",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"今天",
			"end_date":"2天后",
			"authority":"无需关注即可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"answer":
				{
					"title":"问答题1",
					"is_required":"是"
				}
		},{
			"title":"优惠券用户调研02",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"今天",
			"end_date":"2天后",
			"authority":"无需关注即可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"answer":
				{
					"title":"问答题2",
					"is_required":"是"
				}
		}]
		"""

	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0会员积分
	And bill能获得webapp优惠券列表
		"""
		[]
		"""

	#bill参加'积分'奖励用户调研活动
		When bill参加用户调研活动'积分用户调研'
			"""
			[{
				"选择题1":"1"
			},{
				"选择题2":["选择A","选择B"]
			}]
			"""
		When bill访问jobs的webapp
		Then bill在jobs的webapp中拥有100会员积分
		Then bill在jobs的webapp中获得积分日志
			"""
			[{
				"content":"参与活动奖励积分",
				"integral":100
			}]
			"""

	#bill参加'优惠券'奖励用户调研活动
		When bill参加用户调研活动'优惠券用户调研01'
			"""
			{
				"问答题1":"问答题1内容"
			}
			"""
		When bill访问jobs的webapp
		Then bill能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_1",
				"money": 100.00,
				"status": "未使用"
			}]
			"""

	#bill参加'优惠券用户调研02'不再获得优惠券，因为优惠券1限领1张
		When bill参加用户调研活动'优惠券用户调研02'
			"""
			{
				"问答题2":"问答题2内容"
			}
			"""
		When bill访问jobs的webapp
		Then bill能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_1",
				"money": 100.00,
				"status": "未使用"
			}]
			"""

@apps @survey
Scenario:4 参加'未开始'状态的用户调研活动
	#手机端页面按钮显示"请等待活动开始"
	#只能通过校验后台列中的参与人数来验证用户无法参与未开始状态的活动

	Given jobs登录系统
	When jobs新建用户调研活动
		"""
		[{
			"title":"未开始用户调研",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"明天",
			"end_date":"2天后",
			"authority":"无需关注即可参与",
			"prize_type":"无奖励",
			"choose":
				[{
					"title":"选择题1",
					"single_or_multiple":"单选",
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
					"single_or_multiple":"多选",
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

	When bill关注jobs的公众号
	When tom关注jobs的公众号
	When tom取消关注jobs的公众号

	#会员bill参与(页面按钮显示"请等待活动开始")
		When bill访问jobs的webapp
		When bill参加jobs的用户调研活动'未开始用户调研'
			"""
			[{
				"选择题1":"1"
			},{
				"选择题2":"选项B"
			}]
			"""

		When bill把jobs的用户调研活动'未开始用户调研'的活动链接分享到朋友圈

		Given jobs登录系统
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"未开始用户调研",
				"status":"未开始",
				"parti_person_cnt":0,
				"prize_type":"无奖励"
			}]
			"""

	#取消关注会员tom参与(页面按钮显示"请等待活动开始")
		When tom点击bill分享的用户调研活动'未开始用户调研'的活动链接
		When tom参加jobs的用户调研活动'未开始用户调研'
			"""
			[{
				"选择题1":"2"
			},{
				"选择题2":"选项B"
			}]
			"""

		Given jobs登录系统
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"未开始用户调研",
				"status":"未开始",
				"parti_person_cnt":0,
				"prize_type":"无奖励"
			}]
			"""

	#非会员marry参与(页面按钮显示"请等待活动开始")
		When marry点击bill分享的用户调研活动'未开始用户调研'的活动链接
		When marry参加jobs的用户调研活动'未开始用户调研'
			"""
			[{
				"选择题1":"2"
			},{
				"选择题2":"选项B"
			}]
			"""

		Given jobs登录系统
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"未开始用户调研",
				"status":"未开始",
				"parti_person_cnt":0,
				"prize_type":"无奖励"
			}]
			"""

@apps @survey
Scenario:5 参加'已结束'状态的用户调研活动
	#手机端页面按钮显示"活动已结束"
	#只能通过校验后台列中的参与人数来验证用户无法参与已结束状态的活动

	Given jobs登录系统
	When jobs新建用户调研活动
		"""
		[{
			"title":"已结束用户调研",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"2天前",
			"end_date":"昨天",
			"authority":"无需关注即可参与",
			"prize_type":"无奖励",
			"choose":
				[{
					"title":"选择题1",
					"single_or_multiple":"单选",
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
					"single_or_multiple":"多选",
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

	When bill关注jobs的公众号
	When tom关注jobs的公众号
	When tom取消关注jobs的公众号

	#会员bill参与(页面按钮显示"活动已结束")
		When bill访问jobs的webapp
		When bill参加jobs的用户调研活动'已结束用户调研'
			"""
			[{
				"选择题1":"1"
			},{
				"选择题2":"选项B"
			}]
			"""

		When bill把jobs的用户调研活动'已结束用户调研'的活动链接分享到朋友圈

		Given jobs登录系统
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"已结束用户调研",
				"status":"已结束",
				"parti_person_cnt":0,
				"prize_type":"无奖励"
			}]
			"""

	#取消关注会员tom参与(页面按钮显示"活动已结束")
		When tom点击bill分享的用户调研活动'已结束用户调研'的活动链接
		When tom参加jobs的用户调研活动'已结束用户调研'
			"""
			[{
				"选择题1":"2"
			},{
				"选择题2":"选项B"
			}]
			"""

		Given jobs登录系统
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"已结束用户调研",
				"status":"已结束",
				"parti_person_cnt":0,
				"prize_type":"无奖励"
			}]
			"""

	#非会员marry参与(页面按钮显示"活动已结束")
		When marry点击bill分享的用户调研活动'已结束用户调研'的活动链接
		When marry参加jobs的用户调研活动'已结束用户调研'
			"""
			[{
				"选择题1":"2"
			},{
				"选择题2":"选项B"
			}]
			"""

		Given jobs登录系统
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"已结束用户调研",
				"status":"已结束",
				"parti_person_cnt":0,
				"prize_type":"无奖励"
			}]
			"""

