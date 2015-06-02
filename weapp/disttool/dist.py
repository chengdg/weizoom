#-*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
import time
from optparse import OptionParser

sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(__file__), '../..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'weapp.settings'

from utils import resource_util

FILTERS = ['']

GLOBAL_OPTIONS = None

HTML2JS = {}
HTML2CSS = {}

def copytree(src, dst, excludes=('.svn',)):
	names = os.listdir(src)
	if not os.path.exists(dst):
		os.makedirs(dst)

	for name in names:
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)
		try:
			if os.path.isdir(srcname):
				do_copy = True
				for exclude in excludes:
					if exclude in name:
						do_copy = False
						break
				if do_copy:
					copytree(srcname, dstname, excludes)
			else:
				shutil.copy2(srcname, dstname)
		except (IOError, os.error), why:
			print "Can't copy %s to %s: %s" % (`srcname`, `dstname`, str(why))


EXCLUDES = set(['.svn', 'dist', 'init.bat', 'start_mockapi_server.bat', '.idea', 'deploy_dist'])
def copy_files_to(dist_dir):
	src_path = '.'
	dst_path = dist_dir
	for file in os.listdir(src_path):
		if file in EXCLUDES:
			print 'ignore ', file
			continue

		src = file
		dst = os.path.join(dst_path, file)
		if os.path.isdir(file):
			print 'copy dir %s to %s' % (src, dst)
			copytree(src, dst)
		else:
			print 'copy file %s to %s' % (src, dst)
			shutil.copy2(src, dst)


################################################################################
# 修改mode
################################################################################
def change_mode():
	print 'change mode from "develop" to "deploy"'
	src_file = open('./weapp/settings.py', 'rb')
	content = src_file.read()
	content = content.replace("MODE = 'develop'", "MODE = 'deploy'")
	content = content.replace("MODE = 'test'", "MODE = 'deploy'")
	content = content.replace("DEBUG_MERGED_JS = True", "DEBUG_MERGED_JS = False")
	content = content.replace("USE_DEV_JS = True", "USE_DEV_JS = False")
	src_file.close()

	dst_file = open('./weapp/settings.py', 'wb')
	print >> dst_file, content
	dst_file.close()


################################################################################
# change path to contain md5 digest
################################################################################
def generate_md5_version_file(path):
	src = open(path, 'rb')
	content = src.read()
	src.close()

	import hashlib
	md5 = hashlib.md5(content)
	digest = md5.hexdigest()

	pos = path.rfind('.')
	prefix = path[:pos]
	suffix = path[pos+1:]
	new_path = '%s_%s.%s' % (prefix, digest, suffix)
	import shutil
	shutil.copyfile(path, new_path)
	print '[md5] generate md5 file %s for %s' % (new_path, path)
	#os.rename(path, new_path)
	return new_path


def to_minified_path(path):
	pos = path.rfind('.')
	prefix = path[:pos]
	suffix = path[pos+1:]
	return '%s.min.%s' % (prefix, suffix)


################################################################################
# 以下为js代码的操作
################################################################################
def get_js_files_from_template_file(content_base_html):
	shouldRecord = False
	js_files = []
	for line in open(content_base_html):
		if '*start develop js*' in line:
			shouldRecord = True
			continue

		if '*finish develop js*' in line:
			shouldRecord = False
			continue

		if shouldRecord:
			if '<!--' in line:
				continue
				
			line = line.strip()
			if line:
				if 'src="' in line:
					beg = line.find('src="')+5
					end = line.find('"', beg)
				else:
					beg = line.find("src='")+5
					end = line.find("'", beg)
				if beg == 4 or end == -1:
					print '[invalid js] ' + line
					continue

				js = line[beg:end][1:] #去掉开始的/
				js_files.append(js)

	return js_files


