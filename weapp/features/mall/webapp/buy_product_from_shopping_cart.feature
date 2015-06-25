# last change(2015-06-23 19:12) by: yanzhao@weizoom.com

@func:webapp.modules.mall.views.list_products
Feature: 在webapp中从购物车中购买商品
	bill能在webapp中从购物车中购买商品

Background:
	Given jobs登录系统
	When jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}]
		"""
	When jobs开通使用微众卡权限
	When jobs添加支付方式
		"""
		[{
			"type": "微众卡支付",
			"description": "我的微众卡支付",
			"is_active": "启用"
		}]
		"""
	When jobs添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00
		},{
			"name":"EMS",
			"first_weight":1,
			"first_weight_price":0.00,
			"added_weight":1,
			"added_weight_price":0.00,
			"special_area": [{
				"to_the":"河北省",
				"first_weight_price":20.00,
				"added_weight_price":10.00
			},{
				"to_the":"北京市,天津市",
				"first_weight_price":30.00,
				"added_weight_price":20.00
			}]
		}]
		"""
	And jobs选择'顺丰'运费配置
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 3.3
		}, {
			"name": "商品2",
			"price": 5.3
		}, {
			"name": "商品3",
			"price": 5.5
		}, {
			"name": "商品4",
			"price": 2.0,
			"weight":1,
			"pay_interfaces":[{
				"type": "在线支付"
			}],
			"postage": "顺丰"
		}, {
			"name": "商品5",
			"price": 3.0,
			"weight":1,
			"pay_interfaces":[{
				"type": "在线支付"
			}],
			"postage": "顺丰"
		}, {
			"name": "商品6",
			"price": 5.0,
			"weight":1,
			"postage": "0"
		}, {
			"name": "商品7",
			"price": 10.0,
			"weight":1,
			"postage": "0"
		}]
		"""
	Given tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品2",
			"count": 2
		}]
		"""

@mall @mall2 @zy_wsc01 @mall.webapp @mall.webapp.shopping_cart
Scenario: 从购物车购买单个商品
	bill将jobs的一个商品加入购物车后
	1. bill能从购物车中下单
	2. bill的订单中的信息正确
	3. bill的购物车被清空
	4. tom的购物车不受影响

	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 2
		}]
		"""
	When bill从购物车发起购买操作
		"""
		{
			"action": "click",
			"context": [{
				"name": "商品1"
			}]
		}
		"""
	Then bill获得待编辑订单
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	When bill从购物车发起购买操作
	"""
	{
		"action": "pay",
		"context": [{
			"name": "商品1"
		}]
	}
	"""

	And bill填写收货信息
	"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
	"""

	And bill在购物车订单编辑中点击提交订单
	"""
	{
		"pay_type": "货到付款"
	}
	"""

	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"final_price": 6.6,
			"products": [{
				"name": "商品1",
				"price": 3.3,
				"count": 2
			}]
		}
		"""
	And bill能获得购物车
		"""
		{
			"product_groups": [],
			"invalid_products": []
		}
		"""
	When tom访问jobs的webapp
	Then tom能获得购物车
		"""
		{
			"product_groups": [{
				"promotion": null,
				"can_use_promotion": false,
				"products": [{
					"name": "商品1",
					"count": 1
				}]
			}, {
				"promotion": null,
				"can_use_promotion": false,
				"products": [{
					"name": "商品2",
					"count": 2
				}]
			}],
			"invalid_products": []
		}
		"""

@mall @mall2 @zy_wsc02 @mall.webapp @mall.webapp.shopping_cart
Scenario: 从购物车购买全部商品
	bill将jobs的多个商品加入购物车后
	1. bill能从购物车中下单
	2. bill的订单中的信息正确
	3. bill的购物车被清空
	4. tom的购物车不受影响

	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 2
		}, {
			"name": "商品2",
			"count": 1
		}]
		"""
	When bill从购物车发起购买操作
		"""
			{
				"action": "click",
				"context": [{
					"name": "商品1"
				}, {
					"name": "商品2"
				}]
			}
		"""
	Then bill获得待编辑订单
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}, {
				"name": "商品2",
				"count": 1
			}]
		}
		"""
	When bill从购物车发起购买操作
		"""
			{
				"action": "pay",
				"context": [{
					"name": "商品1"
				}, {
					"name": "商品2"
				}]
			}
		"""
  And bill填写收货信息
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
  And bill在购物车订单编辑中点击提交订单
  """
  {
  	"pay_type": "货到付款"
  }
  """
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"final_price": 11.9,
			"products": [{
				"name": "商品1",
				"price": 3.3,
				"count": 2
			}, {
				"name": "商品2",
				"price": 5.3,
				"count": 1
			}]
		}
		"""
	And bill能获得购物车
		"""
		{
      "product_groups": [],
      "invalid_products": []
		}
		"""
	When tom访问jobs的webapp
	Then tom能获得购物车
		"""
		{
      "product_groups": [{
        "promotion": null,
        "can_use_promotion": false,
        "products": [{
          "name": "商品1",
          "count": 1
        }]
      }, {
        "promotion": null,
        "can_use_promotion": false,
        "products": [{
          "name": "商品2",
          "count": 2
        }]
      }],
      "invalid_products": []
		}
		"""


