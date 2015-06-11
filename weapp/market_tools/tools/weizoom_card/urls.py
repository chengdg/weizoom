# -*- coding: utf-8 -*-

__author__ = "guoliyan"


from django.conf.urls import *

import views
# import api_views


urlpatterns = patterns('',
    (r'^weizoom_card/(\d+)/expense_record/$', views.weizoom_card_expense_record),
    (r'^', views.list_weizoom_card),

 #    (r'^weizoom_card/create/$', views.create_weizoom_card_rule),
 #    (r'^weizoom_card_rule_detail/$', views.weizoom_card_rule_detail),
 #    (r'^list_accounts/$', views.list_weizoom_card_accounts),
 #    (r'^adjust_accounts/$', views.list_adjust_accounts),
 #    (r'^adjust_accounts/detail/$', views.detail_adjust_accounts),
 #    (r'^adjust_accounts/integral/(\d+)/$', views.list_integral),

	# url(r'^account/', include('market_tools.tools.weizoom_card.account_has_permissions.urls')),

 #    (r'^api/', api_views.call_api),

 #    (r'^adjust_accounts/export/', api_views.export_adjust_accounts),
 #    (r'^detail_adjust_accounts/export/', api_views.export_detail_adjust_accounts),
    
)
