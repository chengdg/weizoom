# -*- coding: utf-8 -*-

#启用gevent
# from gevent import monkey
# monkey.patch_all(
# 	socket=True,
# 	dns=True,
# 	time=True,
# 	select=True,
# 	thread=True,
# 	os=True,
# 	ssl=True,
# 	httplib=False,
# 	aggressive=True
# )

#
# 配置，使behave能使用django的model
#
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'weapp.settings'

import sys
path = os.path.abspath(os.path.join('.', '..'))
sys.path.insert(0, path)

import unittest
import time
from pymongo import Connection

from weapp import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test.client import Client
from django.test.utils import setup_test_environment as setup_django_test_environment
from django.db.models import Q

from features.testenv.model_factory import *
from account import models as account_models
from webapp import models as webapp_models
from product import models as weapp_product_models
#from mall import models as mall_models
from mall import models as mall_models
from mall.promotion import models as promotion_models
from webapp.modules.cms import models as cms_models
from watchdog import models as watchdog_models
from weixin.user import models as weixin_user_models
from weixin.message.qa import models as weixin_qa_models
from weixin.message.material import models as weixin_material_models
from product import module_api as weapp_product_api
from auth import models as auth_models

from account.social_account.models import SocialAccount
from modules.member import models as member_models
#from watchdog import models as watchdog_models
from market_tools.tools.delivery_plan import models as delivery_models
from market_tools.tools.activity import models as activity_models
from market_tools.tools.red_envelope import models as red_envelope_models
from market_tools.tools.point_card import models as point_card_models
from market_tools.tools.vote import models as vote_models
from market_tools.tools.test_game import models as test_game_models
from market_tools.tools.store import models as store_models
from market_tools.tools.lottery import models as lottery_models
from market_tools.tools.channel_qrcode import models as channel_qrcode_models
from market_tools.tools.member_qrcode import models as member_qrcode_models
from weixin2 import models as weixin2_models
from stats import models as stats_models
from modules.member import models as modules_member_models

from selenium import webdriver
from test.pageobject.page_frame import PageFrame
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.chrome.options import Options
from apps import models as customized
from apps import apps_manager

from django.core.cache import cache
from weapp import celeryconfig
from termite2 import models as termite2_models


def add_touch_support_in_selenium():
	"""
	HACK: add touch support into selenium
	"""
	from selenium.webdriver.remote.webelement import WebElement
	def inner_func(self, element_will_be_delete=False):
		driver = self.parent
		script = "arguments[0].setAttribute('selenium-focus', 'true')"
		driver.execute_script(script, self)

		script = "$('[selenium-focus]').trigger('touchstart')"
		driver.execute_script(script)

		if not element_will_be_delete:
			script = "$('[selenium-focus]').trigger('touchend')"
			driver.execute_script(script)

			script = "$('arguments[0].removeAttribute('selenium-focus')"
			driver.execute_script(script, self)
	WebElement.touch = inner_func

add_touch_support_in_selenium()


def enhance_selenium_webdriver_webelement():
	from selenium.webdriver.chrome.webdriver import WebDriver
	WebDriver.f = WebDriver.find_element_by_css_selector
	WebDriver.fs = WebDriver.find_elements_by_css_selector

	from selenium.webdriver.remote.webelement import WebElement
	WebElement.f = WebElement.find_element_by_css_selector
	WebElement.fs = WebElement.find_elements_by_css_selector

	def attr(self, attr_name):
		return self.get_attribute(attr_name).strip()
	WebElement.attr = attr

	def val(self):
		return self.get_attribute('value').strip()
	WebElement.val = val

enhance_selenium_webdriver_webelement()


def __clear_all_account_data():
	"""
	清空账号数据
	"""
	User.objects.filter(id__gt=2).delete()

	#会员
	member_models.MemberGrade.objects.all().delete()
	SocialAccount.objects.all().delete()
	member_models.WebAppUser.objects.all().delete()
	member_models.Member.objects.all().delete()
	member_models.MemberFollowRelation.objects.all().delete()
	member_models.IntegralStrategySttings.objects.all().delete()

	#webapp
	webapp_models.GlobalNavbar.objects.all().delete()

	# 粉丝数据
	weixin2_models.FanCategory.objects.all().delete()


