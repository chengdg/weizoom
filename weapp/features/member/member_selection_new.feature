# __author__ : "王丽"

Feature: 筛选会员列表
"""
	jobs能管理会员列表
	1、默认展示两行筛选条件，点击展开后显示所有，当点击收起后展示为默认状态
		筛选条件顺序如下
		会员名称、会员状态、关注时间
		会员等级、会员分组、会员来源
		消费总额、购买次数、最后购买时间
		积分范围、最后对话时间
	2、筛选规则
	（1）【会员名称】：模糊匹配
	（2）【会员状态】：下拉选择（已关注、全部、取消关注）；默认"已关注"
	（3）【关注时间】：开始和结束时间，过滤会员的关注时间；
					开始时间必须小于结束时间，不能清空；
					开始时间为空，提示"请输入关注开始时间"；
					结束时间为空，提示"请输入关注结束时间"；
	（4）【会员等级】：下拉选择（全部、会员等级列表按照创建的顺序）；默认"全部"
	（5）【会员分组】：下拉选择（全部、会员分组列表按照创建的顺序）；默认"全部"
	（6）【会员来源】：下拉选择（全部、直接关注、推广扫码、会员分享）；默认"全部"
	（7）【消费总额】：会员提交支付的所有订单的实付金额总和
				=∑ 订单.实付金额[(订单.买家=当前会员) and (订单.状态 in {待发货、已发货、已完成、退款中、退款成功})]
	（8）【购买次数】：会员提交支付的所有订单的总和
				=∑ 订单.个数[(订单.买家=当前会员) and (订单.状态 in {待发货、已发货、已完成、退款中、退款成功})]
	（9）【最后购买时间】：会员最后一个提交已支付的订单的下单时间
	（10）【积分范围】：会员目前拥有的积分
	（11）【最后对话时间】：
	3.筛选出会员发送优惠券
	#除已跑路外
	4.筛选条件下所有会员群发消息
	#除已跑路外
	#鼠标移入“群发消息”时显示群发选项，移出时隐藏
	#选择会员后点击群发消息,可跳转到群发消息页，当选择给选中会员群发消息时显示群发会员名称
	（无备注的显示昵称、有备注的显示备注名称），鼠标移入会员名称时出现删除标志，点击删除标志后移除该会员，
	点击重新筛选则回到会员管理页面，当选择按筛选条件群发消息时，显示筛选条件，点击重新筛选则回到会员管理页面。
"""