def merge_javascripts(js_name):
	if 'termite' in js_name:
		js_path = 'termite/static/js'
		js_files = get_js_files_from_template_file('./termite/termite_templates/%s.html' % js_name)
	elif 'v2' in js_name:
		js_path = 'static_v2/js'
		js_files = get_js_files_from_template_file('./templates/%s.html' % js_name)
	else:
		js_path = 'static/js'
		js_files = get_js_files_from_template_file('./templates/%s.html' % js_name)
	print 'merge %d js files in %s' % (len(js_files), js_name)

	#合并js文件
	dst_js_path = os.path.join(js_path, '%s_all.js' % js_name)
	if os.path.exists(dst_js_path):
		print 'delete old ', dst_js_path
		os.remove(dst_js_path)
		
	dst_js = open(dst_js_path, 'wb')
	for src_file_name in js_files:
		if (js_name == 'jqm_content_base') or ('termite' in js_name):
			src_file_name = src_file_name.replace('static/', 'termite/static/')
		if (js_name == 'new_jqm_content_base') or (js_name == 'webapp_content_base'):
			src_file_name = src_file_name.replace('termite_static/', 'termite/static/')

		print '\t[merge]: process js file: ', src_file_name
		print >> dst_js, "/****************************************************/"
		print >> dst_js, ' /* conent from %s' % src_file_name
		print >> dst_js, "/****************************************************/"
		src_file = open(src_file_name.split('?')[0], 'rb')
		content = src_file.read()
		if 'W.component.Component' in content:
			#处理Rhino不能接受js keyword作为object key的bug
			content = content.replace('default:', '"default":')
		print >> dst_js, content
		print >> dst_js, ";" #避免缺少分号导致的异常函数调用
		src_file.close()
	dst_js.close()
	print 'merge all js files into ', dst_js_path

	items = dst_js_path.split('.')
	HTML2JS[js_name] = dst_js_path


def change_js_reference(js_name):
	dst_js_file_name = '%s_all.min.js' % js_name
	src_js_file_name = '%s_all.js' % js_name
	print 'change all.js reference in %s.html to %s' % (js_name, dst_js_file_name)
	timestamp = time.strftime('%Y%m%d%H%M%S')
	if 'termite' in js_name:
		html_file = './termite/termite_templates/%s.html' % js_name
	else:
		html_file = './templates/%s.html' % js_name
	src_file = open(html_file, 'rb')
	lines = []

	#get md5 version file path
	js_file_name = to_minified_path(HTML2JS[js_name])
	dst_js_file_name = generate_md5_version_file(js_file_name)
	HTML2JS[js_name] = dst_js_file_name
	dst_js_file_name = dst_js_file_name.split('/')[-1]
	
	shouldRecord = True
	for line in src_file:
		if '*start js*' in line:
			if (js_name == 'base') or (js_name == 'termite_base'):
				line_content = ['\t\t{{ ""|load_templates_v1|safe }}\n\t\t{% if debug_merged_js %}', '\t\t<script type="text/javascript" src="/static/js/%s?version=%s"></script>' % (src_js_file_name, timestamp), '{% else %}', '\t\t<script type="text/javascript" src="{{cdn_host}}/standard_static/js/%s"></script>' % dst_js_file_name, '{% endif %}']
				lines.append('\n\t\t'.join(line_content))
			elif (js_name == 'base_v2'):
				line_content = ['\t\t{{ ""|load_templates_v2|safe }}\n\t\t{% if debug_merged_js %}', '\t\t<script type="text/javascript" src="/static/js/%s?version=%s"></script>' % (src_js_file_name, timestamp), '{% else %}', '\t\t<script type="text/javascript" src="{{cdn_host}}/standard_static/js/%s"></script>' % dst_js_file_name, '{% endif %}']
				lines.append('\n\t\t'.join(line_content))
			elif js_name == 'webapp_content_base':
				lines.append('\t\t<script type="text/javascript" src="{{cdn_host}}/standard_static/js/%s"></script>' % dst_js_file_name)
			else:
				lines.append('\t\t<script type="text/javascript" src="/standard_static/js/%s"></script>' % dst_js_file_name)
			shouldRecord = False
			continue

		if '*finish js*' in line:
			shouldRecord = True
			continue

		if not shouldRecord:
			continue

		lines.append(line.rstrip())
	src_file.close()

	dst_file = open(html_file, 'wb')
	print >> dst_file, '\n'.join(lines)
	dst_file.close()

	if js_name == 'jqm_content_base':
		change_jqm_preview_page_js_reference('jqm_preview_page', dst_js_file_name, timestamp)
	if js_name == 'new_jqm_content_base':
		change_jqm_preview_page_js_reference('new_jqm_preview_page', dst_js_file_name, timestamp)


def change_jqm_preview_page_js_reference(html_name, dst_js_file_name, timestamp):
	html_file = './termite/workbench/templates/workbench/%s.html' % html_name
	print 'change all.js reference in %s' % html_file
	src_file = open(html_file, 'rb')
	lines = []
	shouldRecord = True
	for line in src_file:
		if '*start js*' in line:
			lines.append('\t\t<script type="text/javascript" src="/standard_static/js/%s"></script>' % dst_js_file_name)
			shouldRecord = False
			continue

		if '*finish js*' in line:
			shouldRecord = True
			continue

		if not shouldRecord:
			continue

		lines.append(line.rstrip())
	src_file.close()

	dst_file = open(html_file, 'wb')
	print >> dst_file, '\n'.join(lines)
	dst_file.close()
	
	
