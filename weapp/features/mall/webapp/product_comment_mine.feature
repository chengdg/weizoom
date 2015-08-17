# __author__ : "benchi"
Feature: bill在webapp中对已到货的商品进行完评价后，在我的评价中，能看到以前自己评价过的内容信息，如果没有评价过商品，则为空
        信息显示顺序是按评价时间的倒序
        显示内容包括：商品名 （有规格的显示规格），评价的时间，评价内容，晒图

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
@mall2 @mall.webapp.comment.aa
Scenario: 1 评价包括文字与晒图
    # bill没有进行购买评价，访问商品评价时，无评价信息
    When bill访问jobs的webapp
    And bill查看'商品评价'
    # 以前名称叫我的评价，后来改为 商品评价
    Then bill成功获取'商品评价'列表
    """
        []
    """

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
    Then bill成功获取'商品评价'列表
        """
        [{
        "review_detail": "商品1还不错！！！！！",
        "product_name": "商品1"
        }]
        """

    When bill完成订单'2'中'商品2'的评价包括'文字'
    """
        {
            "product_score": "4",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "review_detail": "商品2不太好！！！！！！！"
        }
    """
    Then bill成功获取'商品评价'列表
        """
        [{
            "review_detail": "商品2不太好！！！！！！！",
            "product_name":"商品2"
        },{
            "review_detail": "商品1还不错！！！！！",
            "product_name":"商品1"
        }]
        """
