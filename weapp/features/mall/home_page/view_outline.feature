#watcher:zhangsanxiang@weizoom.com,wangli@weizoom.com,benchi@weizoom.com
#_edit_:张三香
#editor:王丽 2015.10.13

Feature: 获得店铺首页的经营概况和购买趋势信息
"""
	jobs通过管理系统能获得首页经营概况和购买趋势信息
		#2015-9-23:云商通整合,微商城'首页-统计概况'需求变动:
			1、经营概况
				未读消息:统计微信实时消息的未读消息列表中未读消息的总和;点击链接跳转到微信实时消息的未读消息列表页面
				昨日新增会员:昨天新关注的会员数量（不包括取消关注的会员）
				昨日下单数:昨天该店铺发生的待发货、已发货和已完成的订单数之和
				昨日成交额:该店铺已支付订单和货到付款提交成功订单的总金额
				关注会员:当前关注的会员总数
			2、购买趋势:图表形式展现订单数和销售额
"""

Background:
	Given jobs登录系统
	When jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}]
		"""
	When jobs已添加商品
		"""
		[{
			"name": "东坡肘",
			"category": "分类1,分类2",
			"model": {
				"models": {
					"standard": {
						"price": 11.1,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name": "叫花鸡",
			"category": "分类1",
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		},{
			"name": "水晶虾",
			"category": "",
			"model": {
				"models": {
					"standard": {
						"price": 3.0
					}
				}
			}
		}]
		"""
	When jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		}, {
			"type": "微信支付",
			"is_active": "启用"
		}]
		"""
	Given bill关注jobs的公众号
	And tom关注jobs的公众号

	Given nokia登录系统
	When nokia已添加商品
		"""
		[{
			"name": "酸菜鱼",
			"model": {
				"models": {
					"standard": {
						"price": 22.2,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	When nokia已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		}, {
			"type": "微信支付",
			"is_active": "启用"
		}]
		"""
	Given bill关注nokia的公众号

@mall2 @homePage @statistics
Scenario:1 获得店铺首页经营概况的未读消息信息
	Given jobs登录系统
	When jobs已添加单图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容"
		}]
		"""

	#添加关键词自动回复
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": [{
					"keyword": "关键词tom2",
					"type": "equal"
				}],
			"keyword_reply": [{
					 "reply_content":"关键字回复内容tom2",
					 "reply_type":"text"
				}]
		},{
			"rules_name":"规则2",
			"keyword": [{
					 "keyword": "关键词bill2",
					 "type": "like"
				}],
			"keyword_reply": [{
					 "reply_content":"图文1",
					 "reply_type":"text_picture"
				}]
		}]
		"""

	#bill2关注jobs的公众号进行消息互动，发送一条，无回复
	When 清空浏览器
	And bill2关注jobs的公众号
	And bill2访问jobs的webapp
	And bill2在微信中向jobs的公众号发送消息'bill2发送一条文本消息，未回复'
	And bill2在微信中向jobs的公众号发送消息'关键词bill2'

	#tom2关注jobs的公众号进行消息互动，发送两条，第一条回复文本消息，第二条无回复
	When 清空浏览器
	And tom2关注jobs的公众号
	And tom2在微信中向jobs的公众号发送消息'tom2发送一条文本消息1，未回复'
	And tom2在微信中向jobs的公众号发送消息'关键词tom2'
	And tom2在微信中向jobs的公众号发送消息'tom2发送一条文本消息2，未回复'

	Given jobs登录系统
	Then jobs能获取商铺首页的数量信息
		"""
		{
			"unread_message_count": 3
		}
		"""

@mall2 @homePage @statistics  @mall.outline
Scenario:2 获得商铺首页经营概况的订单数量信息
	jobs的用户购买商品后，jobs能获得正确的待发货订单列表

	When 微信用户批量消费jobs的商品
		| order_id | date  | consumer |product   | payment | action    |
		| 0001     | 3天前 | tom      |东坡肘,1  | 支付    |           |
		| 0002     | 1天前 | -lili    |东坡肘,1  | 支付    |           |
		| 0003     | 1天前 | tom      |东坡肘,1  | 支付    |           |
		| 0004     | 1天前 | bill     |东坡肘,1  |         |           |
		| 0005     | 1天前 | tom      |东坡肘,1  |         |           |
		| 0006     | 1天前 | bill     |水晶虾,2  | 支付    |           |
		| 0007     | 1天前 | bill     |水晶虾,2  | 支付    | jobs,取消 |
		| 0008     | 今天  | bill     |水晶虾,2  | 支付    |           |
		| 0009     | 今天  | bill     |东坡肘,1  | 支付    |           |
		| 0010     | 今天  | bill     |东坡肘,1  | 支付    | jobs,取消 |

	When 微信用户批量消费nokia的商品
		| order_id | date  | consumer  |product   | payment | action |
		| 0011     | 1天前 | bill      |酸菜鱼,2  | 支付    |        |

	Given jobs登录系统
	Then jobs能获取商铺首页的数量信息
		"""
		{
			"order_count_for_yesterday": 3,
			"order_money_for_yesterday": 28.2
		}
		"""

@mall2 @homePage @statistics
Scenario:3 获得商铺首页经营概况的会员数量信息
	When bill取消关注jobs的公众号
	When tom取消关注jobs的公众号
	When tom1关注jobs的公众号于'1天前'
	When tom2关注jobs的公众号于'1天前'
	When tom3关注jobs的公众号于'1天前'
	When tom3取消关注jobs的公众号
	When tom4关注nokia的公众号于'1天前'
	When tom5关注jobs的公众号于'2天前'
	Given jobs登录系统
	Then jobs能获取商铺首页的数量信息
		"""
		{
			"new_member_count": 2,
			"subscribed_member_count": 3
		}
		"""

@mall2 @homePage @statistics
Scenario:4 获得店铺首页的购买趋势
	jobs的用户购买商品后，jobs能获得正确的购买趋势

	When 微信用户批量消费jobs的商品
		| order_id| date  | consumer | product   | payment | action    |
		| 0001    | 7天前 | -lili    | 东坡肘,1  | 支付    |           |
		| 0002    | 7天前 | bill     | 叫花鸡,1  | 支付    |           |
		| 0003    | 7天前 | tom      | 水晶虾,2  | 支付    |           |
		| 0004    | 7天前 | bill     | 东坡肘,1  |         | jobs,取消 |
		| 0005    | 7天前 | tom      | 东坡肘,1  |         |           |
		| 0006    | 6天前 | bill     | 东坡肘,1  | 支付    |           |
		| 0007    | 5天前 | bill     | 东坡肘,1  | 支付    |           |
		| 0008    | 5天前 | bill     | 东坡肘,1  | 支付    |           |
		| 0009    | 5天前 | bill     | 东坡肘,1  |         | jobs,取消 |
		| 0010    | 5天前 | tom      | 东坡肘,1  |         |           |
		| 0011    | 4天前 | bill     | 东坡肘,1  | 支付    |           |
		| 0012    | 4天前 | bill     | 东坡肘,1  |         | jobs,取消 |
		| 0013    | 4天前 | tom      | 东坡肘,1  | 支付    |           |
		| 0014    | 4天前 | -tom1    | 东坡肘,1  | 支付    |           |
		| 0015    | 3天前 | tom      | 东坡肘,1  |         |           |
		| 0016    | 3天前 | tom      | 东坡肘,1  | 支付    |           |
		| 0017    | 3天前 | tom      | 东坡肘,1  | 支付    |           |
		| 0018    | 1天前 | -lili    | 东坡肘,1  | 支付    |           |
		| 0019    | 1天前 | tom      | 东坡肘,1  |         |           |
		| 0020    | 1天前 | tom      | 东坡肘,1  | 支付    |           |
		| 0021    | 1天前 | bill     | 东坡肘,1  | 支付    |           |
		| 0022    | 今天  | bill     | 东坡肘,1  |         |           |
		| 0023    | 今天  | bill     | 东坡肘,1  | 支付    |           |
		| 0024    | 今天  | bill     | 东坡肘,1  |         | jobs,取消 |

	When 微信用户批量消费nokia的商品
		| order_id| date | consumer | product   | payment | action    |
		| 0025    | 今天 | bill     | 酸菜鱼,2  | 支付    |           |

	Given jobs登录系统
	#当今天为最后一天时不显示今天的数据，所以只有六天
	Then jobs能获取'7天'购买趋势
		| date  | product_count | money |
		| 6天前 | 1             | 11.1  |
		| 5天前 | 2             | 22.2  |
		| 4天前 | 3             | 33.3  |
		| 3天前 | 2             | 22.2  |
		| 2天前 | 0             | 0.0   |
		| 1天前 | 3             | 33.3  |
