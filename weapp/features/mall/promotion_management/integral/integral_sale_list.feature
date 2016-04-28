#_author_：张三香 2016.04.27

Feature:浏览积分应用活动列表
	"""
		1）多商品积分应用，列表中显示该活动的所有商品，并且共用'抵扣上限'、'金额占比'、'状态'、'起止时间'和'操作'5个字段，对应的字段值居中显示；
		2）积分活动中的商品状态发生变化，下架或者删除，列表中对应商品图片下方位置显示该商品的状态（待售和已删除）
		3）多商品积分应用，列表中的'金额占比'显示最小的那个值
		4)商品部分或全部下架，活动状态不变
		5）商品部分删除，活动状态不变；全部删除后，活动变为'已结束'
		6）自营平台
			积分应用活动（多商品），部分或全部商品【更新】后，活动状态不变
	"""

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
			"name": "商品01",
			"price": 10.00
		}, {
			"name": "商品02",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 10.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 20.00,
						"stock_type": "无限"
					}
				}
			}
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
		}]
		"""
	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2
		}
		"""

@promotionIntegral @integral 
Scenario:1 积分应用活动（单商品），商品下架或下架后再上架，活动状态不变
	Given jobs登录系统
	#积分应用活动（单个商品）-商品下架,活动状态不变
		When jobs创建积分应用活动
			"""
			[{
				"name": "单商品积分应用1",
				"promotion_title":"",
				"start_date": "今天",
				"end_date": "10天后",
				"product_name": "商品01",
				"is_permanent_active": false,
				"rules": 
					[{
						"member_grade": "全部会员",
						"discount": 50,
						"discount_money": 5.00
					}]
			}]
			"""
		Then jobs获取积分应用活动列表
			"""
			[{
				"name":"单商品积分应用1",
				"product_name": "商品01",
				"status":"进行中"
			}]
			"""
		When jobs'下架'商品'商品01'
		Then jobs获取积分应用活动列表
			"""
			[{
				"name":"单商品积分应用1",
				"product_name": "商品1",
				"products_status":[{
					"name": "商品01",
					"status": "待售"
					}],
				"status":"进行中"
			}]
			"""
	#积分应用活动（单个商品）-商品下架后再上架,商品可继续参与积分应用活动
		When jobs'上架'商品'商品01'
		Then jobs获取积分应用活动列表
			"""
			[{
				"name":"单商品积分应用1",
				"product_name": "商品01",
				"status":"进行中"
			}]
			"""

@promotionIntegral @integral
Scenario:2 积分应用活动（多商品），商品部分或全部下架，活动状态不变
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "多商品积分应用1",
			"promotion_title":"",
			"product_name": "商品01,商品02",
			"is_permanent_active": true,
			"rules": 
				[{
					"member_grade": "普通会员",
					"discount": 50,
					"discount_money": 5.00
				},{
					"member_grade": "铜牌会员",
					"discount": 55,
					"discount_money": 5.50
				},{
					"member_grade": "银牌会员",
					"discount": 100,
					"discount_money": 10.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name": "多商品积分应用1",
			"product_name": "商品01,商品02",
			"product_price":"10.00,10.00 ~ 20.00",
			"is_permanent_active": true,
			"discount": "50.0%~100.0%",
			"discount_money":"5.00~10.00",
			"status":"进行中"
		}]
		"""

	#商品部分下架,活动状态不变
		When jobs'下架'商品'商品01'
		Then jobs获取积分应用活动列表
			"""
			[{
				"name": "多商品积分应用1",
				"product_name": "商品01,商品02",
				"products_status":[{
					"name": "商品01",
					"status": "待售"
					}],
				"status":"进行中",
				"is_permanent_active": true
			}]
			"""
	#商品全部下架,活动状态不变
		When jobs'下架'商品'商品02'
		Then jobs获取积分应用活动列表
			"""
			[{
				"name": "多商品积分应用1",
				"product_name": "商品01,商品02",
				"products_status":[{
						"name": "商品01",
						"status": "待售"
					},{
						"name": "商品02",
						"status": "待售"
					}],
				"status":"进行中",
				"is_permanent_active": true
			}]
			"""

@promotionIntegral @integral
Scenario:3 积分应用活动（多商品），商品部分或全部删除
	#积分应用活动（多商品），商品部分删除，活动状态不变
	#积分应用活动（多商品），商品全部删除，活动状态为已结束

	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "多商品积分应用1",
			"start_date": "今天",
			"end_date": "10天后",
			"product_name": "商品01,商品02",
			"is_permanent_active": false,
			"rules": 
				[{
					"member_grade": "全部会员",
					"discount": 50,
					"discount_money": 5.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name": "多商品积分应用1",
			"product_name": "商品01,商品02",
			"product_price":"10.00,10.00 ~ 20.00",
			"start_date": "今天",
			"end_date": "10天后",
			"is_permanent_active": false,
			"discount": "50.0%",
			"discount_money":5.00,
			"status":"进行中"
		}]
		"""
	#商品部分删除，活动状态不变
		When jobs'删除'商品'商品01'
		Then jobs获取积分应用活动列表
			"""
			[{
				"name": "多商品积分应用1",
				"product_name": "商品01,商品02",
				"products_status":[{
					"name": "商品01",
					"status": "已删除"
					}],
				"status":"进行中"
			}]
			"""
	#商品全部删除，活动状态为已结束
		When jobs'删除'商品'商品02'
		Then jobs获取积分应用活动列表
			"""
			[{
				"name": "多商品积分应用1",
				"product_name": "商品01,商品02",
				"products_status":[{
						"name": "商品01",
						"status": "已删除"
					},{
						"name": "商品02",
						"status": "已删除"
					}],
				"status":"已结束"
			}]
			"""

