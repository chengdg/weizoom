#_author_:王丽 2015.12.02

Feature:手机端用户参与活动报名
"""
	1 活动报名设置成"无需关注即可参与"：没有关注和取消关注、关注状态的微信账号都可以参与，没有关注的账号参与之后在结果中显示的头像和昵称为空
	2 活动报名设置成"必粗关注才可参与"：没有关注和取消关注的微信账号都不可以参与，只有关注状态的微信账号可参与
"""

@apps @event
Scenario:1 活动报名-无奖励-无需关注即可参与
	Given jobs登录系统
	When jobs新建活动报名
		"""
		{
			"title":"活动报名-无奖励",
			"subtitle":"活动报名-副标题-无奖励",
			"content":"内容描述-无奖励",
			"start_date":"今天",
			"end_date":"2天后",
			"right":"无需关注即可参与",
			"prize_type": "无奖励",
			"items_select":[{
						"item_name":"姓名",
						"is_selected":true
					},{
						"item_name":"手机",
						"is_selected":true
					},{
						"item_name":"邮箱",
						"is_selected":true
					},{
						"item_name":"QQ",
						"is_selected":true
					},{
						"item_name":"职位",
						"is_selected":false
					},{
						"item_name":"住址",
						"is_selected":false
					}],
			"items_add":[{
						"item_name":"其他",
						"is_required":"false"
					}]
		}
		"""

	#会员
		Given bill关注jobs的公众账号
		When bill访问jobs的webapp

		Given tom关注jobs的公众账号
		When tom访问jobs的webapp
		When tom取消关注jobs的公众号

	#会员参与
		When 清空浏览器	
		When bill参加活动报名'活动报名-无奖励'于'今天'
			"""
			{
				"姓名":"bill",
				"手机":"15213265987",
				"邮箱":"123456@qq.com",
				"QQ":"12345",
				"其他":""
			}
			"""
		Then bill获得提示"提交成功"
	#取消关注的会员参与
		When 清空浏览器
		When tom参加活动报名'活动报名-无奖励'于'今天'
			"""
			{
				"姓名":"tom",
				"手机":"15213265987",
				"邮箱":"123456@qq.com",
				"QQ":"12345",
				"其他":"其他"
			}
			"""
		Then tom获得提示"提交成功"
	#非会员参与
		When 清空浏览器
		When lily参加活动报名'活动报名-无奖励'于'今天'
			"""
			{
				"姓名":"lily",
				"手机":"15213265987",
				"邮箱":"123456@qq.com",
				"QQ":"12345",
				"其他":"其他"
			}
			"""
		Then lily获得提示"提交成功"
	#同以会员第二次参与同一活动报名
		When 清空浏览器
		When bill参加活动报名'活动报名-无奖励'于'今天'
			"""
			{}
			"""
		Then bill获得提示"您已报名"

