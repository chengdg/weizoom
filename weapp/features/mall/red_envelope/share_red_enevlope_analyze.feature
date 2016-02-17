#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
# __author__ : "冯雪静"

Feature: 分享红包分析
"""
	1.jobs能获取分享红包分析统计
	2.jobs能获取分享红包分析详情
	3.jobs能获取分享红包-会员引入详情
"""

Background:
	Given jobs登录系统
	And jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00
		},{
			"name": "商品2",
			"price": 50.00
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "全体券1",
			"money": 100.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "单品券2",
			"money": 100.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "2天后",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品1"
		}]
		"""
	And jobs已添加分享红包
		"""
		[{
			"name": "红包1",
			"prize_info": "全体券1",
			"is_permanant_active": false,
			"start_date": "今天",
			"end_date": "2天后",
			"limit_money": "200",
			"receive_method": "下单领取",
			"detail": "活动说明",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"remark": "分享有礼"
		}, {
			"name": "红包2",
			"prize_info": "单品券2",
			"is_permanant_active": true,
			"limit_money": "无限制",
			"receive_method": "下单领取",
			"detail": "活动说明",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"remark": "分享有礼"
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号
	And jobs登录系统
	Then jobs能获得优惠券'全体券1'的码库
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
			},
			"coupon1_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

@mall2 @promotion @promotionRedbag
Scenario: 1 分享红包分析
	1.jobs能获取分享红包分析统计
	2.jobs能获取分享红包分析详情
	3.jobs能获取分享红包-会员引入详情

	Given jobs登录系统
	When jobs'开启'分享红包'红包1'
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"order_id": "00001",
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill'能够'领取分享红包
	When bill把jobs的分享红包链接分享到朋友圈
	When tom访问jobs的webapp
	When tom点击bill分享红包链接
  	#避免时间太短无法排序
  	When 休眠1秒
	#nokia是非会员
	#暂时用先关注再取消关注的方式来模拟非会员的情况，需要改进
	When nokia关注jobs的公众号
	And nokia取消关注jobs的公众号
	And nokia访问jobs的webapp
	And nokia点击bill分享红包链接

	When tom访问jobs的webapp
	And tom购买jobs的商品
		"""
		{
			"order_id": "00002",
			"products": [{
				"name": "商品1",
				"count": 1
			}, {
				"name": "商品2",
				"count": 2
			}],
			"coupon": "coupon1_id_2"
		}
		"""
	And tom使用支付方式'货到付款'进行支付
	Then tom'能够'领取分享红包

	Given jobs登录系统
	When jobs对订单进行发货
		"""
		{
			"order_no":"00002",
			"logistics":"顺丰速运",
			"number":"123456789",
			"shipper":"jobs"
		}
		"""
	When jobs'完成'最新订单
	Then jobs能获得分享红包"红包1"的分析统计
		"""
		[{
			"新关注人数": 0,
			"领取人数": 4,
			"产生消费": 100.00,
			"使用人数": 1
		}]
		"""
	Then jobs能获得分享红包"红包1"的分析详情
		| 下单会员 | 会员状态 | 引入领取人数 | 引入使用人数 | 引入新关注 | 引入消费额 | 领取时间 | 使用状态 | 操作         |
		| tom      | 普通会员 | 0            | 0            | 0          | 0.00        | 今天     | 未使用   | 查看引入详情 |
		| bill     | 普通会员 | 2            | 1            | 0          | 100.00      | 今天     | 未使用   | 查看引入详情 |

	Then jobs能获得分享红包'红包1-bill'订单号'00001'的引入详情
		| 分享会员 | 会员状态 | 引入领取人数 | 引入使用人数 | 引入新关注 | 引入消费额 | 领取时间 | 使用状态 | 操作         |
		| nokia    | 非会员   | 0            | 0            | 0          | 0.00       | 今天     | 未使用   |              |
		| tom      | 普通会员 | 0            | 0            | 0          | 0.00        | 今天     | 已使用   | 查看使用订单 |

	Then jobs能获得分享红包"红包2"的分析统计
		"""
		[{
			"新关注人数": 0,
			"领取人数": 0,
			"产生消费": 0.00,
			"使用人数": 0
		}]
		"""
	Then jobs能获得分享红包"红包2"的分析详情
		"""
		[]
		"""