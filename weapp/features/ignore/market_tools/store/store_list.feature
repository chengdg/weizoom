# __author__ : "崔帅帅"
@func:market_tools.tools.store
Feature:Get Store List
		jobs能通过系统获取已添加的所有门店列表

Background:
    Given jobs登录系统
    Given jobs已经添加门店信息
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
            "num":"13345678",
            "detail":"一次消费满200元,返券10元"
        },{
            "name":"水西门店",
            "thumbnails_url":"aa.jpg",
            "store_intro":"本店经营重庆小吃",
            "swipe_images":[
                {"url": "1.jpg"},
                {"url": "2.jpg"},
                {"url": "3.jpg"}
            ],
            "city":"南京",
            "address":"水西门88号",
            "location":"118.81855,31.966008",
            "bus_line":"乘坐22路,23路到水西门店",
            "zone":"025",
            "num":"12345678",
            "detail":"一次消费满200元,返券10元"
        }]
        """

@weapp.market_tools.tools.store
Scenario:门店列表
	1.jobs点击“门店管理”后，能获取已添加的门店列表，该门店按被添加的时间倒序排列

	Given jobs登录系统
	Then jobs能获取门店列表
	"""
	[{
        "name":"山西路门店",
        "city":"南京"
    },{
		"name":"新街口门店",
		"city":"南京"
	},{
        "name":"水西门店",
        "city":"南京"
    }]
	"""

