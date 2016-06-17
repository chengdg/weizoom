#editor:许韦 2016.06.19

Feature: jobs在后台对已有评价进行审核
"""
    1.审核通过：用户评价内容将显示在商品详情页；
    2.屏蔽处理：该评价将不被允许显示在商品详情页；
    3.通过并置顶：是指审核通过该评论，并且置顶显示该评价；
    4.置顶时间为15天，置顶周期结束后，恢复按评价时间倒序显示。
    5 同款商品，3个置顶操作，最后置顶的，排在最上面
    6.同款商品，最多可置顶3条评价信息，第4条置顶时，第一条置顶信息失去优先级，按原有时间顺序排列
    7.回复会员评论：回复的内容显示在会员个人中心列表中；
"""

Background:
    Given jobs登录系统
    And jobs已添加商品
        """
        [{
            "name": "商品1",
            "price": "10.00"
        }]
        """
    When jobs配置商品评论自定义模板
    """
    {
        "type":"custom",
            "answer":
                [{
                    "title":"您使用产品后的感受是",
                    "is_required":"是"
                }],
            "choose":
                [{
                    "title":"您对本产品的包装是否满意",
                    "type":"单选",
                    "is_required":"是",
                    "option":[{
                            "options":"是"
                        },{
                            "options":"否"
                        }]
                }],
            "participate_info":
                [{
                    "items_select":[{
                            "item_name":"姓名",
                            "is_selected":"true"
                        }],
                    "items_add":[{
                        "item_name":"性别",
                        "is_required":"否"
                        }]
                }]
    }
    """
    Given bill关注jobs的公众号
    And jobs已有的订单
        """
        [{
            "order_no":"1",
            "member":"bill",
            "status":"已完成",
            "sources":"本店",
            "order_price":10.00,
            "payment_price":10.00,
            "postage":0.00,
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
            "status":"已完成",
            "sources":"本店",
            "order_price":20.00,
            "payment_price":20.00,
            "postage":0.00,
            "ship_name":"bill",
            "ship_tel":"13013013011",
            "ship_area":"北京市,北京市,海淀区",
            "ship_address":"泰兴大厦",
            "products":[{
                "name":"商品1",
                "price": 20.00,
                "count": 2
            }]
        }]
        """
    When 清空浏览器
    When bill访问jobs的webapp
    And bill完成订单'1'中'商品1'的评价
        """
        {
            "product_score": "1",
            "answer":[{
                "title":"您使用产品后的感受是",
                "value":"商品1很好"
                }],
            "choose":[{
                "title":"您对本产品的包装是否满意",
                "value":"是"
                }],
            "participate_info":[{
                "name":"bill",
                "gender":"女"
            }],
            "picture_list": ["1.png","2.png"]
        }
        """
    And bill完成订单'2'中'商品1'的评价
        """
        {
            "product_score": "2",
            "answer":[{
                "title":"您使用产品后的感受是",
                "value":"商品1又来买了"
                }],
            "choose":[{
                "title":"您对本产品的包装是否满意",
                "value":"是"
                }],
            "participate_info":[{
                "name":"bill",
                "gender":"女"
            }],
            "picture_list": ["3.png"]
        }
        """
    When 清空浏览器
    Given tom关注jobs的公众号
    And jobs已有的订单
        """
        [{
            "order_no":"3",
            "member":"tom",
            "status":"已完成",
            "sources":"本店",
            "order_price":30.00,
            "payment_price":30.00,
            "postage":0.00,
            "ship_name":"tom",
            "ship_tel":"13667190229",
            "ship_area":"湖北省,武汉市,武昌区",
            "ship_address":"马房山小区",
            "products":[{
                "name":"商品1",
                "price": 30.00,
                "count": 3
            }]
        },{
            "order_no":"4",
            "member":"tom",
            "status":"已完成",
            "sources":"本店",
            "order_price":40.00,
            "payment_price":40.00,
            "postage":0.00,
            "ship_name":"tom",
            "ship_tel":"13667190229",
            "ship_area":"北京市,北京市,海淀区",
            "ship_address":"马房山小区",
            "products":[{
                "name":"商品1",
                "price": 40.00,
                "count": 4
            }]
        }]
        """ 
    When 清空浏览器
    When tom访问jobs的webapp
    And tom完成订单'3'中'商品1'的评价
        """
        {
            "product_score": "3",
            "answer":[{
                "title":"您使用产品后的感受是",
                "value":"商品1棒棒哒"
                }],
            "choose":[{
                "title":"您对本产品的包装是否满意",
                "value":"是"
                }],
            "participate_info":[{
                "name":"tom",
                "gender":"男"
            }],
            "picture_list": ["4.png"]
        }
        """
    And tom完成订单'4'中'商品1'的评价
        """
        {
            "product_score": "4",
            "answer":[{
                "title":"您使用产品后的感受是",
                "value":"商品1超喜欢"
                }],
            "choose":[{
                "title":"您对本产品的包装是否满意",
                "value":"是"
                }],
            "participate_info":[{
                "name":"tom",
                "gender":"男"
            }],
            "picture_list": ["5.png"]
        }
        """
    When 清空浏览器
    Given jerry关注jobs的公众号
    And jobs已有的订单
        """
        [{
            "order_no":"5",
            "member":"jerry",
            "status":"已完成",
            "sources":"本店",
            "order_price":50.00,
            "payment_price":50.00,
            "postage":0.00,
            "ship_name":"jerry",
            "ship_tel":"13705183408",
            "ship_area":"江苏省,南京市,下关区",
            "ship_address":"下关小学",
            "products":[{
                "name":"商品1",
                "price": 50.00,
                "count": 5
            }]
        }]
        """ 
    When 清空浏览器
    When jerry访问jobs的webapp
    And jerry完成订单'5'中'商品1'的评价
        """
        {
            "product_score": "5",
            "answer":[{
                "title":"您使用产品后的感受是",
                "value":"会推荐商品1"
                }],
            "choose":[{
                "title":"您对本产品的包装是否满意",
                "value":"否"
                }],
            "participate_info":[{
                "name":"jerry",
                "gender":"男"
            }],
            "picture_list": []
        }
        """

