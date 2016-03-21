#coding:utf8
"""
@package services.cancel_not_pay_order_service.tasks
取消超时的未付款订单的service
"""
from datetime import datetime, timedelta
import time
import logging

from django.conf import settings
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_info

from mall.promotion import models as promotion_models
from mall import models as mall_models
from account.models import UserProfile
from mall.module_api import update_order_status

from celery import task


@task
def cancel_not_pay_order_timeout(request, args):
    """
    取消超时的未付款订单
    """
    user2webapp_id = dict([(user_profile.user, user_profile.webapp_id)for user_profile in UserProfile.objects.filter(is_active=True)])
    users = user2webapp_id.keys()
    webapp_id2user = {}
    for k, v in user2webapp_id.items():
        webapp_id2user[v] = k

    user2order_expired_hour = dict([(config.owner_id, config.order_expired_day)for config in mall_models.MallConfig.objects.filter(owner__in=users)])
    webapp_id2expired_time = {}
    for user in users:
        user_id = user.id
        if user not in user2webapp_id.keys() or user_id not in user2order_expired_hour.keys():
            continue
        webapp_id = user2webapp_id[user]
        expired_hour = user2order_expired_hour[user_id]
        if expired_hour:
            expired_time = datetime.now() - timedelta(hours=expired_hour)
            webapp_id2expired_time[webapp_id] = expired_time
        else:
            webapp_id2expired_time[webapp_id] = 0

    orders = mall_models.Order.objects.filter(status=mall_models.ORDER_STATUS_NOT)
    need_cancel_orders = []
    for order in orders:
        if webapp_id2expired_time.get(order.webapp_id, None) == None:
            try:
                user = UserProfile.objects.get(webapp_id=order.webapp_id).user
            except:
                logging.info(u"订单所属用户已不存在！")
                watchdog_info(u"订单所属用户已不存在！", type="mall")
                continue
            update_order_status(user, 'cancel', order)
            logging.info(u"订单所属用户已失效！并将其订单自动取消。(order_id=%s, webapp_id=%s)" % (order.order_id, order.webapp_id))
            watchdog_info(u"订单所属用户已失效！并将其订单自动取消。(order_id=%s, webapp_id=%s)" \
                % (order.order_id, order.webapp_id), type="mall")
        elif webapp_id2expired_time[order.webapp_id] and order.created_at < webapp_id2expired_time[order.webapp_id]:
            need_cancel_orders.append(order)

        if len(need_cancel_orders) > 50:
            break
    for order in need_cancel_orders:
        update_order_status(webapp_id2user[order.webapp_id], 'cancel', order)
        logging.info(u"user webapp_id:%s order %s cancel success" % (order.webapp_id, order.order_id))

    logging.info(u"cancel order total count %d" % len(need_cancel_orders))
    return "OK cancel order length is %s" % len(need_cancel_orders)