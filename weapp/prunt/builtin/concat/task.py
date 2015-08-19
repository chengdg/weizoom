# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import os
import logging
logger = logging.getLogger('prunt-concat')

from prunt.decorator import register_task

@register_task('prunt-concat')
def concat(prunt):
	u"""
	合并文件内容
	"""
	prunt.config.require('files')
	prunt.config.require('comment')

	files = prunt.config['files']
	src_files = files['src']
	dest = files['dest']

	path_map = prunt.config.get('path_map', None)
	if path_map:
		logger.info('use path map: %s', path_map)

	if type(src_files) == str:
		src_files = [src_files]
	
	logger.info('concat files [%s] into "%s"' % ('; '.join(src_files), dest))

	#文件名替换
	if path_map:
		for i in range(len(src_files)):
			src_file = src_files[i]
			old_src_file = src_file
			for rule in path_map.items():
				src_file = src_file.replace(rule[0], rule[1])
			src_files[i] = src_file
			logger.info('change [%s] to [%s]', old_src_file, src_files[i])

	#检查文件
	target_file_type = None
	for src_file in src_files:
		if path_map:
			for rule in path_map.items():
				old_src_file = src_file
				src_file = src_file.replace(rule[0], rule[1])
				logger.info('change [%s] to [%s]', old_src_file, src_file)

		#检查文件有效性
		if not os.path.exists(src_file):
			raise RuntimeError('Task prunt-concat FAILED! %s is not exists' % src_file)

		#确保文件同类型
		pos = src_file.rfind('.')
		file_type = src_file[pos+1:]
		if not target_file_type:
			target_file_type = file_type
		if file_type != target_file_type:
			raise RuntimeError('Task prunt-concat FAILED! cant concat *.%s file with *.%s file' % (target_file_type, file_type))

	#content_suffix是在每一个content后附加的内容，可以解决js文件缺少分号(;)导致的异常函数调用
	content_suffix = None
	if target_file_type == 'js':
		content_suffix = ';'

	comment_tmpl = prunt.config['comment'].replace('comment', '%s')
	contents = []
	for src_file in src_files:
		comment = u' start file content for %s' % src_file
		contents.append(u'\n\n')
		contents.append(unicode(comment_tmpl % comment))
		f = open(src_file, 'rb')
		content = f.read()
		f.close()
		contents.append(content.decode('utf-8'))
		if content_suffix:
			contents.append(content_suffix)
		comment = ' finish file content for %s' % src_file
		contents.append(unicode(comment_tmpl % comment))
	
	#确保dest的目录存在
	dest_dir = os.path.dirname(dest)
	if not os.path.exists(dest_dir):
		os.makedirs(dest_dir)

	#写入dest文件
	dst_file = open(dest, 'wb')
	print >> dst_file, '\n'.join(contents).encode('utf-8')
	dst_file.close()