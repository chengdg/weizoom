#_author_:张三香 2015.12.03

Feature:微信投票活动列表-参与人数

Background:
	Given jobs登录系统
	When jobs新建微信投票活动
		"""
		[{
			"title":"微信投票01",
			"subtitle":"微信投票01",
			"content":"谢谢投票",
			"start_date":"昨天",
			"end_date":"5天后",
			"permission":"无需关注即可参与",
			"prize_type":"无奖励",
			"text_options":
				[{
					"title":"选择题",
					"type":"单选",
					"is_required":"是",
					"option":[{
							"options":"1"
						},{
							"options":"2"
						},{
							"options":"3"
						}]
				}]
		}]
		"""
	When jobs新建微信投票活动
		"""
		[{
			"title":"微信投票02",
			"subtitle":"微信投票02",
			"content":"谢谢投票",
			"start_date":"昨天",
			"end_date":"5天后",
			"permission":"必须关注才可参与",
			"prize_type":"积分",
			"integral":20,
			"participate_info":[{
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

@mall2 @apps @vote @vote_list_participate_number
Scenario:1 微信投票活动列表参与人数的校验
	Given jobs登录系统
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票02",
			"participant_count":1
		},{
			"name":"微信投票01",
			"participant_count":3
		}]
		"""



