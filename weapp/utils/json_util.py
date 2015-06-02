# -*- coding: utf-8 -*-

__author__ = 'chuter'

def string_json(str):
	sb=[];
	for char in str:
		if char == '\"':
			sb.append("\\\"")
		elif char == '\\':
			sb.append('\\\\')
		elif char == '/':
			sb.append('\\/')
		elif char == '\b':
			sb.append('\\b');
		elif char == '\f':
			sb.append('\\f')
		elif char == '\n':
			sb.append('<br\\/>')
		elif char == '\r':
			sb.append('\\r')
		elif char == '\t':
			sb.append('\\t')
		else:
			sb.append(char)
	return ''.join(sb)