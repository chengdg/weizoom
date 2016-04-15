#author:张三香
#editor: 王丽 2016.04.15

Feature:优惠券规则列表中,操作列信息的验证
		#说明：
			#针对线上"bug3854"补充feature
			#bug3854:【促销管理】-【优惠券】已过期的优惠券，其操作列信息显示不对#
			#不同状态的优惠券规则其操作列显示不同：
				#未开始：码库 链接 编辑 查看 使失效
				#进行中：码库 链接 编辑 查看 使失效
				#已失效：码库
				#已过期：码库 删除
		补充需求修改 2016.04.15
		1 查询字段【优惠券类型】："全部","通用券","多商品券"
		2 优惠券规则列表
			（1）【类型】字段值修改成"通用券"或"多商品券"
			（2）【有效期】字段折行显示
			（3）增加【专属商品】字段
					类型为“通用券”时，“专属商品”显示“全部”
					类型为“多商品券”时，“专属商品”显示“查看专属商品”按钮

		3 “查看专属商品”按钮
			查看对应的多商品券的商品列表
				【商品条码】：商品详情中的"商品条码"
				【商品名称】：商品详情中的"商品名称"
				【商品价格(元)】：商品详情中的"商品价格"
				【商品库存】：商品详情中的"商品库存"
				【状态】："在售"或"已下架"或"已删除"；当为"已下架"或"已删除"时，红色高亮显示
		4 优惠券规则列表按照优惠券规则的添加顺序倒序排列

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		},{
			"name": "商品2",
			"price": 200.00
		},{
			"name": "商品3",
			"price": 200.00
		},{
			"name": "商品3",
			"price": 200.00
		}]
		"""
	When jobs添加优惠券规则
		"""
		[{
			"name": "通用券-已失效",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_id_prefix": "coupon1_id_"
		},{
			"name": "通用券-进行中",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_id_prefix": "coupon2_id_"
		},{
			"name": "通用券-已过期",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "2天前",
			"end_date": "1天前",
			"description":"使用说明",
			"coupon_id_prefix": "coupon3_id_"
		},{
			"name": "多商品券-进行中",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_product": "商品1",
			"coupon_id_prefix": "coupon4_id_"
		},{
			"name": "多商品券-未开始",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "1天后",
			"end_date": "3天后",
			"description":"使用说明",
			"coupon_product": "商品2,商品3,商品4",
			"coupon_id_prefix": "coupon5_id_"
		}]
		"""
	When jobs失效优惠券'通用券-已失效'

@promotion @promotionCoupon @online_bug
Scenario:1 优惠券规则列表按照添加顺序倒序排列
	Given jobs登录系统
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "多商品券-未开始",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "1天后",
			"end_date": "3天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "未开始",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "多商品券-进行中",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "进行中",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "通用券-已过期",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "2天前",
			"end_date": "1天前",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已过期",
			"actions": ["码库","删除"]
		},{
			"name": "通用券-进行中",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "进行中",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "通用券-已失效",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已失效",
			"actions": ["码库"]
		}]
		"""

