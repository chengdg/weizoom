# -*- coding: utf-8 -*-

import time

import datetime
from django.core.management.base import BaseCommand, CommandError
from market_tools.tools.distribution.models import ChannelDistributionQrcodeSettings, ChannelDistributionQrcodeHasMember, \
                                                    ChannelDistributionDetail, ChannelDistributionFinish
from mall.models import Order
from django.db.models import F

class Command(BaseCommand):
    """
    微信用户下单后, 更新二维码绑定用户收到的佣金

    """
    def __init__(self):
        # start_datetime = '2016-8-5 17:12'
        start_datetime = datetime.datetime.now() - datetime.timedelta(days=11)  # 只处理11天之前的数据
        self.start_time = start_datetime
        super(Command , self).__init__()

    help = ''
    args = ''

    def handle(self, *args, **options):
        # 所有的绑过的{memberid: qrcode_id}
        members_dict = {}
        members = ChannelDistributionQrcodeHasMember.objects.all()
        for member in members:
            members_dict[member.id] = member.channel_qrcode_id

        # 取出所有的订单
        orders = Order.objects.filter(created_at__gt=self.start_time, status=5)  # 搜索大于启动时间, 并已完成的订单

        finish_order_list = []  # 从数据库取出所有结算过的信息
        finish_orders = ChannelDistributionFinish.objects.all()
        for finish_order in finish_orders:
            finish_order_list.append(finish_order.order_id)

        qrcodes_dict = {}  # 所有渠道分销二维码信息 {qrcode_id: qrcode}
        qrcodes = ChannelDistributionQrcodeSettings.objects.all()
        for qrcode in qrcodes:
            qrcodes_dict[qrcode.id] = qrcode
        for order in orders:

            # 如果此订单的购买者之前绑过渠道分销二维码
            if members_dict.has_key(order.webapp_user_id) and  order.id not in finish_order_list:
                # qrcode = ChannelDistributionQrcodeSettings.objects.filter(id=members_dict[order.webapp_user_id])
                order_qrcode = qrcodes_dict[members_dict[order.webapp_user_id]]  # 此订单会员绑定的二维码
                conform_minimun_return_rate = True if order.final_price /order.product_price > order_qrcode.minimun_return_rate / 100.0 else False  # 满足最低返现折扣

                if order_qrcode.distribution_rewards and conform_minimun_return_rate:  # 如果返佣金
                    if order_qrcode.return_standard:  # 有返回天数限制
                        if order.created_at > datetime.datetime.now() - datetime.timedelta(days=order_qrcode.return_standard):
                            return None

                    ChannelDistributionQrcodeHasMember.filter(id=order.webapp_user_id).update(
                        cost_money = F('cost_money') + order.final_price,
                        buy_times = F('buy_times') + 1,
                        commission = F('commission') + order.final_price * order_qrcode.commission_rate
                    )
                    ChannelDistributionQrcodeSettings.objects.filter(id=order_qrcode.id).update(
                        will_return_reward = F('will_return_reward') + order.final_price * order_qrcode.commission_rate,
                        total_transaction_volume = F('total_transaction_volume') + order.final_price,
                        total_return = F('total_return') + order.final_price * order_qrcode.commission_rate,
                   
                    )
                    ChannelDistributionDetail.objects.create(
                        money = order.final_price * order_qrcode.commission_rate,
                        member_id = order_qrcode.bing_member_id,
                        order_id = order.id
                    )
                    ChannelDistributionFinish.objects.create(
                        order_id = order.id,
                        order_time = order.created_at
                    )
                    print u'订单号%s已处理'% order.id

            else:  # 没有绑定过不处理
                pass
