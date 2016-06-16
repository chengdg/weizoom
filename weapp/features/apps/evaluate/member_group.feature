#author 许韦:2016.06.08
Feature: 管理员在审核评价页面调整会员分组

Background:
	Given jobs登录系统
    And jobs已添加商品
   		"""
   		[{
    		"name":"商品1",
    		"price":10.00
    	},{
    		"name":"商品2",
    		"price":20.00
    	}]
   		"""
#    When jobs添加会员等级
#		"""
#		[{
#			"name": "银牌会员",
#			"upgrade": "手动升级",
#			"discount": "10"
#		},{
#			"name": "金牌会员",
#			"upgrade": "手动升级",
#			"discount": "9"
#		}]
#		"""
    And jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2",
			"tag_id_3": "分组3"
		}
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
                    "items_select":
                        [{
                            "item_name":"手机",
                            "is_selected":"true"
                        },{
                            "item_name":"姓名",
                            "is_selected":"true"
                        }],
                    "items_add":
                        [{
                            "item_name":"职称",
                            "is_required":"否"
                        }]
                }]
        }
        """
    When 清空浏览器
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
   	 	}]
    	"""
    When 清空浏览器
    Given tom关注jobs的公众号
    And jobs已有的订单
        """
        [{
            "order_no":"2",
            "member":"tom",
            "status":"已完成",
            "sources":"本店",
            "order_price":20.00,
            "payment_price":20.00,
            "postage":0.00,
            "ship_name":"tom",
            "ship_tel":"13667190229",
            "ship_area":"北京市,北京市,海淀区",
            "ship_address":"泰兴大厦",
            "products":[{
                "name":"商品2",
                "price": 20.00,
                "count": 1
            }]
        }]
        """
    When 清空浏览器
    When bill访问jobs的webapp
   	And bill完成订单'1'中'商品1'的评价
        """
        {
            "product_score": "5",
            "answer":[{
                "title":"您使用产品后的感受是",
                "value":"商品很好，棒棒哒！"
                }],
            "choose":[{
                "title":"您对本产品的包装是否满意",
                "value":"是"
                }],
            "participate_info":[{
                "name":"bill",
                "tel":"13013013011",
                "title":"工程师"
            }],
            "picture_list": ["1.png","2.jpg"]
        }
        """
    When 清空浏览器
    When tom访问jobs的webapp
    And tom完成订单'2'中'商品2'的评价
        """
        {
             "product_score": "2",
            "answer":[{
                "title":"您使用产品后的感受是",
                "value":"用完皮肤过敏了~~呜呜呜~~"
                }],
            "choose":[{
                "title":"您对本产品的包装是否满意",
                "value":"否"
                }],
            "participate_info":[{
                "name":"tom",
                "tel":"13013013058",
                "title":"设计师"
            }],
            "picture_list": []
        }
        """

@mall @apps @apps_evaluate @evaluate_detail_member_group
Scenario:1 jobs登录系统，在商品评价详情页面给会员调分组
	Given jobs登录系统
    Then jobs能获得订单"2"中的"商品2"评价详情
        """
        {
            "product_name": "商品2",
            "order_no": "2",
            "member": "tom",
            "member_rank":"普通会员",
            "tags":["未分组"],
            "product_score":"2",
            "comments":[{
                    "title":"您使用产品后的感受是",
                    "value":"用完皮肤过敏了~~呜呜呜~~"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"否"
                },{
                    "title":"tel",
                    "value":"13013013058"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"title",
                    "value":"设计师"
                }],
            "picture_list":[]
        }
        """
    When jobs给"tom"调分组
		"""
		["分组2","分组3"]
		"""
    Then jobs能获得订单"2"中的"商品2"评价详情
        """
        {
            "product_name": "商品2",
            "order_no": "2",
            "member": "tom",
            "member_rank":"普通会员",
            "tags":["分组2","分组3"],
            "product_score":"2",
            "comments":[{
                    "title":"您使用产品后的感受是",
                    "value":"用完皮肤过敏了~~呜呜呜~~"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"否"
                },{
                    "title":"tel",
                    "value":"13013013058"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"title",
                    "value":"设计师"
                }],
            "picture_list":[]
        }
        """
	Then jobs可以获得会员列表
        | name  |      tags     |
        | tom   |   分组2,分组3 |
        | bill  |     未分组    |