Background:
	
	Given jobs登录系统

	#添加相关基础数据
		When jobs添加商品
			"""
			[{
				"name": "商品1",
				"postage":10,
				"price":100,
				"stock_type": "无限"
			}, {
				"name": "商品2",
				"postage":15,
				"price":100,
				"stock_type": "无限"
			}]
			"""
		And jobs已添加支付方式
			"""
			[{
				"type": "货到付款",
				"is_active": "启用"
			},{
				"type": "微信支付",
				"is_active": "启用"
			},{
				"type": "支付宝",
				"is_active": "启用"
			}]
			"""
		And jobs添加会员等级
			"""
			[{
				"name": "银牌会员",
				"upgrade": "不自动升级",
				"shop_discount": "100%"
			},{
				"name": "金牌会员",
				"upgrade": "自动升级",
				"shop_discount": "90%"
			}]
			"""
		Then jobs能获取会员等级列表
			"""
			[{
				"name": "普通会员",
				"upgrade": "自动升级",
				"shop_discount": "100%"
			},{
				"name": "银牌会员",
				"upgrade": "不自动升级",
				"shop_discount": "100%"
			},{
				"name": "金牌会员",
				"upgrade": "自动升级",
				"shop_discount": "90%"
			}]
			"""
		When jobs添加会员分组
			"""
			[{
				"tag_id_1": "分组1",
				"tag_id_2": "分组2",
				"tag_id_3": "分组3"
			}]
			"""

	#批量获取微信用户关注
		When jobs批量获取微信用户关注
			| member_name   | attention_time 	 | member_source |
			| tom1 			| 2014-8-4 23:59:59  | 直接关注      |
			| tom2 			| 2014-8-5 00:00:00  | 推广扫码      |
			| tom3	 	    | 2014-8-5 8:00:00   | 会员分享      |
			| tom4 			| 2014-8-5 23:59:59  | 会员分享      |
			| tom5 			| 2014-8-6 00:00:00  | 会员分享      |
			| tom6          | 2014-10-1 8:00:00  | 推广扫码      |
			| tom7          | 2014-10-1 8:00:00  | 直接关注      |

		And tom2取消关注jobs的公众号
		And tom4取消关注jobs的公众号

	#好友
		#bill和tom1建立好友关系
			When tom1访问jobs的webapp
			When tom1把jobs的微站链接分享到朋友圈
			
			When 清空浏览器
			When bill点击tom1分享链接
			When bill关注jobs的公众号
			When bill访问jobs的webapp

		#bill2和tom1建立好友关系
			When 清空浏览器
			When bill2关注jobs的公众号
			When bill2访问jobs的webapp
			When bill2点击tom1分享链接

		#bill3和tom3建立好友关系
			When tom3访问jobs的webapp
			When tom3把jobs的微站链接分享到朋友圈

			When 清空浏览器
			When bill3关注jobs的公众号
			When bill3点击tom3分享链接
			When bill3访问jobs的webapp

	#获取会员积分

		When tom2访问jobs的webapp
		When tom2获得jobs的50会员积分
		Then tom2在jobs的webapp中拥有50会员积分

		When tom3访问jobs的webapp
		When tom3获得jobs的100会员积分
		Then tom3在jobs的webapp中拥有100会员积分

		When tom4访问jobs的webapp
		When tom4获得jobs的20会员积分
		Then tom4在jobs的webapp中拥有20会员积分

	#微信用户批量下订单
		When 微信用户批量消费jobs的商品
			| date       | consumer | type      |businessman|   product | payment | payment_method | freight |   price  | integral | coupon | paid_amount | weizoom_card | alipay | wechat | cash |      action       |  order_status   |
			| 2015-1-1   | tom1     | 	 购买   | jobs      | 商品1,1   | 支付    | 支付宝         | 10      | 100      | 		   |        | 110         |              | 110    | 0      | 0    | jobs,支付         |  待发货         |
			| 2015-1-2   | tom1     | 	 购买   | jobs      | 商品2,2   | 未支付  | 支付宝         | 15      | 100      |          |        | 0           |              | 0      | 0      | 0    | jobs,取消         |  已取消         |	
			| 2015-2-1   | tom2     |    购买   | jobs      | 商品2,2   | 支付    | 支付宝         | 15      | 100      |          |        | 215         |              | 215    | 0      | 0    | jobs,发货         |  已发货         |
			| 2015-2-2   | tom2     |    购买   | jobs      | 商品1,1   | 支付    | 微信支付       | 10      | 100      |          |        | 110         |              | 0      | 110    | 0    | jobs,完成         |  已完成         |
			| 2015-2-4   | tom2     |    购买   | jobs      | 商品1,1   | 未支付  | 微信支付       | 10      | 100      |          |        | 0           |              | 0      | 0      | 0    | jobs,无操作       |  未支付         |
			| 2015-3-2   | tom3     |    购买   | jobs      | 商品1,1   | 支付    | 货到付款       | 10      | 100      |          |        | 110         |              | 0      | 0      | 110  | jobs,完成         |  已完成         |
			| 2015-3-4   | tom3     |    购买   | jobs      | 商品2,1   | 支付    | 微信支付       | 15      | 100      |          |        | 115         |              | 0      | 115    | 0    | jobs,退款         |  退款中         |
			| 2015-3-5   | tom3     |    购买   | jobs      | 商品1,1   | 支付    | 支付宝         | 10      | 100      |          |        | 110         |              | 110    | 0      | 0    | jobs,完成退款     |  退款完成       |

	#设置会员等级
		When jobs选择会员
			| member_name   | attention_time 	| member_source |     member_rank   |
			| tom1 			| 2014-8-4 23:59:59 | 直接关注      |      普通会员     |
			| tom3 			| 2014-8-5 8:00:00  | 会员分享      |      普通会员     |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给选中的人修改等级",
				"member_rank":"银牌会员"
			}]
			"""
		When jobs选择会员
			| member_name   | attention_time 	| member_source |     member_rank   |
			| tom4 			| 2014-8-5 23:59:59 | 会员分享      |      普通会员     |
			| tom5 			| 2014-8-6 00:00:00 | 会员分享      |      普通会员     |
			| tom7 			| 2014-10-1 8:00:00 | 直接关注      |      普通会员     |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给选中的人修改等级",
				"member_rank":"金牌会员"
			}]
			"""

	#设置会员分组

		When jobs选择会员
			| member_name   | attention_time 	| member_source | grouping |
			| tom1 			| 2014-8-4 23:59:59 | 直接关注      |          |
			| tom2 			| 2014-8-5 00:00:00 | 推广扫码      |          |
			| tom3 			| 2014-8-5 8:00:00  | 会员分享      |          |

		When jobs批量添加分组
				"""
				[{
					"modification_method":"给选中的人添加分组",
					"grouping":"分组1"
				}]
				"""

		When jobs选择会员
			| member_name   | attention_time 	| member_source | grouping |
			| tom3 			| 2014-8-5 8:00:00  | 会员分享      |  分组1   |
			| tom4 			| 2014-8-5 23:59:59 | 会员分享      |          |
			| tom5 			| 2014-8-6 00:00:00 | 会员分享      |          |

		When jobs批量添加分组
				"""
				[{
					"modification_method":"给选中的人添加分组",
					"grouping":"分组3"
				}]
				"""