def compress_js(js_name):
	#压缩js文件
	if 'termite' in js_name:
		src_js_file = "./termite/static/js/%s_all.js" % js_name
		dst_js_file = "./termite/static/js/%s_all.min.js" % js_name
	elif 'v2' in js_name:
		src_js_file = "./static_v2/js/%s_all.js" % js_name
		dst_js_file = "./static_v2/js/%s_all.min.js" % js_name
	else:
		src_js_file = "./static/js/%s_all.js" % js_name
		dst_js_file = "./static/js/%s_all.min.js" % js_name
	cmd = 'java -Xss20m -jar disttool/yuicompressor-2.4.6.jar %s -o %s' % (src_js_file, dst_js_file)
	print 'compress js by : %s' % cmd
	subprocess.call(cmd.split(' '))

	change_js_reference(js_name)


def merge_views_to(js_name):
	if 'v2' in js_name:
		static_dir = 'static_v2'
		version = '2'
	else:
		static_dir = 'static'
		version = '1'
	dst_js_path = os.path.join('%s/js' % static_dir, '%s_all.js' % js_name)
	print 'merge all model|view|dialog js into ', dst_js_path

	src_js_paths = []
	template_sources = []

	for model in resource_util.get_web_models(version):
		src_js_paths.append(model['js_file_path'])

	for view in resource_util.get_web_views(version):
		src_js_paths.append(view['js_file_path'])
		template_sources.append('\n<!--')
		template_sources.append('content from %s' % view['template_file_path'])
		template_sources.append('-->')
		template_sources.append(view['template_source'])

	for dialog in resource_util.get_web_dialogs(version):
		src_js_paths.append(dialog['js_file_path'])
		template_sources.append('\n<!--')
		template_sources.append('content from %s' % dialog['template_file_path'])
		template_sources.append('-->')
		template_sources.append(dialog['template_source'])


	dst_js = open(dst_js_path, 'ab')
	for src_js_path in src_js_paths:
		print >> dst_js, "\n/****************************************************/"
		print >> dst_js, '/* js from %s' % src_js_path
		print >> dst_js, "/****************************************************/"
		src_file = open(src_js_path, 'rb')
		print >> dst_js, src_file.read()
		print >> dst_js, ";" #避免缺少分号导致的异常函数调用
		src_file.close()
	dst_js.close()

	dst_template_path = os.path.join('templates', 'all_merged_templates_v%s.html' % version)
	dst_template_file = open(dst_template_path, 'wb')
	print >> dst_template_file, '\n'.join(template_sources)
	dst_template_file.close()
	print 'write all template into ', dst_template_path



################################################################################
# 以下为css代码的操作
################################################################################
def get_css_files_from_template_file(content_base_html):
	shouldRecord = False
	css_files = []
	for line in open(content_base_html):
		if '*start develop css*' in line:
			shouldRecord = True
			continue

		if '*finish develop css*' in line:
			shouldRecord = False
			continue

		if shouldRecord:
			if '<!--' in line:
				continue
				
			line = line.strip()
			if line:
				beg = line.find('href="')+6
				end = line.find('"', beg)
				if beg == 4 or end == -1:
					print '[invalid css] ' + line
					continue

				css = line[beg:end][1:] #去掉开始的/
				css_files.append(css)
	
	return css_files


