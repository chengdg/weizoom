# -*- coding: utf-8 -*-
from utils.json_util import string_json
import json
from django.conf import settings
from weixin2.models import News

def get_news_url(news):
	'''
	获取一条图文的url
	'''
	if news.url:
		if 'model=share_red_envelope&action=get' in news.url:
			news.url = '%s&material_id=%s' % (news.url, news.material_id)
		if news.url.find('./') == 0:
			domain = 'http://%s/workbench/jqm/preview/?' % settings.DOMAIN
			return news.url.replace('./?', domain)

		if news.url.find('m/apps/') > 0 and not news.url.startswith('http') :
			if news.url.startswith('/m'):
				url = 'http://%s%s' % (settings.DOMAIN, news.url)
			else:
				url = 'http://%s/%s' % (settings.DOMAIN, news.url)
			return url

		if news.url.startswith('/apps/'):
			url = 'http://%s/m%s' % (settings.DOMAIN, news.url)
			return url

		return news.url
	else:
		return 'http://{}/weixin/message/material/news_detail/mshow/{}/'.format(settings.DOMAIN, news.id)


def get_newses_object(newses, is_complement_url=False):
	"""
	组织图文的格式
	"""
	newses_object = []
	news_count = len(newses)


	for news in newses:
		one_news = {}
		one_news['id'] = news.id
		one_news['title'] = news.title
		one_news['display_index'] = news.display_index
		one_news['type'] = 'news'
		if news_count > 0:
			one_news['text'] = string_json(news.text.encode("utf-8"))
		one_news['date'] = news.created_at.strftime('%m月%d日').strip('0')

		one_news['url'] = news.url
		if is_complement_url:
			one_news['url'] = get_news_url(news)

		if len(news.link_target) > 0:
			one_news['link_target'] = json.loads(news.link_target)
		else:
			one_news['link_target'] = ""
		one_news['pic_url'] = news.pic_url
		one_news['summary'] = string_json(news.summary)
		if news.display_index == 1:
			one_news['metadata'] = {'autoSelect':'true'};
		else:
			one_news['metadata'] = {};
		one_news['is_show_cover_pic'] = news.is_show_cover_pic
		newses_object.append(one_news)

	return news_count, newses_object


def __get_absolute_url(orig_url, user_profile):
	absolute_url = None

	path = 'workbench/jqm/preview'
	if user_profile.is_use_wepage and 'home_page' in orig_url:
		path = 'termite2/webapp_page'

	if orig_url.startswith('/apps/'):
		path = 'm'

	if orig_url.startswith('/m/'):
		absolute_url = u'http://%s%s' % (user_profile.host, orig_url)
	elif orig_url.startswith('/'):
		absolute_url = u'http://%s/%s%s' % (user_profile.host, path, orig_url)
	elif orig_url.startswith('.'):
		absolute_url = u'http://%s/%s%s' % (user_profile.host, path, orig_url[1:])
	else:
		if not orig_url.startswith('http'):
			absolute_url = u'http://%s/%s/%s' % (user_profile.host, path, orig_url)

	return absolute_url if (absolute_url is not None) else orig_url


def get_articles_object(newses):
	"""
	组织回复图文消息的格式
	"""
	articles_object = []
	news_count = len(newses)
	user_profile = None
	if news_count > 0:
		for news in newses:
			if user_profile is None:
				user_profile = news.user.get_profile()
			one_articles = {}
			one_articles['title'] = news.title
			one_articles['description'] = news.summary
			one_articles['url'] = get_news_url(news)
			one_articles['picurl'] = 'http://%s%s' % (user_profile.host, news.pic_url) if news.pic_url.find('http') == -1 else news.pic_url
			articles_object.append(one_articles)

	return articles_object


def get_material_news_info(material_id):
	"""
	获取图文消息详细信息
	"""
	material_id = int(material_id)
	news = list(News.objects.filter(material_id=material_id, is_active=True))
	return news