#-*- coding: utf-8 -*-

__author__ = 'liupeiyu chuter'


from core.exceptionutil import unicode_full_stack
import urllib2, datetime
from account.views import save_head_img_local

from watchdog.utils import watchdog_fatal

#==============================================================================
# _download_image : 下载图片
#==============================================================================
def _download_image(image_url):
	return urllib2.urlopen(image_url).read()

#==============================================================================
# _save_head_image_local : 将头像保存到本地
#==============================================================================
def _save_head_image_local(image_content):
	date = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
	file_name = "%s.gif" % date
	file_path, relative_path = save_head_img_local(file_name, image_content)
	return relative_path

#==============================================================================
# save_weixin_user_head_img : 保存微信用户头像，给定头像url地址，保存到本地
#==============================================================================
def save_weixin_user_head_img(img_url):
	new_img_url = None

	try:
		if img_url:
			image_content = _download_image(img_url)
			new_img_url = _save_head_image_local(image_content)
	except:
		notify_message = u"将微信用户头像保存到本地失败({})，cause:\n{}".format(img_url, unicode_full_stack())
		watchdog_fatal(notify_message)

	return new_img_url

