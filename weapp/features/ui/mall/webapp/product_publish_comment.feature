# __author__ : "新新8.27"
Feature: bill在webapp中对已到货的商品进行评价
"""
    该feature中需要修改和补充,涉及到场景如下
    #发表评价列表按时间倒序显示
    一 发表评价
    #文字小于5个字发评论按钮置灰
    #评价字数在200个之内，显示项包括，商品名称
    #评价图片最多上传5张,满5张时,无'+'按钮
    #待评价列表显示订单号,创建订单时间,商品名称,规格,订单总实付款
    1.bill评价包括，有图，无图，有文字,默认项,商品评分服务态度，发货速度，物流服务 都为5颗星
    2.商品评价,服务评分各项不是默认值时,提交评价
    3.文本评价后,返回首页操作后,可追加晒图
    4.评价完成后会有“感谢您的评价”页面，如果还有待评价的商品,有“返回首页”和“继续评价”,否则只有"返回首页"
    二 我的评价
    5.评价后,bill即刻在我的评价中看到
    #包括商品图片,商品名称,评价时间评价内容及评价图片(不显示规格)
    #如果没有评价过商品，则为空
    #信息显示顺序是按评价时间的倒序
    三 后台评价审核后,前台显示
    6.评价后,jobs审核通过后,商品详情中能够看到对商品评价信息
    #默认只显示两条评价信息；
    #显示昵称,头像,评价日期,评价内容
        1）该评价信息，如果是后台进行了置顶操作，则显示在第一个
        2）否则按评价时间倒叙
        3）其他评价内容在"更多评价"中显示

"""
Background:
    Given jobs登录系统
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
    Then bill成功获取个人中心的'待评价'列表
    """
    [{
        "order_no": "1",
        "products": [
            {
                "product_name": "商品1"
            }
        ]

    }, {
        "order_no": "2",
        "products": [
            {
                "product_name": "商品2"
            }
        ]

    }]
    """
   

Scenario: 1 评价包括文字与晒图
    When bill访问jobs的webapp
    And bill完成订单'1'中'商品1'的评价包括'文字与晒图'
    """
        {
            "product_score": "4",
            "review_detail": "商商商品1还不错！！！！！品1还不错！！！商商品1还不错！！！！！品1还不错！！！商商品1还不错！！！！！品1还不错！！！商商品1还不错！！！！！品1还不错！！！商商品1还不错！！！！！品1还不错！！！商商品1还不错！！！！！品1还不错！！！商商品1还不错！！！！！品1还不错！！！商商品1还不错！！！！！品1还不错！！！商商品1还不错！！！！！品1还不错！！！商品1还不错！！！！！品1还不错！！！!",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAFAAoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9F/2sf2ZviFo/x9/ZygX9pz44yL4g+JN7ZqW07win9mgeEvElxviCaGoc/uPL23AmTbKzbfNWOWP6BtP2YvG1taxxv+0V8Y53RArSyab4UDSED7x26KFyevAA9AKKKAP/2Q=="]
        }
    """

    Then 订单'1'中'商品1'的评商品评价提示信息'发表评价失败'
    # And 订单'1'中'商品1'的评商品评价提示详情'评价文字要求在200字以内'

    #文字在200以内，成功提交
    When bill完成订单'1'中'商品1'的评价包括'文字与晒图'
    """
        {
            "product_score": "4",
            "review_detail": "商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAFAAoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9F/2sf2ZviFo/x9/ZygX9pz44yL4g+JN7ZqW07win9mgeEvElxviCaGoc/uPL23AmTbKzbfNWOWP6BtP2YvG1taxxv+0V8Y53RArSyab4UDSED7x26KFyevAA9AKKKAP/2Q=="]
        }
    """

    Then bill成功获取个人中心的'待评价'列表
        """
        [{
            "order_no": "2",
            "products": [
                {
                    "product_name": "商品2"
                }
            ]
        }]
        """
    

Scenario: 2 无晒图
    When bill访问jobs的webapp
    And bill完成订单'1'中'商品1'的评价包括'文字与晒图'
    """
        {
            "product_score": "4",
            "review_detail": "商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4"
        }
    """

    Then bill成功获取个人中心的'待评价'列表
        """
        [{
            "order_no": "1",
            "products": [
                {
                    "product_name": "商品1"
                }
            ]
        }, {
            "order_no": "2",
            "products": [
                {
                    "product_name": "商品2"
                }
            ]
        }]
        """