@mall @mall2 @zy_wsc03 @mall.webapp @mall.webapp.shopping_cart
Scenario: 从购物车购买部分商品
	bill将jobs的多个商品加入购物车后
	1. bill能从购物车中下单,购买部分商品
	2. bill的订单中的信息正确
	3. bill的购物车已下单的商品被清除
	4. tom的购物车不受影响

	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 2
		}, {
			"name": "商品2",
			"count": 1
		}, {
			"name": "商品3",
			"count": 2
		}]
		"""
	When bill从购物车发起购买操作
		"""
				{
					"action": "click",
					"context": [{
						"name": "商品1"
					}, {
						"name": "商品2"
					}, {
						"name": "商品3"
					}]
				}
		"""
	Then bill能获得待编辑订单
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}, {
				"name": "商品2",
				"count": 1
			}, {
				"name": "商品3",
				"count": 2
			}]
		}
		"""
	When bill从购物车发起购买操作
		"""
				{
					"action": "pay",
					"context": [{
						"name": "商品1"
					}, {
						"name": "商品3"
					}]
				}
		"""
	And bill填写收货信息
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
	And bill在购物车订单编辑中点击提交订单
	"""
	{
    "pay_type": "货到付款"
  }
  """
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"final_price": 17.6,
			"products": [{
				"name": "商品1",
				"price": 3.3,
				"count": 2
			}, {
				"name": "商品3",
				"price": 5.5,
				"count": 2
			}]
		}
		"""
	And bill能获得购物车
		"""
		{

			"product_groups": [{
        "promotion": null,
        "can_use_promotion": false,
        "products": [{
          "name": "商品2",
          "count": 1
        }]
      }],
			"invalid_products": []
		}
		"""
	When tom访问jobs的webapp
	Then tom能获得购物车
		"""
		{

      "product_groups": [{
        "promotion": null,
        "can_use_promotion": false,
        "products": [{
          "name": "商品1",
          "count": 1
        }]
      }, {
        "promotion": null,
        "can_use_promotion": false,
        "products": [{
          "name": "商品2",
          "count": 2
        }]
      }],
      "invalid_products": []
		}
		"""

@mall @mall2 @zy_wsc04 @mall.webapp @mall.webapp.shopping_cart
Scenario: 从购物车购买空商品
	bill将jobs的多个商品加入购物车后
	1. bill不选中商品去下单
	2. bill下单失败
	3. bill的购物车没有变化
	4. tom的购物车不受影响

	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 2
		}, {
			"name": "商品2",
			"count": 1
		}, {
			"name": "商品3",
			"count": 2
		}]
		"""
	When bill从购物车发起购买操作
		"""
			{
				"action": "click",
				"context": [{
					"name": "商品1"
				}, {
					"name": "商品2"
				}, {
					"name": "商品3"
				}]
			}
		"""
	Then bill能获得待编辑订单
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}, {
				"name": "商品2",
				"count": 1
			}, {
				"name": "商品3",
				"count": 2
			}]
		}
		"""
	When bill从购物车发起购买操作
	"""
	{
    "action": "pay",
    "context": []
  }
  """
	Then bill能获得购物车
		"""
		{
			"product_groups": [{
				"promotion": null,
				"can_use_promotion": false,
				"products": [{
					"name": "商品1",
					"count": 2
				}]
			}, {
				"promotion": null,
				"can_use_promotion": false,
				"products": [{
					"name": "商品2",
					"count": 1
				}]
			}, {
				"promotion": null,
				"can_use_promotion": false,
				"products": [{
					"name": "商品3",
					"count": 2
				}]
			}],
			"invalid_products": []
		}
		"""
	When tom访问jobs的webapp
	Then tom能获得购物车
		"""
		{
      "product_groups": [{
        "promotion": null,
        "can_use_promotion": false,
        "products": [{
          "name": "商品1",
          "count": 1
        }]
      }, {
        "promotion": null,
        "can_use_promotion": false,
        "products": [{
          "name": "商品2",
          "count": 2
        }]
      }],
      "invalid_products": []
		}
		"""


@mall @mall2 @zy_wsc05 @mall.webapp @mall.webapp.shopping_cart
Scenario: 从购物车购买商品时有商品下架
	bill将jobs的多个商品加入购物车，并进入订单编辑后，jobs将其中某个商品下架
	1. bill下单失败
	2. bill的购物车不受影响

	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 2
		}, {
			"name": "商品2",
			"count": 1
		}]
		"""
	When bill从购物车发起购买操作
		"""
			{
				"action": "click",
				"context": [{
					"name": "商品1"
				}, {
					"name": "商品2"
				}]
			}
		"""
	Then bill能获得待编辑订单
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}, {
				"name": "商品2",
				"count": 1
			}]
		}
		"""



	When bill从购物车发起购买操作
	"""
	{
    "action": "pay",
    "context": [{
      "name": "商品1"
    },{
      "name": "商品2"
    }]
  }

  """
  And bill填写收货信息
  """
  {
    "ship_name": "bill",
    "ship_tel": "13811223344",
    "area": "北京市 北京市 海淀区",
    "ship_address": "泰兴大厦"
  }
  """
	Given jobs登录系统
	When jobs下架商品'商品1'
	When bill访问jobs的webapp
	When bill在购物车订单编辑中点击提交订单
	"""
	{
    "pay_type": "货到付款"
  }
  """

	Then bill获得错误提示'有商品已下架<br/>2秒后返回购物车<br/>请重新下单'


@mall @mall2 @zy_wsc06 @mall.webapp @mall.webapp.shopping_cart
Scenario: 从购物车同时购买"有运费和无运费"的商品，并且商品总重超过续重阈值
	bill将jobs有运费的商品和无运费的商品加入购物车后
	1. bill能从购物车中下单,购买商品
	2. bill的订单中的信息正确

	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品4",
			"count": 2
		}, {
			"name": "商品5",
			"count": 1
		}, {
			"name": "商品6",
			"count": 1
		}]
		"""
	When bill从购物车发起购买操作
		"""
			{
				"action": "click",
				"context": [{
					"name": "商品4"
				}, {
					"name": "商品5"
				}, {
					"name": "商品6"
				}]
			}
		"""
	Then bill能获得待编辑订单
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 2
			}, {
				"name": "商品5",
				"count": 1
			}, {
				"name": "商品6",
				"count": 1
			}]
		}
		"""
	When bill从购物车发起购买操作
		"""
				{
					"action": "pay",
					"context": [{
						"name": "商品4"
					}, {
						"name": "商品5"
					}, {
						"name": "商品6"
					}]
				}
		"""
	And bill填写收货信息
	"""
	{
      "ship_name": "bill",
      "ship_tel": "13811223344",
      "area": "北京市 北京市 海淀区",
      "ship_address": "泰兴大厦"
  }
  """
	And bill在购物车订单编辑中点击提交订单
	"""
	{
    "pay_type": "货到付款"
  }
  """
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 37.0,
			"postage":25.0
		}
		"""


