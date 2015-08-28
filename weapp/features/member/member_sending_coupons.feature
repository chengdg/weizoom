Feature: 群发优惠券
"""
	筛选出会员发送优惠券
	#除已跑路外
"""
@memberList
# __editor__ : "新新"
Scenario:15 筛选出会员发送优惠券
	#除已跑路外
	Given jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "单品券2",
			"money": 10.00,
			"each_limit": "不限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品1"
		}]
		"""
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_5": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_6": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_7": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_8": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_9": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_10": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

	Given nokia关注jobs的公众号
	Given tom关注jobs的公众号
	Given tom2关注jobs的公众号
	Given tom3关注jobs的公众号
	Given tom5关注jobs的公众号

	When jobs选择条件为
		"""
		{
			"member_rank":"普通会员"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "nokia",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"buy_time": "2014-12-31",
			"integral": 20,
			"friends_sum": 1,
			"sources": "会员分享",
			"packet": "分组2",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"buy_time": "2014-12-22",
			"integral": 20,
			"friends_sum": 2,
			"sources": "会员分享",
			"packet": "分组1",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 4,
			"buy_time": "2014-11-30",
			"integral": 220,
			"friends_sum": 2,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-11-30",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 500.00,
			"buy_sum": 5,
			"buy_time": "2014-09-01",
			"integral": 300,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-09-01",
			"status": "已关注"
		},{
			"name": "tom5",
			"member_rank": "普通会员",
			"price": 0.00,
			"buy_sum": 0,
			"buy_time": "2014-05-30",
			"integral": 20,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-01-03",
			"status": "已跑路"
		}]
		"""
	When jobs为会员发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 2,
			"members": ["nokia","tom","tom2","tom3"]
		}
		"""
	Then jobs优惠券发放成功
	When nokia访问jobs的webapp
	Then nokia能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_1",
				"money": 10.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_2",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_3",
				"money": 10.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_4",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	When tom2访问jobs的webapp
	Then tom2能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_5",
				"money": 10.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_6",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	When tom3访问jobs的webapp
	Then tom3能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_7",
				"money": 10.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_8",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	When tom5访问jobs的webapp
	Then tom5能获得webapp优惠券列表
		"""
		[]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "nokia"
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "nokia"
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			},
			"coupon2_id_5": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "tom2"
			},
			"coupon2_id_6": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "tom2"
			},
			"coupon2_id_7": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "tom3"
			},
			"coupon2_id_8": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "tom3"
			},
			"coupon2_id_9": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": "tom5"
			},
			"coupon2_id_10": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": "tom5"
			}
		}
		"""