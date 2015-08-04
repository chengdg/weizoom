# -*- coding: utf-8 -*-
from django.conf.urls import *

import views
import order_api_views
import messages_view
import api_views
import order_static_api_views
import sales_api_views

urlpatterns = patterns('',
	(r'^$', views.app_login),
	(r'^logout/$', views.app_logout),
	(r'^main/$', views.app_main),
	(r'^messages/$',views.list_messages),
	(r'^messages/session_history/show/(\d*)$', views.get_session_histories),
	(r'^messages/reply/$', views.reply_session),
	(r'^order/$',views.list_orders),
	(r'^order_detail/(\d+)/$',views.order),
	(r'^show_index/$', api_views.show_index),
	#api获取数据
	(r'^api/order_list/get/$', order_api_views.get_order_list),
	(r'^api/order/get/$', order_api_views.get_order),
	(r'^api/order_express_name/get/$', order_api_views.get_order_express_name),
	(r'^api/express_info/add/$',order_api_views.add_express_info),
	(r'^api/order_status/update/$',order_api_views.update_order_status),
	(r'^new_base/$',views.new_base),
	(r'^api/messages/$',messages_view.list_messages),
	(r'^api/messages/session_history/$', messages_view.get_session_histories),
	(r'^api/messages/reply/$', messages_view.reply_session),
	(r'^api/messages/get_unread_count/$', messages_view.get_realtime_unread_count),
	(r'^api/messages/send_media/$', messages_view.send_media),
	(r'^api/messages/send_mui_media/$', messages_view.send_mui_media),
	(r'^api/order_daily_trend/get/$', api_views.get_order_daily_trend),
	(r'^api/sale_daily_trend/get/$', api_views.get_sale_daily_trend),
	(r'^api/visit_daily_trend/get/$', api_views.get_visit_daily_trend),
	(r'^api/message_daily_trend/get/$', api_views.get_message_daily_trend),
	(r'^api/yesterday_count_trend/get/$', api_views.get_yesterday_count_trend),
	(r'^api/yesterday_price_trend/get/$', api_views.get_yesterday_price_trend),
	(r'^api/login/get/$', api_views.get_login),
	(r'^api/logout/get/$', api_views.get_logout),
	(r'^api/version/check/$', api_views.check_version),

	(r'^api/buy_trend/get/$', api_views.get_buy_trend),#(2.0版本使用)
	(r'^api/daily_message_trend/get/$', api_views.get_daily_message_trend),#(2.0版本使用)
	(r'^get_index_html/$', api_views.get_index_html),

	#数据统计
	(r'^api/order_statistic/order_by_pay_type/get/$',order_static_api_views.get_order_by_pay_type),
	(r'^api/order_statistic/order_by_product/get/$',order_static_api_views.get_order_by_product),
	(r'^api/order_statistic/order_by_source/get/$',order_static_api_views.get_order_by_source),
	(r'^api/order_statistic/user_source_by_day/get/$',order_static_api_views.get_user_source_by_day),
	(r'^api/order_statistic/user_source_by_week/get/$',order_static_api_views.get_user_source_by_week),
	(r'^api/order_statistic/user_static/get/$',order_static_api_views.get_user_static),

	(r'^api/order_statistic/order_by_day/get/', sales_api_views.get_order_by_day),
	(r'^api/order_statistic/order_by_week/get/', sales_api_views.get_order_by_week),
	(r'^api/order_statistic/order_by_month/get/', sales_api_views.get_order_by_month),
	(r'^api/order_statistic/order_by_status/get/', sales_api_views.get_order_by_status),

	(r'^api/mui/messages/$', messages_view.mui_list_messages),
	(r'^api/mui/messages/session_history/$', messages_view.mui_get_session_histories),
	(r'^api/mui/messages/additional_history/$', messages_view.mui_get_additional_histories),

    #新增数据罗盘
   	(r'^api/stats/brand_value/$', api_views.brand_value),
    (r'^api/stats/overview_board/$',api_views.overview_board),
    (r'^api/stats/order_value/$', api_views.order_value),
    (r'^api/stats/sales_chart/get/$', api_views.sales_chart),

)
