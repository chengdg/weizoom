#editor:江秋丽 2016.6.7

Feature: jobs在后台对已有评价进行审核
"""
    [商品详情页的验证]
    1.审核通过：用户评价内容将显示在商品详情页；
    2.屏蔽处理：该评价将不被允许显示在商品详情页；
    3.通过并置顶：是指审核通过该评论，并且置顶显示该评价；
    4.置顶时间为15天，置顶周期结束后，恢复按评价时间倒序显示。
    5 同款商品，3个置顶操作，最后置顶的，排在最上面
    6.同款商品，最多可置顶3条评价信息，第4条置顶时，第一条置顶信息失去优先级，按原有时间顺序排列
"""
Background:
    Given 重置weapp的bdd环境
    Given jobs登录系统:weapp
    And jobs已添加商品:weapp
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
    And jobs已有的订单:weapp
        """
        [{
            "order_no":"1",
            "member":"bill",
            "type":"普通订单",
            "status":"已完成",
            "sources":"本店",
            "order_price":10.00,
            "payment_price":10.00,
            "freight":0.00,
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
            "freight":0.00,
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
            "freight":0.00,
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
            "freight":0.00,
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
            "freight":0.00,
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
            "freight":0.00,
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
            "freight":0.00,
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
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "answer": "整体还可以",
            "choose":"是",
            "name":"bill",
            "tel":"13650088986",
            "title":"",
            "picture_list": ['1.png','2.png']
        }
        """
    And bill完成订单'12'中'商品1'的评价
        """
        {
            "product_score": "4",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "answer": "整体还可以",
            "choose":"否",
            "name":"bill",
            "tel":"13650088986",
            "title":"",
            "picture_list": ['3.png']
        }
        """
    And bill完成订单'13'中'商品1'的评价
        """
        {
            "product_score": "4",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "answer": "整体还可以",
            "choose":"不好说",
            "name":"bill",
            "tel":"13650088986",
            "title":"",
            "picture_list": ['4.png']
        }
        """
    And bill完成订单'14'中'商品1'的评价
        """
        {
            "product_score": "4",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "answer": "整体还可以",
            "choose":"是",
            "name":"bill",
            "tel":"13650088986",
            "title":"",
            "picture_list": ['1.png']
        }
        """
    And bill完成订单'15'中'商品1'的评价
        """
        {
            "product_score": "5",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "answer": "腰不酸腿不痛，走路不抽经了！！！！",
            "choose":"是",
            "name":"bill",
            "tel":"13652587988",
            "title":"",
            "picture_list": ['1.png','2.jpg']
        }
        """
    And bill完成订单'16'中'商品1'的评价
        """
        {
            "product_score": "5",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "answer": "腰不酸腿不痛，走路不抽经了！！！！",
            "choose":"是",
            "name":"bill",
            "tel":"13652587988",
            "title":"",
            "picture_list": ['1.png','2.jpg']
        }
        """

    And bill完成订单'2'中'商品2'的评价
        """
        {
            "product_score": "5",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "answer": "腰不酸腿不痛，走路不抽经了！！！！",
            "choose":"是",
            "name":"bill",
            "tel":"13652587988",
            "title":"",
        }
        """
    Given tom关注jobs的公众号
    And jobs已有的订单:weapp
        """
        [{
            "order_no":"3",
            "member":"tom",
            "type":"普通订单",
            "status":"已完成",
            "sources":"本店",
            "order_price":10.00,
            "payment_price":10.00,
            "freight":0.00,
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
            "freight":0.00,
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
    And tom完成订单'3'中'商品1'的评价
        """
        {
            "product_score": "4",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "answer": "整体还可以",
            "choose":"是",
            "name":"tom",
            "tel":"13650088986",
            "title":"",
            "picture_list": "['/static/upload/webapp/3_20151102/2015_11_02_18_24_49_948000.png']"
        }
        """
    And tom完成订单'4'中'商品2'的评价
        """
        {
            "product_score": "5",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "answer": "腰不酸腿不痛，走路不抽经了！！！！",
            "choose":"是",
            "name":"tom",
            "tel":"13652587900",
            "title":"",
        }
        """


    1.审核通过:用户评价内容将显示在商品详情页
    2.屏蔽处理：该评价将不被允许显示在商品详情页
    3.通过并置顶：是指审核通过该评论，并且置顶显示该评价
    4.回复会员评论：回复的内容显示在会员个人中心列表中；


    Given jobs登录系统:weapp
    When jobs已完成对商品的评价信息审核:weapp
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
            "status": "2",          
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

    When bill访问jobs的webapp
    Then bill在商品详情页成功获取'商品1'的评价列表
        """
        [{
            "member": "bill",
            "review_detail": "12商品1还不错！！！！！"
        },{
            "member": "bill",
            "review_detail": "1商品1还不错！！！！！"
        }]
        """

    And bill在商品详情页成功获取'商品2'的评价列表
        """
        [{
            "member": "bill",
            "review_detail": "商品2不太好！！！！！！！"
        }]
        """  
    Given jobs登录系统:weapp
    
    And jobs完成'商品1'的评价的回复
    	"""
        {
            "product_name": "商品1",
            "order_no": "3",
            "member": "bill",
            "review_detail": "1商品1还不错！！！！！",
            "reply": "谢谢评价"
        }，{
            "product_name": "商品1",
            "order_no": "12",
            "member": "bill|",
            "review_detail": "12商品1还不错！！！！！",
            "reply": "谢谢评价"
        }
        """
        And jobs完成'商品2'的评价的回复
    	"""
        {
            "product_name": "商品2",
            "order_no": "4",
            "member": "bill",
            "review_detail": "商品2不太好！！！！！！！",
            "reply": "谢谢评价"
        }
        """
        When bill访问jobs的webapp
        Then bill在个人中心成功获取'商品1'的评价列表
        """
        [{
            "member": "bill",            
            "review_detail": "12商品1还不错！！！！！",
            "reply": "谢谢评价"
        },{
            "member": "bill",            
            "review_detail": "1商品1还不错！！！！！",
            "reply": "谢谢评价"
        }]
        """

