# -*- coding: utf-8 -*-
import json
import time
from behave import when, then
from test import bdd_util


@when(u"{webapp_user}查看'{text}'")
def step_visit_product_review(context, webapp_user, text):
    pass


@then(u"{webapp_user}成功获取'{text}'列表")
def step_product_review_should(context, webapp_user, text):
    url = "/workbench/jqm/preview/?woid=%d&module=mall&model=product_review_list&action=get&member_id=%d" % (context.webapp_owner_id, context.member.id)
    response = context.client.get(bdd_util.nginx(url), follow=True)
    # 期望的输出
    expected = json.loads(context.text)
    # 实际的输出
    actual = []
    product_review_list = response.context['product_review_list']
    for i in product_review_list:
        product_review = {}
        product_review['review_detail'] = i.review_detail
        product_review['product_name'] = i.product.name
        actual.append(product_review)
    print("-"*10, 'actual', "-"*10, actual)
    print("-"*10, 'expected', "-"*10, expected)
    bdd_util.assert_list(expected, actual)


@when(u"{webapp_user}完成订单'{order_code}'中'{product_name}'的评价包括'{has_picture}'")
def step_finished_a_product_review(context, webapp_user, order_code, product_name, has_picture):
    url = '/webapp/api/project_api/call/'
    order_has_product = bdd_util.get_order_has_product(order_code, product_name)
    # 输入
    data = {}
    context_dict = json.loads(context.text)
    data.update(context_dict)
    data['target_api'] = 'product_review/create'
    data['module'] = 'mall'
    data['woid'] = context.webapp_owner_id
    data['order_id'] = order_has_product.order_id
    data['product_id'] = order_has_product.product_id
    data['order_has_product_id'] = order_has_product.id
    has_picture = context_dict.get('picture_list', None)
    if has_picture:
        data['picture_list'] = str(has_picture)

    context.client.post(url, data)


@when(u"{webapp_owner}已获取对商品的评价信息")
def step_jobs(context, webapp_owner):
    pass


# @when(u"{webapp_owner}已完成对商品的评价信息审核")
# def step_webapp_owner_verified_review(context, webapp_owner):
#     """
#      [{
#         "member": "tom",
#         "status": "-1",  -> ('-1', '已屏蔽'),  ('0', '待审核'),  ('1', '已通过'),  ('2', '通过并置顶')
#         "product_name": "商品1",
#         "order_no": "3"
#     }, {
#         "member": "bill",
#         "status": "1",
#         "product_name": "商品1",
#         "order_no": "1"
#     }]
#
#
#     """
#     url = '/mall2/api/product_review/?design_mode=0&version=1'
#     context_dict = json.loads(context.text)
#     for i in context_dict:
#         product_name = i.get('product_name')
#         order_code = i.get('order_no')
#         product_review = bdd_util.get_product_review(order_code, product_name)
#         args = {
#             "product_review_id": product_review.id,
#             "status": i.get("status")
#         }
#         context.client.post(url, args)


@when(u"{webapp_user}在商城首页点击'{product_name}'的链接")
def step_click_product(context, webapp_user, product_name):
    pass


@then(u"{webapp_user}在商品详情页成功获取'{product_name}'的评价列表")
def step_webapp_user_get_product_review(context, webapp_user, product_name):
    product = bdd_util.get_product_by(product_name)
    expected = json.loads(context.text)
    url = "/workbench/jqm/preview/?woid=%d&module=mall&model=product&rid=%d" % (context.webapp_owner_id, product.id)
    response = context.client.get(bdd_util.nginx(url), follow=True)
    product_review_list = response.context['product']['product_review']
    actual = []
    if product_review_list:
        for i in product_review_list:
            data = {}
            data['member'] = i.member_name
            data['review_detail'] = i.review_detail
            actual.append(data)
    else:
        actual.append({})
    bdd_util.assert_list(expected, actual)


@when(u"{webapp_user}在'{product_name}'的商品详情页点击'更多评价'")
def step_click_more(context, webapp_user, product_name):
    pass


@then(u"{webapp_user}成功获取'{product_name}'的商品详情的'更多评价'")
def step_get_more(context, webapp_user, product_name):
    expected = json.loads(context.text)
    product = bdd_util.get_product_by(product_name)
    url = "/workbench/jqm/preview/?woid=%d&module=mall&model=product_review_list&action=get&product_id=%d" % (context.webapp_owner_id, product.id)
    response = context.client.get(bdd_util.nginx(url), follow=True)
    product_review_list = response.context['product_review_list']
    actual = []
    for i in product_review_list:
        data = {}
        data['member'] = i.member_name
        data['review_detail'] = i.review_detail
        actual.append(data)
    bdd_util.assert_list(expected, actual)


@then(u"{webapp_user}成功获取个人中心的'待评价'列表")
def step_get_presonal_review_list(context, webapp_user):
    expected = json.loads(context.text)
    url = "/workbench/jqm/preview/?woid=%d&module=mall&model=order_review_list&action=get" % context.webapp_owner_id
    response = context.client.get(bdd_util.nginx(url), follow=True)
    orders = response.context['orders']
    actual = []
    if orders:
        for order in orders:
            if not order.order_is_reviewed:
                data = {}
                data['order_no'] = order.order_id
                data['products'] = []
                for product in order.products:
                    p_data = {}
                    p_data['product_name'] = product.name
                    p_model_name = product.product_model_name
                    if p_model_name:
                        the_model_name = ""
                        for model in p_model_name:
                            the_model_name += model['property_value']
                        p_data['product_model_name'] = the_model_name
                    data['products'].append(p_data)
                actual.append(data)
    else:
        actual.append({})
    if not actual:
        actual.append({})
    bdd_util.assert_list(expected, actual)


@then(u"{webapp_user}成功获取商品评价后'感谢评价'页面")
def step_get_user_thanks_page(context, webapp_user):
    from webapp.modules.mall.request_api_util import get_review_status
    expected = json.loads(context.text)
    orders_is_finish = get_review_status(context)
    actual = []
    if not orders_is_finish:
        actual.append({
            "title1": "继续评价",
            "title2": "返回首页"})
    else:
        actual.append({
            "title2": "返回首页"
        })
    bdd_util.assert_list(expected, actual)


@then(u"订单'{order_no}'中'{product_name}'的评商品评价提示信息'{review_status}'")
def step_get_user_publish_review(context, order_no, product_name, review_status):
    product_review = bdd_util.get_product_review(order_no, product_name)
    count = len(product_review.review_detail)
    assert count > 200


# @then(u"订单'1'中'商品1'的评商品评价提示详情'评价文字要求在200字以内'")
# def step_get_user_publish_review_error_detail(context):
#     pass
