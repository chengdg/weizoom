#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
# __author__ : "冯雪静"
Feature: 添加微众卡钱包
	jobs在微信营销管理系统后台创建新的钱包规则，以便印刷，发放给客户。


@market_tools @weapp.market_tools.weizoom_card
Scenario:添加微众卡钱包
	jobs创建多个钱包后
	1.jobs能获得每一个钱包
	2.钱包中有对应的微众卡
	3.jobs的钱包列表按创建顺序倒序排列
	#规则名称、微众卡金额、微众卡数量、过期时间为必填项，备注为非必填项.
	
	Given jobs登录系统
	When jobs创建微众卡钱包
		"""
		[{
			"name": "微众钱包A",
			"price": 100.00,
			"card": {
				"count": 2,
				"password": "p1"
			},
			"expire_time": "2020-01-01 00:00",
			"remarks": "钱包"
		},{
			"name": "微众钱包D",
			"price": 200.00,
			"card": {
				"count": 1,
				"password": "p2"
			},
			"expire_time": "2020-01-02 00:00",
			"remarks":""
		}]
		"""	
	
	Then jobs能获取微众卡钱包'微众钱包A'
		"""
		{
			"name": "微众钱包A",
			"price": 100.00,
			"count": 2,
			"expire_time": "2020-01-01 00:00",
			"remarks": "钱包",
			"cards": [{
				"id": "0000001",
				"password": "p1",
				"status": "未激活",
				"price": 100.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			},{
				"id": "0000002",
				"password": "p1",
				"status": "未激活",
				"price": 100.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			}]
		}
		"""
	
	Then jobs能获取微众卡钱包'微众钱包D'
		"""
		{
			"name": "微众钱包D",
			"price": 200.00,
			"count": 1,
			"expire_time": "2020-01-02 00:00",
			"remarks":"",
			"cards": [{
				"id": "0000003",
				"password": "p2",
				"status": "未激活",
				"price": 200.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			}]
		}
		"""
	Then jobs能获取微众卡钱包列表
		"""
		[{
			"name": "微众钱包D",
			"price": 200.00,
			"count": 1,
			"remarks":""
		},{
			"name": "微众钱包A",
			"price": 100.00,
			"count": 2,
			"remarks":"钱包"
		}]
		"""
	

@market_tools @weapp.market_tools.weizoom_card
Scenario:追加微众卡
	jobs给已创建的'微众卡钱包'追加微众卡
	1.钱包中有对应的微众卡
	2.微众卡正序排列

	Given jobs登录系统
	And jobs已添加微众卡钱包
		"""
		[{
			"name": "微众钱包B",
			"price": 300.00,
			"card": {
				"count": 1,
				"password": "p3"
			},
			"expire_time": "2020-01-03 00:00",
			"remarks":""
			
		}, {
			"name": "微众钱包C",
			"price": 500.00,
			"card": {
				"count": 1,
				"password": "p4"
			},
			"expire_time": "2020-01-04 00:00",
			"remarks":""
		}]
		"""
	When jobs给微众卡钱包'微众钱包C'追加2张微众卡
	Then jobs能获取微众卡钱包'微众钱包C'
		"""
		{
			"name": "微众钱包C",
			"price": 500.00,
			"count": 3,
			"expire_time": "2020-01-04 00:00",
			"remarks": "",
			"cards": [{
				"id": "0000002",
				"password": "p4",
				"status": "未激活",
				"price": 500.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			},{
				"id": "0000003",
				"password": "p4",
				"status": "未激活",
				"price": 500.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			},{
				"id": "0000004",
				"password": "p4",
				"status": "未激活",
				"price": 500.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			}]
		}
		"""
	When jobs给微众卡钱包'微众钱包B'追加2张微众卡
	Then jobs能获取微众卡钱包'微众钱包B'
		"""
		{
			"name": "微众钱包B",
			"price": 300.00,
			"count": 3,
			"expire_time": "2020-01-01 00:00",
			"remarks": "",
			"cards": [{
				"id": "0000001",
				"password": "p3",
				"status": "未激活",
				"price": 300.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			},{
				"id": "0000005",
				"password": "p3",
				"status": "未激活",
				"price": 300.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			},{
				"id": "0000006",
				"password": "p3",
				"status": "未激活",
				"price": 300.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			}]
		}
		"""
	Then jobs能获取微众卡钱包列表
		"""
		[{
			"name": "微众钱包C",
			"price": 500.00,
			"count": 3,
			"remarks":""
		},{
			"name": "微众钱包B",
			"price": 300.00,
			"count": 3,
			"remarks":""
		}]
		"""


@market_tools @weapp.market_tools.weizoom_card
Scenario:微众卡
	jobs可以给未过期的微众卡激活/停用
	1.激活微众卡后可做停用操作
	
	Given jobs登录系统
	And jobs待激活微众卡
		"""
		{
			"name": "微众钱包E",
			"price": 1000.00,
			"count": 3,
			"expire_time": "2020-01-03 00:00",
			"remarks": "",
			"cards": [{
				"id": "0000001",
				"password": "p1",
				"status": "未激活",
				"price": 1000.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			},{
				"id": "0000002",
				"password": "p1",
				"status": "未激活",
				"price": 1000.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			},{
				"id": "0000003",
				"password": "p1",
				"status": "未激活",
				"price": 1000.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			}]
		}
		"""
	When jobs给id为'0000001'的微众卡激活
	Then jobs能获取微众卡钱包'微众钱包E'
		"""
		{
			"name": "微众钱包E",
			"price": 1000.00,
			"count": 3,
			"expire_time": "2020-01-03 00:00",
			"remarks": "",
			"cards": [{
				"id": "0000001",
				"password": "p1",
				"status": "未使用",
				"price": 1000.00,
				"active_time": "",
				"target": "",
				"actions": ["停用"]
			},{
				"id": "0000002",
				"password": "p1",
				"status": "未激活",
				"price": 1000.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			},{
				"id": "0000003",
				"password": "p1",
				"status": "未激活",
				"price": 1000.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			}]
		}
		"""
	Then jobs能获取微众卡'0000001'
		"""
		{
			"status":"未使用",
			"price":1000.00,
			"log":[{
				"merchant":"jobs",
				"order_id":"激活",
				"price":0
			}]
		}
		"""
	When jobs给id为'0000001'的微众卡停用
	Then jobs能获取微众卡钱包'微众钱包E'
		"""
		{
			"name": "微众钱包E",
			"price": 1000.00,
			"count": 3,
			"expire_time": "2020-01-03 00:00",
			"remarks": "",
			"cards": [{
				"id": "0000001",
				"password": "p1",
				"status": "未激活",
				"price": 1000.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			},{
				"id": "0000002",
				"password": "p1",
				"status": "未激活",
				"price": 1000.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			},{
				"id": "0000003",
				"password": "p1",
				"status": "未激活",
				"price": 1000.00,
				"active_time": "",
				"target": "",
				"actions": ["激活"]
			}]
		}
		"""
	Then jobs能获取微众卡'0000001'
		"""
		{
			"status":"未激活",
			"price": 1000.00,
			"log":[{
				"merchant":"jobs",
				"order_id":"激活",
				"price": 0
			},{
				"merchant":"jobs",
				"order_id":"停用",
				"price": 0
			}]
		}
		"""