@mall @apps @app_evaluate @comment_examination
Scenario:1 审核通过 屏蔽处理 通过并置顶
    Given jobs登录系统
    When jobs已完成对商品的评价信息审核
        """
        [{
            "product_name": "商品1",
            "order_no": "1",
            "member": "bill",
            "status": "通过并置顶"
        },{
            "product_name": "商品1",
            "order_no": "2",
            "member": "bill",
            "status": "通过审核"
        },{
            "product_name": "商品1",
            "order_no": "3",
            "member": "tom",
            "status": "屏蔽处理"
        },{
            "product_name": "商品1",
            "order_no": "4",
            "member": "tom",
            "status": "通过审核"
        }]
        """ 
    When 清空浏览器
    When bill访问jobs的webapp
    #Then bill在商品详情页成功获取'商品1'的评价列表::h5
    #    """
    #    [{
    #        "member": "bill",
    #        "comments": [{
    #                "title":"您使用产品后的感受是",                
    #                "value":"商品1很好"
    #            },{
    #                "title":"您对本产品的包装是否满意",
    #                "value":"是"
    #            }]
    #    },{
    #        "member": "tom",
    #        "comments": [{
    #                "title":"您使用产品后的感受是",                
    #                "value":"商品1超喜欢"
    #            },{
    #                "title":"您对本产品的包装是否满意",
    #                "value":"是"
    #            }]
    #    }]
    #    """
    Then bill能获取'商品1'的更多评价列表
        """
        [{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"商品1很好"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                }],
            "picture_list": ["1.png","2.png"]
        },{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"商品1超喜欢"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                }],
            "picture_list": ["5.png"]
        },{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"商品1又来买了"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                }],
            "picture_list": ["3.png"]
        }]
        """
    
