# -*- coding: utf-8 -*-
"""@package weapp.hack_django
Hack Django

修改Django CursorDebugWrapper的默认实现，记录sql发生时的stack trace

"""

from django.db.backends import BaseDatabaseWrapper as DjangoBaseDatabaseWrapper
from django.db.backends import util as orm_util
from django.db.models.query import QuerySet
from django.db.models import Q, F
from django.dispatch import Signal
from django.db.models import Model
from django.conf import settings
from django.db.models.manager import Manager
from django.contrib.auth.models import User

import traceback


class WeappDebugWrapper(orm_util.CursorDebugWrapper):
	"""
	"""
	def __init__(self, cursor, db):
		orm_util.CursorDebugWrapper.__init__(self, cursor, db)

	def execute(self, sql, params=None):
		try:
			return super(WeappDebugWrapper, self).execute(sql, params)
		finally:
			stack_entries = traceback.extract_stack()
			stack_entries = filter(lambda entry: (('weapp' in entry[0]) and (not 'hack_django' in entry[0])), stack_entries)
			buf = []
			for stack_entry in stack_entries:
				filename, line, function_name, text = stack_entry
				formated_stack_entry = "<span>File `%s`, line %s, in %s</span><br/><span>&nbsp;&nbsp;&nbsp;&nbsp;%s</span>" % (filename, line, function_name, text)
				buf.append(formated_stack_entry)
			stack = '<br/>'.join(buf).replace("\\", '/').replace('"', "``").replace("'", '`')
			self.db.queries[-1]['stack'] = stack


def hackCursorDebugWrapper(params):
	if not params['enable_record_sql_stacktrace']:
		return

	def weapp_make_debug_cursor(self, cursor):
		return WeappDebugWrapper(cursor, self)
	DjangoBaseDatabaseWrapper.make_debug_cursor = weapp_make_debug_cursor


post_update_signal = Signal(providing_args=["model", "instance"])
def hackQuerySetUpdate():
	old_update = QuerySet.update
	def new_update(self, **kwargs):
		old_update(self, **kwargs)
		cache_args = getattr(Model, 'cache_args', None)
		setattr(Model, 'cache_args', None)
		instance = self
		if cache_args:
			instance = cache_args.get('instance', self)
		post_update_signal.send(sender=self.model, model=self.model, instance=instance, cache_args=cache_args)
	QuerySet.update = new_update


post_delete_signal = Signal(providing_args=["model", "instance"])
def hackQuerySetDelete():
	old_delete = QuerySet.delete
	def new_delete(self, **kwargs):
		old_delete(self, **kwargs)
		cache_args = getattr(Model, 'cache_args', None)
		setattr(Model, 'cache_args', None)
		instance = self
		if cache_args:
			instance = cache_args.get('instance', self)
		post_delete_signal.send(sender=self.model, model=self.model, instance=instance, cache_args=cache_args)
	QuerySet.delete = new_delete


def hackQuerySetFilter():
	old_filter = QuerySet.filter
	def new_filter(self,  *args, **kwargs):
		from mall import models as mall_models

		try:
			if 'owner' in kwargs and kwargs['owner'].id == 216:
				if self.model == mall_models.Product:
					owner = kwargs.pop('owner')
					if 'shelve_type' in kwargs:
						# print 'jz-----1', kwargs, args ,owner
						shelve_type = kwargs.pop('shelve_type')
						return old_filter(self, *args, **kwargs).filter(Q(owner=owner, shelve_type=shelve_type) |\
								Q(weshop_sync__gt=0, shelve_type=mall_models.PRODUCT_SHELVE_TYPE_ON, weshop_status=shelve_type))
					# kwargs['shelve_type'] = mall_models.PRODUCT_SHELVE_TYPE_ON
					# kwargs['weshop_status'] = mall_models.PRODUCT_SHELVE_TYPE_ON
					# print 'jz-----1.5', kwargs, args ,owner
					return old_filter(self, **kwargs).filter(Q(owner=owner) | Q(weshop_sync__gt=0))
				if self.model == mall_models.ProductModelProperty:
					owner = kwargs.pop('owner')
			if 'owner_id' in kwargs and kwargs['owner_id'] == 216:
				if self.model == mall_models.Product:
					owner_id = kwargs.pop('owner_id')
					if 'shelve_type' in kwargs:
						# print 'jz-----2', kwargs, args ,owner_id
						shelve_type = kwargs.pop('shelve_type')
						return old_filter(self, *args, **kwargs).filter(Q(owner_id=owner_id, shelve_type=shelve_type) |\
								Q(weshop_sync__gt=0, shelve_type=mall_models.PRODUCT_SHELVE_TYPE_ON, weshop_status=shelve_type))

					# print 'jz-----2.5', kwargs, args ,owner_id
					# kwargs['shelve_type'] = mall_models.PRODUCT_SHELVE_TYPE_ON
					# kwargs['weshop_status'] = mall_models.PRODUCT_SHELVE_TYPE_ON
					return old_filter(self, **kwargs).filter(Q(owner_id=owner_id) | Q(weshop_sync__gt=0))
		except:
			pass

		return old_filter(self, *args, **kwargs)
	QuerySet.filter = new_filter

