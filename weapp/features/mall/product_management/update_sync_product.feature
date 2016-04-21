# watcher: zhangsanxiang@weizoom.com,benchi@weizoom.com
#_author_:张三香 2016.03.31

Feature:自营平台-更新同步商品
	"""
	1、从'供货商'同步到'商城'的商品,其商品详情页面增加"下单位置:商城/供货商",默认选择'商城'
	2、供货商-指商家；商城-指微众系列的公众号统称（微众家、微众学生等等）
	3、'下单位置'当勾选'供货商'并保存时，验证该商品是否正在参与活动，如果参与则不能保存并提示： "请先停止该商品参与的活动"
	4、'下单位置'为'供货商'的商品不能参与活动,包括：限时抢购、买赠、积分应用、优惠券、禁用优惠券商品
	5、新建以下促销活动时,商品选择弹窗的商品列表中隐藏掉'下单位置'为'供货商'的商品：
		(限时抢购、买赠、积分应用、单品券及禁用优惠券商品)
	6、商品若参与了'未开始'或'进行中'状态的促销活动，修改下单位置为'供货商'保存时会弹出提示信息
	"""

#特殊说明：jobs、表示自营平台;bill、tom表示商家;

Background:
	#自营平台jobs的信息
		Given 设置jobs为自营平台账号
		Given jobs登录系统
		And jobs已添加支付方式
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
		When jobs开通使用微众卡权限
		When jobs添加支付方式
			"""
			[{
				"type": "微众卡支付",
				"is_active": "启用"
			}]
			"""
		And jobs已添加商品
			"""
			[{
				"name":"jobs自建商品0",
				"price":10.00
			}]
			"""

	#商家bill的信息
		Given 添加bill店铺名称为'bill商家'
		Given bill登录系统
		And bill已添加支付方式
			"""
			[{
				"type": "微信支付",
				"is_active": "启用"
			}]
			"""
		And bill已添加商品规格
			"""
			[{
				"name": "颜色",
				"type": "图片",
				"values": [{
					"name": "黑色",
					"image": "/standard_static/test_resource_img/icon_color/icon_1.png"
				}, {
					"name": "白色",
					"image": "/standard_static/test_resource_img/icon_color/icon_5.png"
				}]
			},{
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
				"name":"bill商品1",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0101",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.0
			},{
				"name":"bill商品2",
				"model": {
					"models": {
						"standard": {
							"price": 20.00,
							"user_code":"0102",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				}
			},{
				"name":"bill商品3",
				"is_enable_model": "启用规格",
				"model": {
					"models": {
						"黑色 S": {
							"price": 30.0,
							"weight": 1,
							"stock_type": "有限",
							"stocks": 100
						},
						"白色 S": {
							"price": 30.0,
							"weight": 2,
							"stock_type": "无限"
						}
					}
				}
			}]
			"""

	#商家tom的信息
		When tom暂停1秒
		Given 添加tom店铺名称为'tom商家'
		Given tom登录系统
		And tom已添加支付方式
			"""
			[{
				"type": "微信支付",
				"is_active": "启用"
			}]
			"""
		And tom已添加商品
			"""
			[{
				"name":"tom商品1",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0201",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"status":"在售"
			}]
			"""

	#jobs后台商品信息
		Given jobs登录系统
		When jobs批量将商品放入待售
			"""
			["tom商品1","bill商品2","bill商品1"]
			"""
		When jobs更新商品'bill商品1'
			"""
			{
				"name":"bill商品1下单位置商城",
				"supplier":"bill商家",
				"purchase_price": 9.00,
				"buy_position":"商城",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0101",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.00
			}
			"""
		When jobs更新商品'bill商品2'
			"""
			{
				"name":"bill商品2下单位置商城",
				"supplier":"bill商家",
				"purchase_price": 19.00,
				"buy_position":"商城",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 20.00,
							"user_code":"0102",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":0.00
			}
			"""
		When jobs更新商品'tom商品1'
			"""
			{
				"name":"tom商品1下单位置供货商",
				"supplier":"tom商家",
				"purchase_price": 9.00,
				"buy_position":"供货商",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0201",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.00
			}
			"""
		When jobs批量上架商品
			"""
			["bill商品1下单位置商城","bill商品2下单位置商城","tom商品1下单位置供货商"]
			"""

