#watcher:zhangsanxiang@weizoom.com,benchi@weizoom.com
#_author_:张三香 2015.12.03

Feature:手机端用户参与微信投票活动

@mall2 @apps @vote @users_participate_vote
Scenario:1 微信投票活动-无奖励-无需关注即可参与
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
					"title":"文本选项",
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

	#会员
		Given bill关注jobs的公众号
		When bill访问jobs的webapp

		Given tom关注jobs的公众号
		When tom访问jobs的webapp
		When tom取消关注jobs的公众号

	#会员参与
		When 清空浏览器
		When bill参加微信投票活动"微信投票01"于"今天"
			"""
			{
				"文本选项":
					[{
					"title":"文本选项",
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
					}]
			}
			"""
		#Then bill获得信息提示"提交成功"

	#取消关注的会员参与
		When 清空浏览器
		When tom参加微信投票活动"微信投票01"于"今天"
			"""
			{
				"文本选项":
					[{
					"title":"文本选项",
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
					}]
			}
			"""
		#Then tom获得信息提示"提交成功"
	#非会员参与
		When 清空浏览器
		When lily关注jobs的公众号
		When lily取消关注jobs的公众号
		When lily参加微信投票活动"微信投票01"于"今天"
			"""
			{
				"文本选项":
					[{
					"title":"文本选项",
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
					}]
			}
			"""
		#Then lily获得信息提示"提交成功"

	#同一会员第二次参与同一微信投票
		When 清空浏览器
		When bill参加微信投票活动"微信投票01"于"今天"
			"""
			{}
			"""
		#Then bill获得提示"您已参加过该活动"

@mall2 @apps @vote @users_participate_vote
Scenario:2 微信投票-积分-必须关注才可参与
	Given jobs登录系统
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

	#会员参与
		When 清空浏览器
		When bill参加微信投票活动"微信投票02"于"今天"
			"""
			{
				"参与人信息":
					[{
						"value":{
						"姓名":"bill",
						"手机":"15211223344",
						"填写项1":"11",
						"填写项2":""
					}
				}]
			}
			"""
		#Then bill获得信息提示"提交成功"
		When bill访问jobs的webapp
		Then bill在jobs的webapp中拥有20会员积分

	#取消关注的会员参与
		When 清空浏览器
		When tom参加微信投票活动"微信投票02"于"今天"
			"""
			{}
			"""
		#Then tom获得信息提示"请关注后进行参与!"
		#Then tom获得jobs的公众号二维码

	#非会员参与
		When 清空浏览器
		When lily关注jobs的公众号
		When lily取消关注jobs的公众号
		When lily参加微信投票活动"微信投票02"于"今天"
			"""
			{}
			"""
		#Then lily获得信息提示"请关注后进行参与!"
		#Then lily获得获得jobs的公众号二维码

	#同一会员第二次参与同一微信投票
		When 清空浏览器
		When bill参加微信投票活动"微信投票02"于"今天"
			"""
			{}
			"""
		#Then bill获得信息提示"您已参加过该活动"

@mall2 @apps @vote @users_participate_vote
Scenario:3 微信投票-优惠券-无需关注即可参与
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
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_2": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	When jobs新建微信投票活动
		"""
		[{
			"title":"微信投票03",
			"subtitle":"微信投票03",
			"content":"谢谢投票",
			"start_date":"3天前",
			"end_date":"明天",
			"permission":"无需关注即可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"text_options":
				[{
					"title":"选择题1",
					"type":"单选",
					"is_required":"否",
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
					"is_required":"是",
					"option":[{
							"options":"A"
						},{
							"options":"B"
						},{
							"options":"C"
						}]
				}],
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

	#会员参与
		When 清空浏览器
		When bill参加微信投票活动"微信投票03"于"今天"
			"""
			{
				"文本选项":
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
					},{
						"title":"选择题2",
						"value":[{
								"title":"A",
								"type":"多选",
								"isSelect":"是"
							},{
								"title":"B",
								"type":"多选",
								"isSelect":"是"
							},{
								"title":"C",
								"type":"多选",
								"isSelect":"否"
							}]
					}],
				"参与人信息":
				[{
					"value":{
						"姓名":"bill",
						"手机":"15111223344",
						"填写项1":"",
						"填写项2":""
					}
				}]
			}
			"""
		#Then bill获得信息提示"提交成功"
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
		When tom参加微信投票活动"微信投票03"于"今天"
			"""
			{
				"文本选项":
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
					},{
						"title":"选择题2",
						"value":[{
								"title":"A",
								"type":"多选",
								"isSelect":"是"
							},{
								"title":"B",
								"type":"多选",
								"isSelect":"否"
							},{
								"title":"C",
								"type":"多选",
								"isSelect":"否"
							}]
					}],
				"参与人信息":
				[{
					"value":{
						"姓名":"tom",
						"手机":"15211223344",
						"填写项1":"",
						"填写项2":""
					}
				}]
			}
			"""
		#Then tom获得信息提示"提交成功"
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
		When lily关注jobs的公众号
		When lily取消关注jobs的公众号
		When lily参加微信投票活动"微信投票03"于"今天"
			"""
			{
				"文本选项":
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
					},{
						"title":"选择题2",
						"value":[{
								"title":"A",
								"type":"多选",
								"isSelect":"否"
							},{
								"title":"B",
								"type":"多选",
								"isSelect":"是"
							},{
								"title":"C",
								"type":"多选",
								"isSelect":"否"
							}]
					}],
				"参与人信息":
				[{
					"value":{
						"姓名":"lily",
						"手机":"15311223344",
						"填写项1":"",
						"填写项2":""
					}
				}]
			}
			"""
		#Then lily获得信息提示"提交成功"
		When lily关注jobs的公众号
		When lily访问jobs的webapp
		Then lily能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_3",
				"money": 100.00,
				"status": "未使用"
			}]
			"""