self_id = 582
target_id = 570
owner_ids = (target_id, self_id, 102, 443)

self_webapp_id = '3716'
target_webapp_id = '3704'
webapp_ids = (target_webapp_id, self_webapp_id, '3211', '3595')
def hackQuerySetFilterForShow():
	"""
	丰富用于为客户演示的账号的数据
	"""
	old_filter = QuerySet.filter
	def new_filter(self,  *args, **kwargs):
		import modules.member.models as member_models
		import stats.models as stats_models
		import mall.models as mall_models
		try:
			if 'owner' in kwargs and kwargs['owner'].id == self_id:
				owner = kwargs.pop('owner')

				#商品列表只显示一家的
				if self.model == mall_models.Product:
					return old_filter(self, **kwargs).filter(owner_id=target_id)

				return old_filter(self, **kwargs).filter(owner_id__in=owner_ids)

			if 'owner_id' in kwargs and kwargs['owner_id'] == self_id:
				owner_id = kwargs.pop('owner_id')
				return old_filter(self, **kwargs).filter(owner_id__in=owner_ids)

			if 'webapp_id' in kwargs and kwargs['webapp_id'] == self_webapp_id:
				webapp_id = kwargs.pop('webapp_id')
				if self.model == member_models.IntegralStrategySttings:
					return old_filter(self, **kwargs).filter(webapp_id=target_webapp_id)

				if self.model == stats_models.BrandValueHistory:
					kwargs['webapp_id'] = self_webapp_id
					return old_filter(self, **kwargs)
				
				return old_filter(self, **kwargs).filter(webapp_id__in=webapp_ids)

			if 'webapp_source_id' in kwargs and kwargs['webapp_source_id'] == self_webapp_id:
				webapp_source_id = kwargs.pop('webapp_source_id')
				return old_filter(self, **kwargs).filter(webapp_source_id__in=webapp_ids)
		except:
			pass

		return old_filter(self, *args, **kwargs)
	QuerySet.filter = new_filter


def hackModel():
	"""
	改进django model，添加to_dict方法
	"""
	def model_todict(self, *attrs):
		columns = [field.get_attname() for field in self._meta.fields]
		result = {}
		for field in self._meta.fields:
			result[field.get_attname()] = field.value_from_object(self)
		for attr in attrs:
			if hasattr(self, attr):
				result[attr] = getattr(self, attr, None)
		return result
	Model.to_dict = model_todict

	def model_str(self):
		return str(self.to_dict())
	Model.__str__ = model_str
	Model.__unicode__ = model_str

	def from_dict(cls, dict):
		if dict == None:
			return None
		#obj = cls.__new__(cls)
		obj = cls()
		for key, value in dict.items():
			try:
				setattr(obj, key, value)
			except AttributeError:
				pass
		return obj
	Model.from_dict = classmethod(from_dict)

	def from_list(cls, list):
		objs = []
		for dict in list:
			obj = cls.__new__(cls)
			for key, value in dict.items():
				setattr(obj, key, value)
			objs.append(obj)
		return objs
	Model.from_list = classmethod(from_list)


def hackRenderToResponse():
	"""
	改进template render行为，在develop模式下，为response中添加context
	"""
	if settings.DEBUG:
		from django import shortcuts
		django_render_to_response = shortcuts.render_to_response
		def new_render_to_response(*args, **kwargs):
			response = django_render_to_response(*args, **kwargs)
			response._debug_context = args[1]
			return response

		shortcuts.render_to_response = new_render_to_response


def hackModelManager():
	def record_cache_args(self, **kwargs):
		Model.cache_args = kwargs
		return self

	def clear_cache_args(self):
		Model.cache_args = None

	Manager.record_cache_args = record_cache_args
	Manager.clear_cache_args = clear_cache_args


#duhao 20151019 注释
# def hackUser():
# 	def has_perm(self, perms):
# 		if self.is_superuser:
# 			return True
# 		if self.get_profile().is_manager:
# 			#根账号拥有所有权限
# 			return True

# 		permission_set = getattr(self, 'permission_set', None)
# 		if not permission_set:
# 			return False

# 		if isinstance(perms, unicode) or isinstance(perms, str):
# 			return perms in permission_set
# 		else:
# 			for perm in perms:
# 				if perm in permission_set:
# 					return True

# 		return False
# 	User.has_perm = has_perm


def hack(params):
	hackCursorDebugWrapper(params)
	hackQuerySetUpdate()
	hackQuerySetDelete()
	hackQuerySetFilter()
	hackModel()
	hackRenderToResponse()
	hackModelManager()
	# hackUser() duhao 20151019 注释
	hackQuerySetFilterForShow()
