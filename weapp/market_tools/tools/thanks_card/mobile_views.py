# # -*- coding: utf-8 -*-
#
# __author__ = 'sunny'
#
# import os
# import subprocess
# import time
# import base64
#
# from django.http import HttpResponseRedirect, HttpResponse, Http404
# from django.template import Context, RequestContext
# from django.shortcuts import render_to_response
#
# from core.jsonresponse import JsonResponse, create_response, decode_json_str
#
# from core.exceptionutil import unicode_full_stack
# from models import *
# from modules.member import util as member_util
# from modules.member import module_api as member_module_api
# from mall.models import ThanksCardOrder
# from account.views import save_base64_img_file_local_for_webapp
# from watchdog.utils import watchdog_alert, watchdog_fatal
#
# ######################################################
# # 制作感恩贺卡
# ######################################################
# def edit_thanks_card(request):
# 	if request.POST:
# 		thanks_card_id = request.POST.get('thanks_card_id')
# 		title = request.POST.get('title', '')
# 		content = request.POST.get('card_content', '')
# 		type = request.POST.get('thanks_card_att_type', '')
#
# 		thanks_card_order = ThanksCardOrder.objects.get(id=thanks_card_id)
# 		#如果贺卡已经被使用, 跳入到预览页面
# 		if thanks_card_order.is_used:
# 			c = __fill_show_thanks_card(request, thanks_card_order)
# 			return render_to_response('thanks_card/webapp/thanks_card.html', c)
#
# 		thanks_card_order.title = title
# 		thanks_card_order.content = content
# 		thanks_card_order.is_used = True
# 		thanks_card_order.card_count = thanks_card_order.card_count + 1
# 		thanks_card_order.listen_count = thanks_card_order.listen_count + 1
#
# 		if type == 'image':	#上传的是图片
# 			file = request.POST['thanks_card_img']
# 			try:
# 				is_bdd_test = request.POST.get('bbd_test', False)
# 				if is_bdd_test:
# 					att_url = 'bdd/test/url'
# 				else:
# 					att_url = save_base64_img_file_local_for_webapp(request, file)
# 				thanks_card_order.att_url = att_url
# 				thanks_card_order.type = 0
# 			except Exception, e:
# 				c = RequestContext(request, {
# 					'page_title': '制作贺卡失败',
# 					'thanks_card_id': thanks_card_id,
# 					'error_info': '制作贺卡失败'
# 				})
# 				return render_to_response('thanks_card/webapp/convert_error.html', c)
# 		elif type == 'video':
# 			try:
# 				is_bdd_test = request.POST.get('bbd_test', False)
# 				if is_bdd_test:
# 					create_failure = request.POST.get('create_failure', False)
# 					if create_failure:
# 						raise Exception(u'转换视频格式失败')
# 					video_urls = ['bdd/test/url']
# 				else:
# 					video_urls = __upload_video(request)
# 				thanks_card_order.att_url = ','.join(video_urls)
# 				thanks_card_order.type = 1
# 			except Exception, e:
# 				c = RequestContext(request, {
# 					'page_title': '制作贺卡失败',
# 					'thanks_card_id': thanks_card_id,
# 					'error_info': '制作贺卡失败'
# 				})
# 				return render_to_response('thanks_card/webapp/convert_error.html', c)
# 		thanks_card_order.save()
#
# 		c = __fill_show_thanks_card(request, thanks_card_order)
# 		return render_to_response('thanks_card/webapp/thanks_card.html', c)
# 	else:
# 		thanks_card_id = request.GET.get('thanks_card_id', 0)
# 		secret = request.GET.get('secret', '')
# 		order_id = request.GET.get('order_id', 0)
# 		c = RequestContext(request, {
# 			'page_title': '制作感恩贺卡',
# 			'thanks_card_id': thanks_card_id,
# 			'secret': secret,
# 			'order_id': order_id
# 		})
# 		return render_to_response('thanks_card/webapp/editor_thanks_card.html', c)
#
# ######################################################
# # get_thanks_card: 展示感恩贺卡
# ######################################################
# def get_thanks_card(request):
# 	thanks_card_id = request.GET.get('thanks_card_id', 0)
# 	thanks_card_order = None
# 	if thanks_card_id == 0:
# 		thanks_secret = request.GET.get('secret')
# 		thanks_card_order = ThanksCardOrder.objects.get(thanks_secret=thanks_secret)
# 	else:
# 		thanks_card_order = ThanksCardOrder.objects.get(id=thanks_card_id)
# 	thanks_card_order.listen_count = thanks_card_order.listen_count + 1
# 	thanks_card_order.save()
#
# 	c = __fill_show_thanks_card(request, thanks_card_order)
# 	return render_to_response('thanks_card/webapp/thanks_card.html', c)
#
# ######################################################
# # show_thanks_card: 跳转至密码输入页面
# ######################################################
# def show_thanks_card(request):
# 	c = RequestContext(request, {
# 		'page_title': '播放感恩贺卡',
# 	})
# 	return render_to_response('thanks_card/webapp/input_pwd.html', c)
#
# ######################################################
# # __fill_show_thanks_card: 获取需要展示贺卡的context
# ######################################################
# def __fill_show_thanks_card(request, thanks_card_order):
# 	is_image = False
# 	is_video = False
# 	video_urls = []
# 	has_attr = False
#
# 	#判断是否包含附件
# 	if thanks_card_order.att_url != '':
# 		has_attr = True
#
# 	if thanks_card_order.type == 0:
# 		is_image = True
# 	if thanks_card_order.type == 1:
# 		is_video = True
# 		for video_url in thanks_card_order.att_url.split(','):
# 			video_urls.append(video_url)
#
# 	member = member_module_api.get_member_by_id(int(thanks_card_order.member_id))
# 	member_name = ''
# 	member_icon = ''
# 	if member:
# 		member_name = member.username
# 		member_icon = member.user_icon
# 	c = RequestContext(request, {
# 		'page_title': '播放感恩贺卡',
# 		'thanks_card_id': thanks_card_order.id,
# 		'thanks_card_content': thanks_card_order.content,
# 		'is_used': thanks_card_order.is_used,
# 		'from_user_name': member_name,
# 		'user_icon': member_icon,
# 		'is_image': is_image,
# 		'is_video': is_video,
# 		'image_src': thanks_card_order.att_url,
# 		'video_urls': video_urls,
# 		'has_attr': has_attr
# 	})
# 	return c
#
# ##############################################################
# # __upload_video: 上传视频,格式转换: ffmpeg不能转换成ogg格式
# ##############################################################
# def __upload_video(request):
# 	date = time.strftime('%Y%m%d')
# 	dir_path_suffix = 'webapp/%d_%s' % (request.user_profile.user_id, date)
# 	dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
#
# 	if not os.path.exists(dir_path):
# 		os.makedirs(dir_path)
#
# 	#获取文件的扩展名
# 	source_file_name = ('%s_%s' % (time.strftime("%Y_%m_%d_%H_%M_%S"), request.POST['card_img'])).lower()
# 	source_file_path = '%s/%s' % (dir_path, source_file_name)	#原文件路径
#
# 	file_content = request.POST['thanks_card_img']
# 	is_save_success = __save_video(file_content, source_file_path)
# 	video_urls = []
# 	if is_save_success:
# 		if source_file_name.endswith('.mp4'):
# 			video_urls.append('/static/upload/%s/%s' % (dir_path_suffix, source_file_name))
# 		else:
# 			#转换成mp4
# 			mp4_file_name = '%s_%s' % (time.strftime("%Y_%m_%d_%H_%M_%S"), '.mp4')
# 			mp4_file_path = os.path.join(dir_path, mp4_file_name)
# 			cmd = "ffmpeg -i {}  -f mp4 -vcodec mpeg4 -s 480x260 -vb 800k {}".format(source_file_path, mp4_file_path)
# 			if __convert_video(cmd, mp4_file_path):
# 				video_urls.append('/static/upload/%s/%s' % (dir_path_suffix, mp4_file_name))
# 		return video_urls
#
# ######################################################
# # __convert_video: 视频格式转换
# ######################################################
# def __convert_video(cmd, target_file):
# 	output = None
# 	try:
# 		converter = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# 		output = converter.communicate()[0]
#
# 		if not os.path.exists(target_file):
# 			raise Exception(u'没有找到转换后的mp4，确认ffmpeg操作正常')
# 		#upload_atts.append('/static/upload/%s/%s' % (dir_path_suffix, mp4_file_name))
# 		return True
# 	except:
# 		alert_message = ''
# 		if output:
# 			alert_message = u"转换视频格式失败，视频文件:{}, ffmpeg输出:\n{}\ncause:\n{}".format(ajax_path, output.decode('utf-8'), unicode_full_stack())
# 		else:
# 			alert_message = u"转换视频格式失败，视频文件:{}, cause:\n{}".format(ajax_path, unicode_full_stack())
# 		watchdog_alert(alert_message)
# 		raise Exception(u'转换视频格式失败')
#
#
# ######################################################
# # __save_video: 保存视频
# ######################################################
# def __save_video(ajax_file, ajax_path):
# 	try:
# 		ajax_file = ajax_file.split(',')
# 		video_content = base64.b64decode(ajax_file[1])
# 		video_file = open(ajax_path, 'wb')
# 		video_file.write(video_content)
# 		video_file.close()
# 		return True
# 	except:
# 		alert_message = u"保存原视频失败：{}, cause:\n{}".format(ajax_path, unicode_full_stack())
# 		watchdog_alert(alert_message)
# 		raise Exception(alert_message)
