#_author_:张三香
#editor:雪静 2015.10.14
Feature:删除买赠活动
	jobs能结束状态为"已结束"的买赠活动

Background:
	Given jobs登录系统
	And jobs已添加商品规格
		"""
		[{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name":"商品1",
			"price":100.00,
			"shelve_type": "上架"
		},{
			"name":"赠品1",
			"price":100.00,
			"shelve_type": "上架"
		},{
			"name": "商品2",
			"shelve_type": "上架",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 100.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 200.00,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name":"商品3",
			"price":100.00,
			"shelve_type": "上架",
			"is_member_product": "on"
		},{
			"name":"商品4",
			"bar_code":"123456",
			"price":100.00,
			"shelve_type": "上架",
			"is_member_product": "on"
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
	When jobs创建买赠活动
		"""
		[{
			"name": "活动名称:商品4买赠",
			"product_name": "商品4",
			"product_price":100.00,
			"status":"已结束",
			"start_date": "2天前",
			"end_date": "今天",
			"actions": ["详情","删除"],
			"premium_products": [{
				"name": "赠品1"
			}]
		},{
			"name": "活动名称:商品3买赠",
			"product_name": "商品3",
			"product_price":100.00,
			"status":"已结束",
			"start_date": "2天前",
			"end_date": "1天前",
			"actions": ["详情","删除"],
			"premium_products": [{
				"name": "赠品1"
			}]
		},{
			"name": "活动名称:商品2买赠",
			"product_name": "商品2",
			"product_price":"100.00~200.00",
			"status":"进行中",
			"start_date": "今天",
			"end_date": "3天后",
			"actions": ["详情","结束"],
			"premium_products": [{
				"name": "赠品1"
			}]
		},{
			"name": "活动名称:商品1买赠",
			"product_name": "商品1",
			"product_price":100.00,
			"status":"未开始",
			"start_date": "明天",
			"end_date": "3天后",
			"actions": ["详情","结束"],
			"premium_products": [{
				"name": "赠品1"
			}]
		}]
		"""

@mall2 @promotion @promotionPremium
Scenario: 1 删除状态为'已结束'的买赠活动
	Given jobs登录系统
	When jobs'删除'促销活动'活动名称:商品3买赠'
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "活动名称:商品1买赠"
		},{
			"name": "活动名称:商品2买赠"
		},{
			"name": "活动名称:商品4买赠"
		}]
		"""

@mall2 @promotion @promotionPremium
Scenario: 2 批量删除买赠活动（不包括未结束状态的）
	Given jobs登录系统
	When jobs批量'删除'促销活动
		"""
		[{
			"name": "活动名称:商品3买赠"
		},{
			"name": "活动名称:商品4买赠"
		}]
		"""
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "活动名称:商品1买赠"
		},{
			"name": "活动名称:商品2买赠"
		}]
		"""

# __author__ : "王丽" 补充在查询结果中删除活动
@mall2 @promotion @promotionPremium
Scenario: 3 在按"商品名称"查询的查询结果下删除买赠活动

	Given jobs登录系统
	When jobs设置查询条件
		"""
		{
			"product_name":"商品4"
		}
		"""
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "活动名称:商品4买赠"
		}]
		"""
	When jobs'删除'促销活动'活动名称:商品4买赠'
	Then jobs获取买赠活动列表
		"""
		[]
		"""

@mall2 @promotion @promotionPremium
Scenario: 4 在按"商品条码"查询的查询结果下删除买赠活动

	Given jobs登录系统
	When jobs设置查询条件
		"""
		{
			"bar_code":"123456"
		}
		"""
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "活动名称:商品4买赠"
		}]
		"""
	When jobs'删除'促销活动'活动名称:商品4买赠'
	Then jobs获取买赠活动列表
		"""
		[]
		"""

@mall2 @promotion @promotionPremium
Scenario: 5 在按"促销状态"查询的查询结果下删除买赠活动

	Given jobs登录系统
	When jobs设置查询条件
		"""
		{
			"status":"已结束"
		}
		"""
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "活动名称:商品3买赠",
			"status":"已结束"
		},{
			"name": "活动名称:商品4买赠",
			"status":"已结束"
		}]
		"""
	When jobs'删除'促销活动'活动名称:商品4买赠'
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "活动名称:商品3买赠",
			"status":"已结束"
		}]
		"""


@mall2 @promotion @promotionPremium
Scenario: 6 在按"活动时间"查询的查询结果下删除买赠活动

	Given jobs登录系统
	When jobs设置查询条件
		"""
		{
			"status":"已结束",
			"start_date":"2天前",
			"end_date":"今天"
		}
		"""
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "活动名称:商品3买赠",
			"status":"已结束",
			"start_date": "2天前",
			"end_date": "1天前"
		},{
			"name": "活动名称:商品4买赠",
			"status":"已结束",
			"start_date": "2天前",
			"end_date": "今天"
		}]
		"""
	When jobs'删除'促销活动'活动名称:商品4买赠'
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "活动名称:商品3买赠"
		}]
		"""
