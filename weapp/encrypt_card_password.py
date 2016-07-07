# -*- coding: utf-8 -*-
import sys


reload(sys)
sys.setdefaultencoding("utf-8")
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)
from mall.module_api import encrypt_msg
from mall.promotion.models import MemberHasWeizoomCard, VirtualProductHasCode
from mall.promotion.virtual_product import encrypt_password

from apps.models import AppsWeizoomCard

print('----MemberHasWeizoomCard start...')

cards = MemberHasWeizoomCard.objects.all()

for card in cards:
	if len(card.card_password) < 10:
		card.card_password = encrypt_msg(card.card_password)

		card.save()
	print('**card_number:{},card_password:{}'.format(card.card_number,card.card_password))
print('MemberHasWeizoomCard end...')


print('----VirtualProductHasCode start...')
vproducts = VirtualProductHasCode.objects.all()

for vproduct in vproducts:
	if len(vproduct.password) < 10:
		vproduct.password = encrypt_password(vproduct.password)
		vproduct.save()

print('VirtualProductHasCode end...')

print('----AppsWeizoomCard start...')
for single_card in AppsWeizoomCard.objects.all():
	ps = single_card.weizoom_card_password
	if len(ps) < 10:
		single_card.weizoom_card_password = encrypt_password(ps)
		single_card.save()

print('----AppsWeizoomCard end...')


print('-------all end---------')