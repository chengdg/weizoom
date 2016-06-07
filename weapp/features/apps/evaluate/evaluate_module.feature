# __author__ : "许韦 2016.06.03"

Feature: jobs在weapp中配置自定义评价模板
"""
    自定义评价模板
        1.可以添加单独的问答模块
            问答题模块可输入文本内容
        2.可以添加单独的选择题模块
            选择题模块分为单选、多选2种类型
        3.可以添加单独的参与人信息模块
            参与人信息中除了提供的姓名、手机、邮箱、QQ、职位、住址，还可以添加信息字段，设置是否必填
            提供的信息字段，勾选后在手机端是必填项，手动添加的信息字段，可以设置必填和非必填属性
        4.可以混合添加各个模块
        5.问答、选择题模块可以重复添加，参与人信息模块只能添加一次
"""

@mall @apps @app_evaluate @app_evaluate_template
Scenario:1 配置自定义模板,添加'问答'模块   
    Given jobs登录系统
    When jobs配置商品评论自定义模板
    """
    {
        "type":"customized",
        "answer":
            [{
                "title":"您使用产品后的感受是",
                "is_required":"是"
            },{
                "title":"您对本产品不满意的部分是",
                "is_required":"否"
            }]
    }
    """
    Then jobs能获得商品评价评论模板
    """
    {
        "type":"customized",
        "answer":
            [{
                "title":"您使用产品后的感受是",
                "is_required":"是"
            },{
                "title":"您对本产品不满意的部分是",
                "is_required":"否"
            }]
    }
    """

@mall @apps @app_evaluate @app_evaluate_template
Scenario:2 配置自定义模板,添加'选择题'模块   
    Given jobs登录系统
    When jobs配置商品评论自定义模板
    """
    {
        "type":"customized",
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
            },{
                "title":"您喜欢本产品的哪些口味",
                "type":"多选",
                "is_required":"否",
                 "option":[{
                        "options":"蓝莓"
                    },{
                        "options":"芦荟"
                    },{
                        "options":"原味"
                    }]
            }]
    }
    """
    Then jobs能获得商品评价评论模板
    """
    {
        "type":"customized",
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
            },{
                "title":"您喜欢本产品的哪些口味",
                "type":"多选",
                "is_required":"否",
                 "option":[{
                        "options":"蓝莓"
                    },{
                        "options":"芦荟"
                    },{
                        "options":"原味"
                    }]
            }]
    }
    """

@mall @apps @app_evaluate @app_evaluate_template
Scenario:3 配置自定义模板,添加'参与人信息'模块   
    Given jobs登录系统
    When jobs配置商品评论自定义模板
    """
    {
        "type":"customized",
        "participate_info":
            {
                "items_select":
                    [{
                        "item_name":"姓名",
                        "is_selected":"false"
                    },{
                        "item_name":"手机",
                        "is_selected":"true"
                    },{
                        "item_name":"邮箱",
                        "is_selected":"true"
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
                        "item_name":"填写项1",
                        "is_required":"是"
                    },{
                        "item_name":"填写项2",
                        "is_required":"否"
                    },{
                        "item_name":"填写项3",
                        "is_required":"否"
                    }]
            }
    }
    """
    Then jobs能获得商品评价评论模板
    """
    {
        "type":"customized",
         "participate_info":
            {
                "items_select":
                    [{
                        "item_name":"姓名",
                        "is_selected":"false"
                    },{
                        "item_name":"手机",
                        "is_selected":"true"
                    },{
                        "item_name":"邮箱",
                        "is_selected":"true"
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
                        "item_name":"填写项1",
                        "is_required":"是"
                    },{
                        "item_name":"填写项2",
                        "is_required":"否"
                    },{
                        "item_name":"填写项3",
                        "is_required":"否"
                    }]
            }
    }
    """

@mall @apps @app_evaluate @app_evaluate_template
Scenario:4 配置自定义模板,添加所有模块   
    Given jobs登录系统
    When jobs配置商品评论自定义模板
    """
    {
        "type":"customized",
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
            {
                "items_select":
                    [{
                        "item_name":"姓名",
                        "is_selected":"false"
                    },{
                        "item_name":"手机",
                        "is_selected":"true"
                    },{
                        "item_name":"邮箱",
                        "is_selected":"true"
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
                        "item_name":"填写项1",
                        "is_required":"是"
                    }]
            }
    }
    """
    Then jobs能获得商品评价评论模板
    """
    {
        "type":"customized",
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
            {
                "items_select":
                    [{
                        "item_name":"姓名",
                        "is_selected":"false"
                    },{
                        "item_name":"手机",
                        "is_selected":"true"
                    },{
                        "item_name":"邮箱",
                        "is_selected":"true"
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
                        "item_name":"填写项1",
                        "is_required":"是"
                    }]
            }
    }
    """

@mall @apps @app_evaluate @app_evaluate_template
Scenario:5 配置普通模板
    Given jobs登录系统
    When jobs配置商品评论自定义模板
    """
    {
        "type":"normal"
    }
    """
    Then jobs能获得商品评价评论模板
    """
    {
        "product_score":"5"
        "evaluate": "",    
        "picture_list":[],
        "service_attitude":"5",
        "delivery_speed":"5",
        "logistics_service":"5"
    }
    """