@promotion @promotionCoupon
Scenario:2 优惠券规则列表-多商品券(一个商品)商品下架、删除
	#添加多商品券-一个商品
	#多商品券商品全部下架，多商品券依然可用
	#多商品券商品全部删除，多商品券失效

	Given jobs登录系统

	#多商品券(一个商品)商品下架
	#优惠券不变，优惠券中的对应商品变为"已下架"
	When jobs'下架'商品'商品1'
	Then jobs获得优惠券规则'多商品券-进行中'
		"""
		{
			"name": "多商品券-进行中",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_product": "商品1",
			"products_status":[{
				"name": "商品1",
				"status": "已下架"
				}],
			"coupon_id_prefix": "coupon1_id_"
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "多商品券-未开始",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "1天后",
			"end_date": "3天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "未开始",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "多商品券-进行中",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "进行中",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "通用券-已过期",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "2天前",
			"end_date": "1天前",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已过期",
			"actions": ["码库","删除"]
		},{
			"name": "通用券-进行中",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "进行中",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "通用券-已失效",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已失效",
			"actions": ["码库"]
		}]
		"""
	Then jobs查看优惠券'多商品券-进行中'专属商品
		"""
		[{
			"name":"商品1",
			"status":"已下架"
		}]
		"""

	#多商品券(一个商品)商品删除
	#优惠券活动失效，优惠券中的对应商品变为"已删除"
	When jobs'删除'商品'商品1'
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "多商品券-未开始",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "1天后",
			"end_date": "3天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "未开始",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "多商品券-进行中",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已失效",
			"actions": ["码库"]
		},{
			"name": "通用券-已过期",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "2天前",
			"end_date": "1天前",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已过期",
			"actions": ["码库","删除"]
		},{
			"name": "通用券-进行中",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "进行中",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "通用券-已失效",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已失效",
			"actions": ["码库"]
		}]
		"""
	Then jobs查看优惠券'多商品券-进行中'专属商品
		"""
		[{
			"name":"商品1",
			"status":"已删除"
		}]
		"""

@promotion @promotionCoupon
Scenario:3 优惠券规则列表-多商品券(多个商品)商品下架、删除
	#添加多商品券-多个商品
	#多商品券商品部分下架，多商品券依然可用
	#多商品券商品全部下架，多商品券依然可用、
	#多商品券商品部分删除，多商品券依然可用
	#多商品券商品全部删除，多商品券失效

	#多商品券(多个商品)部分商品下架
	#优惠券不变，优惠券中的对应商品变为"已下架"
	When jobs'下架'商品'商品2'
	Then jobs获得优惠券规则'多商品券-未开始'
		"""
		{
			"name": "多商品券-未开始",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "1天后",
			"end_date": "3天后",
			"description":"使用说明",
			"coupon_product": "商品2,商品3,商品4",
			"products_status":[{
				"name": "商品2",
				"status": "已下架"
				},{
				"name": "商品3",
				"status": ""
				},{
				"name": "商品4",
				"status": ""
			}],
			"coupon_id_prefix": "coupon1_id_"
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "多商品券-未开始",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "1天后",
			"end_date": "3天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "未开始",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "多商品券-进行中",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "进行中",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "通用券-已过期",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "2天前",
			"end_date": "1天前",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已过期",
			"actions": ["码库","删除"]
		},{
			"name": "通用券-进行中",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "进行中",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "通用券-已失效",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已失效",
			"actions": ["码库"]
		}]
		"""
	Then jobs查看优惠券'多商品券-进行中'专属商品
		"""
		[{
			"name":"商品2",
			"status":"已下架"
		},{
			"name":"商品3",
			"status":"在售"
		},{
			"name":"商品4",
			"status":"在售"
		}]
		"""

	#多商品券(多个商品)全部商品下架
	#优惠券不变，优惠券中的对应商品变为"已下架"
	When jobs'下架'商品'商品3'
	When jobs'下架'商品'商品4'
	Then jobs获得优惠券规则'多商品券-未开始'
		"""
		{
			"name": "多商品券-未开始",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "1天后",
			"end_date": "3天后",
			"description":"使用说明",
			"coupon_product": "商品2,商品3,商品4",
			"products_status":[{
				"name": "商品2",
				"status": "已下架"
				},{
				"name": "商品3",
				"status": ""
				},{
				"name": "商品4",
				"status": ""
			}],
			"coupon_id_prefix": "coupon1_id_"
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "多商品券-未开始",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "1天后",
			"end_date": "3天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "未开始",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "多商品券-进行中",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "进行中",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "通用券-已过期",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "2天前",
			"end_date": "1天前",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已过期",
			"actions": ["码库","删除"]
		},{
			"name": "通用券-进行中",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "进行中",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "通用券-已失效",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已失效",
			"actions": ["码库"]
		}]
		"""
	Then jobs查看优惠券'多商品券-进行中'专属商品
		"""
		[{
			"name":"商品2",
			"status":"已下架"
		},{
			"name":"商品3",
			"status":"已下架"
		},{
			"name":"商品4",
			"status":"已下架"
		}]
		"""

	#多商品券(多个商品)部分商品删除
	#优惠券不变，优惠券中的对应商品变为"已删除"
	When jobs'删除'商品'商品2'
	Then jobs获得优惠券规则'多商品券-未开始'
		"""
		{
			"name": "多商品券-未开始",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "1天后",
			"end_date": "3天后",
			"description":"使用说明",
			"coupon_product": "商品2,商品3,商品4",
			"products_status":[{
				"name": "商品2",
				"status": "已下架"
				},{
				"name": "商品3",
				"status": ""
				},{
				"name": "商品4",
				"status": ""
			}],
			"coupon_id_prefix": "coupon1_id_"
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "多商品券-未开始",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "1天后",
			"end_date": "3天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "未开始",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "多商品券-进行中",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "进行中",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "通用券-已过期",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "2天前",
			"end_date": "1天前",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已过期",
			"actions": ["码库","删除"]
		},{
			"name": "通用券-进行中",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "进行中",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "通用券-已失效",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已失效",
			"actions": ["码库"]
		}]
		"""
	Then jobs查看优惠券'多商品券-进行中'专属商品
		"""
		[{
			"name":"商品2",
			"status":"已删除"
		},{
			"name":"商品3",
			"status":"已下架"
		},{
			"name":"商品4",
			"status":"已下架"
		}]
		"""

	#多商品券(多个商品)全部商品删除
	#优惠券活动失效，优惠券中的对应商品变为"已删除"
	When jobs'删除'商品'商品3'
	When jobs'删除'商品'商品4'
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "多商品券-未开始",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "1天后",
			"end_date": "3天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已失效",
			"actions": ["码库"]
		},{
			"name": "多商品券-进行中",
			"type": "多商品券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "查看专属商品",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "进行中",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "通用券-已过期",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "2天前",
			"end_date": "1天前",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已过期",
			"actions": ["码库","删除"]
		},{
			"name": "通用券-进行中",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "进行中",
			"actions": ["码库","链接","编辑","查看","使失效"]
		},{
			"name": "通用券-已失效",
			"type": "通用券",
			"money": 100.00,
			"limit_counts": 1,
			"remained_count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"special_product": "全部",
			"get_person_count": 0,
			"get_number": 0,
			"use_count": 0,
			"status": "已失效",
			"actions": ["码库"]
		}]
		"""
	Then jobs查看优惠券'多商品券-进行中'专属商品
		"""
		[{
			"name":"商品2",
			"status":"已删除"
		},{
			"name":"商品3",
			"status":"已删除"
		},{
			"name":"商品4",
			"status":"已删除"
		}]
		"""

