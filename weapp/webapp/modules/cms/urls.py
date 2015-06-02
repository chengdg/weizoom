# -*- coding: utf-8 -*-

from django.conf.urls import *

import views
import api_views
import category_views
import category_api_views
import article_views
import article_api_views
import special_article_views
import special_article_api_views

urlpatterns = patterns('',
	# Termite GENERATED START: url
	(r'^$', category_views.list_categories),

	# MODULE START: productcategory
	(r'^editor/categories/$', category_views.list_categories),
	(r'^editor/category/create/$', category_views.add_category),
	(r'^editor/category/update/(\d+)/$', category_views.update_category),
	(r'^editor/category/delete/(\d+)/$', category_views.delete_category),

	(r'^api/category/display_index/update/$', category_api_views.update_category_display_index),
	(r'^api/categories/get/$', category_api_views.get_categories),
	#(r'^editor/category_product/delete/(\d+)/$', views.category_has_product_delete),	
	# MODULE END: productcategory


	# MODULE START: article
	(r'^editor/articles/$', article_views.list_articles),
	(r'^editor/article/create/$', article_views.add_article),
	(r'^editor/article/update/(\d+)/$', article_views.update_article),
	(r'^editor/article/delete/(\d+)/$', article_views.delete_article),

	(r'^api/article_display_index/update/$', article_api_views.update_article_display_index),	
	(r'^api/articles/get/$', article_api_views.get_articles),
	(r'^api/article/get/$', article_api_views.get_article),
	(r'^api/help_center_categories/get/$', article_api_views.get_help_center_categories),
	# MODULE END: product

	(r'^editor/special_articles/$', special_article_views.list_articles),
	(r'^editor/special_article/update/(\d+)/$', special_article_views.update_article),
	# Termite GENERATED END: url
)