def __clear_all_app_data():
	"""
	清空应用数据
	"""
	#webapp
	member_models.ShipInfo.objects.all().delete()
	webapp_models.PageVisitLog.objects.all().delete()
	webapp_models.PageVisitDailyStatistics.objects.all().delete()

	#watchdog
	watchdog_models.Message.objects.all().delete()

	#cms
	cms_models.CategoryHasArticle.objects.all().delete()
	cms_models.Category.objects.all().delete()
	cms_models.Article.objects.all().delete()

	#促销
	promotion_models.Promotion.objects.all().delete()
	promotion_models.FlashSale.objects.all().delete()
	promotion_models.PriceCut.objects.all().delete()
	promotion_models.PremiumSale.objects.all().delete()
	promotion_models.IntegralSale.objects.all().delete()

	#商城
	mall_models.PayInterface.objects.all().delete()
	account_models.UserWeixinPayOrderConfig.objects.all().delete()

	mall_models.Image.objects.all().delete()
	mall_models.ImageGroup.objects.all().delete()
	mall_models.ProductProperty.objects.all().delete()
	mall_models.TemplateProperty.objects.all().delete()
	mall_models.ProductPropertyTemplate.objects.all().delete()
	mall_models.PostageConfig.objects.filter(~Q(name=u'免运费')).delete()
	mall_models.PostageConfig.objects.all().update(is_used=True)
	mall_models.ProductModelPropertyValue.objects.all().delete()
	mall_models.ProductModelProperty.objects.all().delete()
	mall_models.ProductModel.objects.all().delete()
	mall_models.ProductCategory.objects.all().delete()
	mall_models.ProductSwipeImage.objects.all().delete()
	mall_models.Product.objects.all().delete()
	mall_models.Order.objects.all().delete()
	mall_models.OrderHasProduct.objects.all().delete()
	mall_models.OrderHasPromotion.objects.all().delete()
	mall_models.OrderOperationLog.objects.all().delete()
	mall_models.WeizoomMall.objects.all().delete()
	mall_models.ShoppingCart.objects.all().delete()
	mall_models.MallCounter.objects.all().delete()
	mall_models.MemberProductWishlist.objects.all().delete()
	mall_models.OrderReview.objects.all().delete()
	mall_models.ProductReview.objects.all().delete()
	mall_models.ProductReviewPicture.objects.all().delete()

	#权限
	auth_models.UserHasPermission.objects.all().delete()
	auth_models.UserHasGroup.objects.all().delete()
	auth_models.GroupHasPermission.objects.all().delete()
	auth_models.SystemGroup.objects.all().delete()
	auth_models.DepartmentHasUser.objects.all().delete()
	auth_models.Department.objects.all().delete()

	#会员
	#member_models.MemberGrade.objects.all().update(usable_integral_percentage_in_order=100)
	#member_models.WebAppUser.objects.all().delete()
	#member_models.MemberGrade.objects.all().delete()
	member_models.Member.objects.all().delete()
	member_models.MemberFollowRelation.objects.all().delete()
	member_models.MemberSharedUrlInfo.objects.all().delete()
	member_models.Member.objects.all().delete()

	#自动回复消息
	weixin_qa_models.Rule.objects.all().delete()
	weixin_material_models.News.objects.all().delete()
	weixin_material_models.Material.objects.all().delete()

	#优惠券
	promotion_models.Coupon.objects.all().delete()
	promotion_models.CouponRule.objects.all().delete()
	# promotion_models.CouponConfig.objects.all().delete()
	# promotion_models.CouponSallerDate.objects.all().delete()

	#配送套餐
	delivery_models.DeliveryPlan.objects.all().delete()

	#趣味测试
	test_game_models.TestGame.objects.all().delete()
	test_game_models.TestGameQuestion.objects.all().delete()
	test_game_models.TestGameQuestionAnswer.objects.all().delete()
	test_game_models.TestGameResult.objects.all().delete()
	test_game_models.TestGameRecord.objects.all().delete()

	#门店管理
	store_models.Store.objects.all().delete()
	store_models.StoreSwipeImage.objects.all().delete()

	#activity
	activity_models.Activity.objects.all().delete()

	#red_envelope
	red_envelope_models.RedEnvelope.objects.all().delete()

	#积分
	point_card_models.PointCardRule.objects.all().delete()
	point_card_models.PointCard.objects.all().delete()

	#微信投票
	vote_models.Vote.objects.all().delete()
	vote_models.VoteOption.objects.all().delete()
	vote_models.VoteOptionHasWebappUser.objects.all().delete()

	# 微信抽奖
	lottery_models.Lottery.objects.all().delete()
	lottery_models.LotteryHasPrize.objects.all().delete()
	lottery_models.LotteryRecord.objects.all().delete()

	# 渠道扫码
	channel_qrcode_models.ChannelQrcodeSettings.objects.all().delete()
	channel_qrcode_models.ChannelQrcodeHasMember.objects.all().delete()

	# 会员扫码
	member_qrcode_models.MemberQrcode.objects.all().delete()
	member_qrcode_models.MemberQrcodeLog.objects.all().delete()
	modules_member_models.MemberMarketUrl.objects.all().delete()

	# 店铺装修
	termite2_models.TemplateCustomModule.objects.all().delete()

	#watchdog
	watchdog_models.Message.objects.all().delete()

	#统计方面的
	stats_models.BrandValueHistory.objects.all().delete()

	# 缓存
	cache.clear()