@promotion @promotionCoupon
Scenario:4 优惠券规则列表查询
	Given jobs登录系统

	#按照"优惠券名称"查询
		#空查询
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"name":""
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "多商品券-未开始",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "1天后",
				"end_date": "3天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "未开始",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "多商品券-进行中",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-已过期",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "2天前",
				"end_date": "1天前",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已过期",
				"actions": ["码库","删除"]
			},{
				"name": "通用券-进行中",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-已失效",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已失效",
				"actions": ["码库"]
			}]
			"""

		#模糊匹配
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"name":"多商品券"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "多商品券-未开始",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "1天后",
				"end_date": "3天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "未开始",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "多商品券-进行中",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			}]
			"""

		#查询结果为空
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"name":"33"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[]
			"""

	#按照"优惠券码"查询
		#空查询
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"coupon_code":""
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "多商品券-未开始",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "1天后",
				"end_date": "3天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "未开始",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "多商品券-进行中",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-已过期",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "2天前",
				"end_date": "1天前",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已过期",
				"actions": ["码库","删除"]
			},{
				"name": "通用券-进行中",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-已失效",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已失效",
				"actions": ["码库"]
			}]
			"""

		#模糊匹配
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"coupon_code":"coupon1_id_"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "通用券-已失效",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已失效",
				"actions": ["码库"]
			}]
			"""

		#查询结果为空
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"coupon_code":"33"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[]
			"""

	#按照"优惠券类型"查询
		#全部
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"coupon_type":"全部"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "多商品券-未开始",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "1天后",
				"end_date": "3天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "未开始",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "多商品券-进行中",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-已过期",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "2天前",
				"end_date": "1天前",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已过期",
				"actions": ["码库","删除"]
			},{
				"name": "通用券-进行中",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-已失效",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已失效",
				"actions": ["码库"]
			}]
			"""

		#通用券
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"coupon_type":"通用券"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "通用券-已过期",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "2天前",
				"end_date": "1天前",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已过期",
				"actions": ["码库","删除"]
			},{
				"name": "通用券-进行中",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-已失效",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已失效",
				"actions": ["码库"]
			}]
			"""

		#多商品券
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"coupon_type":"多商品券"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "多商品券-未开始",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "1天后",
				"end_date": "3天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "未开始",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "多商品券-进行中",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			}]
			"""

	#按照"促销状态"查询
		#全部
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"status":"全部"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "多商品券-未开始",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "1天后",
				"end_date": "3天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "未开始",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "多商品券-进行中",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-已过期",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "2天前",
				"end_date": "1天前",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已过期",
				"actions": ["码库","删除"]
			},{
				"name": "通用券-进行中",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-已失效",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已失效",
				"actions": ["码库"]
			}]
			"""

		#未开始
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"status":"未开始"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "多商品券-未开始",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "1天后",
				"end_date": "3天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "未开始",
				"actions": ["码库","链接","编辑","查看","使失效"]
			}]
			"""

		#进行中
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"status":"进行中"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "多商品券-进行中",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-进行中",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			}]
			"""

		#已过期
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"status":"已过期"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "通用券-已过期",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "2天前",
				"end_date": "1天前",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已过期",
				"actions": ["码库","删除"]
			}]
			"""

		#已失效
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"status":"已失效"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "通用券-已失效",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已失效",
				"actions": ["码库"]
			}]
			"""

	#按活动时间查询
		#空查询
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"start_time":"",
				"end_time":""
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "多商品券-未开始",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "1天后",
				"end_date": "3天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "未开始",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "多商品券-进行中",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-已过期",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "2天前",
				"end_date": "1天前",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已过期",
				"actions": ["码库","删除"]
			},{
				"name": "通用券-进行中",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-已失效",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已失效",
				"actions": ["码库"]
			}]
			"""

		#时间区间查询
		#空查询
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"start_time":"1天前",
				"end_time":"1天后"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "多商品券-进行中",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-进行中",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			},{
				"name": "通用券-已失效",
				"type": "通用券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "全部",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "已失效",
				"actions": ["码库"]
			}]
			"""

	#条件组合查询
		When jobs设置优惠券规则列表查询条件
			"""
			{
				"name":"多商品券",
				"coupon_code":"coupon",
				"coupon_type":"多商品券",
				"status":"进行中",
				"start_time":"1天前",
				"end_time":"1天后"
			}
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "多商品券-进行中",
				"type": "多商品券",
				"money": 100.00,
				"limit_counts": 1,
				"remained_count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"special_product": "查看专属商品",
				"get_person_count": 0,
				"get_number": 0,
				"use_count": 0,
				"status": "进行中",
				"actions": ["码库","链接","编辑","查看","使失效"]
			}]
			"""