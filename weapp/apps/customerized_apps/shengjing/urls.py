# -*- coding: utf-8 -*-

from django.conf.urls import *

from user_center import mobile_api_views as user_center_mobile_api_views
from user_center import api_views as user_center_api_views

from study_plan import mobile_api_views as study_plan_mobile_api_views
from study_plan import api_views as study_plan_api_views
from study_plan import views as study_plan_views
from order import mobile_api_views as order_mobile_api_views
from views import *
import api_views


urlpatterns = patterns('',
	# url(r'^user_center/', include('apps.customerized_apps.shengjing.user_center.urls')),
	
	# url(r'^study_plan/', include('apps.customerized_apps.shengjing.study_plan.urls')),

	# 临时链接页面
	(r'^$', get_link_all),
	
	(r'^apps/$', list_apps),

	#study_plan api
	(r'^study_plan/api/courses/get/$', study_plan_mobile_api_views.get_courses),
	(r'^study_plan/api/study_plan/get/$', study_plan_mobile_api_views.get_study_plan),
	(r'^study_plan/api/course/apply/$', study_plan_mobile_api_views.apply_course),
	(r'^study_plan/api/editor_courses/get/$', study_plan_api_views.get_courses),
	(r'^study_plan/api/course_display_index/update/$', study_plan_api_views.update_course_display_index),
	(r'^study_plan/api/course/delete/$', study_plan_api_views.delete_course),
	(r'^study_plan/course/list/$', study_plan_views.list_course),
	(r'^study_plan/course/add/$', study_plan_views.add_course),
	(r'^study_plan/course/edit/$', study_plan_views.edit_course),
	 
	 url(r'^order/api/order/list/$', order_mobile_api_views.list_order),

	#user_cent api
	(r'^user_center/api/send_captcha/$', user_center_mobile_api_views.send_captcha),
	(r'^user_center/api/record_binding_phone/$', user_center_mobile_api_views.record_binding_phone),
	(r'^user_center/api/member_qrcode/get/$', user_center_mobile_api_views.get_member_qrcode_ticket),

	# (r'^user_center/integral/$', settings_page),
	(r'^user_center/api/settings/update/$', user_center_api_views.update_settings),
	
	# 释放接口
	(r'^api/send_template_message/$', api_views.send_release_template_message),
	# 创建接口
	(r'^api/send_create_template_message/$', api_views.send_create_template_message),
)

