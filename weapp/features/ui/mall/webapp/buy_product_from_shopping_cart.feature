@func:webapp.modules.mall.views.list_products
Feature: 在webapp中从购物车中购买商品
	bill能在webapp中从购物车中购买商品

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 3.3
		}, {
			"name": "商品2",
			"price": 5.3
		}]	
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}]
		"""
	Given tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom加入jobs的商品到购物车
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
		}]
		"""


@ui @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 从购物车购买商品，不勾选商品时，获得错误提示
	bill将jobs的一个商品加入购物车后
	1. 不勾选商品时点击下单，获得错误提示
	
	Given bill关注jobs的公众号
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1"
		}]
		"""
	When bill从购物车发起购买操作:ui
	Then bill获得出错提示'请选择结算的商品':ui


@ui @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 从购物车购买单个商品
	bill将jobs的一个商品加入购物车后
	1. bill能从购物车中下单
	2. bill的订单中的信息正确
	3. bill的购物车被清空
	4. tom的购物车不受影响
	
	Given bill关注jobs的公众号
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1"
		}]
		"""
	When bill从购物车发起购买操作:ui
		"""
		{
			"products":"all",
			"ship_info": {
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦"
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1,
				"price": 3.3
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1",
				"price": 3.3,
				"count": 1
			}]
		}
		"""
	And bill能获得购物车:ui
		"""
		[]
		"""
	When tom访问jobs的webapp:ui
	Then tom能获得购物车:ui
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
		}]
		"""


@ui @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 从购物车购买多个商品
	bill将jobs的多个商品加入购物车后
	1. bill能从购物车中下单
	2. bill能调整购物车中的商品数量
	2. bill的订单中的信息正确
	3. bill的购物车被清空
	4. tom的购物车不受影响
	
	Given bill关注jobs的公众号
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
		}]
		"""
	When bill从购物车发起购买操作:ui
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
	Then bill获得待编辑订单:ui
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
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
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
	And bill能获得购物车:ui
		"""
		[]
		"""
	When tom访问jobs的webapp:ui
	Then tom能获得购物车:ui
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
		}]
		"""

Scenario: 从购物车购买全部商品
	bill将jobs的多个商品加入购物车后
	1. bill能从购物车中下单
	2. bill的订单中的信息正确
	3. bill的购物车被清空
	4. tom的购物车不受影响

	Given bill关注jobs的公众号:ui
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1",
			"count": 2
		}, {
			"name": "商品2",
			"count": 1
		}]
		"""
	When bill从购物车发起购买操作:ui
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
	Then bill获得待编辑订单:ui
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
	When bill从购物车发起购买操作:ui
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
  And bill填写收货信息:ui
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
  And bill在购物车订单编辑中点击提交订单:ui
  """
  {
  	"pay_type": "货到付款"
  }
  """
	Then bill成功创建订单:ui
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
	And bill能获得购物车:ui
		"""
		{
      "product_groups": [],
      "invalid_products": []
		}
		"""
	When tom访问jobs的webapp:ui
	Then tom能获得购物车:ui
		"""
		{
      "product_groups": [{
        "promotion": null,
        "can_use_promotion": false,
        "products": [{
          "name": "商品1",
          "count": 1
        }, {
          "name": "商品2",
          "count": 2
        }]
      }],
      "invalid_products": []
		}
		"""

Scenario: 从购物车购买空商品
	bill将jobs的多个商品加入购物车后
	1. bill不选中商品去下单
	2. bill下单失败
	3. bill的购物车没有变化
	4. tom的购物车不受影响

	Given bill关注jobs的公众号:ui
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
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
	When bill从购物车发起购买操作:ui
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
	Then bill能获得待编辑订单:ui
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
	When bill从购物车发起购买操作:ui
	"""
	{
    "action": "pay",
    "context": []
 	}
  	"""
	Then bill能获得购物车:ui
		"""
		{
			"product_groups": [{
				"promotion": null,
				"can_use_promotion": false,
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
			}],
			"invalid_products": []
		}
		"""
	When tom访问jobs的webapp:ui
	Then tom能获得购物车:ui
		"""
		{
      "product_groups": [{
        "promotion": null,
        "can_use_promotion": false,
        "products": [{
          "name": "商品1",
          "count": 1
        }, {
          "name": "商品2",
          "count": 2
        }]
      }],
      "invalid_products": []
		}
		"""

