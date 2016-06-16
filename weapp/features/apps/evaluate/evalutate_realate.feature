#_author_许韦 2016.06.08

Feature: jobs给商品添加关联
	1.建立关联后，这些商品的已置顶评价全部取消置顶
	2.这些商品的共用评价，最多可置顶3条
	3.前台某商品的评价中可以看到其他关联商品的已通过评价，评价排序规则仍旧按照评价时间倒序排列
	4.在已连接商品的列表中，展示商品名称、评论数，可进行解除关联的操作

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
    When jobs已添加商品
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
    When jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2",
			"tag_id_3": "分组3"
		}
		"""
	When jobs批量获取微信用户关注
		| member_name   |   attention_time     | member_source |
		| bill 			| 2016-06-06 23:59:59  |    直接关注   |
		| tom 			| 2016-06-06 00:00:00  |    推广扫码   |
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
        	"member":"tom",
        	"status":"已完成",
        	"sources":"本店",
        	"order_price":20.00,
        	"payment_price":20.00,
        	"postage":0.00,
        	"ship_name":"bill",
        	"ship_tel":"13667190229",
        	"ship_area":"北京市,北京市,海淀区",
        	"ship_address":"泰兴大厦",
        	"products":[{
            	"name":"商品2",
            	"price": 20.00,
            	"count": 1
        	}]
    	},{
       		"order_no":"3",
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
            	"name":"商品1",
            	"price": 10.00,
            	"count": 1
        	}]
    	},{
    		"order_no":"4",
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
                "gender":"女"
            }],
            "picture_list": ["1.png","2.jpg"]
        }
        """
    And bill完成订单'4'中'商品2'的评价
        """
        {
            "product_score": "3",
            "answer":[{
                "title":"您使用产品后的感受是",
                "value":"东西马马虎虎"
                }],
            "choose":[{
                "title":"您对本产品的包装是否满意",
                "value":"是"
                }],
            "participate_info":[{
                "name":"bill",
                "gender":""
            }],
            "picture_list": ["3.png","4.jpg"]
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
                "gender":"男"
            }],
            "picture_list": []
        }
        """
    And tom完成订单'3'中'商品1'的评价
        """
        {
            "product_score": "5",
            "answer":[{
                "title":"您使用产品后的感受是",
                "value":"最满意的一次购物！"
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
    Given jobs登录系统
	When jobs已完成对商品的评价信息审核
        """
        [{
            "product_name": "商品2",
            "order_no": "4",
            "member": "bill",
            "status": "通过并置顶"
        },{
            "product_name": "商品1",
            "order_no": "3",
            "member": "tom",
            "status": "通过审核"
        },{
            "product_name": "商品2",
            "order_no": "2",
            "member": "tom",
            "status": "通过并置顶"
        },{
           "member": "bill",
           "order_no": "1",
           "product_name": "商品1",
           "status": "通过并置顶"
        }]
        """

@mall @apps @apps_evaluate @product_evaluate_relate @sun1
Scenario:1 关联商品评论
    When bill访问jobs的webapp
    Then bill能获取'商品1'的更多评价列表
        """
        [{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"商品很好，棒棒哒！"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"bill"
                },{
                    "title":"gender",
                    "value":"女"
                }],
            "picture_list": ["1.png","2.jpg"]               
        },{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"最满意的一次购物！"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"gender",
                    "value":"男"
                }],
            "picture_list": ["5.png"]
        }]
        """
    And bill能获取'商品2'的更多评价列表
        """
        [{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"用完皮肤过敏了~~呜呜呜~~"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"否"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"gender",
                    "value":"男"
                }],
            "picture_list": []
        },{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"东西马马虎虎"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"bill"
                },{
                    "title":"gender",
                    "value":""
                }],
            "picture_list": ["3.png","4.jpg"]
        }]
        """
	Given jobs登录系统
	When jobs设置商品查询条件
		"""
		{
			"product_name":"商品"
		}
		"""
	And jobs成功关联商品评价
		"""
		[{
			"product_name":"商品1",
			"price":10.00,
			"comment":2
		},{
			"product_name":"商品2",
			"price":20.00,
			"comment":2
		}]
		"""
	Then jobs能获得商品评价关联列表
		"""
		[{
			"product_list":{
					"product_name":"商品1"
				},{
					"product_name":"商品2"
				},
			"comment":"4"
		}]
		"""

	When bill访问jobs的webapp
    Then bill能获取'商品1'的更多评价列表
        """
        [{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"最满意的一次购物！"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"gender",
                    "value":"男"
                }],
            "picture_list": ["5.png"]
        },{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"用完皮肤过敏了~~呜呜呜~~"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"否"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"gender",
                    "value":"男"
                }],
            "picture_list": []
        },{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"东西马马虎虎"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"bill"
                },{
                    "title":"gender",
                    "value":""
                }],
            "picture_list": ["3.png","4.jpg"]
        },{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"商品很好，棒棒哒！"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"bill"
                },{
                    "title":"gender",
                    "value":"女"
                }],
            "picture_list": ["1.png","2.jpg"]               
        }]
        """
    Then bill能获取'商品2'的更多评价列表
        """
        [{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"最满意的一次购物！"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"gender",
                    "value":"男"
                }],
            "picture_list": ["5.png"]
        },{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"用完皮肤过敏了~~呜呜呜~~"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"否"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"gender",
                    "value":"男"
                }],
            "picture_list": []
        },{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"东西马马虎虎"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"bill"
                },{
                    "title":"gender",
                    "value":""
                }],
            "picture_list": ["3.png","4.jpg"]
        },{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"商品很好，棒棒哒！"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"bill"
                },{
                    "title":"gender",
                    "value":"女"
                }],
            "picture_list": ["1.png","2.jpg"]               
        }]
        """

@mall @apps @apps_evaluate @product_evaluate_release
Scenario:2 解除商品评论关联
	Given jobs登录系统
	When jobs设置商品查询条件
		"""
		{
			"product_name":"商品"
		}
		"""
	And jobs成功关联商品评价
		"""
		[{
			"product_name":"商品1",
			"price":10.00,
			"comment":2
		},{
			"product_name":"商品2",
			"price":20.00,
			"comment":2
		}]
		"""
    When jobs已完成对商品的评价信息审核
        """
        [{
            "product_name": "商品2",
            "order_no": "2",
            "member": "tom",
            "status": "通过并置顶"
        },{
            "product_name": "商品1",
            "order_no": "3",
            "member": "tom",
            "status": "通过并置顶"
        },{
            "product_name": "商品2",
            "order_no": "4",
            "member": "bill",
            "status": "通过并置顶"
        },{
           "member": "bill",
           "order_no": "1",
           "product_name": "商品1",
           "status": "通过审核"
        }]
        """
    Then bill能获取'商品1'的更多评价列表
        """
        [{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"最满意的一次购物！"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"gender",
                    "value":"男"
                }],
            "picture_list": ["5.png"]
        },{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"用完皮肤过敏了~~呜呜呜~~"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"否"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"gender",
                    "value":"男"
                }],
            "picture_list": []
        },{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"东西马马虎虎"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"bill"
                },{
                    "title":"gender",
                    "value":""
                }],
            "picture_list": ["3.png","4.jpg"]
        },{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"商品很好，棒棒哒！"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"bill"
                },{
                    "title":"gender",
                    "value":"女"
                }],
            "picture_list": ["1.png","2.jpg"]               
        }]
        """
    Then bill能获取'商品2'的更多评价列表
        """
        [{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"最满意的一次购物！"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"gender",
                    "value":"男"
                }],
            "picture_list": ["5.png"]
        },{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"用完皮肤过敏了~~呜呜呜~~"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"否"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"gender",
                    "value":"男"
                }],
            "picture_list": []
        },{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"东西马马虎虎"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"bill"
                },{
                    "title":"gender",
                    "value":""
                }],
            "picture_list": ["3.png","4.jpg"]
        },{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"商品很好，棒棒哒！"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"bill"
                },{
                    "title":"gender",
                    "value":"女"
                }],
            "picture_list": ["1.png","2.jpg"]               
        }]
        """
    When jobs解除商品关联评价
		"""
		[{
			"product_list":{
					"product_name":"商品1"
				},{
					"product_name":"商品2"
				},
			"comment":"4"
		}]
		"""
	Then jobs能获得商品评价关联列表
		"""
		[]
		"""
	When bill访问jobs的webapp
 	Then bill能获得'商品1'的更多评价列表
        """
        [{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"最满意的一次购物！"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"gender",
                    "value":"男"
                }],
            "picture_list": ["5.png"]
        },{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"商品很好，棒棒哒！"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"bill"
                },{
                    "title":"gender",
                    "value":"女"
                }],
            "picture_list": ["1.png","2.jpg"]               
        }]
        """
    And bill能获得'商品2'的更多评价列表
        """
        [{
            "member": "bill",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"东西马马虎虎"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"是"
                },{
                    "title":"name",
                    "value":"bill"
                },{
                    "title":"gender",
                    "value":""
                }],
            "picture_list": ["3.png","4.jpg"]
        },{
            "member": "tom",
            "comments": [{
                    "title":"您使用产品后的感受是",                
                    "value":"用完皮肤过敏了~~呜呜呜~~"
                },{
                    "title":"您对本产品的包装是否满意",
                    "value":"否"
                },{
                    "title":"name",
                    "value":"tom"
                },{
                    "title":"gender",
                    "value":"男"
                }],
            "picture_list": []
        }]
        """