@apps @event
Scenario:2 活动报名-积分奖励-必须关注才可参与
	Given jobs登录系统
	When jobs新建活动报名
		"""
		{
			"title":"活动报名-积分",
			"subtitle":"活动报名-副标题-积分",
			"content":"内容描述-积分",
			"start_date":"1天前",
			"end_date":"2天后",
			"right":"必须关注才可参与",
			"prize_type": "积分",
			"integral": 50,
			"items_select":[{
						"item_name":"姓名",
						"is_selected":true
					},{
						"item_name":"手机",
						"is_selected":true
					},{
						"item_name":"邮箱",
						"is_selected":false
					},{
						"item_name":"QQ",
						"is_selected":false
					},{
						"item_name":"职位",
						"is_selected":false
					},{
						"item_name":"住址",
						"is_selected":false
					}],
			"items_add":[{
						"item_name":"店铺类型",
						"is_required":"true"
					},{
						"item_name":"开店时间",
						"is_required":"true"
					}]
		}
		"""

	#会员
		Given bill关注jobs的公众账号
		When bill访问jobs的webapp

		Given tom关注jobs的公众账号
		When tom访问jobs的webapp
		When tom取消关注jobs的公众号

	#会员参与
		When 清空浏览器
		When bill参加活动报名'活动报名-积分'于'今天'
			"""
			{
				"姓名":"bill",
				"手机":"15213265987",
				"店铺类型":"旗舰店",
				"开店时间":"2015-10"
			}
			"""
		Then bill获得提示"提交成功"
		When bill访问jobs的webapp
		Then bill在jobs的webapp中拥有50会员积分
	#取消关注的会员参与
		When 清空浏览器
		When tom参加活动报名'活动报名-积分'于'今天'
			"""
			{
				"姓名":"tom",
				"手机":"15213265987",
				"店铺类型":"旗舰店",
				"开店时间":"2015-10"
			}
			"""
		Then tom获得提示"店铺二维码"
	#非会员参与
		When 清空浏览器
		When lily参加活动报名'活动报名-积分'于'今天'
			"""
			{
				"姓名":"lily",
				"手机":"15213265987",
				"店铺类型":"旗舰店",
				"开店时间":"2015-10"
			}
			"""
		Then lily获得提示"店铺二维码"

@apps @event
Scenario:3 活动报名-优惠券奖励-无需关注即可参与
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts": 1,
			"start_date": "4天前",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建活动报名
		"""
		{
			"title":"活动报名-优惠券",
			"subtitle":"活动报名-副标题-优惠券",
			"content":"内容描述-优惠券",
			"start_date":"3天前",
			"end_date":"1天后",
			"right":"无需关注即可参与",
			"prize_type": "优惠券",
			"coupon":"优惠券1",
			"items_select":[{
						"item_name":"姓名",
						"is_selected":true
					},{
						"item_name":"手机",
						"is_selected":true
					},{
						"item_name":"邮箱",
						"is_selected":false
					},{
						"item_name":"QQ",
						"is_selected":false
					},{
						"item_name":"职位",
						"is_selected":false
					},{
						"item_name":"住址",
						"is_selected":true
					}],
			"items_add":[{
						"item_name":"店铺类型",
						"is_required":"true"
					},{
						"item_name":"开店时间",
						"is_required":"true"
					}]
		}
		"""

	#会员
		Given bill关注jobs的公众账号
		When bill访问jobs的webapp

		Given tom关注jobs的公众账号
		When tom访问jobs的webapp
		When tom取消关注jobs的公众号

	#会员参与
		When 清空浏览器		
		When bill参加活动报名'活动报名-优惠券'于'今天'
			"""
			{
				"姓名":"bill",
				"手机":"15213265987",
				"店铺类型":"旗舰店",
				"开店时间":"2015-10"
			}
			"""
		Then bill获得提示"提交成功"
		When bill访问jobs的webapp
		Then bill能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_1",
				"money": 100.00,
				"status": "未使用"
			}]
			"""
	#取消关注的会员参与
		When 清空浏览器
		When tom参加活动报名'活动报名-优惠券'于'今天'
			"""
			{
				"姓名":"tom",
				"手机":"15213265987",
				"店铺类型":"旗舰店",
				"开店时间":"2015-10"
			}
			"""
		Then tom获得提示"提交成功"
		When tom访问jobs的webapp
		Then tom能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_2",
				"money": 100.00,
				"status": "未使用"
			}]
			"""
	#非会员参与
		When 清空浏览器
		When lily参加活动报名'活动报名-优惠券'于'今天'
			"""
			{
				"姓名":"lily",
				"手机":"15213265987",
				"店铺类型":"旗舰店",
				"开店时间":"2015-10"
			}
			"""
		Then lily获得提示"提交成功"
		When lily关注jobs的公众账号
		When lily访问jobs的webapp
		Then lily能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_3",
				"money": 100.00,
				"status": "未使用"
			}]
			"""
