# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from webapp.modules.cms.models import *


#######################################################################
# __supplement_article: 补足一个文章的数据
#######################################################################
def __supplement_article(article):
	article_prototype = {
		"category" : "",
		"content" :	"<p>内容1<br/></p>",
		"summary" : "摘要1",
		"title" : "文章1"
	}

	article_prototype.update(article)

	#处理分类
	category_name = article_prototype['category']
	if category_name:
		category = Category.objects.get(name=category_name)
		article_prototype['category'] = category.id
	else:
		article_prototype['category'] = -1

	return article_prototype


#######################################################################
# __add_product: 添加一个文章
#######################################################################
def __add_article(context, article):
	article = __supplement_article(article)
	response = context.client.post('/cms/editor/article/create/', article)


@when(u"{user}添加文章")
def step_impl(context, user):
	client = context.client
	context.articles = json.loads(context.text)
	for article in context.articles:
		__add_article(context, article)
		time.sleep(1)


@then(u"{user}能获取文章'{article_title}'")
def step_impl(context, user, article_title):
	existed_article = Article.objects.get(title=article_title)
	response = context.client.get('/cms/editor/article/update/%d/' % existed_article.id)
	article = response.context['article']

	#处理category	
	categories = response.context['categories']
	category_name = ''
	for category in categories:
		if hasattr(category, 'is_selected') and category.is_selected:
			category_name = category.name
			break

	actual = {
		"title": article.title,
		"content": article.content,
		"summary": article.summary,
		'category': category_name,
	}
	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)
	

# @then(u"{user}找不到文章'{article_name}'")
# def step_impl(context, user, article_name):
# 	context.tc.assertEquals(0, article.objects.filter(name=article_name).count())
	

@then(u"{user}能获取文章列表")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client

	response = client.get('/cms/api/articles/get/?version=1&count_per_page=50&page=1')

	data = json.loads(response.content)['data']
	if hasattr(context, 'caller_step_text'):
		expected = json.loads(context.caller_step_text)
	else:
		expected = json.loads(context.text)
	actual = data['items']
	bdd_util.assert_list(expected, actual)


@then(u"{user}能获取文章列表'{product_list}'")
def step_impl(context, user, product_list):
	context.caller_step_text = product_list
	context.execute_steps(u"then %s能获取文章列表" % user)


# @when(u"{user}'{direction}'调整'{article_name}'")
# def step_impl(context, user, direction, article_name):
# 	products = list(article.objects.all())
# 	products.sort(lambda x,y: cmp(y.display_index, x.display_index))

# 	index = 0
# 	src_product = None
# 	for i, article in enumerate(products):
# 		if article_name == article.name:
# 			index = i
# 			src_product = article
# 			break

# 	if direction == 'up':
# 		dst_product = products[index-1]
# 	else:
# 		dst_product = products[index+1]

# 	client = context.client
# 	client.get('/mall/api/product_display_index/update/?version=1&src_id=%d&dst_id=%d' % (src_product.id, dst_product.id))


# @when(u"{user}置顶文章'{article_name}'")
# def step_impl(context, user, article_name):
# 	article = ProductFactory(name=article_name)

# 	client = context.client
# 	url = '/mall/api/product_display_index/update/?version=1&src_id=%d&dst_id=0' % article.id
# 	client.get(url)


# @when(u"{user}更新文章'{article_name}'")
# def step_impl(context, user, article_name):
# 	existed_product = ProductFactory(name=article_name)

# 	article = json.loads(context.text)
# 	__process_product_data(article)
# 	article = __supplement_article(article)

# 	url = '/mall/editor/article/update/%d/' % existed_product.id
# 	context.client.post(url, article)

# @when(u"{user}删除文章'{article_name}'")
# def step_impl(context, user, article_name):
# 	article = ProductFactory(name=article_name)
# 	url = '/mall/editor/article/delete/%d/' % article.id
# 	context.client.get(url)