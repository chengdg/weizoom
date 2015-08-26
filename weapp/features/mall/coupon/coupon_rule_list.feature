
#_author_:张三香

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
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "优惠券1",
			"start_date": "明天",
			"end_date": "4天后",
			"status":"未开始",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "商品1"
		}, {
			"name": "优惠券2",
			"start_date": "今天",
			"end_date": "2天后",
			"status":"进行中",
			"coupon_id_prefix": "coupon2_id_"
		}, {
			"name": "优惠券3",
			"start_date": "今天",
			"end_date": "2天后",
			"status":"已失效",
			"coupon_id_prefix": "coupon3_id_"
		}, {
			"name": "优惠券4",
			"start_date": "3天前",
			"end_date": "1天前",
			"status":"已过期",
			"coupon_id_prefix": "coupon4_id_"
		}]
		"""

@promotion @promotionCoupon @online_bug
Scenario: 不同状态的优惠券规则,其操作列显示不同
	Given jobs登录系统
	Then jobs能获得优惠券规则列表
		"""
			[{
				"name": "优惠券4",
				"status":"已过期",
				"actions":["码库","删除"]
			},{
				"name": "优惠券3",
				"status":"已失效",
				"actions":["码库"]
			},{
				"name": "优惠券2",
				"status":"进行中",
				"actions":["码库","链接","编辑","查看","使失效"]
			},{
				"name": "优惠券1",
				"status":"未开始",
				"actions":["码库","链接","编辑","查看","使失效"]
			}]
		"""