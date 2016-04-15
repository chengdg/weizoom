# __author__ : "新新2016.4.6"


Feature: 评价管理导出
"""
	1.用户id,用户名,商品名称,订单号,姓名,电话,评价时间,状态,产品评星,评价内容,图片链接


"""
	Given jobs登录系统
    And jobs已添加商品
        """
        [{
            "name": "商品1",
            "price": "10.00"
            }, {
            "name": "商品2",
            "price": "20.00"
            }, {
            "name": "商品3",
            "price": "30.00"
        }]
        """
    Given bill关注jobs的公众号
    And jobs已有的订单
        """
        [{
            "order_no":"1",
            "member":"bill",
            "type":"普通订单",
            "status":"已完成",
            "sources":"本店",
            "order_price":10.00,
            "payment_price":10.00,
            "freight":0,
            "ship_name":"bill",
            "ship_tel":"13013013011",
            "ship_area":"北京市,北京市,海淀区",
            "ship_address":"泰兴大厦",
            "products":[{
                "name":"商品1",
                "price": 10.00,
                "count": 1
            }]
        },{
            "order_no":"12",
            "member":"bill",
            "type":"普通订单",
            "status":"已完成",
            "sources":"本店",
            "order_price":10.00,
            "payment_price":10.00,
            "freight":0,
            "ship_name":"bill",
            "ship_tel":"13013013011",
            "ship_area":"北京市,北京市,海淀区",
            "ship_address":"泰兴大厦",
            "products":[{
                "name":"商品1",
                "price": 10.00,
                "count": 1
            }]
        },{
            "order_no":"13",
            "member":"bill",
            "type":"普通订单",
            "status":"已完成",
            "sources":"本店",
            "order_price":10.00,
            "payment_price":10.00,
            "freight":0,
            "ship_name":"bill",
            "ship_tel":"13013013011",
            "ship_area":"北京市,北京市,海淀区",
            "ship_address":"泰兴大厦",
            "products":[{
                "name":"商品1",
                "price": 10.00,
                "count": 1
            }]
        },{
            "order_no":"14",
            "member":"bill",
            "type":"普通订单",
            "status":"已完成",
            "sources":"本店",
            "order_price":10.00,
            "payment_price":10.00,
            "freight":0,
            "ship_name":"bill",
            "ship_tel":"13013013011",
            "ship_area":"北京市,北京市,海淀区",
            "ship_address":"泰兴大厦",
            "products":[{
                "name":"商品1",
                "price": 10.00,
                "count": 1
            }]
        },{
            "order_no":"15",
            "member":"bill",
            "type":"普通订单",
            "status":"已完成",
            "sources":"本店",
            "order_price":10.00,
            "payment_price":10.00,
            "freight":0,
            "ship_name":"bill",
            "ship_tel":"13013013011",
            "ship_area":"北京市,北京市,海淀区",
            "ship_address":"泰兴大厦",
            "products":[{
                "name":"商品1",
                "price": 10.00,
                "count": 1
            }]
        },{
            "order_no":"16",
            "member":"bill",
            "type":"普通订单",
            "status":"已完成",
            "sources":"本店",
            "order_price":10.00,
            "payment_price":10.00,
            "freight":0,
            "ship_name":"bill",
            "ship_tel":"13013013011",
            "ship_area":"北京市,北京市,海淀区",
            "ship_address":"泰兴大厦",
            "products":[{
                "name":"商品1",
                "price": 10.00,
                "count": 1
            }]
        },{
            "order_no":"2",
            "member":"bill",
            "type":"普通订单",
            "status":"已完成",
            "sources":"本店",
            "order_price":20.00,
            "payment_price":20.00,
            "freight":0,
            "ship_name":"bill",
            "ship_tel":"13013013011",
            "ship_area":"北京市,北京市,海淀区",
            "ship_address":"泰兴大厦",
            "products":[{
                "name":"商品2",
                "price": 20.00,
                "count": 1
            }]
        }]
        """

    When bill访问jobs的webapp
    And bill完成订单'1'中'商品1'的评价
        """
        {
            "product_score": "4",
            "review_detail": "1商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": "['/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png']"
        }
        """
    And bill完成订单'12'中'商品1'的评价
        """
        {
            "product_score": "4",
            "review_detail": "12商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": "['/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png']"
        }
        """
    And bill完成订单'13'中'商品1'的评价
        """
        {
            "product_score": "4",
            "review_detail": "13商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": "['/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png']"
        }
        """
    And bill完成订单'14'中'商品1'的评价
        """
        {
            "product_score": "4",
            "review_detail": "14商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": "['/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png']"
        }
        """
    And bill完成订单'15'中'商品1'的评价
        """
        {
            "product_score": "4",
            "review_detail": "15商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": "['/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png']"
        }
        """
    And bill完成订单'16'中'商品1'的评价
        """
        {
            "product_score": "4",
            "review_detail": "16商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": "['/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png']"
        }
        """

    And bill完成订单'2'中'商品2'的评价
        """
        {
            "product_score": "4",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "review_detail": "商品2不太好！！！！！！！"
        }
        """
    Given tom关注jobs的公众号
    And jobs已有的订单
        """
        [{
            "order_no":"3",
            "member":"tom",
            "type":"普通订单",
            "status":"已完成",
            "sources":"本店",
            "order_price":10.00,
            "payment_price":10.00,
            "freight":0,
            "ship_name":"bill",
            "ship_tel":"13013013011",
            "ship_area":"北京市,北京市,海淀区",
            "ship_address":"泰兴大厦",
            "products":[{
                "name":"商品1",
                "price": 10.00,
                "count": 1
            }]
        },{
            "order_no":"4",
            "member":"tom",
            "type":"普通订单",
            "status":"已完成",
            "sources":"本店",
            "order_price":20.00,
            "payment_price":20.00,
            "freight":0,
            "ship_name":"bill",
            "ship_tel":"13013013011",
            "ship_area":"北京市,北京市,海淀区",
            "ship_address":"泰兴大厦",
            "products":[{
                "name":"商品2",
                "price": 20.00,
                "count": 1
            }]
        }]
        """
    When tom访问jobs的webapp
    When tom完成订单'3'中'商品1'的评价
        """
        {
            "product_score": "4",
            "review_detail": "商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": "['/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png']"
        }
        """
    When tom完成订单'4'中'商品2'的评价
        """
        {
            "product_score": "4",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "review_detail": "商品2不太好！！！！！！！"
        }
        """
    Given jobs登录系统
    When jobs已完成对商品的评价信息审核
        """
        [{
            "product_name": "商品1",
            "order_no": "3",
            "member": "tom",
            "status": "-1"
        },{
            "product_name": "商品1",
            "order_no": "1",
            "member": "bill",
            "status": "1"
        },{
            "product_name": "商品1",
            "order_no": "12",
            "member": "bill",
            "status": "2"
        },{
           "member": "tom",
           "order_no": "4",
           "product_name": "商品2",
           "status": "0"
        },{
           "member": "bill",
           "order_no": "2",
           "product_name": "商品2",
           "status": "2"
        }]
        """


