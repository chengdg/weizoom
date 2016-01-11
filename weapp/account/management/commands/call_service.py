# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from mall.models import Product, ProductSwipeImage

from webapp.models import GlobalNavbar, Workspace

class Command(BaseCommand):
	help = "call service"
	args = ''
	
	def handle(self, **options):
		from webapp.handlers import event_handler_util
		event_data = {'id': 0}
		event_handler_util.handle(event_data, 'finish_promotion')

