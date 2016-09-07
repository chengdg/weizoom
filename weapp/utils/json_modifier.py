# -*- coding: utf-8 -*-
import re
import copy

pattern = re.compile(r'.*\d+')


def __is_digit_in(s):
	return bool(pattern.match(s))


class JsonModifier(object):
	def __init__(self, obj, modify_rule):

		self.modify_key_func = modify_rule.modify_key_func
		self.modify_value_func = modify_rule.modify_value_func

		self.obj = copy.deepcopy(obj)

	def __modify_name(self, underline_format):
		"""
			下划线命名格式驼峰命名格式
		"""
		# if __is_digit_in(underline_format):
		# 	return underline_format
		camel_format = ''
		if isinstance(underline_format, basestring):
			words = underline_format.split('_')
			camel_format = words[0]
			for word in words[1:]:
				camel_format += word.capitalize()
		return camel_format

	def __modify_dict(self, obj):

		for key, value in obj.items():
			# _tmp_value = obj.pop(key)
			new_key = self.modify_key_func(key)
			new_value = self.modify_value_func(obj.pop(key))
			if isinstance(value, dict):
				obj[new_key] = self.__modify_dict(new_value)
			elif isinstance(value, list):
				obj[new_key] = self.__modify_list(new_value)
			else:
				obj[new_key] = new_value

		return obj

	def __modify_list(self, obj):
		for i, item in enumerate(obj):
			if isinstance(item, dict):
				obj[i] = self.__modify_dict(item)
			if isinstance(item, list):
				obj[i] = self.__modify_list(item)
		return obj

	def modify(self):
		if isinstance(self.obj, dict):
			return self.__modify_dict(self.obj)
		elif isinstance(self.obj, list):
			return self.__modify_list(self.obj)
		else:
			return self.obj


class ModifyRule(object):
	"""
	如不实现相关方法,则返回原值
	"""

	def modify_key_func(self, key):
		return key

	def modify_value_func(self, value):
		return value
