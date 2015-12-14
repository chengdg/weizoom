# _edit_ : "新新8.20"
@func:webapp.modules.mall.views.list_products
Feature: 在webapp中购买有运费的商品
	bill能在webapp中购买jobs添加的"有运费的商品"

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
		}, {
			"name": "颜色",
			"type": "文字",
			"values": [{
				"name": "red"
			}, {
				"name": "black"
			}]
		}]
		"""
	And jobs已添加运费配置
		"""
		[{
			"name":"顺丰",
			"first_weight": 1,
			"first_weight_price": 13.00,
			"added_weight": 1,
			"added_weight_price": 5.00,
			"special_area": [{
				"to_the":"北京市,江苏省",
				"first_weight": 1,
				"first_weight_price": 20.00,
				"added_weight": 1,
				"added_weight_price": 10.00
			}],
			"free_postages": [{
				"to_the":"北京市",
				"condition": "count",
				"value": 3
			},{
				"to_the":"北京市",
				"condition": "money",
				"value": 200.0
			}]
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"weight": 1,
			"postage": "系统"
		}, {
			"name": "商品2",
			"price": 20.00,
			"weight": 0.6,
			"postage": "系统"
		}, {
			"name": "商品3",
			"price": 100.00,
			"weight": 1,
			"postage": "系统"
		}, {
			"name": "商品4",
			"price": 10.00,
			"weight": 1,
			"postage": 0.0
		}, {
			"name": "商品5",
			"price": 10.00,
			"weight": 1,
			"postage": 15.0
		}, {
			"name": "商品6",
			"price": 10.00,
			"weight": 1,
			"postage": 10.0
		}, {
			"name": "商品7",
			"postage": "系统",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"red M": {
						"price": 50.00,
						"weight": 1,
						"stock_type": "无限"
					},
					"black S": {
						"price": 50.00,
						"weight": 1,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品8",
			"postage": 10.0,
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 50.00,
						"weight": 0.6,
						"stock_type": "无限"
					},
					"S": {
						"price": 50.00,
						"weight": 0.6,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	When jobs选择'顺丰'运费配置
	Given bill关注jobs的公众号
	And tom关注jobs的公众号


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage 
Scenario: 购买单个商品，使用系统运费模板，满足续重
	
	When bill访问jobs的webapp
	When bill设置jobs的webapp的收货地址
		"""
		{
			"area": "河北省 邯郸市 复兴区"
		}
		"""
	When bill访问jobs的webapp:ui
	And bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品1",
				"count": 2
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 218.00,
				"product_price": 200.00,
				"postage": 18.00,
				"integral_money": 0.0,
				"promotion_money": 0.0,
				"coupon_money": 0.0
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 218.00,
			"pay_interface": "货到付款"
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage 
Scenario: 购买单个商品，使用系统运费模板，不满足续重
	
	When bill访问jobs的webapp
	When bill设置jobs的webapp的收货地址
		"""
		{
			"area": "河北省 邯郸市 复兴区"
		}
		"""
	When bill访问jobs的webapp:ui
	And bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品1",
				"count": 1
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 113.00,
				"product_price": 100.00,
				"postage": 13.00,
				"integral_money": 0.0,
				"promotion_money": 0.0,
				"coupon_money": 0.0
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 113.00
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage 
Scenario: 购买单个商品，使用统一运费商品
	
	When bill访问jobs的webapp
	When bill设置jobs的webapp的收货地址
		"""
		{
			"area": "河北省 邯郸市 复兴区"
		}
		"""
	When bill访问jobs的webapp:ui
	And bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品5",
				"count": 2
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 35.00,
				"product_price": 20.00,
				"postage": 15.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 35.00
		}
		"""
	When bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品4",
				"count": 2
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 20.00,
				"product_price": 20.00,
				"postage": 0.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 20.00
		}
		"""

@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage
Scenario: 购买单个商品，使用系统运费模板，满足金额包邮条件
	
	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
	When bill访问jobs的webapp:ui
	And bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品1",
				"count": 2
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 200.00,
				"product_price": 200.00,
				"postage": 0.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 200.00
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage
Scenario: 购买单个商品，使用系统运费模板，满足数量包邮条件
	
	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
	When bill访问jobs的webapp:ui
	And bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品2",
				"count": 3
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 60.00,
				"product_price": 60.00,
				"postage": 0.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 60.00
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage
Scenario: 购买多种商品，使用统一运费
	
	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
	#第一次购买
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品4",
			"count": 1
		}, {
			"name": "商品5",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 35.00,
				"product_price": 20.00,
				"postage": 15.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 35.00
		}
		"""
	#第二次购买
	When bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品6",
			"count": 1
		}, {
			"name": "商品5",
			"count": 1
		}]
		"""
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 45.00,
				"product_price": 20.00,
				"postage": 25.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 45.00
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage
Scenario: 购买多种商品，使用系统运费模板，满足普通续重
	顺丰，河北，2公斤，运费18元
	
	When bill访问jobs的webapp
	When bill设置jobs的webapp的收货地址
		"""
		{
			"area": "河北省 邯郸市 复兴区"
		}
		"""
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品3",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 218.00,
				"product_price": 200.00,
				"postage": 18.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 218.00
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage
Scenario: 购买多种商品，使用系统运费模板，满足特殊地区续重
	顺丰，北京，1.6公斤，运费30元
	
	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品2",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 150.00,
				"product_price": 120.00,
				"postage": 30.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 150.00
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage
Scenario: 购买多种商品，使用系统运费模板，合起来满足数量包邮
	顺丰，北京，3件商品，包邮
	
	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品2",
			"count": 2
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 140.00,
				"product_price": 140.00,
				"postage": 0.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 140.00
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage
Scenario: 购买多种商品，使用系统运费模板，合起来满足金额包邮
	顺丰，北京，商品金额200元，包邮
	
	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品3",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 200.00,
				"product_price": 200.00,
				"postage": 0.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 200.00
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage
Scenario: 购买多种商品，使用统一运费+系统运费模板，普通运费
	
	When bill访问jobs的webapp
	When bill设置jobs的webapp的收货地址
		"""
		{
			"area": "河北省 邯郸市 复兴区"
		}
		"""
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品5",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 138.00,
				"product_price": 110.00,
				"postage": 28.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 138.00
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage
Scenario: 购买多种商品，使用统一运费+系统运费模板，特殊地区运费
	合起来数量满足包邮，但商品5不是使用系统运费模板，所以不包邮

	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品2",
			"count": 2
		}, {
			"name": "商品5",
			"count": 2
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 105.00,
				"product_price": 60.00,
				"postage": 45.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 105.00
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage
Scenario: 购买多种商品，使用统一运费+系统运费模板，特殊地区运费
	使用系统运费模板的商品满足数量包邮，运费为使用统一运费商品的运费

	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品2",
			"count": 2
		}, {
			"name": "商品5",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 165.00,
				"product_price": 150.00,
				"postage": 15.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 165.00
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.postage
Scenario: 购买多种商品，使用统一运费+系统运费模板，特殊地区运费
	使用系统运费模板的商品满足金额包邮，运费为使用统一运费商品的运费

	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品3",
			"count": 1
		}, {
			"name": "商品5",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 225.00,
				"product_price": 210.00,
				"postage": 15.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 225.00
		}
		"""
# _edit_ : "新新8.20"
Scenario: 购买多规格商品，使用系统运费模板，特殊地区，满足续重
	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品7",
			"count": 1,
			"model": "red M"
		}, {
			"name": "商品7",
			"count": 1,
			"model": "black S"
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 130.00,
				"product_price": 100.00,
				"postage": 30.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 130.00
		}
		"""