@mall2 @product @eugene @product_pool 
Scenario:1 商品参与限时抢购活动（未开始）,修改下单位置为'供货商'
	#bill商品1-下单位置选择'商城'
	#bill商品1-参与限时抢购活动
	#修改bill商品1的下单位置为'供货商',保存时提示'请先停止该商品参与的活动'

	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品1限时抢购",
			"promotion_title":"",
			"start_date": "明天",
			"end_date": "1天后",
			"product_name":"bill商品1下单位置商城",
			"member_grade": "全部会员",
			"count_per_purchase": 2,
			"promotion_price": 8.00,
			"limit_period": 1
		}]
		"""
	When jobs更新商品'bill商品1下单位置商城'
			"""
			{
				"name":"bill商品1下单位置商城",
				"supplier":"bill商家",
				"purchase_price": 9.00,
				"buy_position":"供货商",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0101",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.00
			}
			"""
	Then jobs获得提示"请先停止该商品参与的活动"

@mall2 @product @eugene @product_pool
Scenario:2 商品参与买赠活动,修改下单位置为'供货商'
	#bill商品1-下单位置选择'商城'
	#bill商品1-参与买赠活动
	#修改bill商品1的下单位置为'供货商',保存时提示'请先停止该商品参与的活动'

	Given jobs登录系统
	When jobs创建买赠活动
		"""
		[{
			"name": "商品1买二赠一",
			"promotion_title":"",
			"start_date": "今天",
			"end_date": "1天后",
			"member_grade": "全部会员",
			"product_name": "bill商品1下单位置商城",
			"premium_products":
				[{
					"name": "bill商品1下单位置商城",
					"count": 1
				}],
			"count": 2,
			"is_enable_cycle_mode": true
		}]
		"""
	When jobs更新商品'bill商品1下单位置商城'
			"""
			{
				"name":"bill商品1下单位置商城",
				"supplier":"bill商家",
				"purchase_price": 9.00,
				"buy_position":"供货商",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0101",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.00
			}
			"""
	Then jobs获得提示"请先停止该商品参与的活动"

@mall2 @product @eugene @product_pool
Scenario:3 商品参与积分应用活动,修改下单位置为'供货商'
	#bill商品1-下单位置选择'商城'
	#bill商品1-参与积分应用活动
	#修改bill商品1的下单位置为'供货商',保存时提示'请先停止该商品参与的活动'

	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "bill商品1下单位置商城",
			"is_permanant_active": false,
			"discount": 50,
			"discount_money": 50.0
		}]
		"""
	When jobs更新商品'bill商品1下单位置商城'
			"""
			{
				"name":"bill商品1下单位置商城",
				"supplier":"bill商家",
				"purchase_price": 9.00,
				"buy_position":"供货商",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0101",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.00
			}
			"""
	Then jobs获得提示"请先停止该商品参与的活动"

@mall2 @product @eugene @product_pool
Scenario:4 商品参与单品券,修改下单位置为'供货商'
	#bill商品1-下单位置选择'商城'
	#bill商品1-参与单品券
	#修改bill商品1的下单位置为'供货商',保存时提示'请先停止该商品参与的活动'

	Given jobs登录系统
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "单品券1",
			"money": 10.00,
			"limit_counts": 10,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "bill商品1下单位置商城"
		}]
		"""
	When jobs更新商品'bill商品1下单位置商城'
			"""
			{
				"name":"bill商品1下单位置商城",
				"supplier":"bill商家",
				"purchase_price": 9.00,
				"buy_position":"供货商",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0101",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.00
			}
			"""
	Then jobs获得提示"请先停止该商品参与的活动"

@mall2 @product @eugene @product_pool
Scenario:5 商品参与禁用优惠券商品,修改下单位置为'供货商'
	#bill商品1-下单位置选择'商城'
	#bill商品1-参与禁用优惠券商品
	#修改bill商品1的下单位置为'供货商',保存时提示'请先停止该商品参与的活动'

	Given jobs登录系统
	When jobs添加禁用优惠券商品
		"""
		[{
			"products":[{
				"name":"bill商品1下单位置商城"
			}],
			"start_date": "",
			"end_date": "",
			"is_permanant_active": 1
		}]
		"""
	When jobs更新商品'bill商品1下单位置商城'
			"""
			{
				"name":"bill商品1下单位置商城",
				"supplier":"bill商家",
				"purchase_price": 9.00,
				"buy_position":"供货商",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0101",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.00
			}
			"""
	Then jobs获得提示"请先停止该商品参与的活动"