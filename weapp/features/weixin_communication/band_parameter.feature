# __author__ : "师帅"
Feature: 带参数二维码

Background:
	Given jobs添加商品
	"""
		[{
			"name": "商品1",
			"price": 100
		}, {
			"name": "商品2",
			"price": 200
		}, {
			"name": "商品3",
			"price": 300
		}]
	"""

Scenario: 1新建二维码
	When jobs登录系统
	And jobs新建二维码
	"""
		[{
			"name": "二维码1",
			"scan_reward": "积分100",
			"become_designated_member": "普通会员",
			"attention_member_participation": "True",
			"associate_member": "False",
			"scan_code": "1111"
		}, {
			"name": "二维码2",
			"scan_reward": "优惠券",
			"become_designated_member": "普通会员",
			"attention_member_participation": "True",
			"associate_member": "False",
			"scan_code": "1111"
		}, {
			"name": "二维码3",
			"scan_reward": "优惠券",
			"become_designated_member": "银牌会员",
			"attention_member_participation": "False",
			"associate_member": "True",
			"member": "ss"
			"scan_code": "1111"
		}]
	"""

	Then jobs能获取二维码列表
	"""
		[{
			"name": "二维码1",
			"attention_number": 0,
			"attention_money": 100
			"create_time": 2015-08-17,
			"scan_reward": "积分100"
		}, {
			"name": "二维码2",
			"attention_number": 0,
			"attention_money": 100,
			"create_time": 2015-18-13,
			"scan_reward": "优惠券"
		}, {
			"name": "二维码3",
			"attention_number": 0,
			"attention_money": 100,
			"create_time": 2015-18-12,
			"scan_reward": "优惠券"
		}]
	"""

Scenario: 2搜索，查看，排序操作
	Given jobs新建二维码
	"""
		[{
			"name": "二维码1",
			"scan_reward": "积分100",
			"become_designated_member": "普通会员",
			"attention_member_participation": "True",
			"associate_member": "False",
			"scan_code": "1111"
		}, {
			"name": "二维码2",
			"scan_reward": "优惠券",
			"become_designated_member": "普通会员",
			"attention_member_participation": "True",
			"associate_member": "False",
			"scan_code": "1111"
		}, {
			"name": "二维码3",
			"scan_reward": "优惠券",
			"become_designated_member": "银牌会员",
			"attention_member_participation": "False",
			"associate_member": "False",
			"scan_code": "1111"
		}]
	"""

	Then jobs能获取二维码列表
	"""
		[{
			"name": "二维码1",
			"attention_number": 0,
			"attention_money": 100
			"create_time": 2015-08-17,
			"scan_reward": "积分100"
		}, {
			"name": "二维码2",
			"attention_number": 0,
			"attention_money": 100,
			"create_time": 2015-18-13,
			"scan_reward": "优惠券"
		}, {
			"name": "二维码3",
			"attention_number": 0,
			"attention_money": 100,
			"create_time": 2015-18-12,
			"scan_reward": "优惠券"
		}]
	"""
	When jobs点击'二维码1'
	Then jobs进入二维码编辑页面
	When jobs设置筛选条件
	"""
		{
			"name": "1"
		}
	"""
	Then jobs能获取二维码列表
	"""
		{
			"name": "二维码1",
			"attention_number": 0,
			"attention_money": 100
			"create_time": 2015-08-17,
			"scan_reward": "积分100"
		}
	"""
	When jobs查看二维码
	Then jobs显示二维码页面
	When jobs对时间排序
	Then jobs能获取二维码列表
	"""
		[{
			"name": "二维码3",
			"attention_number": 0,
			"attention_money": 100,
			"create_time": 2015-18-12,
			"scan_reward": "优惠券"
		}, {
			"name": "二维码2",
			"attention_number": 0,
			"attention_money": 100,
			"create_time": 2015-18-13,
			"scan_reward": "优惠券"
		}, {
			"name": "二维码1",
			"attention_number": 0,
			"attention_money": 100
			"create_time": 2015-08-17,
			"scan_reward": "积分100"
		}]
	"""
	When jobs对'关注数量'操作
	Then jobs显示'仅显示通过二维码新关注会员'
	When jobs对'扫码后成交金额'操作
	Then jobs显示'仅显示扫码后成交订单'

