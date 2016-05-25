# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json, os, xlrd
import logging
from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource, paginator
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from mall import export
from mall.promotion import models as promotion_models
from mall import models as mall_models

from watchdog.utils import watchdog_alert

import utils
from django.conf import settings

class VirtualProduct(resource.Resource):
	app = 'mall2'
	resource = 'virtual_product'

	@login_required
	def get(request):
		"""
		创建福利卡券活动
		"""
		id = int(request.GET.get('id', 0))
		virtual_product = None
		if id:
			_virtual_product = promotion_models.VirtualProduct.objects.get(id=id)
			product = _virtual_product.product
			product.fill_standard_model()
			_product = {
				'id': product.id,
				'name': product.name,
				'bar_code': product.bar_code,
				'price': product.price,
				'stocks': product.stocks,
				'thumbnails_url': product.thumbnails_url,
				'detail_link': '/mall2/product/?id=%d&source=onshelf' % product.id,
				'created_at': product.created_at.strftime('%Y-%m-%d %H:%M')
			}

			virtual_product = {
				'id': _virtual_product.id,
				'name': _virtual_product.name,
				'product': _product,
				'created_at': _virtual_product.created_at.strftime('%Y-%m-%d %H:%M')
			}

		c = RequestContext(request, {
			'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
            'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
			'third_nav_name': export.MALL_PROMOTION_VIRTUAL_PRODUCTS_NAV,
			'virtual_product': virtual_product
		})

		return render_to_response('mall/editor/promotion/virtual_product.html', c)


	@login_required
	def api_get(request):
		"""
		获取虚拟商品和微众卡商品
		"""
		owner = request.manager
		#获取当前页数
		cur_page = int(request.GET.get('page', '1'))
		#获取每页个数
		count_per_page = int(request.GET.get('count_per_page', 10))

		name = request.GET.get('name', '').strip()
		bar_code = request.GET.get('barCode', '').strip()

		activities = promotion_models.VirtualProduct.objects.filter(owner=request.manager, is_finished=False)
		active_product_ids = [activity.product_id for activity in activities]
		#获取没有参加正在进行中的福利卡券活动的虚拟商品列表
		params = {
			'owner': request.manager, 
			'type__in': [mall_models.PRODUCT_VIRTUAL_TYPE, mall_models.PRODUCT_WZCARD_TYPE],
			'shelve_type': mall_models.PRODUCT_SHELVE_TYPE_ON
		}
		if name:
			params['name__contains'] = name
		if bar_code:
			params['bar_code'] = bar_code

		products = mall_models.Product.objects.filter(**params).order_by('-id')
		pageinfo, products = paginator.paginate(products, cur_page, count_per_page, None)

		items = []
		for product in products:
			product.fill_standard_model()
			_product = {
				'id': product.id,
				'name': product.name,
				'bar_code': product.bar_code,
				'price': product.price,
				'stocks': product.stocks,
				'thumbnails_url': product.thumbnails_url,
				'detail_link': '/mall2/product/?id=%d&source=onshelf' % product.id,
				'created_at': product.created_at.strftime('%Y-%m-%d %H:%M')
			}
			if product.id in active_product_ids:
				_product['can_use'] = False
			else:
				_product['can_use'] = True
			items.append(_product)

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': ''
		}
		return response.get_response()

	@login_required
	def api_put(request):
		"""
		创建福利卡券活动
		"""
		owner = request.manager
		name = request.POST.get('name', '').strip()
		product_id = request.POST.get('product_id', '').strip()
		start_time = request.POST.get('start_time', '').strip()
		end_time = request.POST.get('end_time', '').strip()
		code_file_path = request.POST.get('code_file_path', '').strip()
		
		try:
			#先创建福利卡券活动
			if name and product_id:
				virtual_product = promotion_models.VirtualProduct.objects.create(
									owner=owner,
									name=name,
									product_id=product_id
								)
				#再为该福利卡券活动上传卡密
				success_num = upload_codes_for(owner, code_file_path, virtual_product, start_time, end_time)

				response = create_response(200)
				response.data = {'success_num': success_num}
			else:
				response = create_response(500)
				response.errMsg = u'活动名称或商品不能为空！'
		except Exception, e:
			logging.error(e)
			response = create_response(500)
			response.errMsg = e

		return response.get_response()


	@login_required
	def api_post(request):
		"""
		修改福利卡券活动，补充上传卡密
		"""
		id = request.POST.get('id')
		if id:
			owner = request.manager
			start_time = request.POST.get('start_time', '').strip()
			end_time = request.POST.get('end_time', '').strip()
			code_file_path = request.POST.get('code_file_path', '').strip()
			
			try:
				virtual_product = promotion_models.VirtualProduct.objects.get(owner=owner, id=id, is_finished=False)
				#为该福利卡券活动上传卡密
				success_num = upload_codes_for(owner, code_file_path, virtual_product, start_time, end_time)

				response = create_response(200)
				response.data = {'success_num': success_num}
			except Exception, e:
				logging.error(e)
				response = create_response(500)
				response.errMsg = e
		else:
			response = create_response(500)
			response.errMsg = u'id不能为空！'

		return response.get_response()

