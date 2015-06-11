# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from django.test.client import Client
from django.http import SimpleCookie
from django.contrib.auth.models import User
from django.db.models import Model
from mall.models import *
from webapp.models import *
from account.models import UserProfile
from weapp import settings
from modules.member import models as member_models
from mall import models as mall_models

tc = None

BOUNDARY = 'BoUnDaRyStRiNg'
MULTIPART_CONTENT = 'multipart/form-data; boundary=%s' % BOUNDARY

class WeappClient(Client):
	def __init__(self, enforce_csrf_checks=False, **defaults):
		super(WeappClient, self).__init__(**defaults)

	def request(self, **request):
		if settings.DUMP_TEST_REQUEST:
			print '\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
			print '{{{ request'

		response = super(WeappClient, self).request(**request)

		if settings.DUMP_TEST_REQUEST:
			print '}}}'
			print '\n{{{ response'
			print self.cookies
			print '}}}'
			print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
		return response


	def reset(self):
		self.cookies = SimpleCookie()
		if hasattr(self, 'user'):
			self.user = User()



###########################################################################
# login: 登录系统
###########################################################################
def login(user, password=None, **kwargs):
	if not password:
		password = 'test'

	if 'context' in kwargs:
		context = kwargs['context']
		if hasattr(context, 'client'):
			if context.client.user.username == user:
				#如果已经登录了，且登录用户与user相同，直接返回
				return context.client
			else:
				#如果已经登录了，且登录用户不与user相同，退出登录
				context.client.logout()

	client = WeappClient(HTTP_USER_AGENT='WebKit MicroMessenger Mozilla')
	client.login(username=user, password='test')
	client.user = User.objects.get(username=user)
	client.user.profile = UserProfile.objects.get(user=client.user)

	if 'context' in kwargs:
		context = kwargs['context']
		context.client = client
		context.webapp_owner_id = client.user.id
		context.webapp_id = client.user.profile.webapp_id

	return client


###########################################################################
# get_webapp_id_for: 获取user对应的webapp id
###########################################################################
def get_webapp_id_for(username):
	user = User.objects.get(username=username)
	profile = UserProfile.objects.get(user=user)
	return profile.webapp_id


###########################################################################
# get_user_id_for: 获取username对应的user的id
###########################################################################
def get_user_id_for(username):
	return User.objects.get(username=username).id


###########################################################################
# get_member_for: 获取username对应的会员
###########################################################################
def get_member_for(username, webapp_id):
	from utils.string_util import byte_to_hex
	if isinstance(username, unicode):
		member_nickname_str = username.encode('utf-8')
	else:
		member_nickname_str = username
	username_hexstr = byte_to_hex(member_nickname_str)
	try:
		return member_models.Member.objects.get(webapp_id=webapp_id, username_hexstr=username_hexstr)
	except:
		member = member_models.Member(id=1, grade_id=0)
		return member

def get_order_by_order_no(order_no):
	return mall_models.Order.objects.get(order_id=order_no)


###########################################################################
# use_webapp_template: 为webapp_owner_name模板webapp的模板
###########################################################################
def use_webapp_template(webapp_owner_name, template_name):
	webapp_owner_id = get_user_id_for(webapp_owner_name)
	Workspace.objects.filter(owner_id=webapp_owner_id, inner_name='home_page').update(template_name=template_name)


###########################################################################
# get_project_id_for_webapp_owner: 获取username对应的webapp的简约风尚的模板project的id
###########################################################################
def get_project_id_for_webapp_owner(username, workspace_name):
	user = User.objects.get(username=username)
	workspace = Workspace.objects.get(owner=user, inner_name=workspace_name)
	project = Project.objects.get(workspace=workspace, inner_name='simple_fashion')
	return project.id


def get_ship_area_id_for(ship_area_str):
	from tools.regional.models import Province, City, District
	if ship_area_str:
		areas = ship_area_str.split(' ')
	else:
		areas = '北京市 北京市 海淀区'.split(' ')

	if len(areas) > 0:
		pros = Province.objects.filter(
			name = areas[0]
		)
		pro_count = pros.count()
		if pro_count == 0:
			province = Province.objects.create(
				name = areas[0]
			)
			pro_id = province.id
		else:
			pro_id = pros[0].id
		ship_area = str(pro_id)
	if len(areas) > 1:
		cities = City.objects.filter(
			name = areas[1]
		)
		city_count = cities.count()
		if city_count == 0:
			city = City.objects.create(
				name=areas[1],
				zip_code = '',
				province_id = pro_id
			)
			city_id = city.id
		else:
			city_id = cities[0].id
		ship_area = ship_area + '_' + str(city_id)
	if len(areas) > 2:
		dis = District.objects.filter(
			name = areas[2]
		)
		dis_count = dis.count()
		if dis_count == 0:
			district = District.objects.create(
				name = areas[2],
				city_id = city_id
			)
			ship_area = ship_area + '_' + str(district.id)
		else:
			ship_area = ship_area + '_' + str(dis[0].id)

	return ship_area


