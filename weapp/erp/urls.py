# -*- coding: utf-8 -*-

from django.conf.urls import *

import api_views
import order_api_views
import product_api_views

urlpatterns = patterns('',
    (r'^api/members/get/$', api_views.get_members),
    (r'^api/member/get/$', api_views.get_member),

    (r'^api/orders/get/$', order_api_views.get_orders),
    (r'^api/order/get/$', order_api_views.get_order),

    (r'^api/products/get/$', product_api_views.get_products),
    (r'^api/product/get/$', product_api_views.get_product),
    (r'^api/order_express_info/create/$', order_api_views.create_order_express_info),
    (r'^api/product_stock/update/$', order_api_views.update_product_stock),
)