# _edit_ : "新新8.20"
Scenario: 购买两个多规格商品
	1 商品7使用系统运费模板，特殊地区，满足续重
	2 商品8使用统一运费10元
	3 运费总额为30+10

	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品7",
			"count": 1,
			"model": "red M"
		}, {
			"name": "商品7",
			"count": 1,
			"model": "black S"
		},{
			"name": "商品8",
			"count": 1,
			"model": "M"
		}, {
			"name": "商品8",
			"count": 1,
			"model": "S"
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 240.00,
				"product_price": 200.00,
				"postage": 40.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 240.00
		}
		"""
# _edit_ : "新新8.20"
Scenario: jobs选择'免运费'运费配置
	Given jobs登录系统
	When jobs选择'免运费'运费配置
	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 2
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 200.00,
				"product_price": 200.00,
				"postage": 0.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 200.00
		}
		"""
# _edit_ : "新新8.20"
Scenario: 更新邮费配置后进行购买
	jobs更改邮费配置后bill进行购买
	1.去掉特殊地区和指定地区
	2.bill创建订单成功，邮费正常
	Given jobs登录系统
	When jobs修改'顺丰'运费配置
		"""
		[{
			"name":"顺丰",
			"first_weight": 1,
			"first_weight_price": 13.00,
			"added_weight": 1,
			"added_weight_price": 5.00
		}]
		"""
	Then jobs能获取'顺丰'运费配置
		"""
		[{
			"name":"顺丰",
			"first_weight": 1,
			"first_weight_price": 13.00,
			"added_weight": 1,
			"added_weight_price": 5.00
		}]
		"""
	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
		#第一次购买
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 113.00,
				"product_price": 100.00,
				"postage": 13.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 113.00
		}
		"""
	#第二次购买
	When bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 3
		}]
		"""
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 323.00,
				"product_price": 300.00,
				"postage": 23.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 323.00
		}
		"""
# _edit_ : "新新8.20"
Scenario: 不同等级的会员购买有会员价同时有运费配置
#包邮条件:金额取商品原价的金额
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品14",
			"price": 100.00,
			"member_price": true,
			"weight": 1,
			"postage": "系统",
			"is_member_product": "on"
		}]
		"""
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}]
		"""
	And jobs更新'bill'的会员等级
		"""
		{
			"name": "bill",
			"member_rank": "铜牌会员"
		}
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"discount": "10"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}]
		"""
	And jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "普通会员"
		}, {
			"name": "bill",
			"member_rank": "铜牌会员"
		}]
		"""
###tom购买,订单金额
	When tom访问jobs的webapp
	When tom设置jobs的webapp的默认收货地址
	And tom加入jobs的商品到购物车
		"""
		[{
			"name": "商品14",
			"count": 2
		}]
		"""
	When tom访问jobs的webapp:ui
	And tom从购物车发起购买操作:ui
	Then tom获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 200.00,
				"product_price": 200.00,
				"postage": 0.00
			}
		}
		"""
	When tom使用'货到付款'购买订单中的商品:ui
	Then tom获得支付结果:ui
		"""
		{
			"price": 200.00
		}
		"""
###bill购买,订单金额
	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址
		#第一次购买
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品14",
			"count": 2
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 180.00,
				"product_price": 180.00,
				"postage": 0.00
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 180.00
		}
		"""
