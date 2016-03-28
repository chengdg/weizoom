# -*- coding: utf-8 -*-

__author__ = 'bert'

# from django.conf.urls import *

# import views
# import api_views

# urlpatterns = patterns('',
# # 	#用户中心后台页面
# # 	(r'^$', views.list_memers),
# # 	(r'^member/(\d+)/$', views.show_member),
# # 	(r'^member/(\d+)/integral_log/$', views.show_member_integral_log),
# # 	(r'^member/export/$', views.export_member),
# # 	#api
# # 	(r'^api/get_member_follow_relations/(\d+)/(\d+)/$', api_views.get_member_follow_relations),
# # 	(r'^api/member/update/$', api_views.update_member),

# # 	(r'^api/members/get/$', api_views.get_members),
# # 	(r'^api/massmessage/send/$', api_views.send_mass_message),

# # 	#会员等级
# # 	(r'^grades/$', views.list_grades),
# # 	(r'^grade/create/$', views.add_grade),
# # 	(r'^grade/update/(\d+)/$', views.update_grade),
# # 	(r'^grade/delete/(\d+)/$', views.delete_grade),
# # 	(r'^api/grade_has_members/get/(\d+)/$', api_views.get_grade_has_members),

# # 	#会员等级
# # 	(r'^tags/$', views.list_tags),
# # 	(r'^tag/create/$', views.add_tag),
# #  	(r'^tag/update/(\d+)/$', views.update_tag),
# #  	(r'^tag/delete/(\d+)/$', views.delete_tag),
# # # 	(r'^api/grade_has_members/get/(\d+)/$', api_views.get_grade_has_members),
# )

# -*- coding: utf-8 -*-

from django.conf.urls import *

import member_views
import api_views

import member_grade

import member_shipinfo
import member_browse_record
import member_coupon

urlpatterns = patterns('',
)
