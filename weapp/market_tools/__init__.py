# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os

from django.utils.importlib import import_module
# from util import collect_all_market_tool_pathes

TOOLNAME_2_MODULES = None

class ToolModule(object):
	def __init__(self, module_obj, module_name):
		self.module_obj = module_obj
		self.module_name = module_name

	def __load_sub_module(self, module_name):
		return import_module("{}.{}".format(self.package, module_name))
		try:
			return import_module("{}.{}".format(self.package, module_name))
		except:
			print "{}.{}".format(self.package, module_name)
			raise ImportError(u"load营销工具%s的%s失败" % (self.package, module_name))

	def __load_settings_module(self):
		return self.__load_sub_module('settings')	

	def __load_urls_module(self):
		return self.__load_sub_module('urls')

	def __load_export_module(self):
		return self.__load_sub_module('export')

	@property
	def settings(self):
		if hasattr(self, 'settings_module'):
			return self.settings_module
		else:
			self.settings_module = self.__load_settings_module()
			return self.settings_module

	@property
	def urls(self):
		if hasattr(self, 'urls_module'):
			return self.urls_module
		else:
			self.urls_module = self.__load_urls_module()
			return self.urls_module

	@property
	def export(self):
		if hasattr(self, 'export_module'):
			return self.export_module
		else:
			self.export_module = self.__load_export_module()
			return self.export_module

	@property
	def package(self):
		return self.module_obj.__name__

	@staticmethod
	def all_tool_modules():
		global TOOLNAME_2_MODULES

		if TOOLNAME_2_MODULES is None:
			TOOLNAME_2_MODULES = {}
			
			for tool_path in collect_all_market_tool_pathes():
				_, tool_name = os.path.split(tool_path)
				TOOLNAME_2_MODULES[tool_name] = load_tool_module(tool_path)

		return TOOLNAME_2_MODULES.values()

#
#load营销的module，如果load失败会抛ImportError异常，
#否则返回ToolModule实例
#
def load_tool_module(full_path_to_tool):
	global TOOLNAME_2_MODULES

	tools_root_dir, tool_name = os.path.split(full_path_to_tool)
	if (TOOLNAME_2_MODULES is not None) and (TOOLNAME_2_MODULES.has_key(tool_name)):
		return TOOLNAME_2_MODULES[tool_name]
	
	tool_module_obj = import_module("{}.{}".format('market_tools.tools', tool_name))
	return ToolModule(tool_module_obj, tool_name)