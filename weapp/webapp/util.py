# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil

from models import *
from watchdog.utils import watchdog_debug

########################################################################
# concern_shop_log: 记录点击关注店铺
########################################################################
def concern_shop_log(webapp_user_id, from_webapp_id, to_webapp_id, redirect_url, product_id):
	try:		
		WebappUserClickConcernShopLog.objects.create(
			webapp_user_id = webapp_user_id,
			from_webapp_id = from_webapp_id,
			to_webapp_id = to_webapp_id,
			redirect_url = redirect_url,
			product_id = product_id
		)
	except:
		pass