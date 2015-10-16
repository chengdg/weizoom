#author: 王丽
#editor: 张三香 2015.10.16

Feature: 会员列表-会员详情-传播能力
	"""
		会员分享链接和推广扫码带来的访问量和新增会员数的记录
		1、【二维码引流会员数量】：本会员通过"推广扫码"带来的新增会员数
		2、【分享链接引流会员数量】：本会员通过"分享链接"带来的新增会员数
		3、分享链接明细列表
			【分享链接】：分享链接的页面名称或者活动名称
			【点击】：点击此链接数（包含会员和非会员的点击数），同意人只计算一次
			【关注转化】：通过此链接带来的新增会员数
			【购买转化】：通过此链接带来的付款订单数（订单状态为：待发货、已发货、已完成、退款中、退款成功）
				备注：只能是购买分享的链接的商品
	"""

Background:

	Given jobs登录系统

	And 开启手动清除cookie模式

	#添加相关基础数据
		When jobs已添加商品
			"""
			[{
				"name": "商品1",
				"postage":10,
				"price":100
			}, {
				"name": "商品2",
				"postage":15,
				"price":100
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
	And tom关注jobs的公众号

@mall2 @member @memberList
Scenario:1 会员详情-传播能力

	#tom带来的传播能力数据创建
		#bill和tom建立好友关系
		When tom访问jobs的webapp
		When tom把jobs的微站链接分享到朋友圈
		When tom获得db中在jobs公众号中的mt为'mt_{tom_jobs}'

		When 清空浏览器
		When bill点击tom分享链接
		Then bill在jobs公众号中有uuid对应的webapp_user
		Then 浏览器cookie包含"[fmt, uuid]"
		Then 浏览器cookie等于
			"""
			{"fmt":"mt_{tom_jobs}"}
			"""
		When bill关注jobs的公众号
		When bill访问jobs的webapp

	#bill通过tom分享的商品链接下单购买jobs的商品1
	#待支付
		When bill访问tom分享jobs的微站链接
		And bill购买jobs的商品
			"""
			{
				"order_id": "001",
				"products": [{
					"name": "商品1",
					"count": 1
				}],
				"pay_type": "微信支付"
			}
			"""
	#已取消
		When bill访问tom分享jobs的微站链接
		And bill购买jobs的商品
			"""
			{
				"order_id": "002",
				"products": [{
					"name": "商品1",
					"count": 1
				}],
				"pay_type": "微信支付"
			}
			"""
		And bill取消订单'002'
	#待发货
		When bill访问tom分享jobs的微站链接
		And bill购买jobs的商品
			"""
			{
				"order_id": "003",
				"products": [{
					"name": "商品1",
					"count": 1
				}],
				"pay_type": "微信支付"
			}
			"""
		When 清空浏览器
		Given jobs登录系统
		When jobs'支付'订单'003'
	#已发货
		When 清空浏览器
		When bill访问tom分享jobs的微站链接
		And bill购买jobs的商品
			"""
			{
				"order_id": "004",
				"products": [{
					"name": "商品1",
					"count": 1
				}],
				"pay_type": "微信支付"
			}
			"""
		When 清空浏览器
		Given jobs登录系统
		When jobs'支付'订单'004'

		When jobs对订单进行发货
			"""
			{
				"order_no": "004",
				"logistics": "off",
				"shipper": ""
			}
			"""
	#退款中
		When 清空浏览器
		When bill访问tom分享jobs的微站链接
		And bill购买jobs的商品
			"""
			{
				"order_id": "005",
				"products": [{
					"name": "商品1",
					"count": 1
				}],
				"pay_type": "微信支付"
			}
			"""
		When 清空浏览器
		Given jobs登录系统
		When jobs'支付'订单'005'
		And jobs'申请退款'订单'005'
	#退款成功
		When 清空浏览器
		When bill访问tom分享jobs的微站链接
		And bill购买jobs的商品
			"""
			{
				"order_id": "006",
				"products": [{
					"name": "商品1",
					"count": 1
				}],
				"pay_type": "微信支付"
			}
			"""
		When 清空浏览器
		Given jobs登录系统
		When jobs'支付'订单'006'
		And jobs'申请退款'订单'006'
		And jobs通过财务审核'退款成功'订单'006'

		#bill2和tom建立好友关系
		When bill2关注jobs的公众号
		When bill2访问jobs的webapp

		When tom访问jobs的webapp
		When tom把jobs的微站链接分享到朋友圈
		When tom获得db中在jobs公众号中的mt为'mt_{tom_jobs}'

		When 清空浏览器
		When bill2点击tom分享链接
		Then bill2在jobs公众号中有uuid对应的webapp_user
		Then 浏览器cookie包含"[fmt, uuid]"
		Then 浏览器cookie等于
			"""
			{"fmt":"mt_{tom_jobs}"}
			"""

	#bill2通过tom分享的商品链接下单购买jobs的商品1
	#待发货
		When bill2访问tom分享jobs的微站链接
		And bill2购买jobs的商品
			"""
			{
				"order_id": "007",
				"products": [{
					"name": "商品1",
					"count": 1
				}],
				"pay_type": "微信支付"
			}
			"""
		And bill2使用支付方式'微信支付'进行支付
		Then bill2支付订单成功
			"""
			{
				"status": "待发货",
				"products": [{
					"name": "商品1"
				}]
			}
			"""

	#校验tom的传播能力
		When 清空浏览器
		Given jobs登录系统
		Then jobs获得'tom'的传播能力
			"""
			{
				"scan_qrcode_new_member": 0,
				"share_link_new_member":1,
				"share_detailed_data":[
					{
						"click_number":2,
						"new_member":1,
						"order":1
					}
				]
			}
			"""
