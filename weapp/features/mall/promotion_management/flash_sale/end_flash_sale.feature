#_author_：张三香

Feature:结束限时抢购活动
	Jobs能结束状态为'未开始'和'进行中'的限时抢购活动

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"shelve_type": "上架"
		}, {
			"name": "商品2",
			"price": 100.00,
			"shelve_type": "上架"
		}, {
			"name": "商品3",
			"price": 100.00,
			"shelve_type": "上架"
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
	When jobs创建限时抢购活动
		"""
			[{
				"name": "广告语：商品1抢购",
				"product_name":"商品1",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			},{
				"name": "活动名称：商品2抢购",
				"product_name":"商品2",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			},{
				"name": "活动名称：商品3抢购",
				"product_name":"商品3",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"未开始",
				"start_date": "明天",
				"end_date": "2天后",
				"actions": ["详情","结束"]
			}]
		"""

@promotion @promotionFlash
Scenario: 1 结束状态为'未开始'的限时抢购活动
	Given jobs登录系统
	When jobs'结束'促销活动'活动名称：商品3抢购'
	Then jobs获取限时抢购活动列表
		"""
			[{
				"name": "活动名称：商品3抢购",
				"product_name":"商品3",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "明天",
				"end_date": "2天后",
				"actions": ["详情","删除"]
			},{
				"name": "活动名称：商品2抢购",
				"product_name":"商品2",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			},{
				"name": "广告语：商品1抢购",
				"product_name":"商品1",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			}]
		"""

@promotion @promotionFlash
Scenario: 2 结束状态为'进行中'的限时抢购活动
	Given jobs登录系统
	When jobs'结束'促销活动'活动名称：商品2抢购'
	Then jobs获取限时抢购活动列表
		"""
			[{
				"name": "活动名称：商品3抢购",
				"product_name":"商品3",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"未开始",
				"start_date": "明天",
				"end_date": "2天后",
				"actions": ["详情","结束"]
			},{
				"name": "活动名称：商品2抢购",
				"product_name":"商品2",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","删除"]
			},{
				"name": "广告语：商品1抢购",
				"product_name":"商品1",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			}]
		"""

@ui @promotion @promotionFlash
Scenario: 3 批量结束限时抢购活动（包含已结束状态）
	Given jobs登录系统
	When jobs批量'结束'促销活动
		"""
			[{
				"name": "活动名称：商品3抢购",
				"product_name":"商品3",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"未开始",
				"start_date": "明天",
				"end_date": "2天后",
				"actions": ["详情","结束"]
			},{
				"name": "活动名称：商品2抢购",
				"product_name":"商品2",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			},{
				"name": "广告语：商品1抢购",
				"product_name":"商品1",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			}]
		"""
	Then jobs获得系统提示'不能同时进行删除和结束操作'

@promotion @promotionFlash
Scenario: 4 批量结束限时抢购活动（不包含已结束状态）
	Given jobs登录系统
	When jobs批量'结束'促销活动
		"""
			[{
				"name": "活动名称：商品3抢购",
				"product_name":"商品3",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"未开始",
				"start_date": "明天",
				"end_date": "2天后",
				"actions": ["详情","删除"]
			},{
				"name": "活动名称：商品2抢购",
				"product_name":"商品2",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","删除"]
			}]
		"""
	Then jobs获取限时抢购活动列表
		"""
			[{
				"name": "活动名称：商品3抢购",
				"product_name":"商品3",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "明天",
				"end_date": "2天后",
				"actions": ["详情","删除"]
			},{
				"name": "活动名称：商品2抢购",
				"product_name":"商品2",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","删除"]
			},{
				"name": "广告语：商品1抢购",
				"product_name":"商品1",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			}]
		"""

@promotion @promotionFlash
Scenario: 5 商品下架导致限时抢购活动结束
	Given jobs登录系统
	When jobs批量下架商品
		"""
		["商品2", "商品3"]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"shelve_type": "上架"
		}]
		"""
	And jobs获取限时抢购活动列表
		"""
			[{
				"name": "活动名称：商品3抢购",
				"product_name":"商品3",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "明天",
				"end_date": "2天后",
				"actions": ["详情","删除"]
			},{
				"name": "活动名称：商品2抢购",
				"product_name":"商品2",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","删除"]
			},{
				"name": "广告语：商品1抢购",
				"product_name":"商品1",
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			}]
		"""
