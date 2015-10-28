__author__ = 'zhaolei'
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from datetime import datetime,timedelta
from calendar import monthrange
import mall.models as mall_order
import mall.promotion.models as p_mall_order
class Command(BaseCommand):
     def handle(self, *args, **options):
         delete_orders = mall_order.Order.objects.filter(id__lte=100)
         id2deleteorder = [order.id for order in delete_orders]
         order_id2deleteorder = [order.order_id for order in delete_orders]
         mall_order.OrderOperationLog.objects.filter(order_id__in=order_id2deleteorder).delete()
         mall_order.OrderStatusLog.objects.filter(order_id__in=order_id2deleteorder).delete()
         mall_order.PurchaseDailyStatistics.objects.filter(order_id__in=order_id2deleteorder).delete()
         mall_order.OrderReview.objects.filter(order_id__in=id2deleteorder).delete()
         mall_order.ProductReview.objects.filter(order_id__in =id2deleteorder).delete()
         mall_order.MallOrderFromSharedRecord.objects.filter(order_id__in =id2deleteorder).delete()
         p_mall_order.RedEnvelopeToOrder.objects.filter(order_id__in=id2deleteorder).delete()
         delete_orders.delete()