class FileUploader(resource.Resource):
	app = 'mall2'
	resource = 'upload_virtual_product_file'

	def api_post(request):
		"""
		上传文件
		"""
		upload_file = request.FILES.get('Filedata', None)
		owner_id = request.POST.get('owner_id', None)

		response = create_response(500)
		file_path = ""
		if upload_file and owner_id:
			try:
				now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
				upload_file.name = now + upload_file.name
				file_path = FileUploader.__save_file(upload_file, owner_id)
			except Exception, e:
				logging.error(e)
				response.errMsg = u'保存文件出错'
				return response.get_response()
			try:
				codes, codes_dict = get_codes_dict_from_file(file_path)
			except Exception, e:
				logging.error(e.message)
				response.errMsg = e.message
				return response.get_response()

			valid_codes = get_valid_codes(codes)
			response = create_response(200)
			response.data = {
				'file_path': file_path,
				'valid_num': len(valid_codes)
			}
		else:
			response.errMsg = u'文件错误'
		return response.get_response()

	@staticmethod
	def __save_file(file, owner_id):
		"""
		@param file: 文件
		@param owner_id: webapp_owner_id
		@return: 文件保存路径
		"""
		content = []
		curr_dir = os.path.dirname(os.path.abspath(__file__))
		if file:
			for chunk in file.chunks():
				content.append(chunk)

		dir_path = os.path.join(curr_dir, '../../../', 'upload', 'owner_id'+owner_id)
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		file_path = os.path.join(dir_path, file.name)

		dst_file = open(file_path, 'wb')
		print >> dst_file, ''.join(content)
		dst_file.close()
		return file_path


def upload_codes_for(owner, code_file_path, virtual_product, start_time, end_time):
	if not code_file_path:
		return 0

	codes, codes_dict = get_codes_dict_from_file(code_file_path)
	existed_code_ids = __get_existed_code_ids()

	success_num = 0
	for code in codes:
		#如果库中已存在任何状态的该码，则不添加这个码
		if not code:
			continue
		if existed_code_ids.has_key(code):
			continue

		password = codes_dict[code]
		promotion_models.VirtualProductHasCode.objects.create(
			owner=owner,
			virtual_product=virtual_product,
			code=code,
			password=password,
			start_time=start_time,
			end_time=end_time
		)
		success_num += 1
	logging.info('upload %d codes for virtual_product id %d' % (success_num, virtual_product.id))
	return success_num

def __get_existed_code_ids():
	"""
	获取未领取和已领取的卡密
	"""
	# existed_codes = promotion_models.VirtualProductHasCode.objects.filter(status__in=[promotion_models.CODE_STATUS_NOT_GET, promotion_models.CODE_STATUS_GET])
	#只要上传过，不管是哪个商家上传的，不管现在是什么状态，都不允许再次上传，不允许更改任何信息
	existed_codes = promotion_models.VirtualProductHasCode.objects.all()
	existed_code_ids = {}
	for code in existed_codes:
		# if not code.can_not_use:
		# 	existed_code_ids[code.code] = 1
		existed_code_ids[code.code] = 1

	return existed_code_ids

def get_valid_codes(codes):
	"""
	获取可以添加的卡密列表
	"""
	existed_code_ids = __get_existed_code_ids()
	valid_codes = set()
	for code in codes:
		if not existed_code_ids.has_key(code):
			valid_codes.add(code)
	return valid_codes


def get_codes_dict_from_file(file_path):
	"""
	从文件中读取福利卡券的码库
	"""
	codes = []  #为了保证存到数据库中的顺序与文件中的顺序相同
	codes_dict = {}
	if os.path.exists(file_path):
		data = xlrd.open_workbook(file_path)
		table = data.sheet_by_index(0)
		nrows = table.nrows   #行数
		for i in range(0,nrows):
			code = table.cell(i,0).value
			password = table.cell(i,1).value
			
			if type(code) == float:
				code = str(int(code))
			if type(password) == float:
				password = str(int(password))
			if code != '' and password != '':
				if not code in codes:
					codes_dict[code] = password
					codes.append(code)
			else:
				raise ValueError(u'第%d行数据有误，请核查！' % (i + 1))
	else:
		raise ValueError(u'读取文件失败')

	return codes, codes_dict


def update_stocks():
	"""
	更新商品的库存
	"""
	pass