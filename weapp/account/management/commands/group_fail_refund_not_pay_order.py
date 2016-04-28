#coding:utf8
"""
将团购失败未退款的订单退款
"""
from datetime import datetime, timedelta
import time
import logging

from django.core.management.base import BaseCommand, CommandError

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning

from mall import models as mall_models
from account.models import UserProfile
from mall.order.util import update_order_status_by_group_status

class Command(BaseCommand):
    help = "group fail refund not pay order"
    args = ''

    def handle(self, **options):
        """
        将团购失败未退款的订单退款
        """

        relations = mall_models.OrderHasGroup.objects.filter(
                    group_status=mall_models.GROUP_STATUS_failure
                )

        order_ids = [r.order_id for r in relations]

        orders = mall_models.Order.objects.filter(order_id__in=order_ids, status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP)

        refund_order_ids = [order.order_id for order in orders]
        if refund_order_ids:
            update_order_status_by_group_status(order_ids=refund_order_ids)

        print 'success'