Feature: 管理收货地址
	bill能在webapp中管理收货地址

Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 9.9
		}, {
			"name": "商品2",
			"price": 8.8
		}]	
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"description": "我的支付宝",
			"is_active": "启用"
		}]
		"""
	And bill关注jobs的公众号


@ui @ui-mall @ui-mall.webapp
Scenario: 从个人中心添加一个收货地址
	bill在jobs的webapp中添加一个收货地址
	1. bill能看到该收货地址详情
	
	When bill访问jobs的webapp:ui
	And bill在jobs的webapp中添加收货地址:ui
		"""
		{
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"北京市 北京市 海淀区",
			"ship_address":"泰兴大厦"
		}
		"""
	Then bill在jobs的webapp中查看收货人'bill'的收货地址:ui
		"""
		{
			"name":"bill",
			"tel":"13013013011",
			"province": "北京市",
			"city": "北京市",
			"district": "海淀区",
			"address":"泰兴大厦"
		}
		"""


@ui @ui-mall @ui-mall.webapp
Scenario: 从个人中心添加多个收货地址
	bill在jobs的webapp中添加多个收货地址
	1. bill能看到收货地址列表
	2. 最新添加的地址成为选中的地址
	3. bill购物时使用选中的地址
	4. tom的收货地址不受影响
	
	When bill访问jobs的webapp:ui
	And bill在jobs的webapp中添加收货地址:ui
		"""
		{
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"北京市 北京市 海淀区",
			"ship_address":"泰兴大厦"
		}
		"""
	And bill在jobs的webapp中添加收货地址:ui
		"""
		{
			"ship_name":"tom",
			"ship_tel":"13811223344",
			"ship_area":"北京市 北京市 朝阳区",
			"ship_address":"国贸"
		}
		"""
	Then bill在jobs的webapp中拥有收货地址:ui
		"""
		[{
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"北京市 北京市 海淀区",
			"ship_address":"泰兴大厦",
			"is_selected": false
		}, {
			"ship_name":"tom",
			"ship_tel":"13811223344",
			"ship_area":"北京市 北京市 朝阳区",
			"ship_address":"国贸",
			"is_selected": true
		}]
		"""
	When tom访问jobs的webapp:ui
	Then tom在jobs的webapp中拥有收货地址:ui
		"""
		[]
		"""


@ui @ui-mall @ui-mall.webapp
Scenario: 更新收货地址
	bill在jobs的webapp中添加收货地址后
	1. bill能更新收货地址
	2. active收货地址为最后更新的收货地址
	
	When bill访问jobs的webapp:ui
	And bill在jobs的webapp中添加收货地址:ui
		"""
		{
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"北京市 北京市 海淀区",
			"ship_address":"泰兴大厦"
		}
		"""
	And bill在jobs的webapp中添加收货地址:ui
		"""
		{
			"ship_name":"tom",
			"ship_tel":"13811223344",
			"ship_area":"北京市 北京市 朝阳区",
			"ship_address":"国贸"
		}
		"""
	Then bill在jobs的webapp中拥有收货地址:ui
		"""
		[{
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"北京市 北京市 海淀区",
			"ship_address":"泰兴大厦",
			"is_selected": false
		}, {
			"ship_name":"tom",
			"ship_tel":"13811223344",
			"ship_area":"北京市 北京市 朝阳区",
			"ship_address":"国贸",
			"is_selected": true
		}]
		"""
	When bill在jobs的webapp中更新收货人'bill'的收货地址:ui
		"""
		{
			"ship_name":"bill*",
			"ship_tel":"13013013012",
			"ship_area":"北京市 北京市 东城区",
			"ship_address":"泰兴大厦*"
		}
		"""
	Then bill在jobs的webapp中拥有收货地址:ui
		"""
		[{
			"ship_name":"bill*",
			"ship_tel":"13013013012",
			"ship_area":"北京市 北京市 东城区",
			"ship_address":"泰兴大厦*",
			"is_selected": true
		}, {
			"ship_name":"tom",
			"ship_tel":"13811223344",
			"ship_area":"北京市 北京市 朝阳区",
			"ship_address":"国贸",
			"is_selected": false
		}]
		"""


@ui @ui-mall @ui-mall.webapp
Scenario: 在购物时添加收货地址
	bill在jobs的webapp中购物时，能添加收货地址

	When bill访问jobs的webapp:ui
	And bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""	
	Then bill在jobs的webapp中拥有收货地址:ui
		"""
		[{
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"ship_area":"北京市 北京市 海淀区",
			"ship_address":"泰兴大厦",
			"is_selected": true
		}]
		"""

@ui @ui-mall @ui-mall.webapp
Scenario: 在购物时切换收货地址
	bill在jobs的webapp中购物时
	1. 能添加新的收货地址
	1. 能切换收货地址

	When bill访问jobs的webapp:ui
	And bill在jobs的webapp中添加收货地址:ui
		"""
		{
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"北京市 北京市 海淀区",
			"ship_address":"泰兴大厦"
		}
		"""
	When bill从商品详情页发起购买操作:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"ship_info": {
				"name": "bill",
				"tel": "13013013011",
				"province": "北京市",
				"city": "北京市",
				"district": "海淀区",
				"address": "泰兴大厦"
			}
		}
		"""
	When bill在订单中切换收货地址:ui
		"""
		{
			"ship_name":"tom",
			"ship_tel":"13811223344",
			"ship_area":"北京市 北京市 朝阳区",
			"ship_address":"国贸"
		}
		"""
	When bill在订单中切换收货地址:ui
		"""
		{
			"ship_name":"nokia",
			"ship_tel":"13844332211",
			"ship_area":"北京市 北京市 东城区",
			"ship_address":"西单"
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"ship_info": {
				"name": "nokia",
				"tel": "13844332211",
				"province": "北京市",
				"city": "北京市",
				"district": "东城区",
				"address": "西单"
			}
		}
		"""
	When bill在订单中切换收货地址:ui
		"""
		{
			"ship_name":"tom"
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"ship_info": {
				"name": "tom",
				"tel": "13811223344",
				"province": "北京市",
				"city": "北京市",
				"district": "朝阳区",
				"address": "国贸"
			}
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"ship_name": "tom",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 朝阳区",
			"ship_address": "国贸"
		}
		"""