Scenario:1 默认条件和空条件查询

	Given jobs登录系统

	#首次进入，默认条件查询
		When jobs访问会员列表
		Then jobs获得会员列表默认查询条件
			"""
			[{
				"status":"已关注"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":8
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| bill3 | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    会员分享   |             |
			| bill2 | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    直接关注   |             |
			| bill  | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    会员分享   |             |
			| tom7  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-10-1 8:00:00 |    直接关注   |             |
			| tom6  | 普通会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-10-1 8:00:00 |    推广扫码   |             |	
			| tom5  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-8-6 00:00:00 |    会员分享   | 分组3       |
			| tom3  | 银牌会员 |    1    |    100   |     335.00     |      111.67    |      3     | 2014-8-5 8:00:00  |    会员分享   | 分组1,分组3 |
			| tom1  | 银牌会员 |    2    |     0    |     110.00     |      110.00    |      1     | 2014-8-4 23:59:59 |    直接关注   | 分组1       |

	#空调条件查询，“重置”查询条件，空调间查询所有数据
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":10
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| bill3 | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    会员分享   |             |
			| bill2 | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    直接关注   |             |
			| bill  | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    会员分享   |             |
			| tom7  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-10-1 8:00:00 |    直接关注   |             |
			| tom6  | 普通会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-10-1 8:00:00 |    推广扫码   |             |	
			| tom5  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-8-6 00:00:00 |    会员分享   | 分组3       |
			| tom4  | 金牌会员 |    0    |     20   |     0.00       |      0.00      |      0     | 2014-8-5 23:59:59 |    会员分享   | 分组3       |
			| tom3  | 银牌会员 |    1    |    100   |     335.00     |      111.67    |      3     | 2014-8-5 8:00:00  |    会员分享   | 分组1,分组3 |
			| tom2  | 普通会员 |    0    |     50   |     325.00     |      162.50    |      2     | 2014-8-5 00:00:00 |    推广扫码   | 分组1       |
			| tom1  | 银牌会员 |    2    |     0    |     110.00     |      110.00    |      1     | 2014-8-4 23:59:59 |    直接关注   | 分组1       |

Scenario:2 过滤条件"会员名称"
	
	#会员名称部分匹配查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"bill",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| bill3 | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    会员分享   |             |
			| bill2 | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    直接关注   |             |
			| bill  | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    会员分享   |             |

	#会员名称完全匹配查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom5",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":1
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom5  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-8-6 00:00:00 |    会员分享   | 分组3       |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"marry",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs获得会员列表"没有符合要求的数据"

Scenario:3 过滤条件"会员状态"

	#会员状态匹配
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"取消关注",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom4  | 金牌会员 |    0    |     20   |     0.00       |      0.00      |      0     | 2014-8-5 23:59:59 |    会员分享   | 分组3       |
			| tom2  | 普通会员 |    0    |     50   |     325.00     |      162.50    |      2     | 2014-8-5 00:00:00 |    推广扫码   | 分组1       |

Scenario:4 过滤条件"关注时间"

	#区间时间边界值查询，不包含结束时间
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"2014-8-5 00:00:00",
				"attention_end_time":"2014-8-6 00:00:00",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom4  | 金牌会员 |    0    |     20   |     0.00       |      0.00      |      0     | 2014-8-5 23:59:59 |    会员分享   | 分组3       |
			| tom3  | 银牌会员 |    1    |    100   |     335.00     |      111.67    |      3     | 2014-8-5 8:00:00  |    会员分享   | 分组1,分组3 |
			| tom2  | 普通会员 |    0    |     50   |     325.00     |      162.50    |      2     | 2014-8-5 00:00:00 |    推广扫码   | 分组1       |

	#开始结束时间相同查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"2014-10-1 8:00:00",
				"attention_end_time":"2014-10-1 8:00:00",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom7  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-10-1 8:00:00 |    直接关注   |             |
			| tom6  | 普通会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-10-1 8:00:00 |    推广扫码   |             |	

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"2015-8-10 00:00:00",
				"attention_end_time":"2015-8-11 00:00:00",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs获得会员列表"没有符合要求的数据"

Scenario:5 过滤条件"会员等级"

	#单等级匹配
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"金牌会员",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom7  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-10-1 8:00:00 |    直接关注   |             |
			| tom5  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-8-6 00:00:00 |    会员分享   | 分组3       |
			| tom4  | 金牌会员 |    0    |     20   |     0.00       |      0.00      |      0     | 2014-8-5 23:59:59 |    会员分享   | 分组3       |

Scenario:6 过滤条件"会员分组"

	#单会员分组匹配
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"分组1",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom3  | 银牌会员 |    1    |    100   |     335.00     |      111.67    |      3     | 2014-8-5 8:00:00  |    会员分享   | 分组1,分组3 |
			| tom2  | 普通会员 |    0    |     50   |     325.00     |      162.50    |      2     | 2014-8-5 00:00:00 |    推广扫码   | 分组1       |
			| tom1  | 银牌会员 |    2    |     0    |     110.00     |      110.00    |      1     | 2014-8-4 23:59:59 |    直接关注   | 分组1       |


		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"分组3",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |	
			| tom5  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |    0.00    | 2014-8-6 00:00:00 |    会员分享   | 分组3       |
			| tom4  | 金牌会员 |    0    |     20   |     0.00       |      0.00      |    0.00    | 2014-8-5 23:59:59 |    会员分享   | 分组3       |
			| tom3  | 银牌会员 |    1    |    100   |     0.00       |      0.00      |    0.00    | 2014-8-5 8:00:00  |    会员分享   | 分组1,分组3 |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"marry",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"分组2",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs获得会员列表"没有符合要求的数据"

Scenario:7 过滤条件"会员来源"

	#单会员来源匹配
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部",
				"source":"会员分享",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":5
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| bill3 | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    会员分享   |             |
			| bill  | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    会员分享   |             |
			| tom5  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-8-6 00:00:00 |    会员分享   | 分组3       |
			| tom4  | 金牌会员 |    0    |     20   |     0.00       |      0.00      |      0     | 2014-8-5 23:59:59 |    会员分享   | 分组3       |
			| tom3  | 银牌会员 |    1    |    100   |     335.00     |      111.67    |      3     | 2014-8-5 8:00:00  |    会员分享   | 分组1,分组3 |

Scenario:8 过滤条件"消费总额"

	#区间查询，包含开始和结束数值
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"110",
				"total_spending_end":"335",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom3  | 银牌会员 |    1    |    100   |     335.00     |      111.67    |      3     | 2014-8-5 8:00:00  |    会员分享   | 分组1,分组3 |
			| tom2  | 普通会员 |    0    |     50   |     325.00     |      162.50    |      2     | 2014-8-5 00:00:00 |    推广扫码   | 分组1       |
			| tom1  | 银牌会员 |    2    |     0    |     110.00     |      110.00    |      1     | 2014-8-4 23:59:59 |    直接关注   | 分组1       |

	#开始结束数值相同
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"110",
				"total_spending_end":"110",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":1
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom1  | 银牌会员 |    2    |     0    |     110.00     |      110.00    |      1     | 2014-8-4 23:59:59 |    直接关注   | 分组1       |

	#特殊数据查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"0",
				"total_spending_end":"10",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":10
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| bill3 | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    会员分享   |             |
			| bill2 | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    直接关注   |             |
			| bill  | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    会员分享   |             |
			| tom7  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-10-1 8:00:00 |    直接关注   |             |
			| tom6  | 普通会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-10-1 8:00:00 |    推广扫码   |             |	
			| tom5  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-8-6 00:00:00 |    会员分享   | 分组3       |
			| tom4  | 金牌会员 |    0    |     20   |     0.00       |      0.00      |      0     | 2014-8-5 23:59:59 |    会员分享   | 分组3       |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"-10",
				"total_spending_end":"-1",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs获得会员列表"没有符合要求的数据"

Scenario:9 过滤条件"购买次数"

	#区间查询，包含开始和结束数值
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"1",
				"buy_number_end":"3",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom3  | 银牌会员 |    1    |    100   |     335.00     |      111.67    |      3     | 2014-8-5 8:00:00  |    会员分享   | 分组1,分组3 |
			| tom2  | 普通会员 |    0    |     50   |     325.00     |      162.50    |      2     | 2014-8-5 00:00:00 |    推广扫码   | 分组1       |
			| tom1  | 银牌会员 |    2    |     0    |     110.00     |      110.00    |      1     | 2014-8-4 23:59:59 |    直接关注   | 分组1       |

	#开始结束数值相同
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"2",
				"buy_number_end":"2",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":1
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom2  | 普通会员 |    0    |     50   |     325.00     |      162.50    |      2     | 2014-8-5 00:00:00 |    推广扫码   | 分组1       |

	#特殊数据查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"-2.2",
				"buy_number_end":"2.3",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom2  | 普通会员 |    0    |     50   |     325.00     |      162.50    |      2     | 2014-8-5 00:00:00 |    推广扫码   | 分组1       |
			| tom1  | 银牌会员 |    2    |     0    |     110.00     |      110.00    |      1     | 2014-8-4 23:59:59 |    直接关注   | 分组1       |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"4",
				"buy_number_end":"10.6",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs获得会员列表"没有符合要求的数据"

Scenario:10 过滤条件"最后购买时间"

	#区间时间边界值查询，不包含结束时间
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"2015-1-1 00:00:00",
				"last_buy_end_time":"2015-3-5 00:00:00",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom2  | 普通会员 |    0    |     50   |     325.00     |      162.50    |      2     | 2014-8-5 00:00:00 |    推广扫码   | 分组1       |
			| tom1  | 银牌会员 |    2    |     0    |     110.00     |      110.00    |      1     | 2014-8-4 23:59:59 |    直接关注   | 分组1       |

	#开始结束时间相同查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"2015-2-2 00:00:00",
				"last_buy_end_time":"2015-2-2 00:00:00",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":1
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom2  | 普通会员 |    0    |     50   |     325.00     |      162.50    |      2     | 2014-8-5 00:00:00 |    推广扫码   | 分组1       |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"2015-8-11 00:00:00",
				"last_buy_end_time":"2015-8-12 00:00:00",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs获得会员列表"没有符合要求的数据"

Scenario:11 过滤条件"积分范围"

	#区间查询，包含开始和结束数值
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"20",
				"integral_end":"100",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom4  | 金牌会员 |    0    |     20   |     0.00       |      0.00      |      0     | 2014-8-5 23:59:59 |    会员分享   | 分组3       |
			| tom3  | 银牌会员 |    1    |    100   |     335.00     |      111.67    |      3     | 2014-8-5 8:00:00  |    会员分享   | 分组1,分组3 |
			| tom2  | 普通会员 |    0    |     50   |     325.00     |      162.50    |      2     | 2014-8-5 00:00:00 |    推广扫码   | 分组1       |

	#开始结束数值相同
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"0",
				"integral_end":"0",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":7
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| bill3 | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    会员分享   |             |
			| bill2 | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    直接关注   |             |
			| bill  | 普通会员 |    1    |     0    |     0.00       |      0.00      |      0     |        今天       |    会员分享   |             |
			| tom7  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-10-1 8:00:00 |    直接关注   |             |
			| tom6  | 普通会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-10-1 8:00:00 |    推广扫码   |             |	
			| tom5  | 金牌会员 |    0    |     0    |     0.00       |      0.00      |      0     | 2014-8-6 00:00:00 |    会员分享   | 分组3       |
			| tom1  | 银牌会员 |    2    |     0    |     110.00     |      110.00    |      1     | 2014-8-4 23:59:59 |    直接关注   | 分组1       |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"grade":"全部",
				"grouping":"全部 ",
				"source":"全部",
				"total_spending_start":"",
				"total_spending_end":"",
				"buy_number_start":"",
				"buy_number_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"150",
				"integral_end":"300",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs获得会员列表"没有符合要求的数据"

Scenario:12 过滤条件"最后对话时间"

	#无法在feature中模拟到准确的对话时间，不能实现此场景

Scenario:13 过滤条件"条件组合查询"

	#空调条件查询，“重置”查询条件，空调间查询所有数据
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom",
				"status":"已关注",
				"attention_start_time":"2014-8-3 00:00:00",
				"attention_end_time":"今天",
				"grade":"银牌会员",
				"grouping":"分组1 ",
				"source":"推广扫码",
				"total_spending_start":"100",
				"total_spending_end":"325",
				"buy_number_start":"0",
				"buy_number_end":"2",
				"last_buy_start_time":"2015-1-1",
				"last_buy_end_time":"2015-2-2",
				"integral_start":"0",
				"integral_end":"50",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":1
			}]
			"""
		Then jobs获得会员列表
			| name  |   grade  | friends | integral | total_spending | customer_price | buy_number |   attention_time  | member_source |  grouping   |
			| tom2  | 普通会员 |    0    |     50   |     325.00     |      162.50    |      2     | 2014-8-5 00:00:00 |    推广扫码   | 分组1       |
