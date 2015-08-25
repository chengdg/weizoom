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

from models import *
from core.jsonresponse import create_response, JsonResponse

def _exec_filter():
	product = Product.objects.get(name='product_1')
	return Order.objects.filter(product=product)


def _exec_exclude():
	'''
	exclude将转化为SQL中的 WHERE NOT(...)语句
	'''
	return Product.objects.exclude(name='product_1').exclude(count=2)

def _exec_order_by():
	'''
	order_by将转化为SQL中的ORDER BY语句
	'''
	return Product.objects.all().order_by('-count')

def _exec_reverse():
	'''
	reverse将逆转QuerySet中的排序标准
	'''
	return Product.objects.all().order_by('-count').reverse()

def _exec_distinct():
	'''
	distinct将产生SELECT DISTINCT语句
	'''
	return Order.objects.distinct()

def _exec_values():
	'''
	values将返回产生dict序列的ValuesQuerySet
	'''
	return Product.objects.values('id', 'name', 'detail')


def _exec_values_list():
	'''
	values将返回产生tuple序列的ValuesListQuerySet
	'''
	return Product.objects.values_list('id', 'name', 'detail')


def _exec_select_related():
	'''
	直接产生INNER JOIN连接两个表获取数据的SQL方案，
	相比以下代码而言，更好的解决方案
	orders = Order.objects.all()[:6]
	products = []
	for order in orders:
		products.append(order.product)
	'''
	orders = Order.objects.select_related('product').all()[:6]
	products = []
	for order in orders:
		products.append(order.product)
	return products


def _exec_none():
	'''
	none将不获取任何数据
	'''
	return Product.objects.none()

def _exec_all():
	'''
	all将获取全部数据
	'''
	return Product.objects.all()


def _exec_extra():
	'''
	在生成的SQL语句中插入指定的SQL片段
	'''
	return Product.objects.extra(where=["count > 2", "count < 5"])


def _exec_defer():
	'''
	延迟加载（在访问model.field时）数据库中的数据
	'''
	return Product.objects.defer('detail')


def _exec_only():
	'''
	延迟加载（在访问model.field时）数据库中的数据
	'''
	return Product.objects.only('id', 'name')

def _exec_first():
	'''
	获取数据库中第一个数据
	'''
	return Product.objects.first()


def _exec_exists():
	'''
	判断数据是否存在
	'''
	return Product.objects.filter(name='product').exists()



def _exec_get():
	return Product.objects.get(name='product_1')


def _exec_count():
	product = Product.objects.get(name='product_1')
	return Order.objects.filter(product=product).count()


@login_required
def show_db_window(request):
	actions = []
	for name in globals():
		if '_exec_' in name:
			actions.append(name[6:])
	actions.sort()

	c = RequestContext(request, {
		'actions': actions
	})
	return render_to_response('example/db_app.html', c)