@promotionIntegral @integral
Scenario:4 自营平台对商家同步的商品部分或全部进行【更新】操作，活动状态不变
	#商家bill的商品信息
		Given 添加bill店铺名称为'bill商家'
		Given bill登录系统
		When bill已添加支付方式
			"""
			[{
				"type": "微信支付",
				"is_active": "启用"
			}, {
				"type": "支付宝",
				"is_active": "启用"
			}, {
				"type": "货到付款",
				"is_active": "启用"
			}]
			"""
		And bill已添加商品规格
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
		And bill已添加商品
			"""
			[{
				"name": "bill无规格商品1",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"1112",
							"weight": 5.0,
							"stock_type": "无限"
						}
					}
				}
			},{
				"name": "bill多规格商品2",
				"is_enable_model": "启用规格",
				"model": {
					"models": {
						"M": {
							"price": 10.00,
							"user_code":"4412",
							"weight":1.0,
							"stock_type": "有限",
							"stocks":100
						},
						"S": {
							"price": 20.00,
							"user_code":"4413",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				}
			},{
				"name": "bill无规格商品2",
					"model": {
						"models": {
							"standard": {
								"price": 20.00,
								"user_code":"1112",
								"weight": 5.0,
								"stock_type": "无限"
							}
						}
					}
			}]
			"""

	#自营平台nokia数据
		Given 设置nokia为自营平台账号
		Given nokia登录系统
		When nokia已添加支付方式
			"""
			[{
				"type": "微信支付",
				"is_active": "启用"
			}, {
				"type": "支付宝",
				"is_active": "启用"
			}, {
				"type": "货到付款",
				"is_active": "启用"
			}]
			"""
		Given nokia设定会员积分策略
			"""
			{
				"integral_each_yuan": 2
			}
			"""
		When nokia批量将商品放入待售
			"""
			["bill无规格商品1","bill无规格商品2"]
			"""

	#自营nokia更新商品并上架商品，创建多商品积分应用活动
		When nokia更新商品'bill无规格商品1'
			"""
			{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": 9.00,
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"1112",
							"weight": 5.0,
							"stock_type": "无限"
						}
					}
				}
			}
			"""
		When nokia更新商品'bill无规格商品2'
			"""
			{
				"name": "bill无规格商品2",
				"supplier": "bill商家",
				"purchase_price": 10.00,
				"model": {
					"models": {
						"standard": {
							"price": 20.00,
							"user_code":"1112",
							"weight": 5.0,
							"stock_type": "无限"
						}
					}
				}
			}
			"""
		When nokia'上架'商品'bill无规格商品1'
		When nokia'上架'商品'bill无规格商品2'
		When nokia创建积分应用活动
			"""
			[{
				"name": "多商品积分应用1",
				"promotion_title":"",
				"product_name": "bill无规格商品1,bill无规格商品2",
				"is_permanent_active": true,
				"rules": 
					[{
						"member_grade": "全部会员",
						"discount": 50,
						"discount_money": 5.00
					}]
			}]
			"""
		Then nokia获取积分应用活动列表
			"""
			[{
				"name": "多商品积分应用1",
				"product_name": "bill无规格商品1,bill无规格商品2",
				"product_price":"10.00,20.00",
				"is_permanent_active": true,
				"discount": "50.0%",
				"discount_money":5.00,
				"status":"进行中"
			}]
			"""

	#商家bill修改商品
		Given bill登录系统
		When bill更新商品'bill无规格商品1'
			"""
			{
				"name": "bill无规格商品01",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"1112",
							"weight": 5.0,
							"stock_type": "无限"
						}
					}
				}
			}
			"""
		When bill更新商品'bill无规格商品2'
			"""
			{
				"name": "bill无规格商品02",
				"model": {
					"models": {
						"standard": {
							"price": 20.00,
							"user_code":"1112",
							"weight": 5.0,
							"stock_type": "无限"
						}
					}
				}
			}
			"""

	#自营nokia对同步商品进行【更新】操作，查看活动状态
		Given nokia登录系统
		#更新全部商品，商品部分下架，活动状态不变
		When nokia更新商品池商品'bill无规格商品01'于'2016-04-20 10:30'
		Then nokia获取积分应用活动列表
			"""
			[{
				"name": "多商品积分应用1",
				"product_name": "bill无规格商品01,bill无规格商品2",
				"products_status":[{
					"name": "bill无规格商品01",
					"status": "待售"
					}],
				"is_permanent_active": true,
				"status":"进行中"
			}]
			"""
		#更新全部商品，商品全部下架，活动状态不变
		When nokia更新商品池商品'bill无规格商品02'于'2016-04-21 10:30'
		Then nokia获取积分应用活动列表
			"""
			[{
				"name": "多商品积分应用1",
				"product_name": "bill无规格商品01,bill无规格商品02",
				"products_status":[{
					"name": "bill无规格商品01",
					"status": "待售"
				},{
					"name": "bill无规格商品02",
					"status": "待售"
				}],
				"is_permanent_active": true,
				"status":"进行中"
			}]
			"""