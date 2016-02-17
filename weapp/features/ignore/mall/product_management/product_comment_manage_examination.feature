#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
# __author__ : "benchi"
# __author__ : "冯雪静"
Feature: jobs在后台对已有评价进行审核
"""
    1.审核通过：用户评价内容将显示在商品详情页；
    2.屏蔽处理：该评价将不被允许显示在商品详情页；
    3.通过并置顶：是指审核通过该评论，并且置顶显示该评价；
    4.置顶时间为15天，置顶周期结束后，恢复按评价时间倒序显示。
    5 同款商品，3个置顶操作，最后置顶的，排在最上面
    6.同款商品，最多可置顶3条评价信息，第4条置顶时，第一条置顶信息失去优先级，按原有时间顺序排列
    7.设置商品评价送积分，审核通过后，会给用户加相应的积分
"""

#后续修改.雪静
@mall2 @mall.webapp.comment @ignore
Scenario: 4置顶时间为15天，置顶周期结束后，恢复按评价时间倒序显示。

    Given jobs登录系统
    When jobs已完成对商品的评价信息审核
        """
        [{
            "product_name": "商品2",
            "order_no": "4",
            "member": "tom",
            "status": "-1",
            "time": "3天前"
        },{
            "product_name": "商品1",
            "order_no": "3",
            "member": "tom",
            "status": "1",
            "time": "4天前"
        },{
            "product_name": "商品2",
            "order_no": "2",
            "member": "bill",
            "status": "-1",
            "time": "5天前"
        },{
            "product_name": "商品1",
            "order_no": "16",
            "member": "bill",
            "status": "-1",
            "time": "6天前"
        },{
            "product_name": "商品1",
            "order_no": "15",
            "member": "bill",
            "status": "-1",
            "time": "7天前"
        },{
            "product_name": "商品1",
            "order_no": "14",
            "member": "bill",
            "status": "1",
            "time": "8天前"
        },{
            "product_name": "商品1",
            "order_no": "13",
            "member": "bill",
            "status": "-1",
            "time": "9天前"
        },{
            "product_name": "商品1",
            "order_no": "1",
            "member": "bill",
            "status": "2",
            "time": "10天前"
        },{
            "product_name": "商品1",
            "order_no": "12",
            "member": "bill",
            "status": "2",
            "time": "15天前"
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
            "member": "tom",
            "review_detail": "商品1还不错！！！！！"
        }]
        """
       