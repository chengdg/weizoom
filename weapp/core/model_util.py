# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
from termite.workbench.viper_views import _get_fields_to_be_save

MODEL2ATTRS = {}
FILTER_SET = set([u'id', u'owner_id', u'created_at'])

def get_attrs_for(model_class):
	model_class_name = str(model_class)
	if not model_class_name in MODEL2ATTRS:
		attrs = []
		for field in model_class._meta.fields:
			attr = field.attname
			if attr in FILTER_SET:
				continue
			attrs.append(field.attname)
		MODEL2ATTRS[model_class_name] = attrs

	return MODEL2ATTRS[model_class_name]


def create_record(request):
	project = request.GET['project_id']
	page_id = request.GET['page_id']

	model_class = request.model_class
	attrs = get_attrs_for(model_class)
	record = _get_fields_to_be_save(request)

	data = {}
	for attr in attrs:
		data[attr] = record[attr]
	data['owner'] = request.user
	model_class.objects.create(**data)

	redirect_to_page_id = request.GET.get('submit_redirect_to', page_id)
	if not hasattr(request, 'is_from_app'):
		return HttpResponseRedirect('/workbench/viper/page/?project_id=%s&page_id=%s' % (project_id, redirect_to_page_id))
	

#===============================================================================
# update_record : 更新记录
#===============================================================================
def update_record(request):
	project_id = request.GET['project_id']
	record_id = request.GET['record_id']

	model_class = request.model_class
	attrs = get_attrs_for(model_class)
	record = _get_fields_to_be_save(request)

	data = {}
	for attr in attrs:
		data[attr] = record[attr]
	data['owner'] = request.user
	model_class.objects.filter(id=record_id).update(**data)


#===============================================================================
# get_record : 获取记录
#===============================================================================
def get_record(request):
	project_id = request.GET['project_id']
	record_id = request.GET['record_id']

	model_class = request.model_class

	db_record = model_class.objects.get(id=record_id)
	result = {
		"id": db_record.id
	}
	attrs = get_attrs_for(model_class)
	for attr in attrs:
		result[attr] = getattr(db_record, attr)

	return result


#===============================================================================
# delete_record : 删除记录
#===============================================================================
def delete_record(request):
	record_id = request.GET['record_id']

	model_class = request.model_class
	model_class.objects.filter(id=record_id).delete()
