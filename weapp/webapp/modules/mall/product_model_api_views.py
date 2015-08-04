# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import MySQLdb
import random
import string

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count

from core.jsonresponse import JsonResponse, create_response
from core import paginator
from core.dateutil import get_today

from excel_response import ExcelResponse

from account.models import *
from models import *


########################################################################
# get_product_model_properties: 获得所有的product model property
########################################################################
@login_required
def get_product_model_properties(request):
	properties = []
	for property in ProductModelProperty.objects.filter(owner=request.user, is_deleted=False):
		values = []
		for value in ProductModelPropertyValue.objects.filter(property=property, is_deleted=False):
			values.append({
				"id": value.id,
				"name": value.name,
				"image": value.pic_url
			})

		properties.append({
			"id": property.id,
			"name": property.name,
			"type": "text" if property.type == PRODUCT_MODEL_PROPERTY_TYPE_TEXT else "image",
			"values": values
		})

	response = create_response(200)
	response.data = properties
	return response.get_response()