def merge_css(css_name):
	if 'termite' in css_name:
		css_path = 'termite/static/css'
		css_files = get_css_files_from_template_file('./termite/termite_templates/%s.html' % css_name)
	elif 'v2' in css_name:
		css_path = 'static_v2/css'
		css_files = get_css_files_from_template_file('./templates/%s.html' % css_name)
	else:
		css_path = 'static/css'
		css_files = get_css_files_from_template_file('./templates/%s.html' % css_name)
	print 'merge %d css files' % len(css_files)

	# if css_name == 'new_jqm_content_base':
	# 	add_webapp_css_version('./templates/new_jqm_content_base.html')
	# if css_name == 'webapp_content_base':
	# 	add_webapp_css_version('./templates/webapp_content_base.html')
	#	return

	#合并css文件
	dst_css_path = os.path.join(css_path, '%s_all.css' % css_name)
	if os.path.exists(dst_css_path):
		print 'delete old ', dst_css_path
		os.remove(dst_css_path)
		
	dst_css = open(dst_css_path, 'wb')
	for src_file_name in css_files:
		if (css_name == 'jqm_content_base') or ('termite' in css_name):
			src_file_name = src_file_name.replace('static/', 'termite/static/')
		if (css_name == 'new_jqm_content_base') or (css_name == 'webapp_content_base'):
			src_file_name = src_file_name.replace('termite_static/', 'termite/static/')
		print '\t[merge]: process css file: ', src_file_name
		print >> dst_css, "/****************************************************/"
		print >> dst_css, '/* conent from %s' % src_file_name
		print >> dst_css, "/****************************************************/"
		src_file = open(src_file_name, 'rb')
		print >> dst_css, src_file.read()
		src_file.close()
	dst_css.close()
	print 'merge all css files into ', dst_css_path
	HTML2CSS[css_name] = dst_css_path

	#compress css file
	src_css_file = "./%s/%s_all.css" % (css_path, css_name)
	dst_css_file = "./%s/%s_all.min.css" % (css_path, css_name)
	cmd = 'java -Xss20m -jar disttool/yuicompressor-2.4.6.jar %s -o %s' % (src_css_file, dst_css_file)
	print '[merge css] compress css by', cmd
	subprocess.call(cmd.split(' '))
	
	change_css_reference('%s_all.min.css' % css_name, css_name)

#added by chuter, ugly one, later to process
def add_webapp_css_version(dst_tmpl_file_name):
	timestamp = time.strftime('%Y%m%d%H%M%S')

	src_file = open(dst_tmpl_file_name, 'rb')
	lines = []
	shouldProcess = False
	for line in src_file:
		if '<link' in line and 'type="text/css"' in line:
			line = line.replace('.css', '.css?version={}'.format(timestamp))

		if '<script' in line and 'type="text/javascript' in line:
			if not 'version=' in line:
				line = line.replace('.js', '.js?version={}'.format(timestamp))


		lines.append(line.rstrip())
	src_file.close()

	dst_file = open(dst_tmpl_file_name, 'wb')
	print >> dst_file, '\n'.join(lines)
	dst_file.close()

def change_css_reference(dst_css_file_name, css_name):
	timestamp = time.strftime('%Y%m%d%H%M%S')
	if 'termite' in css_name:
		html_file = './termite/termite_templates/%s.html' % css_name
	else:
		html_file = './templates/%s.html' % css_name
	print 'change all.css reference in %s' % html_file

	#get md5 version file path
	css_file_name = to_minified_path(HTML2CSS[css_name])
	dst_css_file_name = generate_md5_version_file(css_file_name)
	HTML2CSS[css_name] = dst_css_file_name
	dst_css_file_name = dst_css_file_name.split('/')[-1]

	src_file = open(html_file, 'rb')
	lines = []
	shouldRecord = True
	for line in src_file:
		if '*start css*' in line:
			if css_name == 'webapp_content_base':
				lines.append('\t\t<link type="text/css" rel="stylesheet" media="all" href="{{cdn_host}}/standard_static/css/%s">' % dst_css_file_name)
			elif css_name == 'jqm_content_base' or css_name == 'new_jqm_content_base':
				lines.append('\t\t<link type="text/css" rel="stylesheet" media="all" href="/standard_static/css/%s">' % dst_css_file_name)
			else:
				lines.append('\t\t<link type="text/css" rel="stylesheet" media="all" href="{{cdn_host}}/standard_static/css/%s">' % dst_css_file_name)
			shouldRecord = False
			continue

		if '*finish css*' in line:
			shouldRecord = True
			continue

		if not shouldRecord:
			continue

		if css_name == 'webapp_content_base' and '{{request.template_name}}.css' in line:
			line = line.replace('{{request.template_name}}.css', '{{request.template_name}}.css?version=%s' % timestamp)
		lines.append(line.rstrip())
	src_file.close()

	dst_file = open(html_file, 'wb')
	print >> dst_file, '\n'.join(lines)
	dst_file.close()

	if css_name == 'jqm_content_base':
		change_jqm_preview_page_css_reference('jqm_preview_page', dst_css_file_name, timestamp)
	if css_name == 'new_jqm_content_base':
		change_jqm_preview_page_css_reference('new_jqm_preview_page', dst_css_file_name, timestamp)


