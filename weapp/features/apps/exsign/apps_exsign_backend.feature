# __author__ : 邓成龙 2016.07.06
Feature: 后台配置数据
	"""
		用户通过jobs签到成功,活动签到奖励
		1.【活动名称】:不能为空
		2.【签到设置】:每日和连续签到天数获得奖励
	    3.  【会员等级】:会员等级取商城中会员设置的会员等级
		4.【奖励条件】:每日签到获得？奖励；连续？天获得？奖励
		5.【领取方式】:通过回复关键字和快捷按钮签到
		6.配置后台所有数据,优惠券数量足,没有过期
		7.一条奖励下,不添加优惠券,有积分
		8.一条奖励下,添加优惠券,不添加积分
		9.一条奖励下,添加优惠券,添加积分
		10.三条奖励下,一条优惠券,一条积分,一条优惠券加积分
		11.删除优惠券信息
		12.优惠券数量为0,无法添加优惠券
		13.保存后开启签到活动

		【feature注意事项】:
		1.每个添加签到活动的场景中，"sign_settings"集合中的"prize_counts":50，其中prize_counts表示优惠券的库存，这里是一个由于占位需要提供的库存数字，数字可以任意。真实的库存数据，由前端脚本获取。

	"""

Background:
	Given jobs登录系统
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""

	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money":1.00,
			"count":50,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		},{
			"name": "优惠券2",
			"money":1.00,
			"count":50,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	When jobs已添加单图文
		"""
		[{
			"title":"签到活动1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"签到1",
			"content":"签到1",
			"jump_url":"签到活动1"
		}]
		"""
	And jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword":
				[{
					"keyword": "签到1",
					"type": "equal"
				}],
			"keyword_reply":
				[{
					"reply_content":"签到活动1",
					"reply_type":"text_picture"
				}]
		}]
		"""

@mall2 @apps @apps_exsign @apps_exsign_backend
Scenario:1 配置后台所有数据,优惠券数量足,没有过期
#各种等级的会员,相同会员得到的不同优惠券和积分
	When jobs添加专项签到活动"签到活动1",并且保存
		"""
		{
			"status":"off",
			"name": "签到活动1",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",
			"share_pic":"1.jpg",
			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "100",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				},{
					"sign_in": "5",
					"integral": "1000",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"全部"
					}]
					
				}]
		}
		"""
	Then jobs获得专项签到活动"签到活动1"
		"""
		{
			"status":"off",
			"name": "签到活动1",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",
			"share_pic":"1.jpg",
			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "100",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				},{
					"sign_in": "5",
					"integral": "1000",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"全部"
					}]
					
				}]
		}
		"""

@mall2 @apps @apps_exsign @apps_exsign_backend
Scenario:2 一条奖励下,不添加优惠券,有积分
	When jobs添加专项签到活动"签到活动2",并且保存
		"""
		{
			"status":"off",
			"name": "签到活动2",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",
			"share_pic":"2.jpg",
			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "100"
				}]
		}
		"""
	Then jobs获得专项签到活动"签到活动2"
		"""
		{
			"status":"off",
			"name": "签到活动2",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",
			"share_pic":"2.jpg",
			"share_describe": "签到获得奖励",
			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "100"
				}]
		}
		"""

@mall2 @apps @apps_exsign @apps_exsign_backend
Scenario:3 一条奖励下,添加优惠券,不添加积分
	When jobs添加专项签到活动"签到活动3",并且保存
		"""
		{
			"status":"off",
			"name": "签到活动3",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",
			"share_pic":"3.jpg",
			"sign_settings":
				[{
					"sign_in": "0",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				}]
		}
		"""
	Then jobs获得专项签到活动"签到活动3"
		"""
		{
			"status":"off",
			"name": "签到活动3",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",
			"share_pic":"3.jpg",
			"sign_settings":
				[{
					"sign_in": "0",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				}]
		}
		"""

@mall2 @apps @apps_exsign @apps_exsign_backend
Scenario:4 三条奖励下,一条优惠券,一条积分,一条优惠券加积分
	When jobs添加专项签到活动"签到活动5",并且保存
		"""
		{
			"status":"off",
			"name": "签到活动5",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",
			"share_pic":"5.jpg",
			"sign_settings":
				[{
					"sign_in": "0",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				},{
					"sign_in": "3",
					"integral": "300"
				},{
					"sign_in": "5",
					"integral": "500",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				}]
		}
		"""
	Then jobs获得专项签到活动"签到活动5"
		"""
		{
			"status":"off",
			"name": "签到活动5",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",
			"share_pic":"5.jpg",
			"share_describe": "签到获得奖励",
			"reply_content":"签到",
			"sign_settings":
				[{
					"sign_in": "0",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				},{
					"sign_in": "3",
					"integral": "300"
				},{
					"sign_in": "5",
					"integral": "500",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				}]
		}
		"""

@mall2 @apps @apps_exsign @apps_exsign_backend
Scenario:5 更新签到活动的状态
	When jobs添加专项签到活动"签到活动7",并且保存
		"""
		{
			"status":"off",
			"name": "签到活动7",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",
			"share_pic":"7.jpg",
			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "100",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				},{
					"sign_in": "3",
					"integral": "300",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				},{
					"sign_in": "5",
					"integral": "500",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				}]
		}
		"""
	Then jobs的专项签到活动"签到活动7"状态为"关闭"
	#开启签到活动
	When jobs更新专项签到活动的状态
		"""
		{
			"name": "签到活动7",
			"status": "on"
		}
		"""
	Then jobs的专项签到活动"签到活动7"状态为"开启"
	#关闭签到活动
	When jobs更新专项签到活动的状态
		"""
		{
			"name": "签到活动7",
			"status": "off"
		}
		"""
	Then jobs的专项签到活动"签到活动7"状态为"关闭"

@mall2 @apps @apps_exsign @apps_exsign_backend @cl
Scenario:6 删除优惠券信息
	When jobs添加专项签到活动"签到活动7",并且保存
		"""
		{
			"status":"off",
			"name": "签到活动7",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",
			"share_pic":"7.jpg",
			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "100",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				},{
					"sign_in": "3",
					"integral": "300",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				},{
					"sign_in": "5",
					"integral": "500",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				}]
		}
		"""
	When jobs删除专项签到活动"签到活动7"的优惠券,并且保存
		"""
		{
			"status":"off",
			"name": "签到活动7",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",
			"share_pic":"7.jpg",
			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "100",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					}{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				},{
					"sign_in": "3",
					"integral": "300",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				}
				}]
		}
		"""
	Then jobs获得专项签到活动"签到活动5"
		"""
		{
			"status":"off",
			"name": "签到活动7",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",
			"share_pic":"7.jpg",
			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "100",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					}{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"金牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				},{
					"sign_in": "3",
					"integral": "300",
					"coupons":[{
						"send_coupon": "优惠券1",
						"prize_counts":50,
						"member_grade":"铜牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"银牌会员"
					},{
						"send_coupon": "优惠券2",
						"prize_counts":50,
						"member_grade":"金牌会员"
					}]
				}
				}]
		}
		"""

