# __author__ : "benchi"
Feature: jobs在后台对已有评价进行审核

1.审核通过：用户评价内容将显示在商品详情页；
2.屏蔽处理：该评价将不被允许显示在商品详情页；
3.通过并置顶：是指审核通过该评论，并且置顶显示该评价；
4.置顶时间为15天，置顶周期结束后，恢复按评价时间倒序显示。
5 同款商品，3个置顶操作，最后置顶的，排在最上面
6.同款商品，最多可置顶3条评价信息，第4条置顶时，第一条置顶信息失去优先级，按原有时间顺序排列
7.设置商品评价送积分，审核通过后，会给用户加相应的积分

Background:

    Given jobs登录系统
    And jobs设定会员积分策略
    """
    {}
    """
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
    And bill完成订单'1'中'商品1'的评价包括'文字与晒图'
    """
        {
            "product_score": "4",
            "review_detail": "1商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAFAAoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9F/2sf2ZviFo/x9/ZygX9pz44yL4g+JN7ZqW07win9mgeEvElxviCaGoc/uPL23AmTbKzbfNWOWP6BtP2YvG1taxxv+0V8Y53RArSyab4UDSED7x26KFyevAA9AKKKAP/2Q=="]
        }
    """
    And bill完成订单'12'中'商品1'的评价包括'文字与晒图'
    """
        {
            "product_score": "4",
            "review_detail": "12商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAFAAoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9F/2sf2ZviFo/x9/ZygX9pz44yL4g+JN7ZqW07win9mgeEvElxviCaGoc/uPL23AmTbKzbfNWOWP6BtP2YvG1taxxv+0V8Y53RArSyab4UDSED7x26KFyevAA9AKKKAP/2Q=="]
        }
    """
    And bill完成订单'13'中'商品1'的评价包括'文字与晒图'
    """
        {
            "product_score": "4",
            "review_detail": "13商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAFAAoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9F/2sf2ZviFo/x9/ZygX9pz44yL4g+JN7ZqW07win9mgeEvElxviCaGoc/uPL23AmTbKzbfNWOWP6BtP2YvG1taxxv+0V8Y53RArSyab4UDSED7x26KFyevAA9AKKKAP/2Q=="]
        }
    """
    And bill完成订单'14'中'商品1'的评价包括'文字与晒图'
    """
        {
            "product_score": "4",
            "review_detail": "14商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAFAAoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9F/2sf2ZviFo/x9/ZygX9pz44yL4g+JN7ZqW07win9mgeEvElxviCaGoc/uPL23AmTbKzbfNWOWP6BtP2YvG1taxxv+0V8Y53RArSyab4UDSED7x26KFyevAA9AKKKAP/2Q=="]
        }
    """
    And bill完成订单'15'中'商品1'的评价包括'文字与晒图'
    """
        {
            "product_score": "4",
            "review_detail": "15商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAFAAoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9F/2sf2ZviFo/x9/ZygX9pz44yL4g+JN7ZqW07win9mgeEvElxviCaGoc/uPL23AmTbKzbfNWOWP6BtP2YvG1taxxv+0V8Y53RArSyab4UDSED7x26KFyevAA9AKKKAP/2Q=="]
        }
    """
    And bill完成订单'16'中'商品1'的评价包括'文字与晒图'
    """
        {
            "product_score": "4",
            "review_detail": "16商品1还不错！！！！！",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "picture_list": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAFAAoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9F/2sf2ZviFo/x9/ZygX9pz44yL4g+JN7ZqW07win9mgeEvElxviCaGoc/uPL23AmTbKzbfNWOWP6BtP2YvG1taxxv+0V8Y53RArSyab4UDSED7x26KFyevAA9AKKKAP/2Q=="]
        }
    """

    And bill完成订单'2'中'商品2'的评价包括'文字'
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
    When tom完成订单'3'中'商品1'的评价包括'文字与晒图'
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
    When tom完成订单'4'中'商品2'的评价包括'文字'
    """
        {
            "product_score": "4",
            "serve_score": "4",
            "deliver_score": "4",
            "process_score": "4",
            "review_detail": "商品2不太好！！！！！！！"
        }
    """



@mall2 @mall.webapp.comment @prm1
Scenario: 1 审核通过：用户评价内容将显示在商品详情页2.屏蔽处理：该评价将不被允许显示在商品详情页3.通过并置顶：是指审核通过该评论，并且置顶显示该评价；

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

    When bill访问jobs的webapp
    #publish：true为bill可以看到，false 为屏蔽，则bill看不到,top为true则置顶，其他按评价时间倒叙排列
    #在详情页只显示两条，信息内容包括，商品名，评价时间，评价内容，注意：置顶
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