@mall @mall2 @zy_wsc07 @mall.webapp @mall.webapp.shopping_cart
Scenario: 从购物车同时购买"有运费和无运费"的商品，并且商品总重低于续重阈值
	bill将jobs有运费的商品和无运费的商品加入购物车后
	1. bill能从购物车中下单,购买商品
	2. bill的订单中的信息正确

	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品5",
			"count": 1
		}, {
			"name": "商品6",
			"count": 1
		}]
		"""
	When bill从购物车发起购买操作
		"""
				{
					"action": "click",
					"context": [{
						"name": "商品5"
					}, {
						"name": "商品6"
					}]
				}
		"""
	Then bill获得待编辑订单
		"""
		{
			"products": [{
				"name": "商品5",
				"count": 1
			}, {
				"name": "商品6",
				"count": 1
			}]
		}
		"""
	When bill从购物车发起购买操作
		"""
				{
					"action": "pay",
					"context": [{
						"name": "商品5"
					}, {
						"name": "商品6"
					}]
				}
		"""
	And bill填写收货信息
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
  And bill在购物车订单编辑中点击提交订单
  """
  {
    "pay_type": "货到付款"
  }
  """
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 23.0,
			"postage":15.0
		}
		"""


@mall @mall2 @zy_wsc08 @mall.webapp @mall.webapp.shopping_cart
Scenario: 从购物车购买多个"有特殊运费"的商品
	bill将jobs多个'有特殊运费'的商品加入购物车后
	1. bill能从购物车中下单,购买商品
	2. bill的订单中的信息正确

	Given jobs登录系统
	When jobs选择'EMS'运费配置
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品4",
			"count": 2
		}, {
			"name": "商品5",
			"count": 1
		}]
		"""
	When bill从购物车发起购买操作
		"""
				{
					"action": "click",
					"context": [{
						"name": "商品4"
					}, {
						"name": "商品5"
					}]
				}
		"""
	Then bill能获得待编辑订单
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 2
			}, {
				"name": "商品5",
				"count": 1
			}]
		}
		"""
		When bill从购物车发起购买操作
		"""
				{
					"action": "pay",
					"context": [{
						"name": "商品4"
					}, {
						"name": "商品5"
					}]
				}
		"""
	And bill填写收货信息
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"area": "河北省 秦皇岛市 山海关区",
			"ship_address": "泰兴大厦"
		}
		"""
	And bill在购物车订单编辑中点击提交订单
	"""
	{
    "pay_type": "货到付款"
  }
  """
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "河北省 秦皇岛市 山海关区",
			"ship_address": "泰兴大厦",
			"final_price": 47.0,
			"postage":40.0
		}
		"""

