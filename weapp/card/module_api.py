# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
from market_tools.tools.weizoom_card.models import *

#############################################################################
# create_weizoom_card_log: 创建微众卡日志
#############################################################################
def create_weizoom_card_log(owner_id, order_id, event_type, card_id, money, member_integral_log_id=0):
    try:        
        if money != 0:          
            if event_type in TYPE_ZERO:
                money = 0

            WeizoomCardHasOrder.objects.create(     
                owner_id = owner_id,
                card_id = card_id,
                order_id = order_id,
                money = money,
                event_type = event_type,
                member_integral_log_id = member_integral_log_id
            )
    except:
        notify_msg = u"创建微众卡日志失败, card_id={},order_id={},event_type={}, money={}, cause:\n{}".format(card_id,order_id,event_type, money, unicode_full_stack())
        watchdog_alert(notify_msg)
