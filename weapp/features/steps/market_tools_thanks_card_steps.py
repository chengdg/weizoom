# # -*- coding: utf-8 -*-
# import json
# import time
# from test import bdd_util
# from django.contrib.auth.models import User
# from market_tools.tools.test_game.models import *
# from market_tools.tools.delivery_plan.models import *
# from webapp.models import Workspace
# from mall.models import *

# @Then(u"{user}获取到商品列表")
# def step_impl(context, user):
# 	expected = json.loads(context.text)
# 	products = Product.objects.all()
# 	acturals = []
# 	for prodcut in products:
# 		actural = {}
# 		actural['name'] = prodcut.name
# 		if prodcut.is_support_make_thanks_card == 1:
# 			actural['support_make_thanks_card'] = u'是'
# 		else:
# 			actural['support_make_thanks_card'] = u'否'
# 		acturals.append(actural)

# 	bdd_util.assert_list(expected, acturals)

# @When(u"{user}设置{product_names}可以制作感恩贺卡")
# def step_impl(context, user, product_names):
# 	product_names = product_names.split(',')
# 	product_ids = []
# 	for product_name in product_names:
# 		product_name = product_name.replace("'", "")
# 		product = Product.objects.get(name=product_name)
# 		product_ids.append(str(product.id))

# 	param = ','.join(product_ids)
# 	context.client.get('/mall/api/thanks_card_products/update/?version=1&product_ids='+param)

# @Then(u"{webapp_user}获得{count}个感恩贺卡")
# def step_impl(context, webapp_user, count):
# 	thanks_card_counts = ThanksCardOrder.objects.all().count()
# 	context.tc.assertEquals(thanks_card_counts, int(count))

# @When(u"{webapp_user}制作一张贺卡")
# def step_impl(context, webapp_user):
# 	#随机选择一张贺卡进行制作
# 	context.card = json.loads(context.text)
# 	thanks_card_orders = ThanksCardOrder.objects.filter(is_used=0)
# 	make_card = thanks_card_orders[0]
# 	webapp_owner_id = context.webapp_owner_id
# 	url = '/workbench/jqm/preview/?module=market_tool:thanks_card&model=thanks_card&action=edit&workspace_id=market_tool:thanks_card&webapp_owner_id=%s&project_id=0&thanks_card_id=%d' %(webapp_owner_id, make_card.id)

# 	data = {
# 		'thanks_card_id': make_card.id,
# 		'thanks_card_img': '',
# 		'thanks_card_att_type': '',
# 		'card_content': context.card['content']
# 	}
# 	context.client.post(bdd_util.nginx(url), data)
# 	context.make_card_id = make_card.id

# @Then(u"{webapp_user}成功制作贺卡")
# def step_impl(context, webapp_user):
# 	expected = json.loads(context.text)
# 	card = ThanksCardOrder.objects.get(id=context.make_card_id)
# 	actural = {
# 		'content': card.content,
# 		'is_used': u'是' if card.is_used else u'否'
# 	}
# 	bdd_util.assert_dict(expected, actural)

# @Then(u"{webapp_user}剩余{count}张可制作贺卡")
# def step_impl(context, webapp_user, count):
# 	can_use_card_count = ThanksCardOrder.objects.filter(is_used=0).count()
# 	context.tc.assertEquals(int(count), can_use_card_count)

# @When(u"{user}对已制作贺卡修改密码")
# def step_impl(context, user):
# 	if hasattr(context, 'client'):
# 		context.client.logout()

# 	card = ThanksCardOrder.objects.get(id=context.make_card_id)
# 	url = '/mall/api/thanks_card_secret/update/?order_id=%d&secret=%s' %(card.order_id, card.thanks_secret)
# 	context.client = bdd_util.login(user)
# 	response = context.client.get(url)

# @When(u"{webapp_user}制作贺卡")
# def step_impl(context, webapp_user):
# 	webapp_owner_id = context.webapp_owner_id
# 	context.card = json.loads(context.text)

# 	thanks_card_orders = ThanksCardOrder.objects.filter(is_used=0)
# 	make_card = thanks_card_orders[0]
# 	url = '/workbench/jqm/preview/?module=market_tool:thanks_card&model=thanks_card&action=edit&workspace_id=market_tool:thanks_card&webapp_owner_id=%s&project_id=0&thanks_card_id=%d' %(webapp_owner_id, make_card.id)

# 	thanks_card_att_type = ''
# 	if context.card['type'] == u'图片':
# 		thanks_card_att_type = 'image'
# 	elif context.card['type'] == u'视频':
# 		thanks_card_att_type = 'video'
# 	att_content = context.card['att_content']
# 	card_img = context.card['card_img']
# 	data = {
# 		'thanks_card_id': make_card.id,
# 		'thanks_card_img': att_content,
# 		'thanks_card_att_type': thanks_card_att_type,
# 		'card_content': context.card['content'],
# 		'card_img': card_img,
# 		'bbd_test': True
# 	}
# 	if context.card['card_img'] == 'person.3gp':
# 		data['create_failure'] = True
# 	response = context.client.post(bdd_util.nginx(url), data)
# 	context.make_card_id = make_card.id

# @Then(u"{webapp_user}可以查看到贺卡")
# def step_impe(context, webapp_user):
# 	card = ThanksCardOrder.objects.get(id = context.make_card_id)
# 	expected = json.loads(context.text)
# 	if card.is_used == False:
# 		actural = u'制作贺卡失败'
# 		context.tc.assertEquals(expected['content'], actural)
# 	else:
# 		actural = {}
# 		if card.type == 0:
# 			actural['type'] = u'图片'
# 		elif card.type == 1:
# 			actural['type'] = u'视频'
# 		actural["content"] = card.content