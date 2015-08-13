# __author__ : "崔帅帅"
@func:market_tools.tools.store
Feature: 修改门店管理
	Jobs能通过管理系统修改门店信息

Background:
	Given Jobs登录系统
	And Jobs已经添加"山西路店"信息
		"""
		[{
			"name":"山西路门店",
			"small_pic":"aa.jpg",
			"introduction":"本店经营四川小吃",
			"swipe_images":["1.jpg", "2.jpg", "3.jpg"]
			"city":"南京",
			"address":"中山北路88号",
			"point":"118.781474,32.07355",
			"line":"乘坐12路,13路到山西路站",
			"tel":"025-12345678",
			"details":"一次消费满200元,返券10元"
		}]
		"""

	And Jobs已经添加"新街口门店"信息
		"""
		[{
			"name":"新街口门店",
			"small_pic":"aa.jpg",
			"introduction":"本店经营南京小吃",
			"swipe_images":["1.jpg", "2.jpg", "3.jpg"]
			"city":"南京",
			"address":"中山北路88号",
			"point":"118.781474,32.07355",
			"line":"乘坐42路,43路到山西路站",
			"tel":"025-13345678",
			"details":"一次消费满200元,返券10元"
		}]
		"""

	And Jobs已经添加"水西门店"信息
		"""
		[{
			"name":"水西门店",
			"small_pic":"aa.jpg",
			"introduction":"本店经营重庆小吃",
			"swipe_images":["1.jpg", "2.jpg", "3.jpg"]
			"city":"南京",
			"address":"水西门88号",
			"point":"118.81855,31.966008",
			"line":"乘坐22路,23路到水西门店",
			"tel":"025-12345678",
			"details":"一次消费满200元,返券10元"
		}]
		"""
	And Bill已加关注

@weapp.market_tools.store @ignore
Scenario: 修改"门店管理"
	1.Jobs能修改"门店管理"，并保存。
	2.Jobs修改后,门店列表正确显示,且修改后不影响排列顺序
	3.Bill能够在客户端正确显示,且修改后不影响排列顺序(包括所在区域列表和店铺信息列表)

	Given Jobs登录系统
	When Jobs修改"山西路门店"信息
		"""
		[{
			"name":"天安门门店",
			"small_pic":"aa1.jpg",
			"introduction":"本店经营北京小吃",
			"swipe_images":["1.jpg", "2.jpg", "3.jpg"]
			"city":"北京",
			"address":"东郊门巷44号",
			"point":"116.406905,39.908222",
			"line":"乘坐12路,13路到天安门",
			"tel":"010-12345679",
			"details":"一次消费满200元,返券100元"
		}]
		"""
	And Jobs修改"新街口门店"信息
		"""
		[{
			"name":"中关村门店",
			"city":"北京",
			"address":"海淀区阜成路73号",
			"point":"116.305143,39.930737",
			"line":"乘坐33路,32路到中关村站",
			"tel":"010-13345678"
		}]
		"""

	Then Jobs获取"门店列表"
		"""
		[{
			"name":"水西门店"
			"city":"南京",
		},{
			"name":"中关村门店",
			"city":"北京",
		},{
			"name":"天安门门店",
			"city":"北京",
		}]
		"""

	Then Jobs获得"天安门门店"和"中关村门店"信息
		"""
		[{
			"name":"天安门门店",
			"small_pic":"aa1.jpg",
			"introduction":"本店经营北京小吃",
			"swipe_images":[
                {"url": "1.jpg"},
                {"url": "2.jpg"},
                {"url": "3.jpg"}
            ],
            "city":"北京",
			"address":"东郊门巷44号",
			"point":"116.406905,39.908222",
			"line":"乘坐33路,32路到中关村站",
			"tel":"010-12345679",
			"details":"一次消费满200元,返券100元"

		},{
			"name":"中关村门店"
			"small_pic":"aa.jpg",
			"introduction":"本店经营南京小吃",
			"swipe_images":[
                {"url": "1.jpg"},
                {"url": "2.jpg"},
                {"url": "3.jpg"}
            ],
            "city":"北京",
			"address":"海淀区阜成路73号",
			"point":"116.305143,39.930737",
			"line":"乘坐42路,43路到山西路站",
			"tel":"010-13345678",
			"details":"一次消费满200元,返券10元"

		}]
		"""


	Then Bill获取"所在区域"
		"""
		[{
			"city":"南京",
		},{
			"city":"北京",
		}]
		"""

	Then Bill获取"北京"的门店信息列表
		"""
		[{
			"name":"中关村门店",
			"introduction":"本店经营南京小吃"

		},{
			"name":"天安门门店",
			"introduction":"本店经营北京小吃"
		}]
		"""

	Then Bill获取"中关村门店"信息
		"""
		[{
			"swipe_images":["1.jpg", "2.jpg", "3.jpg"]
			"name":"中关村门店",
			"tel":"010-13345678",
			"address":"海淀区阜成路73号",
			"line":"乘坐33路,32路到中关村站",
			"introduction":"本店经营南京小吃"
		}]
		"""





