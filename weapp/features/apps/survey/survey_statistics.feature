#_author_:张三香 2015.12.02

Feature:用户调研-统计

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
	When jobs新建用户调研活动
		"""
		[{
			"title":"用户调研01",
			"subtitle":"所有模块",
			"content":"欢迎参加调研",
			"start_date":"今天",
			"end_date":"2天后",
			"permission":"必须关注才可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"answer":
				[{
					"title":"问答题",
					"is_required":"是"
				}],
			"choose":
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
				}],
			"participate_info":
				[{
					"items_select":[{
						"item_name":"姓名",
						"is_selected":false
					},{
						"item_name":"手机",
						"is_selected":true
					},{
						"item_name":"邮箱",
						"is_selected":true
				}],
					"item_add":[{
						"item_name":"填写项1",
						"is_required":"是"
					},{
						"item_name":"填写项2",
						"is_required":"否"
					}]
				}],
			"upload_pic":
				[{
					"title":"上传图片",
					"is_required":"是"
				}]
		}]
		"""

	When bill关注jobs的公众号
	When tom关注jobs的公众号
	When tom关注jobs的公众号
	When tom关注jobs的公众号

	When 微信用户批量参加jobs的用户调研活动
		| name       | member_name | survey_time | answer        |choose  |    quick                         | upload_pic |
		| 用户调研01 | bill        |2天前        |bill问答题内容 | 1      |bill,15111223344,1234@qq.com,11   | 1.jpg      |
		| 用户调研01 | tom         |昨天         |tom 问答题内容 | 2      |tom, 15211223344,2234@qq.com,22   | 2.jpg      |
		| 用户调研01 | tom1        |今天         |tom1问答题内容 | 1      |tom1,153211223344,3234@qq.com,33  | 3.jpg      |
		| 用户调研01 | tom2        |今天         |tom2问答题内容 | 3      |tom2,15411223344,4234@qq.com,44   | 4.jpg      |

@apps @survey
Scenario:1 查看用户调研的统计结果
	Given jobs登录系统
	When jobs访问用户调研活动'用户调研01'的统计
	Then jobs获得用户调研活动'用户调研01'的统计结果
		"""
		{
			"total_parti_person_count":4,
			[{
				"valid_parti_person_count":4,
				"问答题(问答)":
					[{
						"content":"bill问答题内容",
						"submit_time":"2天前"
					},{
						"content":"tom问答题内容",
						"submit_time":"昨天"
					},{
						"content":"tom1问答题内容",
						"submit_time":"今天"
					},{
						"content":"tom2问答题内容",
						"submit_time":"今天"
					}]
			},{
				"valid_parti_person_count":4,
				"选择题(单选)":
					[{
						"options":"1",
						"submit_time":"2天前"
					},{
						"options":"2",
						"submit_time":"昨天"
					},{
						"options":"1",
						"submit_time":"今天"
					},{
						"options":"1",
						"submit_time":"今天"
					}]
			},{
				"valid_parti_person_count":4,
				"上传图片(上传图片)":
					[{
						"content":"1.jpg",
						"submit_time":"2天前"
					},{
						"options":"2.jpg",
						"submit_time":"昨天"
					},{
						"options":"1.jpg",
						"submit_time":"今天"
					},{
						"options":"3.jpg",
						"submit_time":"今天"
					}]
			}]
		}
		"""


