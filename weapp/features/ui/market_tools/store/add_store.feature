# __author__ : "崔帅帅"
Feature: 添加门店
	Jobs能通过管理系统添加门店

@weapp.market_tools.tools.store
Scenario: 添加门店
	Jobs添加"门店"后，能获取他的门店，"门店"列表会按照添加的倒序排列

	Given jobs登录系统
	When jobs添加门店
		"""
		[{
			"name":"门店1",
			"thumbnails_url": "small1.jpg",
			"store_intro": "历史悠久",
			"swipe_images": [
				{"url": "1.jpg"},
				{"url": "2.jpg"},
				{"url": "3.jpg"}
			],
			"city": "南京",
			"address": "中山东路100号",
			"location": "116.424678,39.921133",
			"bus_line": "64路,20路",
			"zone": "025",
			"num": "12345678",
			"detail": "大家多来光顾哦"
		}]
		"""

	Then jobs能获取'门店1'的信息
		"""
		{
			"name":"门店1",
			"thumbnails_url":"small1.jpg",
			"store_intro":"历史悠久",
			"swipe_images":[
				{"url": "1.jpg"},
				{"url": "2.jpg"},
				{"url": "3.jpg"}
			],
			"city":"南京",
			"address":"中山东路100号",
			"location":"116.424678,39.921133",
			"bus_line":"64路,20路",
			"zone": "025",
			"num": "12345678",
			"detail":"大家多来光顾哦"
		}
		"""

	Then jobs能获取门店列表
		"""
		[{
			"name": "门店1",
			"city":"南京"
		}]
		"""

	Given bill登录系统
	Then bill能获取门店列表
		"""
		[]
		"""
