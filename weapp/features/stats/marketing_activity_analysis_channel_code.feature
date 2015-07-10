#_author_:张三香

Feature:营销活动分析-渠道扫码
"""
#备注信息：
  1、渠道扫码活动分析列表中的'参与次数/人数'统计规则（与渠道扫码一致）：
     前提：渠道码设置为'已关注会员可参与'
     a.同一用户多次扫同一个渠道二维码时，参与次数不累加；
     b.同一用户扫码多个渠道二维码时，'参与次数/人数'只被统计在最后扫的那个渠道码中
     c.用户a关注某渠道二维码后，取消关注后，'参与次数/人数'不减少，再扫码关注时，'参与次数/人数'不增加
  2、渠道扫码活动分析列表按照创建时间倒序排列（翻页，每页10条数据）
  3、渠道扫码活动'结果分析'浮层中包含的字段：
     被推荐用户数：通过该渠道二维码新增的会员数 
     被推荐用户下单人数：通过该渠道二维码新增的会员下单人数
     被推荐用户下单单数：通过该渠道二维码新增的会员总下单数
     被推荐用户下单金额：通过该渠道二维码新增的所有会员下单总金额，包括完成在线支付与货到付款的订单
     推荐扫码下单转换率：被推荐用户下单人数/被推荐用户数
     复购用户数：截止查询时间点，通过该活动新增的会员，下单次数大于等于2的会员总数
     复购订单数：截止查询时间点，通过该活动新增的会员，下单次数大于等于2的所有会员的订单总数
     复购总金额：截止查询时间点，通过该活动新增的会员，下单次数大于等于2的所有会员的订单总金额
"""

