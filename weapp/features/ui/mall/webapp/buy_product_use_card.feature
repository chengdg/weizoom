#_author_ "师帅8.27"
Feature:在webapp使用微众卡购买商品
#后台开启后,手机端购买时显示微众卡,否则不显示
#1.使用一张微众卡，卡内金额大于购买商品金额
#2.使用一张微众卡，卡内金额等于购买商品金额
#3.使用一张微众卡，卡内金额小于购买商品金额，可以添加多张微众卡购买，最多10张
#4.使用微众卡时，输入账号，不输入密码，提示“请输入密码”，输入密码，不输入账号，提示“请输入卡号”，输入错误的账号和密码，提示“卡号或密码错误”;都为空时不输入,提示"请输入卡号"
#5.使用已用完的微众卡购买商品
#6.使用未激活的微众卡购买商品
#7.使用已过期微众卡购买商品
#8.使用两张同样的微众卡购买
#9.使用10张微众卡后，不能在添加第11张
#10.使用微众卡购买后，取消订单，余额返还

Background:
	Given jobs登录系统
	And jobs已添加商品
	"""
		[{
			"name": "商品1",
			"price": 10
		}]
	"""
	And jobs已有微众卡支付权限
	And jobs已添加支付方式
	"""
		[{
			"type": "微众卡支付"
		}]
	"""
	And jobs已创建微众卡
	"""
		[{
			"cards": [{
				"id": "0000001",
				"password": "1234567",
				"status": "未使用",
				"price": 10.0
			}, {
				"id": "0000002",
				"password": "1234567",
				"status": "未使用",
				"price": 200.0
			}, {
				"id": "0000003",
				"password": "1234567",
				"status": "未使用",
				"price": 5.0
			}, {
				"id": "0000004",
				"password": "1234567",
				"status": "已用完",
				"price": 0.0
			}]
		}]
	"""
	And bill关注jobs的公众号

Scenario: 1 使用一张微众卡，卡内金额大于购买商品金额
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""	
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	And bill使用微众卡支付
	"""
		[{
			"id": "0000002",
			"password": "1234567",
			"status": "未使用",
			"price": 200.0
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待发货",
			"final_price": 0.0,
			"product_price": 10.0,
			"weizoom_card_money": 10.0,
			"products": [{
				"name": "商品1",
				"price": "10.0",
				"count": 1
			}]
		}]
	"""
	When bill登录个人中心
	Then bill查询微众卡余额
	"""
		[{
			"id": "0000002",
			"password": "1234567",
			"status": "已使用",
			"price": 190.0
		}]
	"""

Scenario: 2使用一张微众卡，卡内金额等于购买商品金额
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""	
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	And bill使用微众卡支付
	"""
		[{
			"id": "0000001",
			"password": "1234567",
			"status": "未使用",
			"price": 10.0
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待发货",
			"final_price": 0.0,
			"product_price": 10.0,
			"weizoom_card_money": 10.0,
			"products": [{
				"name": "商品1",
				"price": "10.0",
				"count": 1
			}]
		}]
	"""
	When bill登录个人中心
	Then bill查询微众卡余额
	"""
		[{
			"id": "0000002",
			"password": "1234567",
			"status": "已使用",
			"price": 0.0
		}]
	"""

Scenario: 3 使用一张微众卡，卡内金额小于购买商品金额，可以添加多张微众卡购买，最多10张
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""	
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	And bill使用微众卡支付
	"""
		[{
			"id": "0000003",
			"password": "1234567",
			"status": "未使用",
			"price": 5.0
		}]
	"""
	Then bill获得创建订单失败的信息'您的微众卡余额不足！'

Scenario: 4 使用微众卡时，输入账号，不输入密码，提示“请输入密码”，输入密码，不输入账号，提示“请输入卡号”，输入错误的账号和密码，提示“卡号或密码错误”;都为空时不输入,提示"请输入卡号"
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	And bill使用微众卡支付
	"""
		[{
			"id": "",
			"password": "",
			"status": "未使用",
			"price": 5.0
		}]
	"""
	Then bill获得创建订单失败的信息'请输入卡号'
	When bill使用微众卡支付
	"""
		[{
			"id": "0000009",
			"password": "7654321",
			"status": "未使用",
			"price": 5.0
		}]
	"""
	Then bill获得创建订单失败的信息'卡号或密码错误'
	When bill使用微众卡支付
	"""
		[{
			"id": "0000003",
			"password": "",
			"status": "未使用",
			"price": 5.0
		}]
	"""
	Then bill获得创建订单失败的信息'请输入密码'
	When bill使用微众卡支付
	"""
		[{
			"id": "",
			"password": "1234567",
			"status": "未使用",
			"price": 5.0
		}]
	"""
	Then bill获得创建订单失败的信息'请输入卡号'

