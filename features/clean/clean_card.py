# -*- coding: utf-8 -*-
import logging

from card import models as card_models

def clean():
	logging.info('clean database for outline app')
	card_models.WeizoomCardRule.objects.all().delete()
	card_models.WeizoomCard.objects.all().delete()
