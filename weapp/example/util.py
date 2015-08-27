# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
import shutil
try:
    import Image
except:
    from PIL import Image
import copy

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.db import models

from models import *
from core.jsonresponse import create_response, JsonResponse

def convert_models(models):
	if len(models) == 0:
		return {
			'type': 'string',
			'value': 'empty list: []'
		}

	first_model = models[0]

	result = {
		'type':'table',
		'headers': [],
		'rows': []
	}

	if isinstance(first_model, dict):
		for field in first_model:
			result['headers'].append(field)

		for model in models:
			row = []
			for field in first_model:
				row.append(str(model[field]))
			result['rows'].append(row)
	elif isinstance(first_model, tuple):
		for index in range(len(first_model)):
			result['headers'].append('tuple(%d)' % index)

		for model in models:
			result['rows'].append(model)
	else:
		for field in first_model._meta.fields:
			result['headers'].append(field.name)

		for model in models:
			row = []
			for field in first_model._meta.fields:
				row.append(str(field.value_from_object(model)))
			result['rows'].append(row)

	return result


def convert_code_result(data):
	if isinstance(data, models.Model):
		return convert_models([data])
	elif isinstance(data, models.query.QuerySet):
		data = list(data)
		return convert_models(data)
	elif isinstance(data, list):
		if isinstance(data[0], models.Model):
			return convert_models(data)
		else:
			return data
	else:
		return {
			'type': 'string',
			'value': str(data)
		}

