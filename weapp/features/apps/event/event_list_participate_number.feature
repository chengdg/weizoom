#_author_:王丽 2015.12.02

Feature:应用和营销-活动报名-参与人数
"""
	统计参与了本次活动报名的人数
"""

Background:
	Given jobs登录系统
	When jobs新建活动报名
		"""
		[{
			"title":"活动报名-无奖励",
			"subtitle":"活动报名-副标题-无奖励",
			"content":"内容描述-无奖励",
			"start_date":"今天",
			"end_date":"2天后",
			"permission":"无需关注即可参与",
			"prize_type": "无奖励",
			"items_select":[{
						"item_name":"姓名",
						"is_selected":"true"
					},{
						"item_name":"手机",
						"is_selected":"true"
					},{
						"item_name":"邮箱",
						"is_selected":"true"
					},{
						"item_name":"QQ",
						"is_selected":"true"
					},{
						"item_name":"职位",
						"is_selected":"false"
					},{
						"item_name":"住址",
						"is_selected":"false"
					}],
			"items_add":[{
						"item_name":"其他",
						"is_required":"false"
					}]
		}]
		"""
	When jobs新建活动报名
		"""
		[{
			"title":"活动报名-积分",
			"subtitle":"活动报名-副标题-积分",
			"content":"内容描述-积分",
			"start_date":"1天前",
			"end_date":"2天后",
			"permission":"必须关注才可参与",
			"prize_type": "积分",
			"integral": 50,
			"items_select":[{
						"item_name":"姓名",
						"is_selected":"true"
					},{
						"item_name":"手机",
						"is_selected":"true"
					},{
						"item_name":"邮箱",
						"is_selected":"false"
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
						"item_name":"店铺类型",
						"is_required":"true"
					},{
						"item_name":"开店时间",
						"is_required":"true"
					}]
		}]
		"""

	#会员
		Given bill关注jobs的公众号
		When bill访问jobs的webapp

		Given tom关注jobs的公众号
		When tom访问jobs的webapp
		When tom取消关注jobs的公众号

	#无需关注即可参与
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
  			When lily关注jobs的公众号
			When lily访问jobs的webapp
			When lily取消关注jobs的公众号
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
			Then bill获得提示"您已参加过该活动！"

	#必须关注才可参与
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
			#Then tom获得提示"店铺二维码"
		#非会员参与
			When 清空浏览器
  			When lily关注jobs的公众号
			When lily访问jobs的webapp
			When lily取消关注jobs的公众号
			When lily参加活动报名'活动报名-积分'于'今天'
				"""
				{
					"姓名":"lily",
					"手机":"15213265987",
					"店铺类型":"旗舰店",
					"开店时间":"2015-10"
				}
				"""
			#Then lily获得提示"店铺二维码"

@mall2 @apps_event @apps_event_backend @event_list_participate_number
Scenario:1 参与活动报名的人数
	Given jobs登录系统
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-积分",
			"participant_count": 1
		},{
			"name":"活动报名-无奖励",
			"participant_count": 3
		}]
		"""
