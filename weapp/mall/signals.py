# -*- coding: utf-8 -*-
from django.dispatch import Signal

#
# 订单保存
#
#保存订单前，检查订单相关资源的signal
check_order_related_resource = Signal(providing_args=["pre_order", "args", "request"])

#
# 购物车结算
#
#购物车结算前，检查相关商品的signal
check_pre_order_related_resource = Signal(providing_args=["pre_order", "args", "request"])

#保存订单时，消费订单相关资源的signal
consume_order_related_resource = Signal(providing_args=["order", "args"])

#保存订单前扣除相应资源
pre_save_order = Signal(providing_args=["order"])
#完成订单保存后的signal
post_save_order = Signal(providing_args=["order"])





# 向快递100发送订阅请求
post_ship_send_request_to_kuaidi = Signal(providing_args=["order"])

post_ship_order = Signal(providing_args=["order"])

post_pay_order = Signal(providing_args=["order"])

#更新product model property后发送的signal
post_update_product_model_property = Signal(providing_args=['model_property', 'request']) 

#删除product model property前发送的signal
pre_delete_product_model_property = Signal(providing_args=['model_property', 'request']) 

#创建delivery类型的product
create_delivery_product = Signal(providing_args=['delivery_plan'])

#取消订单后发送的signal
cancel_order = Signal(providing_args=['order'])

#商品不再处于上架状态的signal
products_not_online = Signal(providing_args=['product_ids', 'request'])