Background:
	Given jobs登录系统

	And jobs设定会员积分策略
		#"integral_each_yuan": 10
		"""
		{
			"一元等价的积分数量": 10
		}
		"""

	And jobs已添加'渠道扫码'营销活动
		"""
		[{
			"setting_id": 0,
			"name": "渠道扫码03",
			"prize_info": "{\"id\":-1, \"name\": \"non-prize\", \"type\": \"积分\"}",
			"reply_type": 0,
			"reply_material_id": 0,
			"re_old_member": 0,
			"remark": "备注1",
			"create_time":"2015-06-25 09:00:00",
			"authority":"否"
		}, {
			"setting_id": 0,
			"name": "渠道扫码02",
			"prize_info": "{\"id\":-1, \"name\": \"non-prize\", \"type\": \"积分\"}",
			"reply_type": 0,
			"reply_material_id": 0,
			"re_old_member": 0,
			"grade_id": 16,
			"remark": "备注2",
			"create_time":"2015-06-24 10:00:00",
			"authority":"是"
		}, {
			"setting_id": 0,
			"name": "渠道扫码01",
			"prize_info": "{\"id\":-1, \"name\": \"non-prize\", \"type\": \"积分\"}",
			"reply_type": 0,
			"reply_material_id": 0,
			"re_old_member": 0,
			"grade_id": 16,
			"remark": "备注3",
			"create_time":"2015-06-24 09:00:00",
			"authority":"是"
		}]
		"""
     When jobs已设置未付款订单过期时间
         """
         {
          "no_payment_order_expire_day":"1天"
         }
         """

	When jobs已添加商品
		"""
		[{
			"name": "商品1",
			"promotion_title": "促销商品1",
			"detail": "商品1详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"freight":"10",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"synchronized_mall":"是"
		}, {
			"name": "商品2",
			"promotion_title": "促销商品2",
			"detail": "商品2详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"freight":"15",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"synchronized_mall":"是"
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		}, {
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"is_active": "启用"
		}]
		"""
	And jobs开通使用微众卡权限
	And jobs添加支付方式
		"""
		[{
			"type": "微众卡支付",
			"description": "我的微众卡支付",
			"is_active": "启用"
		}]
		"""
	And jobs添加优惠券规则
		"""
		[{
			"name": "ss",
			"money": 10,
			"start_date": "2015-06-20",
			"end_date": "30天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	
	 And bill关注jobs的公众号
	 And tom关注jobs的公众号
	 # added by Victor
	 #And kate关注jobs的公众号
	 #And bob关注jobs的公众号
	 #And jim关注jobs的公众号


#营销活动分析-'渠道扫码'
@stats @wip.channel
Scenario:0 一个用户扫描多个渠道二维码,均设置已关注会员可参与
     #1、bill扫'渠道扫码01'
     #2、bill取消关注，扫'渠道扫码02'，只扫码不关注
     #3、bill取消关注扫'渠道扫码02'，并关注
     #4、bill扫'渠道扫码03'，已关注会员不可参与
	Given jobs登录系统
	Then jobs能看到的渠道扫码列表
		"""
		[{
			"name": "渠道扫码03",
			"remark": "备注1"
		}, {
			"name": "渠道扫码02",
			"remark": "备注2"
		}, {
			"name": "渠道扫码01",
			"remark": "备注3"
		}]
		"""
	#When bill扫描'渠道扫码01'二维码
	When bill通过扫描'渠道扫码01'二维码关注
	
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		|name            | manager  | parti_times | parti_person_cnt | status   | status_text |
		| 渠道扫码01     | jobs     |        1    | 1                | 1        | 已启动      |
		| 渠道扫码02     | jobs     |        0    | 0                | 1        | 已启动      |
		| 渠道扫码03     | jobs     |        0    | 0                | 1        | 已启动      |

	When bill取消关注jobs的公众号
	#When bill扫描'渠道扫码02'二维码
	#When bill通过扫描'渠道扫码02'二维码关注
	
	#Given jobs登录系统
	#Then 获取'渠道扫码'营销活动分析列表
	#	|name            | manager  | parti_times | parti_person_cnt | status   | status_text |
	#	| 渠道扫码01     | jobs     |        1    | 1                | 1        | 已启动      |
	#	| 渠道扫码02     | jobs     |        0    | 0                | 1        | 已启动      |
	#	| 渠道扫码03     | jobs     |        0    | 0                | 1        | 已启动      |

	#When bill扫描'渠道扫码02'二维码关注
	When bill通过扫描'渠道扫码02'二维码关注
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		# 原来是: 渠道扫码01, parti_times=0, parti_person_cnt=0
		|name            | manager  | parti_times | parti_person_cnt | status   | status_text |
		| 渠道扫码01     | jobs     |        0    | 0                | 1        | 已启动      |
		| 渠道扫码02     | jobs     |        1    | 1                | 1        | 已启动      |
		| 渠道扫码03     | jobs     |        0    | 0                | 1        | 已启动      |

	#渠道扫码03，设置为已关注会员不可参与
	#When bill扫描'渠道扫码03'二维码
	When bill通过扫描'渠道扫码03'二维码关注
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		|name            | manager  | parti_times | parti_person_cnt | status   | status_text |
		| 渠道扫码01     | jobs     |        0    | 0                | 1        | 已启动      |
		| 渠道扫码02     | jobs     |        1    | 1                | 1        | 已启动      |
		| 渠道扫码03     | jobs     |        0    | 0                | 1        | 已启动      |



# TODO: 目前的渠道扫码状态是，扫了就算次数
@stats @wip.channel2
Scenario:1 同一用户多次扫同一个二维码不重复记(设置已关注会员可参与)
	#1、bill扫“渠道扫码01”；（参与次数/人数为：1/1）
	#2、bill再扫“渠道扫码01”；(参与次数/人数为：1/1)
	#3、bill取消关注；        (参与次数/人数为：1/1)
	#4、bill取消关注后再扫“渠道扫码01”；(参与次数/人数为：1/1)

	Given jobs登录系统
	Then jobs能看到的渠道扫码列表
		"""
		[{
			"name": "渠道扫码03",
			"remark": "备注1"
		}, {
			"name": "渠道扫码02",
			"remark": "备注2"
		}, {
			"name": "渠道扫码01",
			"remark": "备注3"
		}]
		"""
	When bill通过扫描'渠道扫码01'二维码关注
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		|name            | manager  | parti_times | parti_person_cnt | status   | status_text |
		| 渠道扫码01     | jobs     |        1    | 1                | 1        | 已启动      |
		| 渠道扫码02     | jobs     |        0    | 0                | 1        | 已启动      |
		| 渠道扫码03     | jobs     |        0    | 0                | 1        | 已启动      |

	When bill通过扫描'渠道扫码01'二维码关注
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		|name            | manager  | parti_times | parti_person_cnt | status   | status_text |
		| 渠道扫码01     | jobs     |        1    | 1                | 1        | 已启动      |
		| 渠道扫码02     | jobs     |        0    | 0                | 1        | 已启动      |
		| 渠道扫码03     | jobs     |        0    | 0                | 1        | 已启动      |

	When bill取消关注jobs的公众号
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		|name            | manager  | parti_times | parti_person_cnt | status   | status_text |
		| 渠道扫码01     | jobs     |        1    | 1                | 1        | 已启动      |
		| 渠道扫码02     | jobs     |        0    | 0                | 1        | 已启动      |
		| 渠道扫码03     | jobs     |        0    | 0                | 1        | 已启动      |

	When bill通过扫描'渠道扫码01'二维码关注
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		|name            | manager  | parti_times | parti_person_cnt | status   | status_text |
		| 渠道扫码01     | jobs     |        1    | 1                | 1        | 已启动      |
		| 渠道扫码02     | jobs     |        0    | 0                | 1        | 已启动      |
		| 渠道扫码03     | jobs     |        0    | 0                | 1        | 已启动      |


@stats @wip.channel3
Scenario:2 同一用户扫多个二维码，已关注会员扫'已关注会员不可参与'的二维码
"""
	1、bill扫“渠道扫码01”；（参与次数/人数为：1/1 参与次数/人数为：0/0）
	2、bill再扫“渠道扫码03”；(参与次数/人数为：1/1 参与次数/人数为：0/0)
	3、bill取消关注；        (参与次数/人数为：1/1 参与次数/人数为：0/0)
	4、bill取消关注后再扫“渠道扫码03”关注；(参与次数/人数为：1/1 参与次数/人数为：0/0)
