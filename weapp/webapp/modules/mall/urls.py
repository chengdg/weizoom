# # -*- coding: utf-8 -*-

raise DeprecationWarning(
    "'webapp.modules.mall.urls' is deprecated in favor of 'mall.urls'. "
    "Please use 'mall.urls' instead!")

# from django.conf.urls import *

# import views
# import api_views
# import postage_views
# import order_views
# import order_api_views
# import pay_interface_views
# import product_model_views
# import product_model_api_views

# urlpatterns = patterns('',
# )
# 	# Termite GENERATED START: url
# 	(r'^$', order_views.list_orders),

# 	# MODULE START: productcategory
# 	(r'^editor/productcategories/$', views.list_productcategories),
# 	(r'^editor/productcategory/create/$', views.add_productcategory),
# 	(r'^editor/productcategory/update/(\d+)/$', views.update_productcategory),
# 	(r'^editor/productcategory/delete/(\d+)/$', views.delete_productcategory),

# 	(r'^api/productcategory/display_index/update/$', api_views.update_productcategory_display_index),
# 	(r'^api/categories/get/$', api_views.get_categories),
# 	(r'^editor/category_product/delete/(\d+)/$', views.category_has_product_delete),
# 	# MODULE END: productcategory


# 	# MODULE START: product
# 	(r'^editor/products/$', views.list_products),
# 	(r'^editor/product/create/$', views.add_product),
# 	(r'^editor/product/update/(\d+)/$', views.update_product),
# 	(r'^editor/product/delete/(\d+)/$', views.delete_product),
# 	(r'^editor/product/check_other_mall_product/(\d+)/(\d+)/$', views.check_other_mall_product),
# 	(r'^api/product_display_index/update/$', api_views.update_product_display_index),
# 	(r'^api/products/get/$', api_views.get_products),
# 	(r'^api/category_selectable_products/get/$', api_views.get_category_selectable_products),



# 	# MODULE END: product
# 	# Termite GENERATED END: url

# 	# Termite GENERATED START: url
# 	# MODULE START: postageconfig
# 	(r'^editor/mall_settings/$', views.list_mall_settings),
# 	(r'^editor/mall_settings/update/$', views.update_mall_settings),
# 	(r'^editor/postage_config/create/$', postage_views.add_postage_config),
# 	(r'^editor/postage_config/update/(\d+)/$', postage_views.update_postage_config),
# 	(r'^editor/postage_config/delete/(\d+)/$', postage_views.delete_postage_config),
# 	(r'^editor/pay_interface/create/$', pay_interface_views.add_pay_interface),
# 	(r'^editor/pay_interface/update/(\d+)/$', pay_interface_views.update_pay_interface),
# 	(r'^editor/pay_interface/delete/(\d+)/$', pay_interface_views.delete_pay_interface),
# 	(r'^editor/pay_interface/active/(\d+)/$', pay_interface_views.active_pay_interface),
# 	(r'^editor/pay_interface/inactive/(\d+)/$', pay_interface_views.inactive_pay_interface),

# 	(r'^editor/product_model_property/create/$', product_model_views.add_product_model_property),
# 	(r'^editor/product_model_property/update/$', product_model_views.update_product_model_property),
# 	(r'^editor/product_model_property/delete/(\d+)/$', product_model_views.delete_product_model_property),
# 	(r'^api/product_model_properties/get/$', product_model_api_views.get_product_model_properties),
# 	# MODULE END: postageconfig
# 	# Termite GENERATED END: url

#  	# order urls start
#  	(r'^editor/orders/$', order_views.list_orders),
#  	(r'^editor/orders/export/$', order_views.export_orders),
# 	(r'^editor/order/get/$', order_views.get_order_detail),
# 	(r'^editor/order/update/$', order_views.update_order),
# 	(r'^editor/order_status/update/$', order_views.update_order_status),
# 	(r'^editor/order_express/add/$', order_views.add_express_info),
# 	(r'^api/orders/get/$', order_api_views.get_orders),
# 	(r'^api/order_products/get/$', order_api_views.get_order_products),
# 	# 筛选条件
# 	(r'^api/order_filters/get/$', order_api_views.get_order_filters),
# 	(r'^api/order_filter/save/$', order_api_views.save_order_filter),
# 	(r'^api/order_filter/delete/$', order_api_views.delete_order_filter),
# 	(r'^api/order_filter_params/get/$', order_api_views.get_order_filter_params),
# 	# 批量发货
# 	(r'^api/bulk_shipments/$', order_api_views.bulk_shipments),
# 	#营销工具渠道扫码获取成交订单
# 	(r'^api/channel_qrcode_payed_orders/get/(\d+)/$', order_api_views.get_channel_qrcode_payed_orders),
# 	# order urls end

# 	#营销工具感恩贺卡获取成交订单
# 	(r'^api/thanks_card_orders/get/$', order_api_views.get_thanks_card_orders),
# 	(r'^api/thanks_card_order_products/get/$', order_api_views.get_thanks_card_order_products),
# 	(r'^api/thanks_card_products/update/$', api_views.support_product_make_thanks_card),
# 	(r'^api/thanks_card_products/get/$', api_views.get_thanks_card_products),
# 	(r'^api/thanks_card_secret/update/$', api_views.reset_thanks_secret),

# 	(r'^integral/$', views.integral_settings),

# 	#面板
# 	(r'^editor/panel/$',  views.list_panel),
# 	(r'^api/orders/$', api_views.get_orders),
# 	(r'^api/orders/statistics/$', api_views.total_statistics),
# 	(r'^export/order/csv/$', views.export_order_csv),
# 	(r'^export/order/excel/$', views.export_order_list),
# 	(r'^api/order/daily_day_trend/get/$', api_views.get_order_daily_trend),
# )
