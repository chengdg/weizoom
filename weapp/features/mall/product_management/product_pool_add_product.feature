# watcher: qiaozhanlei@weizoom.com
# __author__ : "乔占磊" 2016-09-02

Feature:商品池同步商品
"""
	给商家池同步商品
"""
Background:
	#商家bill的商品信息
		Given 创建一个特殊的供货商叫-商品池商品供货商
		Then 可以查到一个叫-商品池商品供货商-的供货商
###特殊说明：zy1, zy2表示自营商家, zymanager表示特殊商品池的那个商家webapp_type=2的那个

@product_pool_sync_product
Scenario:1 给商品池同步商品，ziying
	#给商品池同步商品，
		Given 给zy1, zy2两个自营平台同步商品，供货商是-商品池商品供货商
			"""
			{
				"name": "商品池商品测试zy",
				"promotion_title": "商品池商品测试zy-title",
				"purchase_price": 500,
				"price": 999,
				"weight": 2,
				"image": "love.png",
				"stocks": 500,
				"detail": "大家好，这个是bdd测试的商品池商品"
			}
			"""
		Then zy1,zy2可以查看到商品里有一个商品叫-商品池商品测试zy
			"""

			"""