def __binding_wexin_mp_account(user=None):
	"""
	绑定公众号
	"""
	account_models.UserProfile.objects.all().update(is_mp_registered=True)

	if user:
		count = weixin_user_models.WeixinMpUser.objects.filter(owner=user).count()
		if count == 0:
			mpuser = weixin_user_models.WeixinMpUser.objects.create(
				owner = user,
				username = '',
				password= '',
				is_certified = True,
				is_service = True,
				is_active = True
			)
	
			weixin_user_models.WeixinMpUserAccessToken.objects.create(mpuser=mpuser, is_active=True,app_id=user.id, app_secret='app_secret',  access_token='access_token')
			weixin_user_models.MpuserPreviewInfo.objects.create(mpuser=mpuser, name=mpuser.username)
		else:
			weixin_user_models.WeixinMpUser.objects.filter(owner=user).update(is_certified=True, is_service=True, is_active=True)


def __sync_workspace():
	"""
	同步workspace
	"""
	if webapp_models.Workspace.objects.count() > 0:
		print('[environment]: NO need to sync workspace')
		return

	#清理mongo
	print('************* clear MONGODB *************')
	print(settings.PAGE_STORE_SERVER_HOST)
	connection = Connection(settings.PAGE_STORE_SERVER_HOST, settings.PAGE_STORE_SERVER_PORT)
	connection.drop_database(settings.PAGE_STORE_DB)

	#清理数据库
	weapp_product_models.Product.objects.all().delete()
	webapp_models.Workspace.objects.all().delete()
	webapp_models.Project.objects.all().delete()

	client = Client()
	client.login(username='manager', password='test')
	data = {
		'modules_info': '{"modules":["cms","mall","user_center","viper_workspace_home_page"],"allow_update":false}'
	}
	response = client.post('/webapp/api/workspace/sync/', data)


def __create_weapp_product():
	"""
	创建weapp product
	"""
	if weapp_product_models.Product.objects.count() > 0:
		print('[environment]: NO need to create weapp product')
		return

	weapp_product_models.Product.objects.all().delete()

	manager = User.objects.get(username='manager')
	workspace_ids = ','.join([str(workspace.id) for workspace in webapp_models.Workspace.objects.filter(owner=manager)])
	market_tool_names = 'vote,member_qrcode,research,activity,coupon,lottery,complain,test_game,red_envelope,delivery_plan,point_card,channel_qrcode,thanks_card,weizoom_card,store,template_message'

	weapp_product_models.Product.objects.create(
		name = u'完整版',
		max_mall_product_count = 100,
		price = 100,
		webapp_modules = workspace_ids,
		market_tool_modules = market_tool_names,
		footer = 0
	)



def __create_system_user(username):
	"""
	创建系统用户
	"""
	start = time.time()
	user = UserFactory.create(username=username)
	product = weapp_product_models.Product.objects.get(name=u'完整版')
	weapp_product_api.install_product_for_user(user, product.id)
	__binding_wexin_mp_account(user)

	"""
	临时方案：解决 benchi 没有会员等级情况
	"""
	__create_member_grade(user)
	return user

def __create_member_grade(user):
	member_models.MemberGrade.get_default_grade(user.get_profile().webapp_id)
	# member_grade = member_models.MemberGrade.objects.create(name=u'银牌会员', webapp_id=user.get_profile().webapp_id, upgrade_lower_bound=0)
	# member_grade = member_models.MemberGrade.objects.create(name=u'金牌会员', webapp_id=user.get_profile().webapp_id, upgrade_lower_bound=0)

def __create_system_member(username, user):
	"""
	创建系统会员
	"""
	#创建社会化帐号信息
	social_account = __create_social_account(username, user)
	#创建对应会员信息
	member = __create_member(username, social_account)
	__create_member_has_social(member, social_account)

	return member


def __create_social_account(username, user):
	return SocialAccount.objects.create(
			webapp_id = user.get_profile().webapp_id,
			openid = 'openid%s' % username,
			token = 'token%s' % username,
			is_for_test = False
		)

def __create_member(username, social_account):
	member_grade = member_models.MemberGrade.objects.create(name='grade1', webapp_id=social_account.webapp_id, upgrade_lower_bound=0)

	from utils.string_util import byte_to_hex
	if isinstance(username, unicode):
		member_nickname_str = username.encode('utf-8')
	else:
		member_nickname_str = username
	username_hexstr = byte_to_hex(member_nickname_str)

	return 	member_models.Member.objects.create(
		webapp_id = social_account.webapp_id,
		token = 'token-%s' % username,
		user_icon = '',
		username_hexstr = username_hexstr,
		grade = member_grade,
		remarks_name = '',
		is_for_test = social_account.is_for_test
	)