Scenario: 从购物车购买商品时有商品下架
	bill将jobs的多个商品加入购物车，并进入订单编辑后，jobs将其中某个商品下架
	1. bill下单失败
	2. bill的购物车不受影响

	Given bill关注jobs的公众号:ui
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1",
			"count": 2
		}, {
			"name": "商品2",
			"count": 1
		}]
		"""
	When bill从购物车发起购买操作:ui
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
	Then bill能获得待编辑订单:ui
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



	When bill从购物车发起购买操作:ui
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
  And bill填写收货信息:ui
  """
  {
    "ship_name": "bill",
    "ship_tel": "13811223344",
    "area": "北京市 北京市 海淀区",
    "ship_address": "泰兴大厦"
  }
  """
	Given jobs登录系统:ui
	When jobs-下架商品'商品1':ui
	When bill访问jobs的webapp:ui
	When bill在购物车订单编辑中点击提交订单:ui
	"""
	{
    "pay_type": "货到付款"
  }
  """

	Then bill获得错误提示'有商品已下架<br/>2秒后返回购物车<br/>请重新下单':ui

Scenario: 从购物车同时购买"有运费和无运费"的商品，并且商品总重超过续重阈值
	bill将jobs有运费的商品和无运费的商品加入购物车后
	1. bill能从购物车中下单,购买商品
	2. bill的订单中的信息正确

	Given bill关注jobs的公众号:ui
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
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
	When bill从购物车发起购买操作:ui
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
	Then bill能获得待编辑订单:ui
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
	When bill从购物车发起购买操作:ui
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
	And bill填写收货信息:ui
	"""
	{
      "ship_name": "bill",
      "ship_tel": "13811223344",
      "area": "北京市 北京市 海淀区",
      "ship_address": "泰兴大厦"
  }
  """
	And bill在购物车订单编辑中点击提交订单:ui
	"""
	{
    "pay_type": "货到付款"
  }
  """
	Then bill成功创建订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 37.0,
			"postage":25.0
		}
		"""

Scenario: 从购物车同时购买"有运费和无运费"的商品，并且商品总重低于续重阈值
	bill将jobs有运费的商品和无运费的商品加入购物车后
	1. bill能从购物车中下单,购买商品
	2. bill的订单中的信息正确

	Given bill关注jobs的公众号:ui
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品5",
			"count": 1
		}, {
			"name": "商品6",
			"count": 1
		}]
		"""
	When bill从购物车发起购买操作:ui
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
	Then bill获得待编辑订单:ui
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
	When bill从购物车发起购买操作:ui
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
	And bill填写收货信息:ui
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
  And bill在购物车订单编辑中点击提交订单:ui
  """
  {
    "pay_type": "货到付款"
  }
  """
	Then bill成功创建订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 23.0,
			"postage":15.0
		}
		"""

Scenario: 从购物车购买多个"有特殊运费"的商品
	bill将jobs多个'有特殊运费'的商品加入购物车后
	1. bill 在特殊地区
	1. bill能从购物车中下单,购买商品
	2. bill的订单中的信息正确

	Given jobs登录系统:ui
	When jobs选择'EMS'运费配置:ui
	When bill关注jobs的公众号:ui
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品4",
			"count": 2
		}, {
			"name": "商品5",
			"count": 1
		}]
		"""
	When bill从购物车发起购买操作:ui
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
	Then bill能获得待编辑订单:ui
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
		When bill从购物车发起购买操作:ui
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
	And bill填写收货信息:ui
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"area": "河北省 秦皇岛市 山海关区",
			"ship_address": "泰兴大厦"
		}
		"""
	And bill在购物车订单编辑中点击提交订单:ui
	"""
	{
    "pay_type": "货到付款"
  }
  """
	Then bill成功创建订单:ui
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