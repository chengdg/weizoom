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
					"item_add":
						[{
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

	When bill参加jobs的用户调研活动"用户调研01"于"2天前"
		"""
		{
			"问答题":
				[{
					"title":"问答题",
					"value":"bill问答题内容"
				}],
			"选择题":
				[{
					"title":"选择题1",
					"value":[{
							"title":"1",
							"type":"单选",
							"isSelect":"是"
						},{
							"title":"2",
							"type":"单选",
							"isSelect":"否"
						},{
							"title":"3",
							"type":"单选",
							"isSelect":"否"
						}]
				}],
			"快捷模块":
				[{
					"value":{
						"姓名":"bill",
						"手机":"15111223344",
						"邮箱":"1234@qq.com",
						"填写项1":"11"
					}
				}],
			"上传图片":
				[{
					"title":"上传图片",
					"value":"1.jpg"
				}]
		}
		"""
	When tom参加jobs的用户调研活动"用户调研01"于"昨天"
		"""
		{
			"问答题":
				[{
					"title":"问答题",
					"value":"tom问答题内容"
				}],
			"选择题":
				[{
					"title":"选择题1",
					"value":[{
							"title":"1",
							"type":"单选",
							"isSelect":"否"
						},{
							"title":"2",
							"type":"单选",
							"isSelect":"是"
						},{
							"title":"3",
							"type":"单选",
							"isSelect":"否"
						}]
				}],
			"快捷模块":
				[{
					"value":{
						"姓名":"tom",
						"手机":"15211223344",
						"邮箱":"2234@qq.com",
						"填写项1":"22"
					}
				}],
			"上传图片":
				[{
					"title":"上传图片",
					"value":"2.jpg"
				}]
		}
		"""
	When tom1参加jobs的用户调研活动"用户调研01"于"今天"
		"""
		{
			"问答题":
				[{
					"title":"问答题",
					"value":"tom1问答题内容"
				}],
			"选择题":
				[{
					"title":"选择题1",
					"value":[{
							"title":"1",
							"type":"单选",
							"isSelect":"是"
						},{
							"title":"2",
							"type":"单选",
							"isSelect":"否"
						},{
							"title":"3",
							"type":"单选",
							"isSelect":"否"
						}]
				}],
			"快捷模块":
				[{
					"value":{
						"姓名":"tom1",
						"手机":"153211223344",
						"邮箱":"3234@qq.com",
						"填写项1":"33"
					}
				}],
			"上传图片":
				[{
					"title":"上传图片",
					"value":"3.jpg"
				}]
		}
		"""
	When tom2参加jobs的用户调研活动"用户调研01"于"今天"
		"""
		{
			"问答题":
				[{
					"title":"问答题",
					"value":"tom2问答题内容"
				}],
			"选择题":
				[{
					"title":"选择题1",
					"value":[{
							"title":"1",
							"type":"单选",
							"isSelect":"否"
						},{
							"title":"2",
							"type":"单选",
							"isSelect":"否"
						},{
							"title":"3",
							"type":"单选",
							"isSelect":"是"
						}]
				}],
			"快捷模块":
				[{
					"value":{
						"姓名":"tom2",
						"手机":"15411223344",
						"邮箱":"4234@qq.com",
						"填写项1":"44"
					}
				}],
			"上传图片":
				[{
					"title":"上传图片",
					"value":"4.jpg"
				}]
		}
		"""
@mall2 @apps @survey @survey_statistics @yang1
Scenario:1 查看用户调研的统计结果
	Given jobs登录系统
	When jobs访问用户调研活动'用户调研01'的统计
	# Then jobs获得用户调研活动'用户调研01'的统计结果
	# 	"""
	# 	{
	# 		"total_parti_person_count":4,
	# 		[{
	# 			"valid_parti_person_count":4,
	# 			"问答题(问答)":
	# 				[{
	# 					"content":"bill问答题内容",
	# 					"submit_time":"2天前"
	# 				},{
	# 					"content":"tom问答题内容",
	# 					"submit_time":"昨天"
	# 				},{
	# 					"content":"tom1问答题内容",
	# 					"submit_time":"今天"
	# 				},{
	# 					"content":"tom2问答题内容",
	# 					"submit_time":"今天"
	# 				}]
	# 		},{
	# 			"valid_parti_person_count":4,
	# 			"选择题(单选)":
	# 				[{
	# 					"options":"1",
	# 					"submit_time":"2天前"
	# 				},{
	# 					"options":"2",
	# 					"submit_time":"昨天"
	# 				},{
	# 					"options":"1",
	# 					"submit_time":"今天"
	# 				},{
	# 					"options":"1",
	# 					"submit_time":"今天"
	# 				}]
	# 		},{
	# 			"valid_parti_person_count":4,
	# 			"上传图片(上传图片)":
	# 				[{
	# 					"content":"1.jpg",
	# 					"submit_time":"2天前"
	# 				},{
	# 					"options":"2.jpg",
	# 					"submit_time":"昨天"
	# 				},{
	# 					"options":"1.jpg",
	# 					"submit_time":"今天"
	# 				},{
	# 					"options":"3.jpg",
	# 					"submit_time":"今天"
	# 				}]
	# 		}]
	# 	}
	# 	"""


