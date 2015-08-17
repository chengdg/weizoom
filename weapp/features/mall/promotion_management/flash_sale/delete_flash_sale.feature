#_author_：张三香

Feature:删除限时抢购活动
	Jobs能删除状态为'已结束'的限时抢购活动

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品0",
			"price": 100.00
		},{
			"name": "商品1",
			"price": 100.00
		},{
			"name": "商品2",
			"price": 100.00
		},{
			"name": "商品3",
			"price": 100.00
		}]
		"""
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
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"discount": "10.0"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9.0"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8.0"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7.0"
		}]
		"""
	Given jobs已获取限时抢购活动列表
		"""
			[{
				"name": "活动名称：商品3抢购",
				"products":["商品3"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"未开始",
				"start_date": "明天",
				"end_date": "2天后",
				"actions": ["详情","结束"]
			},{
				"name": "活动名称：商品2抢购",
				"products":["商品2"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			},{
				"name": "广告语：商品1抢购",
				"products":["商品1"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			},{
				"name": "广告语：商品0抢购",
				"products":["商品0"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "3天前",
				"end_date": "2天前",
				"actions": ["详情","删除"]
			}]
		"""

@mall2 @promotion @promotionFlash
Scenario: 1 删除状态为'已结束'的限时抢购活动
	Given jobs登录系统
	When jobs删除限时抢购活动'广告语：商品0抢购'
	Then jobs获取限时抢购活动列表
		"""
			[{
				"name": "活动名称：商品3抢购",
				"products":["商品3"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"未开始",
				"start_date": "明天",
				"end_date": "2天后",
				"actions": ["详情","结束"]
			},{
				"name": "活动名称：商品2抢购",
				"products":["商品2"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			},{
				"name": "广告语：商品1抢购",
				"products":["商品1"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			}]
		"""

@mall2 @promotion @promotionFlash
Scenario: 2 批量删除限时抢购活动（不包含状态为未结束的活动）
	Given jobs登录系统
	When jobs批量删除限时抢购活动'广告语：商品1抢购'和'广告语：商品0抢购'
	Then jobs获取限时抢购活动列表
		"""
			[{
				"name": "活动名称：商品3抢购",
				"products":["商品3"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"未开始",
				"start_date": "明天",
				"end_date": "2天后",
				"actions": ["详情","结束"]
			},{
				"name": "活动名称：商品2抢购",
				"products":["商品2"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			}]
		"""

@mall2 @promotion @promotionFlash
Scenario: 3 批量删除限时抢购活动（包含状态为未结束的活动）
	Given jobs登录系统
	When jobs批量删除限时抢购活动
		"""
			[{
				"name": "活动名称：商品3抢购",
				"products":["商品3"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"未开始",
				"start_date": "明天",
				"end_date": "2天后",
				"actions": ["详情","结束"]
			},{
				"name": "活动名称：商品2抢购",
				"products":["商品2"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			},{
				"name": "广告语：商品1抢购",
				"products":["商品1"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			},{
				"name": "广告语：商品0抢购",
				"products":["商品0"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "3天前",
				"end_date": "2天前",
				"actions": ["详情","删除"]
			}]
		"""
	Then jobs获得系统提示'有未结束的活动，请先结束活动'
