# -*- coding: utf-8 -*-

__author__ = 'chuter'

from shengjing.models import (ShengjingBindingMemberInfo, 
	                          ShengjingIntegralStrategySttings,
	                          ShengjingBindingMemberHasCompanys
	                          )

def binded_member_required(function=None):
	def _dec(view_func):
		def _view(request, *args, **kwargs):
			if request.method == "POST":
				binding_member_id = request.POST.get('binding_member_id', -1)
				name  = request.POST.get('name', None)
				position  = request.POST.get('position', '')
				company = request.POST.get('company', '')
				#判断是否绑定过
				if name and binding_member_id != -1: #and ShengjingBindingMemberInfo.objects.filter(binding_id=binding_member_id, name=name).count == 0:
					if ShengjingBindingMemberInfo.objects.filter(binding_id=binding_member_id).count() == 0:
						ShengjingBindingMemberInfo.objects.create(name=name, position=position, binding_id=binding_member_id)
						#绑定成功 给父节点增加积分
						ShengjingIntegralStrategySttings.increase_integral_for_father_by_binding_id(binding_member_id, request.user_profile.webapp_id)
					
						ShengjingBindingMemberHasCompanys.objects.get_or_create(name=company, binding_id=binding_member_id)

			return view_func(request, *args, **kwargs)

		_view.__doc__ = view_func.__doc__
		_view.__dict__ = view_func.__dict__
		_view.__name__ = view_func.__name__

		return _view

	if function is None:
		return _dec
	else:
		return _dec(function)