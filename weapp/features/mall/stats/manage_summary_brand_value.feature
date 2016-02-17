#watcher:wangli@weizoom.com,wangxinrui@weizoom.com,benchi@weizoom.com
#editor:王丽  2015.10.19
#editor: 新新 2015.10.16

Feature: 测试 经营报告->经营概况->微品牌价值

Background:
	#说明：jobs代表商户
	Given jobs登录系统
	When jobs设置未付款订单过期时间24小时
	When jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用"
		}]
		"""
	When jobs已添加商品
		"""
		[{
			"name": "商品1",
			"promotion_title": "促销商品1",
			"detail": "商品1详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 10.00,
						"freight":"10",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"synchronized_mall":"是"
		}, {
			"name": "商品2",
			"promotion_title": "促销商品2",
			"detail": "商品2详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"freight":"15",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"synchronized_mall":"是"
		}]
		"""
		
		When bill关注jobs的公众号
		And tom关注jobs的公众号
		And nokia关注jobs的公众号
		# tom2 => mary
		And mary关注jobs的公众号
		# tom3 => jim
		And jim关注jobs的公众号
		# tom4 => kate
		And kate关注jobs的公众号

@mall2 @bi @operateReport   @stats @wip.brand_value 
Scenario:1 测试只有1个消费用户、1个商品的品牌价值
	When 微信用户批量消费jobs的商品
		# consumer前有'-'表示清空浏览器
		| date    | consumer | product | payment | action |
		| 30天前  | bill     | 商品1,1 | 支付    |        |
		| 60天前  | bill     | 商品1,1 | 支付    |        |
		| 366天前 | bill     | 商品1,1 | 支付    |        |
		| 365天前 | bill     | 商品1,1 | 支付    |        |
		| 今天    | bill     | 商品1,1 | 支付    |        |
	Given jobs登录系统
	When jobs查看微品牌页面
	# 按日期顺序的品牌价值
	Then 微品牌的数据为
		"""
		[{
			"value": 40
		},{
			"value": 40
		},{
			"value": 40
		},{
			"value": 40
		},{
			"value": 40
		},{
			"value": 40
		},{
			"value": 40
		},{
			"value": 40
		},{
			"value": 40
		},{
			"value": 40
		},{
			"value": 40
		},{
			"value": 40
		},{
			"value": 40
		},{
			"value": 30
		},{
			"value": 20
		},{
			"value": 20
		},{
			"value": 20
		},{
			"value": 20
		},{
			"value": 20
		},{
			"value": 30
		}]
		"""

@mall2 @bi @operateReport   @stats @wip.brand_value2 
Scenario:2 测试2个消费用户、2个商品的品牌价值
	品牌价值会参考用户1年(365天)内购买金额和数量。

	# consumer前有'-'表示清空浏览器
	When 微信用户批量消费jobs的商品	
		| date    | consumer | product | payment | action |
		| 30天前  | bill     | 商品1,1 | 支付    |        |
		| 60天前  | bill     | 商品1,1 | 支付    |        |
		| 366天前 | bill     | 商品1,1 | 支付    |        |
		| 365天前 | bill     | 商品1,1 | 支付    |        |
		| 今天    | bill     | 商品1,1 | 支付    |        |
		| 367天前 | tom      | 商品2,1 | 支付    |        |
		| 2天前   | tom      | 商品1,1 | 支付    |        |
		| 1天前   | tom      | 商品2,1 | 支付    |        |
		| 今天    | tom      | 商品1,1 | 未支付  |        |
		| 今天    | tom      | 商品2,1 | 支付    |        |

	Given jobs登录系统
	When jobs查看微品牌页面
	# 按日期顺序的品牌价值
	Then 微品牌的数据为
		"""
		[{
		    "value": 140
		},{
		    "value": 140
		},{
		    "value": 140
		},{
		    "value": 140
		},{
		    "value": 140
		},{
		    "value": 140
		},{
		    "value": 140
		},{
		    "value": 140
		},{
		    "value": 140
		},{
		    "value": 140
		},{
		    "value": 140
		},{
		    "value": 140
		},{
		    "value": 40
		},{
		    "value": 30
		},{
		    "value": 20
		},{
		    "value": 20
		},{
		    "value": 20
		},{
		    "value": 40
		},{
		    "value": 220
		},{
		    "value": 240
		}]
		"""

#Scenario: 测试当日订单情况变化导致微品牌数据变化的场景
#"""
#避免出现，当日数据被缓存而不变的情况
#"""

#Scenario: 测试当日微品牌数据及和昨日相比的增量
