# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
try:
    import Image
except:
    from PIL import Image

from django.template import Context, RequestContext
from django.conf import settings

from models import *
from core.jsonresponse import create_response, JsonResponse
import pagestore as pagestore_manager


product_page_id = '0'
category_page_id = '0'


######################################################################
# example_api: API参考示例
######################################################################
def example_api(request):
	pagestore = pagestore_manager.get_pagestore(request)

	data = {
		'product_list': {
			'data_groups': [{
				'datas': []
			}]
		},
		'product_image': {'image': ''},
	}
	return data