# -*- coding: utf-8 -*-
from django.dispatch import Signal

#
# 订单保存
#
#保存订单时，检查订单相关资源的signal
check_order_related_resource = Signal(providing_args=["order", "args"])

#保存订单时，消费订单相关资源的signal
consume_order_related_resource = Signal(providing_args=["order", "args"])

#完成订单保存后的signal
post_save_order = Signal(providing_args=["order"])





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