Scenario: 5 使用已用完的微众卡购买商品
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	And bill使用微众卡支付
	"""
		[{
			"id": "0000004",
			"password": "1234567",
			"status": "已用完",
			"price": 0.0
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待发货",
			"final_price": 10.0,
			"product_price": 10.0,
			"weizoom_card_money": 0.0,
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""
	When bill登录个人中心
	Then bill查询微众卡余额
	"""
		[{
			"id": "0000004",
			"password": "1234567",
			"status": "已用完",
			"price": 0.0
		}]
	"""

Scenario: 6 使用未激活的微众卡购买商品
	When jobs已创建微众卡
	"""
		[{
			"id": "0000005",
			"password": "1234567",
			"status": "未激活",
			"price": 20.0
		}]
	"""
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	And bill使用微众卡支付
	"""
		[{
			"id": "0000005",
			"password": "1234567",
			"status": "未激活",
			"price": 20.0
		}]
	"""
	Then bill获得创建订单失败的信息'微众卡未激活'

Scenario: 7 使用已过期微众卡购买商品
	When jobs已创建微众卡
	"""
		[{
			"id": "0000006",
			"password": "1234567",
			"status": "已过期",
			"price": 20.0
		}]
	"""
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	And bill使用微众卡支付
	"""
		[{
			"id": "0000005",
			"password": "1234567",
			"status": "已过期",
			"price": 20.0
		}]
	"""
	Then bill获得创建订单失败的信息'微众卡已过期'

Scenario: 8 使用两张同样的微众卡购买
	When jobs已创建微众卡
	"""
		[{
			"id": "0000003",
			"password": "1234567",
			"status": "未使用",
			"price": 5.0
		}]
	"""
	And bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	And bill使用微众卡支付
	"""
		[{
			"weizoom_card": [{
				"card_name": "0000003",
				"card_pass": "1234567"
			}, {
				"card_name": "0000003",
				"card_pass": "1234567"
			}]
		}]
	"""
	Then bill获得创建订单失败的信息'该微众卡已经添加'

Scenario: 9 使用10张微众卡后，不能在添加第11张
	When jobs已创建微众卡
	"""
		[{
			"cards":[{
				"id":"1000001",
				"password":"1234567",
				"status":"未使用",
				"price":1.00
			},{
				"id":"1000002",
				"password":"1234567",
				"status":"已使用",
				"price":1.00
			},{
				"id":"1000003",
				"password":"1234567",
				"status":"未使用",
				"price":1.00
			},{
				"id":"1000004",
				"password":"1234567",
				"status":"未使用",
				"price":1.00
			},{
				"id":"1000005",
				"password":"1234567",
				"status":"已使用",
				"price":1.00
			},{
				"id":"1000006",
				"password":"1234567",
				"status":"已使用",
				"price":1.00
			},{
				"id":"1000007",
				"password":"1234567",
				"status":"未使用",
				"price":1.00
			},{
				"id":"1000008",
				"password":"1234567",
				"status":"未使用",
				"price":1.00
			},{
				"id":"1000009",
				"password":"1234567",
				"status":"已使用",
				"price":1.00
			},{
				"id":"1000010",
				"password":"1234567",
				"status":"已使用",
				"price":1.00
			},{
				"id":"1000011",
				"password":"1234567",
				"status":"已使用",
				"price":1.00
			}]
		}]
	"""
	And bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	And bill使用微众卡支付
	"""
		[{
			"weizoom_card": [{
				"card_name": "1000001"
				"card_pass": "1234567"
			}, {
				"card_name": "1000002"
				"card_pass": "1234567"
			}, {
				"card_name": "1000003"
				"card_pass": "1234567"
			}, {
				"card_name": "1000004"
				"card_pass": "1234567"
			}, {
				"card_name": "1000005"
				"card_pass": "1234567"
			}, {
				"card_name": "1000006"
				"card_pass": "1234567"
			}, {
				"card_name": "1000007"
				"card_pass": "1234567"
			}, {
				"card_name": "1000008"
				"card_pass": "1234567"
			}, {
				"card_name": "1000009"
				"card_pass": "1234567"
			}, {
				"card_name": "1000010"
				"card_pass": "1234567"
			}]
		}]
	"""
	#最多添加10张微众卡，超过不能添加
	Then bill成功创建订单
	"""
		[{
			"status": "待发货",
			"final_price": 0.0,
			"product_price": 10.0,
			"weizoom_card_money": 10.0,
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""
	When bill登录个人中心
	Then bill查询微众卡余额
	"""
		[{
			"id":"1000001",
			"password":"1234567",
			"status":"已用完",
			"price":0.00
		},{
			"id":"1000002",
			"password":"1234567",
			"status":"已用完",
			"price":0.00
		},{
			"id":"1000003",
			"password":"1234567",
			"status":"已用完",
			"price":0.00
		},{
			"id":"1000004",
			"password":"1234567",
			"status":"已用完",
			"price":0.00
		},{
			"id":"1000005",
			"password":"1234567",
			"status":"已用完",
			"price":0.00
		},{
			"id":"1000006",
			"password":"1234567",
			"status":"已用完",
			"price":0.00
		},{
			"id":"1000007",
			"password":"1234567",
			"status":"已用完",
			"price":0.00
		},{
			"id":"1000008",
			"password":"1234567",
			"status":"已用完",
			"price":0.00
		},{
			"id":"1000009",
			"password":"1234567",
			"status":"已用完",
			"price":0.00
		},{
			"id":"1000010",
			"password":"1234567",
			"status":"已用完",
			"price":0.00
		},{
			"id":"1000011",
			"password":"1234567",
			"status":"已使用",
			"price":1.00
		}]
	"""

Scenario: 10 使用微众卡购买后，取消订单，余额返还
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	And bill使用微众卡支付
	"""
		[{
			"id": "0000001",
			"password": "1234567",
			"status": "未使用",
			"price": 10.0
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待发货",
			"final_price": 0.0,
			"product_price": 10.0,
			"weizoom_card_money": 10.0,
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""
	When bill登录个人中心
	Then bill查询微众卡余额
	"""
		[{
			"id": "0000001",
			"password": "1234567",
			"status": "已使用",
			"price": 0.0
		}]
	"""
	When bill进行'取消订单'操作
	Then bill查询微众卡余额
	"""
		[{
			"id": "0000001",
			"password": "1234567",
			"status": "未使用",
			"price": 10.0
		}]
	"""