Scenario:1 导出全部评价
    Given jobs登录系统
    
    Then jobs导出评价列表
        | name_id | member | name | order_no | ship_name | ship_tel | time | status | product_score | review_detail | picture_list |
        | name_id |  tom  | 商品2 |   4     |    bill   | 13013013011 | 今天 | 待审核 |  4  | 商品2不太好！！！！！！！ |   |
        | name_id |  tom  | 商品1 |   3     |    bill   | 13013013011 | 1天前| 已屏蔽 |  4  | 商品1还不错！！！！！ |'/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png'|
        | name_id |  bill | 商品2 |   2     |    bill   | 13013013011 | 1天前| 通过并置顶 |  4  | 商品2不太好！！！！！！！ |   |
        | name_id |  bill | 商品1 |   16    |    bill   | 13013013011 | 1天前| 待审核 |  4  | 16商品1还不错！！！！！ |'/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png'|
        | name_id |  bill | 商品1 |   15    |    bill   | 13013013011 | 1天前| 待审核 |  4  | 15商品1还不错！！！！！ |'/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png'|
        | name_id |  bill | 商品1 |   14    |    bill   | 13013013011 | 2天前| 待审核 |  4  | 14商品1还不错！！！！！ |'/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png'|
        | name_id |  bill | 商品1 |   13    |    bill   | 13013013011 | 2天前| 待审核 |  4  | 13商品1还不错！！！！！ |'/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png'|
        | name_id |  bill | 商品1 |   12    |    bill   | 13013013011 | 2天前| 通过并置顶 |  4  | 12商品1还不错！！！！！ |'/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png'|
        | name_id |  bill | 商品1 |   1     |    bill   | 13013013011 | 2天前| 已通过 |  4  | 1商品1还不错！！！！！ |'/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png'|

Scenario:2 指定筛选条件下导出全部评价

    Given jobs登录系统
    When jobs根据给定条件查询评价
        """
        {
            "status": "待审核"
        }
        """

    Then jobs导出评价列表
        | name_id | member | name | order_no | ship_name | ship_tel | time | status | product_score | review_detail | picture_list |
        | name_id |  tom  | 商品2 |   4     |    bill   | 13013013011 | 今天 | 待审核 |  4  | 商品2不太好！！！！！！！ |   |
        | name_id |  bill | 商品1 |   16    |    bill   | 13013013011 | 1天前| 待审核 |  4  | 16商品1还不错！！！！！ |'/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png'|
        | name_id |  bill | 商品1 |   15    |    bill   | 13013013011 | 1天前| 待审核 |  4  | 15商品1还不错！！！！！ |'/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png'|
        | name_id |  bill | 商品1 |   14    |    bill   | 13013013011 | 2天前| 待审核 |  4  | 14商品1还不错！！！！！ |'/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png'|
        | name_id |  bill | 商品1 |   13    |    bill   | 13013013011 | 2天前| 待审核 |  4  | 13商品1还不错！！！！！ |'/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png'|