Scenario: 3操作'关注数量'和'扫码后成交金额'
	When jobs登录系统
	And tom1关注jobs的公众号
	And tom1购买jobs的商品
	"""
		{
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
	"""
	And tom2关注jobs的公共号
	And tom2购买jobs的商品
	"""
		{
			"products": [{
				"name" "商品2",
				"price": 200.00,
				"count": 1
			}]
		}
	"""
	And jobs新建二维码
	"""
		[{
			"name": "二维码1",
			"scan_reward": "积分100",
			"become_designated_member": "普通会员",
			"attention_member_participation": "True",
			"associate_member": "False",
			"scan_code": "1111"
		}, {
			"name": "二维码2",
			"scan_reward": "优惠券",
			"become_designated_member": "普通会员",
			"attention_member_participation": "True",
			"associate_member": "False",
			"scan_code": "1111"
		}]
	"""

	Then jobs能获取二维码列表
	"""
		[{
			"name": "二维码1",
			"attention_number": 0,
			"attention_money": 100
			"create_time": 2015-08-17,
			"scan_reward": "积分100"
		}, {
			"name": "二维码2",
			"attention_number": 0,
			"attention_money": 100,
			"create_time": 2015-18-13,
			"scan_reward": "优惠券"
		}]
	"""
	When tom1扫码'二维码1'
	And tom1购买jobs的商品
	"""
		{
			"products": [{
				"name": "商品2",
				"price" 200.00,
				"count": 1
			}]
		}
	"""

	And tom2扫码'二维码1'
	And tom2购买jobs的商品
	"""
		{
			"products": [{
				"name": "商品3",
				"price": 300.00,
				"count": 1
			}]
		}
	"""

	And tom3扫码'二维码1'
	Then jobs能获取二维码列表
	"""
		[{
			"name": "二维码1",
			"attention_number": 3,
			"attention_money": 500
		}, {
			"name": "二维码2",
			"attention_number": 0,
			"attention_money": 0
		}]
	"""

	When jobs对'二维码1'的'关注数量'操作
	Then jobs能获取'仅显示通过二维码新关注会员'列表
	"""
		[{
			"fans_name": "tom3",
			"buy_number": 0,
			"integral": 100
		}]
	"""
	When jobs取消勾选'仅显示通过二维码新关注会员'
	Then jobs能获取列表
	"""
		[{
			"fans_name": "tom3",
			"buy_number": 0,
			"integral": 100
		}, {
			"fans_name": "tom2",
			"buy_number": 500,
			"integral": 100
		}, {
			"fans_name": "tom1",
			"buy_number": 300,
			"integral": 100
		}]
	"""

	When jobs对'二维码1'的'扫码后成交金额'操作
	Then jobs能获取'仅显示扫码后成交订单'列表
	"""
		[{
			"status": "已发货",
			"final_price": 300.00,
			"products": [{
				"name": "商品3",
				"price": 300.00,
				"count": 1
			}]
		}, {
			"status": "已完成",
			"final_price": 200.00,
			"products": [{
				"name": "商品2",
				"price": 200.00,
				"count": 1
			}]
		}]
	"""
	When jobs取消勾选'仅显示扫码后成交订单'
	Then jobs能获取列表
	"""
		[{
			"status": "已发货",
			"final_price": 300.00,
			"products": [{
				"name": "商品3",
				"price": 300.00,
				"count": 1
			}]
		}, {
			"status": "已发货",
			"final_price": 200.00,
			"products": [{
				"name": "商品2",
				"price": 200.00,
				"count": 1
			}]
		}, {
			"status": "已发货",
			"final_price": 200.00,
			"products": [{
				"name": "商品2",
				"price": 200.00,
				"count": 1
			}]
		}, {
			"status": "已发货",
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}]
	"""