def change_jqm_preview_page_css_reference(html_name, dst_css_file_name, timestamp):
	html_file = './termite/workbench/templates/workbench/%s.html' % html_name
	print 'change all.css reference in %s' % html_file
	src_file = open(html_file, 'rb')
	lines = []
	shouldRecord = True
	for line in src_file:
		if '*start css*' in line:
			lines.append('\t\t<link type="text/css" rel="stylesheet" media="all" href="/standard_static/css/%s">' % dst_css_file_name)				
			shouldRecord = False
			continue

		if '*finish css*' in line:
			shouldRecord = True
			continue

		if not shouldRecord:
			continue

		lines.append(line.rstrip())
	src_file.close()

	dst_file = open(html_file, 'wb')
	print >> dst_file, '\n'.join(lines)
	dst_file.close()

	add_webapp_css_version(html_file)


def minify_template_css():
	templates_dir = 'webapp/modules/static'
	for template_dir in os.listdir(templates_dir):
		if template_dir.startswith('backend_'):
			template_name = template_dir[8:]
			src_css_file = '%s/%s/css/%s.css' % (templates_dir, template_dir, template_name)
			dst_css_file = '%s/%s/css/%s.min.css' % (templates_dir, template_dir, template_name)
			#compress css file
			cmd = 'java -Xss20m -jar disttool/yuicompressor-2.4.6.jar %s -o %s' % (src_css_file, dst_css_file)
			print '[minify template css] compress css by', cmd
			subprocess.call(cmd.split(' '))


def up_js_css_to_upyun():
	from core import upyun_util
	def map_to_remote_path(path):
		items = path.split('/')
		items[0] = 'standard_static'
		return '/' + '/'.join(items)

	local2remote = {
		#'static/css/webapp_content_base_all.min.css': '/standard_static/css/webapp_content_base_all.min.css',
		#'static/js/webapp_content_base_all.min.js': '/standard_static/js/webapp_content_base_all.min.js'
	}
	for key, local_file in HTML2JS.items():
		local2remote[local_file] = map_to_remote_path(local_file)
	for key, local_file in HTML2CSS.items():
		local2remote[local_file] = map_to_remote_path(local_file)

	templates_dir = 'webapp/modules/static'
	for template_dir in os.listdir(templates_dir):
		if template_dir.startswith('backend_'):
			template_name = template_dir[8:]
			css_file = '%s/%s/css/%s.css' % (templates_dir, template_dir, template_name)
			local2remote[css_file] = '/webapp_static/%s/css/%s.css' % (template_dir, template_name)

	for local, remote in local2remote.items():
		print "[cdn]: upload %s to upyun's %s" % (local, remote)
		upyun_util.upload_static_file(local, remote, True)
			

		

################################################################################
# 总控函数
################################################################################
def dist():
	htmls = ['base', 'base_v2', 'jqm_content_base', 'new_jqm_content_base', 'webapp_content_base']
	
	for html in htmls:
		merge_javascripts(html)
		merge_css(html)	
	merge_views_to('base')
	merge_views_to('base_v2')

	minify_template_css()

	if GLOBAL_OPTIONS.deploy:
		change_mode()
	else:
		'***** not change mode *****'

	if GLOBAL_OPTIONS.compress:
		for html in htmls:
			compress_js(html)
	else:
		'***** not compress *****'
	
	#删除不需要的js文件
	js_path = 'static/js'
	if GLOBAL_OPTIONS.delete_js:
		print 'delete original js'
		shutil.rmtree(os.path.join(js_path, 'system'))
		shutil.rmtree(os.path.join(js_path, 'common'))
		shutil.rmtree(os.path.join(js_path, 'app'))
	else:
		print '***** reserve original js *****'

	if GLOBAL_OPTIONS.cdn:
		up_js_css_to_upyun()

	print '====== HTML2JS ======'
	print HTML2JS
	print '====== HTML2CSS ======'
	print HTML2CSS


if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('--deleteJs', action='store_true', dest = 'delete_js',
	                  help = 'whether to delete original js after merge js.')
	parser.add_option('--compress', action='store_true', dest = 'compress',
	                  help = 'whether to compress js after merge js.')
	parser.add_option('--deploy', action='store_true', dest = 'deploy',
	                  help = 'whether to change mode to deploy.')
	parser.add_option('--cdn', action='store_true', dest='cdn',
				  help ='upload static files to cdn')
	
	(options, args) = parser.parse_args()
	GLOBAL_OPTIONS = options
	dist()