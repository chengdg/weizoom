#watcher:fengxuejing@weizoom.com,benchi@weizoom.com

@func:market_tools.tools.store
Feature: 修改门店管理
    jobs能通过管理系统修改门店信息

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
Scenario: 修改"门店管理"
    1.jobs能修改"门店管理"，并保存。
    2.jobs修改后,门店列表正确显示,且修改后不影响排列顺序
    3.bill能够在客户端正确显示,且修改后不影响排列顺序(包括所在区域列表和店铺信息列表)

    Given jobs登录系统
    When jobs修改'山西路门店'信息
        """
        [{
            "name":"天安门门店",
            "thumbnails_url":"aa1.jpg",
            "store_intro":"本店经营北京小吃",
            "swipe_images":[
                {"url": "1.jpg"},
                {"url": "2.jpg"},
                {"url": "3.jpg"}
            ],
            "city":"北京",
            "address":"东郊门巷44号",
            "location":"116.406905,39.908222",
            "bus_line":"乘坐12路,13路到天安门",
            "zone":"010",
            "num":"12345679",
            "detail":"一次消费满200元,返券100元"
        }]
        """

    Then jobs能获取'天安门门店'的信息
        """
        {
            "name":"天安门门店",
            "thumbnails_url":"aa1.jpg",
            "store_intro":"本店经营北京小吃",
            "swipe_images":[
                {"url": "1.jpg"},
                {"url": "2.jpg"},
                {"url": "3.jpg"}
            ],
            "city":"北京",
            "address":"东郊门巷44号",
            "location":"116.406905,39.908222",
            "bus_line":"乘坐12路,13路到天安门",
            "zone":"010",
            "num":"12345679",
            "detail":"一次消费满200元,返券100元"
        }
        """

    When jobs修改'新街口门店'信息
        """
        [{
            "name":"中关村门店",
            "thumbnails_url":"aa1.jpg",
            "store_intro":"本店经营北京小吃",
            "swipe_images":[
                {"url": "1.jpg"},
                {"url": "2.jpg"},
                {"url": "3.jpg"}
            ],
            "city":"北京",
            "address":"海淀区阜成路73号",
            "location":"116.305143,39.930737",
            "bus_line":"乘坐33路,32路到中关村站",
            "zone":"010",
            "num":"13345678",
            "detail":"一次消费满200元,返券10元"
        }]
        """
    Then jobs不能取到'新街口门店'的信息
        """
        []
        """