def __create_member_has_social(member, social_account):
	member_models.MemberHasSocialAccount.objects.create(
			member = member,
			account = social_account,
			webapp_id = member.webapp_id
			)

def __create_member_follow_relation(member_A, member_B, is_fans=False):
	member_models.MemberFollowRelation.objects.create(member_id=member_A.id, follower_member_id=member_B.id, is_fans=is_fans)
	member_models.MemberFollowRelation.objects.create(member_id=member_B.id, follower_member_id=member_A.id)


def __create_simulator_user():
	from simulator.models import SimulatorUser
	if SimulatorUser.objects.all().count() > 0:
		print('[environment]: NO need to create simulator user')
		return

	from account.management.commands.init_simulator_user import Command
	command = Command()
	command.handle()

def __create_shengjing_app():
	user = User.objects.get(username='jobs')
	app = customized.CustomizedApp.objects.create(owner=user, name='shengjing', display_name='shengjing', status=3, last_version=1, updated_time=datetime.now(), created_at=datetime.now())
	customized.CustomizedAppInfo.objects.create(
		owner=user,
		customized_app=app,
		app_name='shengjing',
		repository_path='',
		repository_username='',
		repository_passwd=''
	)
	apps_manager.manager.start_app(app)


def __update_template_to_v3():
	webapp_models.Workspace.objects.filter(inner_name='home_page').update(backend_template_name='default_v3')
	account_models.UserProfile.objects.all().update(backend_template_name='default_v3')


def before_all(context):
	__clear_all_account_data()
	__binding_wexin_mp_account()
	__sync_workspace()
	__create_weapp_product()
	__create_system_user('jobs')
	__create_system_user('nokia')
	user_bill = __create_system_user('bill')
	__create_system_user('tom')
	# __create_system_user('weizoom')
	# __create_system_user('tom1')
	# __create_system_user('tom2')
	# __create_system_user('tom3')
	# __create_system_user('tom4')
	# __create_system_user('tom5')
	# __create_system_user('tom6')
	__create_simulator_user()
	user_guo = __create_system_user('guo')
	__create_system_user('manager')
	#call_command('loaddata', 'regional')
	__create_shengjing_app()
	__update_template_to_v3()

	# member_A = __create_system_member(u'A',user_guo)
	# member_B = __create_system_member(u'B',user_guo)
	# member_C = __create_system_member(u'C',user_guo)

	#__create_member_follow_relation(member_A, member_B, True)

	#创建test case，使用assert
	context.tc = unittest.TestCase('__init__')
	from test import bdd_util
	bdd_util.tc = context.tc

	#设置django为测试状态
	setup_django_test_environment()

	#为model instance安装__getitem__，方便测试
	enhance_django_model_class()

	#设置bdd模式
	settings.IS_UNDER_BDD = True

	#设置event dispatcher为local
	settings.EVENT_DISPATCHER = 'local'

	#关闭profiling middle
	settings.ENABLE_PROFILE = False

	# 让Celery以同步方式运行
	celeryconfig.CELERY_ALWAYS_EAGER = True


def after_all(context):
	pass


def before_scenario(context, scenario):
	is_ui_test = False
	for tag in scenario.tags:
		if tag.startswith('ui-') or tag == 'ui':
			is_ui_test = True
			break

	if is_ui_test:
		#创建浏览器
		print('[before scenario]: init browser driver')
		chrome_options = Options()
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument("--disable-plugins")
		driver = webdriver.Chrome(chrome_options=chrome_options)
		driver.implicitly_wait(3)
		context.driver = driver

	__clear_all_app_data()

	from utils import cache_util
	cache_util.clear_db()


def after_scenario(context, scenario):
	if hasattr(context, 'client') and context.client:
		context.client.logout()

	if hasattr(context, 'driver') and context.driver:
		print('[after scenario]: close browser driver')
		page_frame = PageFrame(context.driver)
		page_frame.logout()
		context.driver.quit()

	if hasattr(context, 'webapp_driver') and context.driver:
		print('[after scenario]: close webapp browser driver')
		context.webapp_driver.quit()


def enhance_django_model_class():
	"""
	为Django model添加__getitem__
	"""
	from django.db.models import Model

	#def model_getitem(self, key):
	#	return getattr(self, key)
	#Model.__getitem__ = model_getitem

	def model_todict(self, *attrs):
		columns = [field.get_attname() for field in self._meta.fields]
		result = {}
		for field in self._meta.fields:
			result[field.get_attname()] = field.value_from_object(self)
		for attr in attrs:
			result[attr] = getattr(self, attr, None)
		return result
	Model.to_dict = model_todict
