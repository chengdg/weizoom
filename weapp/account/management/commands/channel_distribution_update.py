# -*- coding: utf-8 -*-

import time
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from market_tools.tools.distribution.models import ChannelDistributionQrcodeSettings, ChannelDistributionQrcodeHasMember
from mall.models import Order

class Command(BaseCommand):
    """
    微信用户下单后, 更新二维码绑定用户收到的佣金

    """
    def __init__(self):
        start_datetime = '2016-8-5 17:12'
        now = datetime.datetime.now()
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
        qrcodes = ChannelDistributionQrcodeSettings.objects.all()
        for order in orders:
            # if order.
            # 如果此订单的购买者之前绑过渠道分销二维码
            if members_dict.has_key(order.webapp_user_id) :
                qrcode = ChannelDistributionQrcodeSettings.objects.filter(id=members_dict[order.webapp_user_id])
                if qrcode[0].return_standard:  # 有返回天数限制
                    pass
                pass
