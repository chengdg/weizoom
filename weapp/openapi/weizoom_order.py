# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from core import resource
from core.jsonresponse import create_response

class OrderList2(resource.Resource):
    """
    订单列表资源
    """
    app = "openapi"
    resource = "order_list"

    def get(request):
        """
                '''{
            "order_id": "20151204144404951",
            "order_status": 3,
            "num": 1,
            "order_price": "50.00",
            "pay_time": "2015-12-04 14:44:04",
            "found_time": "2015-12-04 14:44:04",
            "weizoom_card_money": 0,
            "pay_mode": 0,
            "p_price": 3,
            "freight": "0.00",
            "invoice_title": "",
            "store_message": "",
            "express_info": {
                "logistics_number": "121211211221",
                "buyer_message": "尽快发货",
                "receiver_name": "李三",
                "receiver_mobile": "13212312311",
                "receiver_province": "山西省",
                "receiver_city": "阳泉市",
                "receiver_district": "郊区",
                                "receiver_address": "海淀科技大厦 1201",
                                "logistics_name": "shentong"

            },
            "products": [
                {
                    "price": "50.00",
                    "goods_pic": "http://weappimgtest.b0.upaiyun.com/upload/15_20151111/1447231404074_96.jpg",
                    "unit_price": "50.00",
                    "count": 1,
                    "total_price": "50.00",
                    "goods_name": "限时抢购多规格"
                }
            ]
        }'''

        """
        print "zl-------------"
        response = create_response(200)
        response.data = []
        order_info = {}
        order_info['order_id'] = "20151204144404951"
        order_info['order_status'] = 3
        order_info['num'] = 1
        order_info['order_price'] = "50.00"
        order_info['pay_time'] = "2015-12-04 14:44:04"
        order_info['found_time'] = "2015-12-04 14:44:04"
        order_info['weizoom_card_money'] = 0
        order_info['pay_mode'] = 0
        order_info['p_price'] = "3.00"
        order_info['freight'] = "0.00"
        order_info['invoice_title'] = "北京科技大厦"
        order_info['store_message'] = "商家留言"
        order_info['express_info']= {}
        order_info['express_info']['logistics_number'] = "121211211221"
        order_info['express_info']['buyer_message'] = "尽快发货"
        order_info['express_info']['receiver_name'] = "李四"
        order_info['express_info']['receiver_mobile'] = "13011173465"
        order_info['express_info']['receiver_province'] = "北京"
        order_info['express_info']['receiver_city'] = "北京市"
        order_info['express_info']['receiver_district'] = "海淀区"
        order_info['express_info']['receiver_address'] = "海淀科技大厦 1201"
        order_info['express_info']['logistics_name'] = "shentong"
        order_info['products'] = [{
            "price": "50.00",
            "goods_pic": "http://weappimgtest.b0.upaiyun.com/upload/15_20151111/1447231404074_96.jpg",
            "unit_price": "50.00",
            "count": 1,
            "total_price": "50.00",
            "goods_name": "限时抢购多规格"
            }
        ]

        response.data.append(order_info)

        return response.get_response()

    def api_get(request):
        """

        """
        return {"1":"3333"}