@mall @apps @app_evaluate @comment_examination
Scenario:2 同个商品，最多可置顶3条评价信息
#第4条置顶时，第一条置顶信息失去优先级，按原有时间顺序排列
    Given jobs登录系统
    When jobs已完成对商品的评价信息审核
        """
        [{
            "product_name": "商品1",
            "order_no": "1",
            "member": "bill",
            "status": "通过并置顶"
        },{
            "product_name": "商品1",
            "order_no": "2",
            "member": "bill",
            "status": "通过并置顶"       
        },{
            "product_name": "商品1",
            "order_no": "3",
            "member": "tom",
            "status": "通过并置顶"         
        },{
            "product_name": "商品1",
            "order_no": "4",
            "member": "tom",
            "status": "通过并置顶"
        },{
            "product_name": "商品1",
            "order_no": "5",
            "member": "jerry",
            "status": "通过审核"
        }]
        """ 
    When 清空浏览器
    When bill访问jobs的webapp
    #Then bill在商品详情页成功获取'商品1'的评价列表::h5
    #    """
    #    [{
    #        "member": "tom",
    #        "comments": [{
    #                "title":"您使用产品后的感受是",                
    #                "value":"商品1超喜欢"
    #            },{
    #                "title":"您对本产品的包装是否满意",
    #                "value":"是"
    #            }]
    #    },{
    #        "member": "bill",
    #        "comments": [{
    #                "title":"您使用产品后的感受是",                
    #                "value":"商品1棒棒哒"
    #            },{
    #                "title":"您对本产品的包装是否满意",
    #                "value":"是"
    #            }]
    #    }]
    #    """
    Then bill能获取'商品1'的更多评价列表
        """
        [{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"商品1超喜欢"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                }],
            "picture_list": ["5.png"]
        },{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"商品1棒棒哒"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                }],
            "picture_list": ["4.png"]
        },{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"商品1又来买了"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                }],
            "picture_list": ["3.png"]
        },{
            "member": "jerry",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"会推荐商品1"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"否"
                }],
            "picture_list": []
        },{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"商品1很好"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                }],
            "picture_list": ["1.png","2.png"]
        }]
        """

@mall @apps @app_evaluate @comment_examination
Scenario:3 回复用户发表的商品评论
    Given jobs登录系统
    When jobs完成订单'1'中'商品1'的评价回复
        """
        {
            "text":"感谢您的选择，希望我们的产品能让您满意！",
            "url":"/mall2/integral_sales_list/"
        }
        """
    Then jobs能获得订单"1"中的"商品1"评价详情
        """
        {
            "product_name": "商品1",
            "order_no": "1",
            "member": "bill",
            "product_score":"1",
            "comments":[{
                    "title":"您使用产品后的感受是",
                    "value":"商品1很好"
                },{
                    "title":"您对本产品的包装是否满意",
                   "value":"是"
                },{
                    "title":"gender",
                    "value":"女"
                },{
                    "title":"name",
                    "value":"bill"
                }],
            "picture_list":["1.png","2.png"],
            "reply":{
                "text":"感谢您的选择，希望我们的产品能让您满意！",
                "url":"/mall2/integral_sales_list/"
            }
        }
        """
    When 清空浏览器
    When bill访问jobs的webapp
    Then bill成功获取'我的评价'列表
        """
        [{   
            "product_name":"商品1",
            "comments":[{
                "title":"您使用产品后的感受是",
                "value":"商品1又来买了"
            },{
                "title":"您对本产品的包装是否满意",
                "value":"是"
            }],
            "picture_list": ["3.png"]
        },{
            "product_name":"商品1",
            "comments":[{
                "title":"您使用产品后的感受是",
                "value":"商品1很好"
            },{
                "title":"您对本产品的包装是否满意",
                "value":"是"
            }],
            "picture_list": ["1.png","2.png"],
            "reply":{
                "text":"感谢您的选择，希望我们的产品能让您满意！",
                "url":"/mall2/integral_sales_list/"
            }
        }]
        """
    Given jobs登录系统
    When jobs完成订单'1'中'商品1'的评价回复
        """
        {
            "text":"您的满意是我们的追求，哈哈"
        }
        """
    Then jobs能获得订单"1"中的"商品1"评价详情
        """
        {
            "product_name": "商品1",
            "order_no": "1",
            "member": "bill",
            "product_score":"1",
            "comments":[{
                    "title":"您使用产品后的感受是",
                    "value":"商品1很好"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"gender",
                    "value":"女"
                },{
                    "title":"name",
                    "value":"bill"
                }],
            "picture_list":["1.png","2.png"],
            "reply":{
                "text":"您的满意是我们的追求，哈哈"
            }
        }
        """
    When 清空浏览器
    When bill访问jobs的webapp
    Then bill成功获取'我的评价'列表
        """
        [{   
            "product_name":"商品1",
            "comments":[{
                "title":"您使用产品后的感受是",
                "value":"商品1又来买了"
            },{
                "title":"您对本产品的包装是否满意",
                "value":"是"
            }],
            "picture_list": ["3.png"]
        },{
            "product_name":"商品1",
            "comments":[{
                "title":"您使用产品后的感受是",
                "value":"商品1很好"
            },{
                "title":"您对本产品的包装是否满意",
                "value":"是"
            }],
            "picture_list": ["1.png","2.png"],
            "reply":{
                "text":"您的满意是我们的追求，哈哈"
            }
        }]
        """