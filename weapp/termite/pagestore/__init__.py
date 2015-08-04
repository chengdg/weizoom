# -*- coding: utf-8 -*-

NAME2PAGESTORE = {}

###############################################################
# get_pagestore: 获取pagestore
###############################################################
def get_pagestore(request):
	module_name = 'pagestore.mongo'
	pagestore = NAME2PAGESTORE.get(module_name, None)
	if not pagestore:			
		module = __import__(module_name, {}, {}, ['*',])
		pagestore = module.PageStore()
		NAME2PAGESTORE[module_name] = pagestore
	return pagestore


###############################################################
# get_pagestore_by_type: 根据pagestore的类型获取pagestore
###############################################################
def get_pagestore_by_type(type):
	module_name = 'pagestore.%s' % type
	pagestore = NAME2PAGESTORE.get(module_name, None)
	if not pagestore:			
		module = __import__(module_name, {}, {}, ['*',])
		pagestore = module.PageStore()
		NAME2PAGESTORE[module_name] = pagestore
	return pagestore