"""

	Given jobs登录系统
	Then jobs能看到的渠道扫码列表
		"""
		[{
			"name": "渠道扫码03",
			"remark": "备注1"
		}, {
			"name": "渠道扫码02",
			"remark": "备注2"
		}, {
			"name": "渠道扫码01",
			"remark": "备注3"
		}]
		"""
	When bill通过扫描'渠道扫码01'二维码关注
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		| name            | manager  | parti_times | parti_person_cnt | status   | status_text |
		| 渠道扫码01     | jobs     |        1    | 1                | 1        | 已启动      |
		| 渠道扫码02     | jobs     |        0    | 0                | 1        | 已启动      |
		| 渠道扫码03     | jobs     |        0    | 0                | 1        | 已启动      |

	When bill通过扫描'渠道扫码03'二维码关注
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		| name            | manager  | parti_times | parti_person_cnt | status   | status_text |
		| 渠道扫码01     | jobs     |        1    | 1                | 1        | 已启动      |
		| 渠道扫码02     | jobs     |        0    | 0                | 1        | 已启动      |
		| 渠道扫码03     | jobs     |        0    | 0                | 1        | 已启动      |

	When bill取消关注jobs的公众号
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		| name            | manager  | parti_times | parti_person_cnt | status   | status_text |
		| 渠道扫码01     | jobs     |        1    | 1                | 1        | 已启动      |
		| 渠道扫码02     | jobs     |        0    | 0                | 1        | 已启动      |
		| 渠道扫码03     | jobs     |        0    | 0                | 1        | 已启动      |

	When bill通过扫描'渠道扫码03'二维码关注
	Given jobs登录系统
	Then 获取'渠道扫码'营销活动分析列表
		| name            | manager  | parti_times | parti_person_cnt | status   | status_text |
		| 渠道扫码01     | jobs     |        1    | 1                | 1        | 已启动      |
		| 渠道扫码02     | jobs     |        0    | 0                | 1        | 已启动      |
		| 渠道扫码03     | jobs     |        0    | 0                | 1        | 已启动      |


@wip.channel4
Scenario:3 '渠道扫码'活动分析的参与传播和结果分析
     #1.取消关注后再扫渠道码关注的会员不属于'被推荐用户'
     #2.被推荐用户扫渠道码关注之前下的订单（非会员方式下的订单）不统计在被推荐用户订单里面

	Given jobs登录系统
	Then jobs能看到的渠道扫码列表
		"""
		[{
			"name": "渠道扫码03",
			"remark": "备注1"
		}, {
			"name": "渠道扫码02",
			"remark": "备注2"
		}, {
			"name": "渠道扫码01",
			"remark": "备注3"
		}]
		"""

	 #取消关注的会员再扫渠道二维码关注，不属于仅通过扫该码新增的会员(被推荐用户)
	 #账号名称前'-'代表取消关注的会员,账号名称前'*'代表非会员,非会员购买商品时，买家为空，获取不到买家信息
	 #bob jim kate 为通过渠道扫码01新关注的会员	
	When tom取消关注jobs的公众号
	And 微信用户已参加'渠道扫码'营销活动
		| activity_name  | responsible_person | authority |awards      |creat_time          | participant |share_to        |from_who |
		| 渠道扫码01    | jobs               | 是        | [优惠券]ss |2015-06-17 08:00:00 | bill 	|                |         |
		| 渠道扫码01    | jobs               | 是        | [优惠券]ss |2015-06-17 08:00:00 | tom	| bill1          |         |
		| 渠道扫码01    | jobs               | 是        | [优惠券]ss |2015-06-17 08:00:00 | -bob	|                |         |
		| 渠道扫码01    | jobs               | 是        | [优惠券]ss |2015-06-17 08:00:00 | -jim 	| bill01,bill,bob| bill    |
		| 渠道扫码01    | jobs               | 是        | [优惠券]ss |2015-06-17 08:00:00 | -kate     |                | bill1   |

			#|date                 |activity_name  | responsible_person | create_time          |status  | participant |authority |
			#|2015-06-24 09:10:00  | 渠道扫码01    | jobs               | 2015-06-24 09:00:00  |已启动  | bill        | 是       |
			#|2015-06-24 09:10:00  | 渠道扫码01    | jobs               | 2015-06-24 09:00:00  |已启动  | -tom        | 是       |       
			#|2015-06-24 09:10:00  | 渠道扫码01    | jobs               | 2015-06-24 09:00:00  |已启动  | *bob        | 是       |
			#|2015-06-24 09:10:00  | 渠道扫码01    | jobs               | 2015-06-24 09:00:00  |已启动  | *jim        | 是       |
			#|2015-06-24 09:10:00  | 渠道扫码01    | jobs               | 2015-06-24 09:00:00  |已启动  | *kate       | 是       |  

	And 微信用户批量消费jobs的商品
		| date 	| consumer | type |businessman | product 	| integral 	| coupon	| payment 	| action |
		| 今天 	| bill 		| 购买 | jobs      		| 商品1,1 	|  			| 1      		| 支付 		|  		|
		| 今天 	| bill 		| 购买 | jobs      		| 商品1,1 	|  			| 1      		| 支付 		|  		|
		| 今天 	| tom 		| 购买 | jobs      		| 商品1,1 	|  			| 1      		| 	 		|  		|
		| 今天 	| -bob 		| 购买 | jobs      		| 商品1,1 	|  			| 1      		| 支付 		|  		|
		| 今天 	| bob 		| 购买 | jobs      		| 商品1,1 	|  			| 1      		| 支付 		|  		|
		| 今天 	| bob 		| 购买 | jobs      		| 商品1,1 	|  			| 1      		| 支付 		|  		|
		| 今天 	| bob 		| 购买 | jobs      		| 商品1,1 	|  			| 1      		| 支付 		|  		|
		| 今天 	| bob 		| 购买 | jobs      		| 商品1,1 	|  			| 1      		| 支付 		| jobs,取消	|
		| 今天 	| jim 		| 购买 | jobs      		| 商品1,1 	|  			| 1      		| 支付 		|  		|
		| 今天 	| jim 		| 购买 | jobs      		| 商品1,1 	|  			| 1      		| 支付 		|  		|
		| 今天 	| jim 		| 购买 | jobs      		| 商品1,1 	|  			| 1      		| 支付 		|  		|
	     #| date          | consumer | member_source       | businessman | product        | payment | payment_method    | freight |price     | integral | coupon | paid_amount | weizoom_card | alipay | wechat | cash |  order_status   |
	     #| 2015-06-24 11:00:00 | bill    |直接关注,渠道扫码01 | jobs      | 商品1,1       | 支付    | 支付宝支付        | 10      | 100      | 0        | 0      | 110         | 0            | 110    | 0      | 0    |  待发货         |
	     #| 2015-06-24 11:10:00 | bill    |直接关注,渠道扫码01 | jobs      | 商品1,1       | 支付    | 微信支付          | 10      | 100      | 0        | 0      | 110         | 0            | 0      | 110    | 0    |  已发货         |
	     #| 2015-06-24 12:00:00 | tom     |直接关注,渠道扫码01 | jobs      | 商品1,1       | 未支付  | 支付宝支付        | 10      | 100      | 0        | 0      | 110         | 0            | 0      | 0      | 0    |  待支付         |
	     #| 2015-06-23 12:00:00 | *bob    |                    | jobs      | 商品1,1       | 支付    | 支付宝支付        | 10      | 100      | 0        | 0      | 110         | 0            | 110    | 0      | 0    |  待发货         |
	     #| 2015-06-24 11:00:00 | bob     |直接关注, 渠道扫码01| jobs      | 商品1,1,商品2 | 支付    | 微信支付          | 10,15   | 100,100  | 0        | 10     | 215         | 0            | 0      | 215    | 0    |  待发货         |
	     #| 2015-06-24 12:00:00 | bob     |直接关注, 渠道扫码01| jobs      | 商品1,1       | 支付    | 货到付款          | 10      | 100      | 0        | 0      | 110         | 0            | 0      | 0      | 110  |  已发货         |
	     #| 2015-06-24 13:00:00 | bob     |直接关注, 渠道扫码01| jobs      | 商品1,1,商品2 | 支付    | 支付宝支付        | 10,15   | 100,100  | 0        | 0      | 225         | 0            | 225    | 0      |  0   |  已完成         |
	     #| 2015-06-24 14:00:00 | bob     |直接关注, 渠道扫码01| jobs      | 商品1,1       | 支付    | 货到付款          | 10      | 100      | 0        | 0      | 110         | 0            | 0      | 0      | 110  |  已取消         |
	     #| 2015-06-25 14:10:00 | jim     |直接关注, 渠道扫码01| jobs      | 商品1,1       | 支付    | 货到付款          | 10      | 100      | 0        | 0      | 110         | 0            | 0      | 0      | 110  |  已发货         |
	     #| 2015-06-25 14:20:00 | jim     |直接关注, 渠道扫码01| jobs      | 商品1,1       | 支付    | 货到付款          | 10      | 100      | 0        | 0      | 110         | 0            | 0      | 0      | 110  |  退款中         |
	     #| 2015-06-25 14:30:00 | jim     |直接关注, 渠道扫码01| jobs      | 商品1,1       | 支付    | 货到付款          | 10      | 100      | 0        | 0      | 110         | 0            | 0      | 0      | 110  |  退款完成       |

	Given jobs登录系统
	Then 获得'渠道扫码'营销分析中'渠道扫码01'的'参与传播'信息
		"""
		{
			"children": [
				"bill",
				"tom",
				"kate",
				"bob",
				"jim"
			]
		}
		"""
	And 获得'渠道扫码'营销分析中'渠道扫码01'的'结果分析'信息
		"""
		{
			"被推荐用户数": 3,
			"被推荐用户下单人数": 2,
			"被推荐用户下单单数": 4,
			"被推荐用户下单金额": 660,
			"推荐扫码下单转换率": "66.67%",
			"复购用户数": 1,
			"复购订单数": 2,
			"复购总金额": 335
		}
		"""
     #suggested_members-被推荐用户数
     #suggested_ordered_members-被推荐用户下单人数
     #suggested_member_orders-被推荐用户下单单数
     #suggested_member_money-被推荐用户下单金额
     #order_conversion_rate-推荐扫码下单转换率
     #re_purchase_members-复购用户数
     #re_purchase_orders-复购订单数
     #re_purchase_money-复购总金额

     #| name              |suggested_members  | suggested_ordered_members| suggested_member_orders |suggested_member_money |order_conversion_rate |re_purchase_members  |re_purchase_orders   |re_purchase_money  |
     #| 渠道扫码01        | 3                 |              2           |             4           |       660             |       66.67%         |  1                  | 2                   |  335              | 


Scenario:4 '渠道扫码'营销活动分析列表及分页
    #列表按照渠道扫码的创建时间倒序排列
    #有翻页，每页显示10条数据
	Given jobs登录系统
	Then jobs获取渠道扫码列表
		"""
		[{
			"name": "渠道扫码03",
			"remark": "备注1"
		}, {
			"name": "渠道扫码02",
			"remark": "备注2"
		}, {
			"name": "渠道扫码01",
			"remark": "备注3"
		}]
		"""
	When bill已扫描'渠道扫码01'二维码
	Given jobs登录系统
	When jobs已设置分页条件
		"""
		{
			"page_count":1
		}
		"""
     Then jobs获取'渠道扫码'营销活动分析列表
        |name            | manager  | parti_times | parti_person_cnt |  start_at           |end_at    | status   | status_text |
		| 渠道扫码03     | jobs     |        0    | 0                |2015-06-25 09:00:00  |          | 1        | 已启动      |
		
	 And jobs获取显示共3页
	 When jobs浏览'下一页'
	 Then jobs获取'渠道扫码'营销活动分析列表
	    |name            | manager  | parti_times | parti_person_cnt |  start_at           |end_at    | status   | status_text |
	    | 渠道扫码02     | jobs     |        0    | 0                |2015-06-24 10:00:00  |          | 1        | 已启动      |
	 When jobs浏览'第3页'
	 Then jobs获取'渠道扫码'营销活动分析列表
	    |name            | manager  | parti_times | parti_person_cnt |  start_at           |end_at    | status   | status_text |
		| 渠道扫码01     | jobs     |        1    | 1                |2015-06-24 09:00:00  |          | 1        | 已启动      |
	 When jobs浏览'上一页'
	 Then jobs获取'渠道扫码'营销活动分析列表
	    |name            | manager  | parti_times | parti_person_cnt |  start_at           |end_at    | status   | status_text |
	    | 渠道扫码02     | jobs     |        0    | 0                |2015-06-24 10:00:00  |          | 1        | 已启动      |