@mall2 @mall.webapp.comment @ignore
Scenario: 4置顶时间为15天，置顶周期结束后，恢复按评价时间倒序显示。

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
            "status": "2"
       },{
            "product_name": "商品1",
            "order_no": "12",
            "member": "bill",
            "status": "1"
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

    Given bill关注jobs的公众号
    When bill访问jobs的webapp
    #publish：true为bill可以看到，false 为屏蔽，则bill看不到,top为true则置顶，其他按评价时间倒叙排列
    Then bill在商品详情页成功获取'商品1'的评价列表
    """
    [{
        "member": "bill",
        "review_detail": "1商品1还不错！！！！！"
    },{
        "member": "bill",
        "review_detail": "12商品1还不错！！！！！"
    }]
    """

@mall2 @mall.webapp.comment @prm5
Scenario: 5同款商品，3个置顶操作，最后置顶的，排在最上面
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
            "product_name": "商品1",
            "order_no": "13",
            "member": "bill",
            "status": "2"
       },{
            "product_name": "商品1",
            "order_no": "14",
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

    Given bill关注jobs的公众号
    When bill访问jobs的webapp
    #publish：true为bill可以看到，false 为屏蔽，则bill看不到,top为true则置顶，其他按评价时间倒叙排列
    Then bill在商品详情页成功获取'商品1'的评价列表
    """
    [{
        "member": "bill",
        "review_detail": "14商品1还不错！！！！！"
    },{
        "member": "bill",
        "review_detail": "13商品1还不错！！！！！"
    }]
    """
    When bill在'商品1'的商品详情页点击'更多评价'

    Then bill成功获取'商品1'的商品详情的'更多评价'
    """
    [{
        "member": "bill",
        "review_detail": "14商品1还不错！！！！！"
    },{
        "member": "bill",
        "review_detail": "13商品1还不错！！！！！"
    },{
        "member": "bill",
        "review_detail": "12商品1还不错！！！！！"
    },{
        "member": "bill",
        "review_detail": "1商品1还不错！！！！！"
    }]

    """
@mall2 @mall.webapp.comment @prm6
Scenario: 6.同款商品，最多可置顶3条评价信息，第4条置顶时，第一条置顶信息失去优先级，按原有时间顺序排列
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
            "status": "2"
       },{
            "product_name": "商品1",
            "order_no": "12",
            "member": "bill",
            "status": "2"
       },{
            "product_name": "商品1",
            "order_no": "13",
            "member": "bill",
            "status": "2"
       },{
            "product_name": "商品1",
            "order_no": "14",
            "member": "bill",
            "status": "2"
       },{
            "product_name": "商品1",
            "order_no": "15",
            "member": "bill",
            "status": "1"
       },{
            "product_name": "商品1",
            "order_no": "16",
            "member": "bill",
            "status": "1"
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
    Given bill关注jobs的公众号
    When bill访问jobs的webapp
    #publish：true为bill可以看到，false 为屏蔽，则bill看不到,top为true则置顶，其他按评价时间倒叙排列

    And bill在'商品1'的商品详情页点击'更多评价'

    Then bill成功获取'商品1'的商品详情的'更多评价'
    """
    [{
        "member": "bill",
        "review_detail": "14商品1还不错！！！！！"
    },{
        "member": "bill",
        "review_detail": "13商品1还不错！！！！！"
    },{
        "member": "bill",
        "review_detail": "12商品1还不错！！！！！"
    },{
        "member": "bill",
        "review_detail": "16商品1还不错！！！！！"
    },{
        "member": "bill",
        "review_detail": "15商品1还不错！！！！！"
    },{
        "member": "bill",
        "review_detail": "1商品1还不错！！！！！"
    }]
    """

#后续补充.雪静
@mall2 @mall.webapp.comment @prm7
Scenario: 7.jobs通过审核评价，给用户加积分
    tom评价jobs的商品，jobs通过审核，给tom加相应的积分

    When tom访问jobs的webapp
    Then tom在jobs的webapp中获得积分日志
        """
        [{
            "content": "首次关注",
            "integral": 20
        }]
        """
    Given jobs登录系统
    And jobs设置积分策略
        """
        [{
            "review_increase": 20
        }]
        """
    When jobs已完成对商品的评价信息审核
    """
        [{
            "product_name": "商品1",
            "order_no": "3",
            "member": "tom",
            "status": "1"
       }]
        """
    When tom访问jobs的webapp
    Then tom在jobs的webapp中获得积分日志
        """
        [{
            "content": "商品评价奖励",
            "integral": 20
        },{
            "content": "首次关注",
            "integral": 20
        }]
        """
