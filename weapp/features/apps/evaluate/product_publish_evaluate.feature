#__author__ : "许韦" 2016.06.06
Feature: 微信用户发表商品评价
"""
    1.bill在weapp中对已经到货的商品进行评价，包括有图、无图、问答题、选择题、参与人信息，默认项：商品评分，服务态度，发货速度，物流服务都为5颗星，评价字数在200个之内，显示项包括，商品名称，价格
    2.bill在我的评价中查看提交的商品评价
"""

Background:
    Given jobs登录系统
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
                    },{
                        "options":"不好说"
                    }]
            }],
        "participate_info":
            [{
                "items_select":
                    [{
                        "item_name":"姓名",
                        "is_selected":"true"
                    },{
                        "item_name":"手机",
                        "is_selected":"true"
                    },{
                        "item_name":"邮箱",
                        "is_selected":"false"
                    },{
                        "item_name":"QQ",
                        "is_selected":"false"
                    },{
                        "item_name":"职位",
                        "is_selected":"false"
                    },{
                        "item_name":"住址",
                        "is_selected":"false"
                    }],
                "items_add":
                    [{
                        "item_name":"职称",
                        "is_required":"否"
                    }]
            }]
    }
    """
    And jobs已添加商品
        """
        [{
            "name": "商品1",
            "price": 10.00
        }, {
            "name": "商品2",
            "price": 20.00
        }]
        """

    Given jobs已有的订单
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
                "name":"商品2",
                "price": 20.00,
                "count": 1
            }]
        }]
        """
    Given bill关注jobs的公众号
    When bill访问jobs的webapp
#    Then bill成功获取个人中心的'待评价'列表::h5
#        """
#        [{
#            "order_no": "1",
#            "products": [{
#                    "product_name": "商品1"
#                }]
#        }, {
#            "order_no": "2",
#            "products": [{
#                    "product_name": "商品2"
#                }]
#        }]
#        """
@mall @apps @app_evaluate @commit_app_product_comment
Scenario:1 评价包括文字与晒图
#    When bill访问jobs的webapp
#    And bill完成订单'1'中'商品1'的评价
#        """
#        {
#            "product_score": "5",
#            "answer": "",
#            "choose":"是",
#            "name":"bill",
#            "tel":"13013013011",
#            "title":"工程师",
#            "picture_list": ['1.png','2.jpg']
#        }
#        """
#    Then 订单'1'中'商品1'的评商品评价提示信息'发表评价失败'
    # And 订单'1'中'商品1'的评商品评价提示详情'请填写必填项'

#    When bill访问jobs的webapp
#    And bill完成订单'1'中'商品1'的评价
#        """
#        {
#            "product_score": "5",
#            "answer": "腰不酸腿不痛，走路不抽经了！！！！",
#            "choose":"",
#            "name":"bill",
#            "tel":"13013013011",
#            "title":"",
#            "picture_list": ['1.png','2.jpg']
#        }
#        """
#    Then 订单'1'中'商品1'的评商品评价提示信息'发表评价失败'
    # And 订单'1'中'商品1'的评商品评价提示详情'请填写必填项'

#    When bill访问jobs的webapp
#    And bill完成订单'1'中'商品1'的评价
#        """
#        {
#            "product_score": "5",
#            "answer": "腰不酸腿不痛，走路不抽经了！！！！",
#            "choose":"否",
#            "name":"bill",
#            "tel":"",
#            "title":"经理",
#            "picture_list": ['1.png','2.jpg']
#        }
#        """
#    Then 订单'1'中'商品1'的评商品评价提示信息'发表评价失败'
    # And 订单'1'中'商品1'的评商品评价提示详情'请填写必填项'

    #文字在5-200以内，填写必填项，成功提交
    When bill完成订单'1'中'商品1'的评价
        """
        {
            "product_score": "4",
            "answer": "整体还可以",
            "choose":"不好说",
            "name":"bill",
            "tel":"13013013011",
            "title":"",
            "picture_list": ['1.png']
        }
        """
    Then bill成功获取个人中心的'待评价'列表
        """
        [{
            "order_no": "2",
            "products": [{
                    "product_name": "商品2"
                }]
        }]
        """
    Then bill成功获取'商品评价'列表
        """
        [{
            "product_name":"商品1",
            "answer": "整体还可以",
            "choose":"不好说",
            "name":"bill",
            "tel":"13013013011",
            "title":"",
            "picture_list":['1.png']
        }]
        """

@mall @apps @app_evaluate @commit_app_product_comment
Scenario:2 无晒图，追加晒图
    When bill访问jobs的webapp
    And bill完成订单'1'中'商品1'的评价
        """
        {
            "product_score": "5",
            "answer": "商品非常好！！！",
            "choose":"是",
            "name":"bill",
            "tel":"13013013011",
            "title":"",
            "picture_list":[]
        }
        """
    Then bill成功获取个人中心的'待评价'列表
        """
        [{
            "order_no": "1",
            "products": [{
                    "product_name": "商品1"
                }]
        },{
            "order_no": "2",
            "products": [{
                    "product_name": "商品2"
                }]
        }]
        """
    Then bill成功获取'商品评价'列表
        """
        [{
            "product_name":"商品1",
            "answer": "商品非常好！！！",
            "choose":"是",
            "name":"bill",
            "tel":"13013013011",
            "title":""
        }]
        """
    When bill完成订单'1'中'商品1'的追加晒图评价
        """
        {
            "picture_list": ['1.jpg']
        }
        """
    Then bill成功获取个人中心的'待评价'列表
        """
        [{
            "order_no": "2",
            "products": [{
                    "product_name": "商品2"
                }]
        }]
        """
    Then bill成功获取'商品评价'列表
        """
        [{
            "product_name":"商品1",
            "answer": "商品非常好！！！",
            "choose":"是",
            "name":"bill",
            "tel":"13013013011",
            "title":""
            "picture_list":['1.jpg']
        }]
        """