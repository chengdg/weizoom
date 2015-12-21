#_author_:张三香 2015.12.03

Feature:微信投票活动列表-参与人数

Background:
	Given jobs登录系统
	When jobs新建微信投票活动
		"""
		[{
			"title":"微信投票01",
			"sub_title":"微信投票01",
			"content":"谢谢投票",
			"start_date":"昨天",
			"end_date":"5天后",
			"authority":"无需关注即可参与",
			"prize_type":"无奖励",
			"text_options":
				[{
					"title":"选择题",
					"single_or_multiple":"单选",
					"is_required":"是",
					"options":[{
							"option":"1"
						},{
							"option":"2"
						},{
							"option":"3"
						}]
				}]
		}]
		"""
	When jobs新建微信投票活动
		"""
		[{
			"title":"微信投票02",
			"sub_title":"微信投票02",
			"content":"谢谢投票",
			"start_date":"昨天",
			"end_date":"5天后",
			"authority":"必须关注才可参与",
			"prize_type":"积分",
			"integral":20,
			"participate_info":[{
				"items_select":[{
							"item_name":"姓名",
							"is_selected":true
						},{
							"item_name":"手机",
							"is_selected":true
						}],
				"items_add":[{
						"item_name":"填写项1",
						"is_required":"是"
					},{
						"item_name":"填写项2",
						"is_required":"否"
					}]
				}]
		}]
		"""

	#会员
		Given bill关注jobs的公众号
		When bill访问jobs的webapp

		Given tom关注jobs的公众号
		When tom访问jobs的webapp
		When tom取消关注jobs的公众号

	#会员参与'微信投票01'
		When 清空浏览器
		When bill参加微信投票活动'微信投票01'于'今天'
			"""
			{
				"选择题":"1"
			}
			"""

	#取消关注的会员参与'微信投票01'
		When 清空浏览器
		When tom参加微信投票活动'微信投票01'于'今天'
			"""
			{
				"选择题":"2"
			}
			"""

	#非会员参与'微信投票01'
		When 清空浏览器
		When lily参加微信投票活动'微信投票01'于'今天'
			"""
			{
				"选择题":"1"
			}
			"""

	#会员参与'微信投票02'
		When 清空浏览器
		When bill参加微信投票活动'微信投票02'于'今天'
			"""
			{
				"姓名":"bill",
				"手机":"15211223344",
				"填写项1":"11",
				"填写项2":""
			}
			"""

@apps @vote
Scenario:1 微信投票活动列表参与人数的校验
	Given jobs登录系统
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票02",
			"parti_person_cnt":1
		},{
			"name":"微信投票01",
			"parti_person_cnt":3
		}]
		"""



