#watcher:zhangsanxiang@weizoom.com,benchi@weizoom.com
#author:张三香

Feature:优惠券规则列表中,操作列信息的验证
		#说明：
			#针对线上"bug3854"补充feature
			#bug3854:【促销管理】-【优惠券】已过期的优惠券，其操作列信息显示不对#
			#不同状态的优惠券规则其操作列显示不同：
				#未开始：码库 链接 编辑 查看 使失效
				#进行中：码库 链接 编辑 查看 使失效
				#已失效：码库
				#已过期：码库 删除

Background:
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
			"money": 10.00, 
			"limit_counts": 10,
			"start_date": "明天",
			"end_date": "4天后",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "商品1"
		}, {
			"name": "优惠券2",
			"money": 10.00,
			"limit_counts": 10,
			"start_date": "今天",
			"end_date": "2天后",
			"coupon_id_prefix": "coupon2_id_"
		}, {
			"name": "优惠券3",
			"money": 10.00,
			"limit_counts": 10,
			"start_date": "今天",
			"end_date": "2天后",
			"coupon_id_prefix": "coupon3_id_"
		}, {
			"name": "优惠券4",
			"money": 10.00,
			"limit_counts": 10,
			"start_date": "3天前",
			"end_date": "1天前",
			"coupon_id_prefix": "coupon4_id_"
		}]
		"""

@mall2 @promotion @promotionCoupon @online_bug
Scenario: 不同状态的优惠券规则,其操作列显示不同
	Given jobs登录系统
	When jobs失效优惠券'优惠券3'
	Then jobs能获得优惠券状态列表
		"""
		[{
			"name": "优惠券4",
			"status":"已过期"
		},{
			"name": "优惠券3",
			"status":"已失效"
		},{
			"name": "优惠券2",
			"status":"进行中"
		},{
			"name": "优惠券1",
			"status":"未开始"
		}]
		"""