# watcher: dujiashu@weizoom.com
# __author__ : "杜嘉澍" 2016-09-29

Feature:cps展示
"""
	1、商品池：
		(1) 在所有商品中标识出cps的商品。
		(2) 点击cps后过滤出所有cps商品并显示cps专有字段。
	2、在售/代售：
		逻辑同商品池		
"""

###特殊说明：jobs表示自营平台
Background:
	#jobs数据
		Given 设置jobs为自营平台账号

@mall2 @product @showcps
Scenario:1 商品池中显示所有商品同时标识出cps商品。
		Given jobs登录系统
		When jobs虚拟添加商品
			"""
			[{
				"__虚拟商品1":0
			},{
				"__虚拟商品2":0
			},{
				"__虚拟商品3":0
			},{
				"__虚拟商品5":1
			},{
				"__虚拟商品6":1
			},{
				"__虚拟商品7":1
			}]
			"""
		And jobs虚拟添加商品池
			"""
			
			"""
		And jobs虚拟添加cps商品信息
			"""
			
			"""
		Then jobs点击商品池所有商品标签栏
			"""
			[
            {
                "is_cps": 1,
                "name": "__虚拟商品1",
                "promote_money": 10,
                "promote_stock": 11,
                "promote_time_to": "2017/02/14 21:32",
                "promote_time_from": "2014/02/14 21:32"
            },
            {
                "name": "__虚拟商品2"
            },
            {
                "is_cps": 1,
                "name": "__虚拟商品5",
                "promote_money": 1000,
                "promote_stock": 13,
                "promote_time_to": "2017/02/14 21:32",
                "promote_time_from": "2014/02/14 21:32"
            }
        	]
			"""
		And jobs点击商品池cps推广商品标签
			"""
			[
            {
                "is_cps": 1,
                "name": "__虚拟商品1",
                "promote_money": 10,
                "promote_stock": 11,
                "promote_time_to": "2017/02/14 21:32",
                "promote_time_from": "2014/02/14 21:32"
            },
            {
                "is_cps": 1,
                "name": "__虚拟商品5",
                "promote_money": 1000,
                "promote_stock": 13,
                "promote_time_to": "2017/02/14 21:32",
                "promote_time_from": "2014/02/14 21:32"
            }
        ]
			"""		
		And jobs点击在售商品所有商品标签
			"""
			[
            {
                "name": "__虚拟商品7"
            },
            {
                "name": "__虚拟商品6"
            },
            {
                "is_cps": 1,
                "name": "__虚拟商品5",
                "promote_money": 1000,
                "promote_stock": 13,
                "promote_time_to": "2017/02/14 21:32",
                "promote_time_from": "2014/02/14 21:32"
            }
        	]
			"""		
		And jobs点击在售商品cps推广商品标签
			"""
			[
            {
                "is_cps": 1,
                "name": "__虚拟商品5",
                "promote_money": 1000,
                "promote_stock": 13,
                "promote_time_to": "2017/02/14 21:32",
                "promote_time_from": "2014/02/14 21:32"
            }
        ]
			"""		
		And jobs点击待售商品所有商品标签
			"""
			[
            {
                "is_cps": 1,
                "name": "__虚拟商品3",
                "promote_money": 100,
                "promote_stock": 12,
                "promote_time_to": "2017/02/14 21:32",
                "promote_time_from": "2014/02/14 21:32"
            },
            {
                "name": "__虚拟商品2"
            },
            {
                "is_cps": 1,
                "name": "__虚拟商品1",
                "promote_money": 10,
                "promote_stock": 11,
                "promote_time_to": "2017/02/14 21:32",
                "promote_time_from": "2014/02/14 21:32"
            }
        	]
			"""		
		And jobs点击待售商品cps推广商品标签
			"""
			[
            {
                "is_cps": 1,
                "name": "__虚拟商品3",
                "promote_money": 100,
                "promote_stock": 12,
                "promote_time_to": "2017/02/14 21:32",
                "promote_time_from": "2014/02/14 21:32"
            },{
                "is_cps": 1,
                "name": "__虚拟商品1",
                "promote_money": 10,
                "promote_stock": 11,
                "promote_time_to": "2017/02/14 21:32",
                "promote_time_from": "2014/02/14 21:32"
            }
        	]
			"""	
