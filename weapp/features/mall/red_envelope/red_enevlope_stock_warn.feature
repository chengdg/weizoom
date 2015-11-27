#editor 新新 2015.10.20


Feature: 分享红包库存提示
"""
	Jobs能通过管理系统添加"添加红包"

	1、分享红包列表显示优惠券剩余"库存告急"（只有红包开启状态时并且库存小于等于20）
	2、列表页每次重新进入都库存提示，弹窗中显示"红包名称","即将用完"请及时处理
	3、点击"修改库存"按钮，则到优惠券列表页
	4、点击确认按钮，则关闭该弹窗
	5、库存提示弹窗中的列表顺序与分享红包展示顺序一样倒序显示

"""

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品2"
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "全体券3",
			"money": 100.00,
			"count": 10,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
		}, {
			"name": "单品券4",
			"money": 1.00,
			"count": 20,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon4_id_",
			"coupon_product": "商品2"
		}]
		"""
	When jobs添加分享红包
		"""
		[{
			"name": "红包1",
			"prize_info": "全体券3",
			"is_permanant_active": false,
			"start_date": "今天",
			"end_date": "2天后",
			"receive_method": "下单领取",
			"limit_money": 200,
			"detail": "活动说明",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"remark": "分享有礼"

		}, {
			"name": "红包2",
			"prize_info": "单品券4",
			"is_permanant_active": true,
			"receive_method": "图文领取",
			"detail": "活动说明",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"remark": "分享有礼"
		}]
		""" 

@mall2 @promotion @promotionRedbag
Scenario: 1 分享红包列表提示
	jobs在获取红包列表为'开启'状态,优惠券剩余一列小于等于20有“库存告急”提示
	1.切换红包状态,显示相应'库存告急'提示
	2.添加库存后'库存告急'提示

	Given jobs登录系统
	#默认【图文领取】开启状态
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "【图文领取】红包2",
			"status": "开启",
			"surplus":{
				"surplus_count":20,
				"surplus_text":"库存告急"
			},
			"actions": ["分析","删除","查看"]
		}, {
			"name": "红包1",
			"status": "关闭",
			"surplus":{
				"surplus_count":10,
				"surplus_text":""
			},
			"actions": ["分析","开启","删除","查看"]
		}]
		"""
	#调整'红包1'状态为'开启'显示库存告急提示
	When jobs开启分享红包"红包1"
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "【图文领取】红包2",
			"status": "开启",
			"surplus":{
				"surplus_count":20,
				"surplus_text":"库存告急"
			},
			"actions": ["分析","删除","查看"]
		}, {
			"name": "红包1",
			"status": "开启",
			"surplus":{
				"surplus_count":10,
				"surplus_text":"库存告急"
			},
			"actions": ["分析","关闭","查看"]
		}]
		"""
	#调整'红包1'状态为'关闭'不显示库存告急提示
	When jobs关闭分享红包"红包1"
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "【图文领取】红包2",
			"status": "开启",
			"surplus":{
				"surplus_count":20,
				"surplus_text":"库存告急"
			},
			"actions": ["分析","删除","查看"]
		}, {
			"name": "红包1",
			"status": "关闭",
			"surplus":{
				"surplus_count":10,
				"surplus_text":""
			},
			"actions": ["分析","开启","删除","查看"]
		}]
		"""

	#添加库存,分享红包列表提示
	When jobs为优惠券'单品券4'添加库存
		"""
		{
			"count": 2,
			"coupon_id_prefix": "coupon4_id_"
		}
		"""
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "【图文领取】红包2",
			"status": "开启",
			"surplus":{
				"surplus_count":22,
				"surplus_text":""
			},
			"actions": ["分析","删除","查看"]
		}, {
			"name": "红包1",
			"status": "关闭",
			"surplus":{
				"surplus_count":10,
				"surplus_text":""
			},
			"actions": ["分析","开启","删除","查看"]
		}]
		"""

@mall2 @promotion @promotionRedbag
Scenario: 2 获取库存提示弹窗
	jobs在获取红包列表为'开启'状态,弹窗中“库存告急”提示
	1.切换红包状态,显示相应'库存告急'提示
	2.添加库存后'库存告急'提示

	Given jobs登录系统
	#默认【图文领取】开启状态
	
	Then jobs获取库存提示弹窗
		"""
		[{
			"name": "【图文领取】红包2",
			"surplus_text":"即将用完"
		}]
		"""
	When jobs开启分享红包"红包1"
	Then jobs获取库存提示弹窗
		"""
		[{
			"name": "【图文领取】红包2",
			"surplus_text":"即将用完"
		}, {
			"name": "红包1",
			"surplus_text":"即将用完"
		}]
		"""
	When jobs关闭分享红包"红包1"
	Then jobs获取库存提示弹窗
		"""
		[{
			"name": "【图文领取】红包2",
			"surplus_text":"即将用完"
		}]
		"""
	#添加库存,分享红包提示
	When jobs为优惠券'单品券4'添加库存
		"""
		{
			"count": 2,
			"coupon_id_prefix": "coupon4_id_"
		}
		"""
	#无提示弹窗
	Then jobs获取库存提示弹窗
		"""
		[]
		"""
	