###########################################################################
# nginx: 模拟nginx的转换
###########################################################################
def nginx(url):
	if url.startswith('/workbench/'):
		return '/termite%s' % url
	else:
		return url

def convert_to_same_type(a, b):
	def to_same_type(target, other):
		target_type = type(target)
		other_type = type(other)
		if other_type == target_type:
			return True, target, other

		if (target_type == int) or (target_type == float):
			try:
				other = target_type(other)
				return True, target, other
			except:
				return False, target, other

		return False, target, other

	is_success, new_a, new_b = to_same_type(a, b)
	if is_success:
		return new_a, new_b
	else:
		is_success, new_b, new_a = to_same_type(b, a)
		if is_success:
			return new_a, new_b

	return a, b


###########################################################################
# assert_dict: 验证expected中的数据都出现在了actual中
###########################################################################
def assert_dict(expected, actual):
	global tc
	is_dict_actual = isinstance(actual, dict)
	for key in expected:
		expected_value = expected[key]
		if is_dict_actual:
			actual_value = actual[key]
		else:
			actual_value = getattr(actual, key)

		if isinstance(expected_value, dict):
			assert_dict(expected_value, actual_value)
		elif isinstance(expected_value, list):
			assert_list(expected_value, actual_value, {'key': key})
		else:
			expected_value, actual_value = convert_to_same_type(expected_value, actual_value)
			try:
				tc.assertEquals(expected_value, actual_value)
			except:
				print '      Compare Dict Key: ', key
				raise


###########################################################################
# assert_list: 验证expected中的数据都出现在了actual中
###########################################################################
def assert_list(expected, actual, options=None):
	global tc
	try:
		tc.assertEquals(len(expected), len(actual), 'list length DO NOT EQUAL: %d != %d' % (len(expected), len(actual)))
	except:
		if options and 'key' in options:
			print '      Outer Compare Dict Key: ', options['key']
		raise

	for i in range(len(expected)):
		expected_obj = expected[i]
		actual_obj = actual[i]
		if isinstance(expected_obj, dict):
			assert_dict(expected_obj, actual_obj)
		else:
			expected_obj, actual_obj = convert_to_same_type(expected_obj, actual_obj)
			tc.assertEquals(expected_obj, actual_obj)


###########################################################################
# assert_api_call_success: 验证api调用成功
###########################################################################
def assert_api_call_success(response):
	if '<!DOCTYPE html>' in response.content:
		assert False, "NOT a valid json string, call api FAILED!!!!"
	else:
		content = json.loads(response.content)
		assert 200 == content['code'], "code != 200, call api FAILED!!!!"


###########################################################################
# print_json: 将对象以json格式输出
###########################################################################
def print_json(obj):
	print json.dumps(obj, indent=True)


def get_date(str):
	#处理expected中的参数
	today = datetime.now()
	if str == u'今天':
		delta = 0
	elif str == u'昨天':
		delta = -1
	elif str == u'前天':
		delta = -2
	elif str == u'明天':
		delta = 1
	elif str == u'后天':
		delta = 2
	elif u'天后' in str:
		delta = int(str[:-2])
	elif u'天前' in str:
		delta = 0-int(str[:-2])
	else:
		return str

	return today + timedelta(delta)


def get_date_str(str):
	date = get_date(str)
	return date.strftime('%Y-%m-%d')

def get_datetime_str(str):
	date = get_date(str)
	return '%s 00:00:00' % date.strftime('%Y-%m-%d')

def get_datetime_no_second_str(str):
	date = get_date(str)
	return '%s 00:00' % date.strftime('%Y-%m-%d')


def get_order_has_product(order_code, product_name):
    def _get_product_model_name(product_model_names):
        from mall.models import ProductModelPropertyValue
        if product_model_names != "standard":
            pro_id, id = product_model_names.split(":")
            i = ProductModelPropertyValue.objects.get(id=id, property_id=pro_id)
            return i.name
    order = mall_models.Order.objects.get(order_id=order_code)

    # 商品是否包含规格
    if ":" in product_name:
        product_name, product_model_name = product_name.split(":")

    order_has_product_list = mall_models.OrderHasProduct.objects.filter(
            order_id=order.id,
            product_name=product_name)
    # 如果商品不包含规格
    if order_has_product_list.count() == 1:
        return order_has_product_list[0]
    # 如果商品包含规格
    else:
        # 查找到包含此规格的order_has_product
        for i in order_has_product_list:
            the_product_model_name = _get_product_model_name(i.product_model_name)
            if product_model_name in the_product_model_name:
                return i

def get_product_review(order_code, product_name):
    order_has_product = get_order_has_product(order_code, product_name)
    product_review = mall_models.ProductReview.objects.get(
        order_has_product_id=order_has_product.id
    )
    return product_review


def get_product_by(product_name):
    product = mall_models.Product.objects.get(name=product_name)
    return product
