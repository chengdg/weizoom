#_author_:张三香 2015.12.03

Feature:微信投票-统计

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts": "不限",
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建微信投票活动
		"""
		[{
			"title":"微信投票01",
			"sub_title":"微信投票01",
			"content":"谢谢投票",
			"start_date":"今天",
			"end_date":"2天后",
			"authority":"无需关注即可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
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
							"options":"A"
						},{
							"options":"B"
						},{
							"options":"C"
					}]
				}],
			"quick":
				{
					"name":"false",
					"phone":"true",
					"email":"true",
					"item":[{
						"name":"填写项1",
						"is_required":"是"
					},{
						"name":"填写项2",
						"is_required":"否"
					}]
				}
		}]
		"""

	When bill关注jobs的公众号
	When tom关注jobs的公众号
	When tom1关注jobs的公众号
	When tom2关注jobs的公众号

	When 微信用户批量参加jobs的微信投票活动
		| name       | member_name | survey_time |choose  |    quick                         |
		| 微信投票01 | bill        |2天前        | 1,A    |bill,15111223344,1234@qq.com,11   |
		| 微信投票01 | tom         |昨天         | 2,B    |tom, 15211223344,2234@qq.com,22   |
		| 微信投票01 | tom1        |今天         | 1,B    |tom1,153211223344,3234@qq.com,33  |
		| 微信投票01 | tom2        |今天         | 3,A    |tom2,15411223344,4234@qq.com,44   |

@apps @vote
Scenario:1 访问微信投票的统计
	Given jobs登录系统
	When jobs访问微信投票活动'微信投票01'的统计
	Then jobs获得微信投票活动'微信投票01'的统计结果
		"""
		{
			"total_parti_person_count":4,
			[{
				"valid_parti_person_count":4,
				"选择题1(单选)":
					[{
						"options":"1":
						{
							"parti_person_count":2,
							"percent":50%
						},
						"options":"2":
						{
							"parti_person_count":1,
							"percent":25%
						},
						"options":"3":
						{
							"parti_person_count":1,
							"percent":25%
						}
					}]
			},{
					"valid_parti_person_count":4,
					"选择题2(多选)":
					[{
						"options":"A":
						{
							"parti_person_count":2,
							"percent":50%
						},
						"options":"B":
						{
							"parti_person_count":2,
							"percent":50%
						},
						"options":"C":
						{
							"parti_person_count":0,
							"percent":0%
						}
					}]
			}]
		}
		"""