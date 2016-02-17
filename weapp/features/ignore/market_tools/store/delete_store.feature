#watcher:fengxuejing@weizoom.com,benchi@weizoom.com

@func:market_tools.tools.store
Feature: 删除门店
	jobs能通过管理系统修改门店信息

Background:
	Given jobs登录系统
	And jobs已经添加门店信息
		"""
		[{
			"name":"山西路门店",
			"thumbnails_url":"aa.jpg",
			"store_intro":"本店经营四川小吃",
			"swipe_images":[
                {"url": "1.jpg"},
                {"url": "2.jpg"},
                {"url": "3.jpg"}
            ],
            "city":"南京",
			"address":"中山北路88号",
			"location":"118.781474,32.07355",
			"bus_line":"乘坐12路,13路到山西路站",
			"zone":"025",
			"num":"12345678",
			"detail":"一次消费满200元,返券10元"
		},{
			"name":"新街口门店",
			"thumbnails_url":"aa.jpg",
			"store_intro":"本店经营南京小吃",
			"swipe_images":[
                {"url": "1.jpg"},
                {"url": "2.jpg"},
                {"url": "3.jpg"}
            ],
            "city":"南京",
			"address":"中山北路88号",
			"location":"118.781474,32.07355",
			"bus_line":"乘坐42路,43路到山西路站",
			"zone":"025",
			"num":"12345678",
			"detail":"一次消费满200元,返券10元"
		}]
		"""

@weapp.market_tools.tools.store
Scenario: 删除"门店管理"

	Given jobs登录系统
	When jobs删除'山西路门店'
	Then jobs能获取门店列表
		"""
		[{
			"name": "新街口门店",
			"city":"南京"
		}]
		"""

	When jobs删除'新街口门店'
	Then jobs能获取门店列表
		"""
		[]
		"""