#@mall @mall2 @zy_wsc09 @mall.webapp @mall.webapp.shopping_cart
#Scenario: 从购物车购买多个支付方式的商品
#	bill加入jobs的多个商品到购物车后
#	1. bill能从购物车中下单,购买商品
#
#	When bill关注jobs的公众号
#	When bill访问jobs的webapp
#	And bill加入jobs的商品到购物车
#		"""
#			[{
#				"name": "商品4",
#				"count": 1
#			}, {
#				"name": "商品5",
#				"count": 1
#			}, {
#				"name": "商品6",
#				"count": 1
#			}]
#		"""
#	When bill从购物车发起购买操作
#		"""
#			{
#				"action": "click",
#				"context": [{
#					"name": "商品4"
#				}, {
#					"name": "商品5"
#				}, {
#					"name": "商品6"
#				}]
#			}
#		"""
#	Then bill获得待编辑订单
#	"""
#		{
#			"products": [{
#				"name": "商品4",
#				"count": 1
#			}, {
#				"name": "商品5",
#				"count": 1
#			}, {
#				"name": "商品6",
#				"count": 1
#			}]
#		}
 # """
#	When bill从购物车发起购买操作
#		"""
#			{
#				"action": "pay",
#				"context": [{
#					"name": "商品4"
#				}, {
#					"name": "商品5"
#				}, {
#					"name": "商品6"
#				}]
#			}
#		"""
#	And bill填写收货信息
#	"""
#		{
#			"ship_name": "bill",
#			"ship_tel": "13811223344",
#			"area": "北京市 北京市 海淀区",
#			"ship_address": "泰兴大厦"
#		}
 # """
#  And bill在购物车订单编辑中点击提交订单
# """
#		{
#			"pay_type": "货到付款"
#		}
#  """
#	Then bill'能'使用支付方式'微众卡支付'进行支付
#	Then bill'不能'使用支付方式'货到付款'进行支付
#
#
#@mall @mall2 @zy_wsc @mall.webapp @mall.webapp.shopping_cart
#Scenario: 从购物车购买多个配有"货到付款"支付方式的商品
#	bill加入jobs的多个商品到购物车后
#	1. bill能从购物车中下单,购买商品
#
#	When bill关注jobs的公众号
#	When bill访问jobs的webapp
#	And bill加入jobs的商品到购物车
#		"""
#		[{
#			"name": "商品6",
#			"count": 1
#		}, {
#			"name": "商品7",
#			"count": 1
#		}]
#		"""
#	When bill从购物车发起购买操作
#		"""
#				{
#					"action": "click",
#					"context": [{
#						"name": "商品1"
#					}]
#
#						[{
#						"name": "商品6",
#						"count": 1
#					}, {
#						"name": "商品7",
#						"count": 1
#					}]
#				}
#		"""
#	Then bill'能'使用支付方式'微众卡支付'进行支付
#	Then bill'能'使用支付方式'货到付款'进行支付
#
