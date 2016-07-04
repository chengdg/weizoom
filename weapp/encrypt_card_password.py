# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)
from mall.module_api import encrypt_msg
from mall.promotion.models import MemberHasWeizoomCard


print('----start...')

cards = MemberHasWeizoomCard.objects.all()

for card in cards:
	if len(card.card_password) < 10:
		card.card_password = encrypt_msg(card.card_password)

		card.save()
	print('**card_number:{},card_password:{}'.format(card.card_number,card.card_password))
print('end...')
