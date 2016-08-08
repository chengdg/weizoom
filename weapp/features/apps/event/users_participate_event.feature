#_author_:王丽 2015.12.02

Feature:手机端用户参与活动报名
"""
	1 活动报名设置成"无需关注即可参与"：没有关注和取消关注、关注状态的微信账号都可以参与，没有关注的账号参与之后在结果中显示的头像和昵称为空
	2 活动报名设置成"必需关注才可参与"：没有关注和取消关注的微信账号都不可以参与，只有关注状态的微信账号可参与
	3 活动报名时间设置为未来时间，手机端显示请耐心等待活动开始
	4 活动报名时间设置成过去时间，手机端显示活动已结束
"""

@mall2 @apps @apps_event @apps_event_frontend @user_participate_event
Scenario:1 活动报名-无奖励-无需关注即可参与
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

	#会员
		When bill关注jobs的公众号
		When bill访问jobs的webapp

		When tom关注jobs的公众号
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
		Then bill获得提示"您已报名"

@mall2 @apps @apps_event @apps_event_frontend @user_participate_event
Scenario:2 活动报名-积分奖励-必须关注才可参与
	Given jobs登录系统
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

@mall2 @apps @apps_event @apps_event_frontend @user_participate_event
Scenario:3 活动报名-优惠券奖励-无需关注即可参与
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 3,
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
	When jobs新建活动报名
		"""
		[{
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
  		When tom关注jobs的公众号
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
		When lily访问jobs的webapp
		When lily取消关注jobs的公众号
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

@mall2 @apps @apps_event @apps_event_frontend @user_participate_event
Scenario:4 活动报名-设置未来时间-无需关注即可参与
	Given jobs登录系统
	When jobs新建活动报名
		"""
		[{
			"title":"活动报名-无奖励",
			"subtitle":"活动报名-副标题-无奖励",
			"content":"内容描述-无奖励",
			"start_date":"明天",
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
	#会员
		When bill关注jobs的公众号
		When bill访问jobs的webapp
		When bill参加活动报名'活动报名-无奖励'于'今天'
			"""
			{}
			"""
		Then bill获得提示"请等待活动开始..."
	#非会员参与
		When 清空浏览器
		When tom关注jobs的公众号
		When tom访问jobs的webapp
		When tom取消关注jobs的公众号
		When tom参加活动报名'活动报名-无奖励'于'今天'
			"""
			{}
			"""
		Then tom获得提示"请等待活动开始..."

@mall2 @apps @apps_event @apps_event_frontend @user_participate_event
Scenario:5 活动报名-设置过去时间-必须需关注即可参与
	Given jobs登录系统
	When jobs新建活动报名
		"""
		[{
			"title":"活动报名-无奖励",
			"subtitle":"活动报名-副标题-无奖励",
			"content":"内容描述-无奖励",
			"start_date":"前天",
			"end_date":"昨天",
			"permission":"必须关注才可参与",
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
	#会员
		When bill关注jobs的公众号
		When bill访问jobs的webapp
		When bill参加活动报名'活动报名-无奖励'于'今天'
			"""
			{}
			"""
		Then bill获得提示"活动已结束"

	#非会员参与
		When 清空浏览器
		When tom关注jobs的公众号
		When tom访问jobs的webapp
		When tom取消关注jobs的公众号
		When tom参加活动报名'活动报名-无奖励'于'今天'
			"""
			{}
			"""
		Then tom获得提示"活动已结束"

@apps @apps_event @apps_event_frontend @user_participate_event
Scenario:6 活动报名-优惠券奖励(限领一张优惠券)-无需关注即可参与
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 3,
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
	When jobs新建活动报名
		"""
		[{
			"title":"活动报名-优惠券(限领一张)",
			"subtitle":"活动报名-副标题-优惠券",
			"content":"内容描述-优惠券",
			"start_date":"3天前",
			"end_date":"1天后",
			"right":"无需关注即可参与",
			"prize_type": "优惠券",
			"coupon":"优惠券1",
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
			"items_add":[]
		}]
		"""

	#会员
		Given bill关注jobs的公众号
		When bill访问jobs的webapp

	#会员参与
		#给会员发放限领一张优惠券
		When jobs创建优惠券发放规则发放优惠券
			"""
			{
				"name": "优惠券1",
				"count": 1,
				"members": ["bill"]
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

		#通过参与活动领取限领一张优惠券，会员已经有一张，不能再领取到		
		When 清空浏览器
		When bill参加活动报名'活动报名-优惠券(限领一张)'于'今天'
			"""
			{
				"姓名":"bill",
				"手机":"15213265987"
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

@apps @apps_event @apps_event_frontend @user_participate_event
Scenario:7 活动报名-优惠券奖励(仅未下单优惠券)-无需关注即可参与
	Given 重置'apiserver'的bdd环境
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		}]
		"""
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 6,
			"limit_counts": "不限",
			"is_no_order_user":"true",
			"start_date": "4天前",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建活动报名
		"""
		[{
			"title":"活动报名-优惠券(仅未下单)",
			"subtitle":"活动报名-副标题-优惠券",
			"content":"内容描述-优惠券",
			"start_date":"3天前",
			"end_date":"1天后",
			"right":"无需关注即可参与",
			"prize_type": "优惠券",
			"coupon":"优惠券1",
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
			"items_add":[]
		}]
		"""

	#给存在不同订单状态的用户参与活动
		#未支付订单用户，可以领取优惠券
			Given bill关注jobs的公众号
			When bill访问jobs的webapp::apiserver
			When bill购买jobs的商品::apiserver
				"""
				{
					"order_id":"001",
					"pay_type": "微信支付",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then bill成功创建订单::apiserver
				"""
				{
					"order_no":"001",
					"status": "待支付",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			When 清空浏览器
			When bill参加活动报名'活动报名-优惠券(仅未下单)'于'今天'
				"""
				{
					"姓名":"bill",
					"手机":"15213265987"
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

		#待发货订单用户，不可以领取优惠券
			Given tom关注jobs的公众号
			When tom访问jobs的webapp::apiserver
			When tom购买jobs的商品::apiserver
				"""
				{
					"order_id":"002",
					"pay_type": "货到付款",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then tom成功创建订单::apiserver
				"""
				{
					"order_no":"002",
					"status": "待发货",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			When 清空浏览器
			When tom参加活动报名'活动报名-优惠券(仅未下单)'于'今天'
				"""
				{
					"姓名":"tom",
					"手机":"15213265987"
				}
				"""
			Then tom获得提示"提交成功"
			When tom访问jobs的webapp
			Then tom能获得webapp优惠券列表
				"""
				[]
				"""

		#已发货订单用户，不可以领取优惠券
			Given tom1关注jobs的公众号
			When tom1访问jobs的webapp::apiserver
			When tom1购买jobs的商品::apiserver
				"""
				{
					"order_id":"003",
					"pay_type": "货到付款",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then tom1成功创建订单::apiserver
				"""
				{
					"order_no":"003",
					"status": "待发货",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			When 清空浏览器
			When tom1参加活动报名'活动报名-优惠券(仅未下单)'于'今天'
				"""
				{
					"姓名":"tom1",
					"手机":"15213265987"
				}
				"""
			Then tom1获得提示"提交成功"
			When tom1访问jobs的webapp
			Then tom1能获得webapp优惠券列表
				"""
				[]
				"""

		#已完成订单用户，不可以领取优惠券
			Given tom2关注jobs的公众号
			When tom2访问jobs的webapp::apiserver
			When tom2购买jobs的商品::apiserver
				"""
				{
					"order_id":"004",
					"pay_type": "货到付款",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then tom2成功创建订单::apiserver
				"""
				{
					"order_no":"004",
					"status": "待发货",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			Given jobs登录系统
			When jobs对订单进行发货
				"""
				{
					"order_no": "004",
					"logistics": "申通快递",
					"number": "229388967650",
					"shipper": "jobs"
				}
				"""
			When jobs完成订单'004'

			When 清空浏览器
			When tom2参加活动报名'活动报名-优惠券(仅未下单)'于'今天'
				"""
				{
					"姓名":"tom2",
					"手机":"15213265987"
				}
				"""
			Then tom2获得提示"提交成功"
			When tom2访问jobs的webapp
			Then tom2能获得webapp优惠券列表
				"""
				[]
				"""
		
		#退款中和退款完成订单用户，可以领取优惠券
			Given tom3关注jobs的公众号
			When tom3访问jobs的webapp::apiserver
			When tom3购买jobs的商品::apiserver
				"""
				{
					"order_id":"005",
					"pay_type": "微信支付",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			When tom3使用支付方式'微信支付'进行支付
			Then tom3成功创建订单::apiserver
				"""
				{
					"order_no":"005",
					"status": "待发货",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			Given jobs登录系统
			When jobs对订单进行发货
				"""
				{
					"order_no": "004",
					"logistics": "申通快递",
					"number": "229388967650",
					"shipper": "jobs"
				}
				"""
			
			When jobs'申请退款'订单'005'

			When 清空浏览器
			When tom3参加活动报名'活动报名-优惠券(仅未下单)'于'今天'
				"""
				{
					"姓名":"tom3",
					"手机":"15213265987"
				}
				"""
			Then tom3获得提示"提交成功"
			When tom3访问jobs的webapp
			Then tom3能获得webapp优惠券列表
				"""
				[{
					"coupon_id": "coupon1_id_2",
					"money": 100.00,
					"status": "未使用"
				}]
				"""

		#已取消订单用户，可以领取优惠券
			Given tom4关注jobs的公众号
			When tom4访问jobs的webapp::apiserver
			When tom4购买jobs的商品::apiserver
				"""
				{
					"order_id":"006",
					"pay_type": "微信支付",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then tom4成功创建订单::apiserver
				"""
				{
					"order_no":"006",
					"status": "待支付",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			Given jobs登录系统
			When jobs取消订单'006'

			When 清空浏览器
			When tom4参加活动报名'活动报名-优惠券(仅未下单)'于'今天'
				"""
				{
					"姓名":"tom4",
					"手机":"15213265987"
				}
				"""
			Then tom4获得提示"提交成功"
			When tom4访问jobs的webapp
			Then tom4能获得webapp优惠券列表
				"""
				[{
					"coupon_id": "coupon1_id_3",
					"money": 100.00,
					"status": "未使用"
				}]
				"""