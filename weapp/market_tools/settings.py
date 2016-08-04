# -*- coding: utf-8 -*-

#本变量定义营销工具的显示顺序
TOOLS = [
    'coupon',
    'lottery',
    'vote',
    'activity',
    'complain',
    'member_qrcode',
    'channel_qrcode',
    'research',
    'red_envelope',
    'point_card',
    'delivery_plan',
    'store',
    'template_message',
    'card_exchange',
    'distribution'

]

TOOLS_ORDERING = {}

i = 0
for tool in TOOLS:
    i += 1
    TOOLS_ORDERING[tool] = i