# -*- coding: utf-8 -*-
#
# __author__ = 'chuter'
#
# from django.template import Context, RequestContext
# from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from django.shortcuts import render_to_response
# from django.http import HttpResponseRedirect, HttpResponse, Http404
# from views import FIRST_NAV_NAME, HOME_SECOND_NAVS
# from utils import cache_util
# from models import OperationSettings, UserOrderNotifySettings
#
# SECOND_NAV_NAME = 'system_settings'

# @login_required
# def index(request):
# 	#创建缓存
# 	operation_settings_objs = OperationSettings.objects.filter(owner=request.user)
# 	if operation_settings_objs.count() == 0:
# 		operation_settings = OperationSettings.objects.create(owner=request.user)
# 	else:
# 		operation_settings = operation_settings_objs[0]
#
# 	if UserOrderNotifySettings.objects.filter(user=request.user).count() == 0:
# 		for index in range(5):
# 			user_order_setting = UserOrderNotifySettings.objects.create(user=request.user, status=index)
# 			notify_setting_key = "notify_settings_{wo:%s}_{status:%s}" % (request.user.id,index)
# 			print "zl--------------------------",notify_setting_key
# 			cache_util.add_mhash_to_redis(notify_setting_key,user_order_setting.to_dict())
# 	c = RequestContext(request, {
# 		'first_nav_name': FIRST_NAV_NAME,
# 		'second_navs': HOME_SECOND_NAVS,
# 		'second_nav_name': SECOND_NAV_NAME,
# 		'operation_settings': operation_settings,
# 		'notify_settings': UserOrderNotifySettings.objects.filter(user=request.user)
# 	})
# 	return render_to_response('account/settings.html', c)

#===============================================================================
# edit_email_settings : 修改邮箱配置
#===============================================================================
# @login_required
# def edit_email_setting(request,status):
# 	if request.method == 'POST':
# 		emails = request.POST.get('emails', '')
# 		member_ids = request.POST.get('member_ids', '')
# 		if UserOrderNotifySettings.objects.filter(user=request.user, status=status).count() > 0:
# 			UserOrderNotifySettings.objects.filter(user=request.user, status=status).update(emails=emails, black_member_ids=member_ids)
# 			notify_setting_key = "notify_settings_{wo:%s}_{status:%s}" % (request.user.id,status)
# 			cache_util.add_mhash_to_redis(notify_setting_key,{'emails':emails,'black_member_ids':member_ids})
# 		else:
# 			user_order_setting = UserOrderNotifySettings.objects.create(status=status, black_member_ids=member_ids, emails=emails, user=request.user)
# 			notify_setting_key = "notify_settings_{wo:%s}_{status:%s}" % (request.user.id,index)
# 			cache_util.add_mhash_to_redis(notify_setting_key,user_order_setting.to_dict())
#
# 		return HttpResponseRedirect('/account/settings/')
# 	else:
# 		notify_settings = UserOrderNotifySettings.objects.filter(user=request.user, status=status)
# 		if notify_settings.count() > 0:
# 			notify_setting = notify_settings[0]
# 		else:
# 			notify_setting = None
#
# 	c = RequestContext(request, {
# 		'first_nav_name': FIRST_NAV_NAME,
# 		'second_navs': HOME_SECOND_NAVS,
# 		'second_nav_name': SECOND_NAV_NAME,
# 		'notify_setting': notify_setting,
# 	})
# 	return render_to_response('account/edit_notify_settings.html', c)


########################################################################
# update_email_status: 更改email通知状态
########################################################################
# @login_required
# def update_email_status(request, id):
# 	action = request.GET['action']
# 	if action == 'stop':
# 		user_notify_setting = UserOrderNotifySettings.objects.filter(id=id).get()
# 		user_notify_setting.is_active=False
# 		user_notify_setting.save()
# 		notify_setting_key = "notify_settings_{wo:%s}_{status:%s}" % (user_notify_setting.user_id,user_notify_setting.status)
# 		cache_util.add_mhash_to_redis(notify_setting_key,{'is_active':False})
# 	elif action == 'restart':
# 		user_notify_setting = UserOrderNotifySettings.objects.filter(id=id).get()
# 		user_notify_setting.is_active=True
# 		user_notify_setting.save()
# 		print "zl-----------------",user_notify_setting.user_id,user_notify_setting.status
# 		notify_setting_key = "notify_settings_{wo:%s}_{status:%s}" %(user_notify_setting.user_id,user_notify_setting.status)
# 		cache_util.add_mhash_to_redis(notify_setting_key,{'is_active':True})
# 	else:
# 		pass
# 	return HttpResponseRedirect(request.META['HTTP_REFERER'])

#2015-11-19 zhaolei
# ########################################################################
# # edit_integral_detail: 积分详情修改
# ########################################################################
# @login_required
# def edit_integral_detail(request):
# 	if request.method == "POST":
# 		setting,_ = IntegralStrategySttingsDetail.objects.get_or_create(webapp_id=request.user_profile.webapp_id)
# 		setting.is_used = int(request.POST.get('is_used', 0))
# 		setting.increase_count_after_buy = float(request.POST.get('increase_count_after_buy', 0))
# 		setting.buy_via_shared_url_increase_count_for_author = float(request.POST.get('buy_via_shared_url_increase_count_for_author', 0))
# 		setting.buy_increase_count_for_father = float(request.POST.get('buy_increase_count_for_father', 0))
# 		setting.save()
# 	else:
# 		if IntegralStrategySttingsDetail.objects.filter(webapp_id=request.user_profile.webapp_id).count() > 0:
# 			setting = IntegralStrategySttingsDetail.objects.filter(webapp_id=request.user_profile.webapp_id)[0]
# 		else:
# 			setting = IntegralStrategySttingsDetail.objects.create(webapp_id=request.user_profile.webapp_id)
#
# 	c = RequestContext(request, {
# 		'first_nav_name': FIRST_NAV_NAME,
# 		'second_navs': HOME_SECOND_NAVS,
# 		'second_nav_name': SECOND_NAV_NAME,
# 		'setting': setting,
# 	})
# 	return render_to_response('account/edit_integral_detail_settings.html', c)