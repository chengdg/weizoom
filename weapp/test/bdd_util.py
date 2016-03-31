# -*- coding: utf-8 -*-
import json
#import time
from datetime import datetime, timedelta
import re

from django.test.client import Client
from django.http import SimpleCookie
from django.contrib.auth.models import User
#from django.db.models import Model
#from webapp.modules.mall.models import *
from mall.models import *
from webapp.models import *
from account.models import UserProfile
from weapp import settings
from modules.member import models as member_models
from mall import models as mall_models
from market_tools.tools.channel_qrcode import models as channel_qrcode_models
from market_tools.tools.lottery import models as lottery_models

from utils.dateutil import get_current_date

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



def login(user, password=None, **kwargs):
	"""
	登录系统
	"""
	if not password:
		password = 'test'

	if 'context' in kwargs:
		context = kwargs['context']
		if hasattr(context, 'client'):
			if context.client.user.username == user:
				#如果已经登录了，且登录用户与user相同，直接返回
				#return context.client
				context.client.logout()
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


def get_webapp_id_for(username):
	"""
	获取user对应的webapp id
	"""
	user = User.objects.get(username=username)
	profile = UserProfile.objects.get(user=user)
	return profile.webapp_id


def get_webapp_id_via_owner_id(owner_id):
	"""
	获取user对应的webapp id
	"""
	user = User.objects.get(id=owner_id)
	profile = UserProfile.objects.get(user=user)
	return profile.webapp_id


def get_user_id_for(username):
	"""
	获取username对应的user的id
	"""
	return User.objects.get(username=username).id


def get_member_for(username, webapp_id):
	"""
	获取username对应的会员
	"""
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

def get_member_by_username(username, webapp_id):
	"""
	获取username对应的会员
	"""
	from utils.string_util import byte_to_hex
	if isinstance(username, unicode):
		member_nickname_str = username.encode('utf-8')
	else:
		member_nickname_str = username
	username_hexstr = byte_to_hex(member_nickname_str)
	try:
		return member_models.Member.objects.get(webapp_id=webapp_id, username_hexstr=username_hexstr)
	except:
		return None

def get_order_by_order_no(order_no):
	return mall_models.Order.objects.get(order_id=order_no)


def use_webapp_template(webapp_owner_name, template_name):
	"""
	为webapp_owner_name模板webapp的模板
	"""
	webapp_owner_id = get_user_id_for(webapp_owner_name)
	Workspace.objects.filter(owner_id=webapp_owner_id, inner_name='home_page').update(template_name=template_name)


def get_project_id_for_webapp_owner(username, workspace_name):
	"""
	获取username对应的webapp的简约风尚的模板project的id
	"""
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


def nginx(url):
	"""
	模拟nginx的转换
	"""
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


def assert_dict(expected, actual):
	"""
	验证expected中的数据都出现在了actual中
	"""
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


def assert_list(expected, actual, options=None):
	"""
	验证expected中的数据都出现在了actual中
	"""
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


def assert_api_call_success(response):
	"""
	验证api调用成功
	"""
	if '<!DOCTYPE html>' in response.content:
		assert False, "NOT a valid json string, call api FAILED!!!!"
	else:
		content = json.loads(response.content)
		assert 200 == content['code'], "code != 200, call api FAILED!!!!"
		return content


def print_json(obj):
	"""
	将对象以json格式输出
	"""
	print json.dumps(obj, indent=True)


def get_date(str):
	"""
		将字符串转成datetime对象
		今天 -> 2014-4-18
	"""
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
		tmp = str.split(' ')
		if len(tmp) == 1:
			strp = "%Y-%m-%d"
		elif len(tmp[1]) == 8:
			strp = "%Y-%m-%d %H:%M:%S"
		elif len(tmp[1]) == 5:
			strp = "%Y-%m-%d %H:%M"
		return datetime.strptime(str, strp)

	return today + timedelta(delta)

def get_date_to_time_interval (str):
	"""
		将如下格式转化为字符串形式的时间间隔
		今天 -> 2014-2-13|2014-2-14
		"3天前-1天前" 也转为相同的格式
	"""
	date_interval = None
	if u'-' in str:
		m = re.match(ur"(\d*)([\u4e00-\u9fa5]{1,2})[-](\d*)([\u4e00-\u9fa5]{1,2})", unicode(str))
		result = m.group(1, 2, 3, 4)
		if result:
			if result[1] == u'天前' and result[3] == u'天前':
				date_interval = "%s|%s" % (datetime.strftime(datetime.now()-timedelta(days=int(result[0])), "%Y-%m-%d"), datetime.strftime(datetime.now() - timedelta(days=int(result[2])),"%Y-%m-%d"))
			if result[1] == u'天前' and result[2] == u'' and result[3] == u'今天':
				date_interval = "%s|%s" % (datetime.strftime(datetime.now() - timedelta(days=int(result[0])),"%Y-%m-%d"), datetime.strftime(datetime.now(),"%Y-%m-%d"))
			if result[1] == u'今天' and result[3] == u'明天':
				date_interval = "%s|%s" % (datetime.strftime(datetime.now(), "%Y-%m-%d"), datetime.strftime(datetime.now() + timedelta(days=1),"%Y-%m-%d"))
	return date_interval

#def parse_datetime(str):
#	return datetime.strptime(str, "%Y/%m/%d %H:%M:%S")

def get_date_str(str):
	date = get_date(str)
	return date.strftime('%Y-%m-%d')

def get_datetime_str(str):
	"""保留小时数
	"""
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


def get_coupon(coupon_rule_name, member):
	"""
	根据优惠券规则名称返回对应de优惠券
	"""
	from mall.promotion.models import CouponRule, Coupon
	coupon_rule = CouponRule.objects.get(name=coupon_rule_name)
	return Coupon.objects.get(member_id=member.id, coupon_rule_id=coupon_rule.id)


def get_channel_qrcode_setting(channel_qrcode_name):
	"""
	根据名字获取ChannelQrcodeSetting对象
	"""
	settings = channel_qrcode_models.ChannelQrcodeSettings.objects.filter(name=channel_qrcode_name)
	if len(settings) > 0:
		return settings[0]
	return None

def get_lottery_setting(name):
	"""
	根据名字获取Lottery对象
	"""
	settings = lottery_models.Lottery.objects.filter(name=name)
	if len(settings) > 0:
		return settings[0]
	return None



def escape_date_string(str):
	"""
	日期字符串转义

	eg: $(今天) ==> '2015-06-24'
	"""
	# TODO: to be optimized
	print("str: {}".format(str))
	str = re.sub(ur"\$\(今天\)", get_current_date(), str)
	#str = re.sub(r'\$\(今天\+1\)', get_current_date(), str)
	return str


def judge_date_today_for_meanning(str):
	local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
	if local_date == str:
		return u'今天'
	else:
		return  u'其他'