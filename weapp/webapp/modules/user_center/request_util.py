# -*- coding: utf-8 -*-
"""@package webapp.modules.user_center.request_util
“个人中心”数据处理接口

微站页面与数据函数的对应关系：

页面 | 函数
-----|---------
个人中心 | get_user_info(request)

"""


from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
#from django.contrib.auth.decorators import login_required, permission_required
#from django.conf import settings
from django.shortcuts import render_to_response
#from django.contrib.auth.models import User, Group, Permission
#from django.contrib import auth
#from django.db.models import Q

#from core.jsonresponse import JsonResponse, create_response
#from core.dateutil import get_today
#from core.exceptionutil import full_stack, unicode_full_stack

from datetime import datetime
from mall.models import *
from modules.member.models import *
from modules.member import util as member_util
from modules.member import module_api as member_api
from account.models import *

from tools.regional.views import get_str_value_by_string_ids
from core.send_order_email_code import *
#from modules.member.member_decorators import member_required
from market_tools.export_api import *
from market_tools.tools.weizoom_card.models import AccountHasWeizoomCardPermissions
from watchdog.utils import *

from apps.export import get_webapp_usage_link as get_all_cusapps_usage_link
import mall.module_api as mall_api
import cache.order_cache as order_cache

def __get_current_user_info(request, member):
	"""
	获取当前用户的头像和名称信息
	"""

	#if (not member.user_icon) or ('user-1.jpg' in member.user_icon) or member.is_subscribed is False:
	today = datetime.now()
	today_str = datetime.today().strftime('%Y-%m-%d')
	if member.update_time.strftime("%Y-%m-%d") != today_str:
	# 	return None
		member_util.member_basic_info_updater(request.user_profile, member)
		return Member.objects.get(id = member.id)
	return member


def get_user_info(request):
	"""
	获取“个人中心”页面所需要的数据

	“个人中心”页面数据获取流程：

	- 获取个人信息
	- 获取收货信息
	- 获取订单信息
	- 获取购物车信息
	- 获取营销工具链接列表

	优化营销工具链接
	===========
	`get_market_tool_webapp_usage_links`
	-->  `market_tools.export_api.get_market_tool_webapp_usage_links`
	-->  `product.module_api.get_market_tool_modules_via_userid`
	-->  `product.module_api.get_market_tool_modules_for_user`

	`get_all_cusapps_usage_link` (实际上是 `apps.export.get_webapp_usage_link`)

	"""

	profile = request.user_profile
	member = request.member
	#member = Member.objects.get(id=request.member.id)
	week = None
	# TODO: 优化获取头像信息
	member = __get_current_user_info(request, member)
	cur_request_member = member
	member_info = MemberInfo.get_member_info(request.member.id)
	if member_info and member_info.phone_number and len(member_info.phone_number) > 10:
		member_info.phone =  '%s****%s' % (member_info.phone_number[:3],member_info.phone_number[-4:])
	# 历史订单、待支付
	(history_order_count, not_paid_count, not_ship_order_count, shiped_order_count, review_count) = order_cache.get_order_stats(request.webapp_user.id)
	member.history_order_count = history_order_count   # "全部订单"数量
	member.not_payed_order_count = not_paid_count    # "待支付"订单数量
	member.not_ship_order_count = not_ship_order_count    # "待发货"订单数量
	member.shiped_order_count = shiped_order_count    # "已发货"订单数量
	member.review_count = review_count

	#购物车中商品数量
	# 对应页面上"购物车"的数量
	member.shopping_cart_product_count = mall_api.get_shopping_cart_product_nums(request.webapp_user)

	#收藏商品的数量
	member.wishlist_product_count = mall_api.wishlist_product_count(request.webapp_owner_id, request.member.id)

	#营销工具使用情况链接
	market_tools = get_market_tool_webapp_usage_links(request.webapp_owner_id, request.member)
	#添加定制化app在个人中心页面显示的"我的**"
	# TODO: 优化，避免重复从数据库中读入
	#market_tools += get_all_cusapps_usage_link(request.webapp_owner_id, request.member)
	#经验值 (bert add at 14 )
	#grade_lists = MemberGrade.get_all_grades_list(member.webapp_id)
	# 是否允许用微众卡？
	#is_can_use_weizoomcard = AccountHasWeizoomCardPermissions.is_can_use_weizoom_card_by_owner_id(request.webapp_owner_id)

	# 是否享受会员折扣
	#is_enjoy_member_discount = get_is_enjoy_member_discount(request.webapp_user)

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'个人中心',
		'member': member,
		'member_info':member_info,
		'request': request,
	 	'market_tools': market_tools,
	 	'cur_request_member':cur_request_member,
	 	'current_page_name': 'usercenter'
	})
	return render_to_response('%s/user_center.html' % request.template_dir, c)


# def get_is_enjoy_member_discount(webapp_user):
# 	member_discount = webapp_user.get_discount().get('discount', 100)
# 	if member_discount < 100:
# 		return True

# 	return False


def influence_guide(request):
	"""
	积分指南
	"""
	webapp_id = request.user_profile.webapp_id
	rices = Ricepage.objects.filter(built_name=u'积分指南')
	rice = None
	if rices.count() > 0:
		rice = rices[0]
	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': page_title,
		'webapp_id': webapp_id,
	    'influence': rice
	})

	return render_to_response('%s/influence_guide.html' % request.template_dir, c)


def edit_ship_info(request):
	"""
	修改收货人信息
	"""
	webapp_id = request.user_profile.webapp_id
	ship_info_id = request.GET.get('ship_info_id',0)
	if ship_info_id == '':
		ship_info_id = 0
	else:
		ship_info_id = int(ship_info_id)
	if ship_info_id > 0:
		ship_info = ShipInfo.objects.get(id=ship_info_id)
	else:
		ship_info = None

	if not ship_info and request.webapp_user:
		try:
			ship_info = ShipInfo.objects.get(webapp_user_id=request.webapp_user.id)
		except:
			ship_info = ShipInfo.objects.create(
				webapp_user_id = request.webapp_user.id
			)

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'收货人信息',
		'webapp_id': webapp_id,
	    'shipInfo': ship_info
	})
	return render_to_response('%s/ship_info.html' % request.template_dir, c)


def save_ship_info(request):
	"""
	保存收货人信息
	"""
	ship_name = request.POST['ship_name']
	ship_address = request.POST['ship_address']
	ship_tel = request.POST['ship_tel']
	area = request.POST['area']
	ship_id = int(request.POST.get('ship_id', -1))
	request.webapp_user.update_ship_info(
		ship_name = ship_name,
		ship_address = ship_address,
		ship_tel = ship_tel,
		area = area,
		ship_id = ship_id
	)

	url = './?module=user_center&model=user_info&action=get&workspace_id=user_center&webapp_owner_id=%d&project_id=0' % request.webapp_owner_id
	return HttpResponseRedirect(url)


def get_integral_log(request):
	"""
	获取会员积分使用日志

	1. 解析会员信息：当会员信息为空时，直接跳转到404页面。
	2. 获取与该会员对应的积分日志列表（按日期逆序）
	3. 组织积分日志结构，将同一天好友奖励的积分日志在一条记录中显示，并且显示好友头像
	4. 将组织后的日志信息，渲染到`integral_log.html`页面中
	"""

	# 1. 解析会员信息
	member_id = request.GET.get('member_id','')
	try:
		if not hasattr(request, 'member') or request.member is None:
			member = Member.objects.get(id=member_id)
		else:
			member = request.member
		MemberIntegralLog.update_follower_member_token(member)
	except:
		notify_msg = u"webapp，积分日志, cause:\n{}".format(unicode_full_stack())
		watchdog_error(notify_msg)
		raise Http404('不存在该会员')

	# 2. 获取与该会员对应的积分日志列表（按日期倒叙）
	member_integral_logs = MemberIntegralLog.objects.filter(member=member).order_by('-created_at')

	# 3. 组织积分日志结构，将同一天好友奖励的积分日志在一条记录中显示，并且显示好友头像
	organized_integral_log_list = __get_organized_integral_log_list(member_integral_logs)
	if organized_integral_log_list:
		organized_integral_log_list = sorted(organized_integral_log_list.items(), cmp=cmp_datetime, key=lambda x : x[0],  reverse=False)
	# 4. 将组织后的日志信息，渲染到integral_log.html页面中
	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'积分明细',
		'member_integral_logs': organized_integral_log_list,
		'member': member
	})
	return render_to_response('%s/integral_log.html' % request.template_dir, c)


def __get_organized_integral_log_list(log_list):
	"""
	获取组织后的日志列表
	"""
	# 组织后的日志列表
	organized_log_list = list()
	# 当前好友奖励
	current_friend_log_list = None
	# 当前日志日期
	current_friend_log_list_date = None

	log_dict = {}

	for log in log_list:
		current_date = log.created_at.strftime('%Y-%m-%d')
		if log_dict.has_key(current_date):
			date_info = log_dict[current_date]
			date_info.append(_get_current_log_info(log))
			log_dict[current_date] = date_info
		else:
			log_dict[current_date] = [_get_current_log_info(log)]
	return log_dict


def cmp_datetime(a, b):
	a_datetime = datetime.strptime(a, '%Y-%m-%d')
	b_datetime = datetime.strptime(b, '%Y-%m-%d')

	if a_datetime > b_datetime:
		return -1
	elif a_datetime < b_datetime:
		return 1
	else:
		return 0

SHOPING_REWARDES_IMGE = '/static_v2/img/webapp/usercenter/Shoppingrewards.jpg'
SCAN_REWARDES_IMGE = '/static_v2/img/webapp/usercenter/scanReawards.png'
def _get_current_log_info(member_integral_log):
	member_integral_log.is_friend = False
	if u'好友' in member_integral_log.event_type or u'推荐扫码' in member_integral_log.event_type:
		member_integral_log.is_friend = True
		try:
			friend_member = Member.objects.get(token=member_integral_log.follower_member_token)
			if friend_member.user_icon and friend_member.user_icon != '':
				member_integral_log.pic = friend_member.user_icon
				member_integral_log.name = friend_member.username_for_html
			else:
				member_integral_log.pic = SCAN_REWARDES_IMGE
				member_integral_log.name = ''
		except:
			member_integral_log.pic = SCAN_REWARDES_IMGE
			member_integral_log.name = ''

	elif u'购物返利' in member_integral_log.event_type or u'评' in member_integral_log.event_type or member_integral_log.event_type == u'活动奖励':
		member_integral_log.pic = SHOPING_REWARDES_IMGE
	else:
		member_integral_log.pic = SCAN_REWARDES_IMGE
	return member_integral_log
	
def __append_organized_log_list(log_list, current_log):
	"""
	将日志加入到组织后的列表中
	"""
	log_list.append(current_log)
	return log_list

def __is_dueto_friend_action(log):
	"""
	是否为好友奖励

	存在follower_member_token或者event_type是‘好友奖励’的日志为‘好友奖励’日志，返回True；
	否者返回False
	"""
	# if log and (log.follower_member_token or log.event_type == FOLLOWER_CLICK_SHARED_URL):
	# 	return True

	return False

def __create_current_friend_day_logs(member_integral_log):
	"""
	创建一个同一天的好友list
	"""
	day_friend_log = MemberIntegralLog()
	day_friend_log.created_at = member_integral_log.created_at
	day_friend_log.event_type = FOLLOWER_CLICK_SHARED_URL
	day_friend_log.logs = list()
	return day_friend_log

def __append_current_friend_day_logs(day_friend_log, member_integral_log):
	"""
	将一个好友奖励日志，放入同一天的日志list中
	"""
	try:
		friend_member = Member.objects.get(token=member_integral_log.follower_member_token)
		if friend_member.user_icon and friend_member.user_icon != '':
			member_integral_log.pic = friend_member.user_icon
			member_integral_log.name = friend_member.username
		else:
			member_integral_log.pic = ''
			member_integral_log.name = ''
	except:
		member_integral_log.pic = ''
		member_integral_log.name = ''

	if day_friend_log is None:
		day_friend_log = __create_current_friend_day_logs(member_integral_log)

	day_friend_log.logs.append(member_integral_log)
	day_friend_log.integral_count = day_friend_log.integral_count + member_integral_log.integral_count
	return day_friend_log


def get_member_grade(request):
	"""
	会员等级页
	"""
	webapp_id = request.user_profile.webapp_id
	member_grade = MemberGrade.objects.filter(webapp_id=webapp_id)

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'会员等级',
		'member_grades': member_grade,
	})
	return render_to_response('%s/member_guide.html' % request.template_dir, c)


def get_integral_grade(request):
	"""
	积分指南页
	"""
	owner_id = request.webapp_owner_id
	article =  SpecialArticle.objects.get(name='integral_guide', owner_id=owner_id)

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'积分指南',
		'article': article
	})
	return render_to_response('%s/integral_grade.html' % request.template_dir, c)


def get_user_guide(request):
	"""
	用户指南页
	"""
	webapp_owner_id = request.webapp_owner_id
	webapp_id = request.user_profile.webapp_id

	#积分指南
	integral_guide =  SpecialArticle.objects.get(name='integral_guide', owner_id=webapp_owner_id)

	#用户等级
	member_grades = MemberGrade.objects.filter(webapp_id=webapp_id)

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'用户指南',
		'integral_guide': integral_guide,
		'member_grades': member_grades
	})
	return render_to_response('%s/user_guide.html' % request.template_dir, c)


def feed_back_page(request):
	"""
	意见反馈
	"""
	if request.POST:
		page = '%s/success_feed_back.html'
	else:
		page = '%s/feed_back.html'

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'意见反馈'
	})
	return render_to_response(page % request.template_dir, c)


def help_page(request):
	"""
	帮助中心
	"""
	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'帮助中心'
	})
	return render_to_response('%s/help.html' % request.template_dir, c)



def get_integral_introduction(request):
	"""
	积分介绍
	"""
	member = request.member
	integral_strategy_setting = member_api.get_integral_strategy_setting(request.user_profile.webapp_id)

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'我的积分',
		'member': member,
		'integral_strategy_setting': integral_strategy_setting
	})
	return render_to_response('%s/integral_introduction.html' % request.template_dir, c)


def get_wishlist(request):
	"""
	获取会员收藏夹
	"""
	member = request.member
	products = mall_api.get_products_in_wishlist(request.webapp_user, request.webapp_owner_id, member.id)

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'我的收藏',
		'member': member,
		'products': products
	})
	return render_to_response('%s/wishlist.html' % request.template_dir, c)

def get_binding_page(request):
	"""
	获取绑定页面
	"""
	member_info = MemberInfo.get_member_info(member_id=request.member.id)
	page_title =  u'绑定会员'
	if member_info.is_binded:
		page_title =  u'绑定信息'
		member_info.phone =  '%s****%s' % (member_info.phone_number[:3],member_info.phone_number[-4:])

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': page_title,
		'member': request.member,
		'hide_non_member_cover': True,
		'member_info':member_info
	})
	if member_info.is_binded:
		return render_to_response('%s/binding_info.html' % request.template_dir, c)
	else:
		return render_to_response('%s/binding_page.html' % request.template_dir, c)

def get_binded_user_info(request):
	"""
	获取绑定信息
	"""
	member_info = MemberInfo.objects.get(member=request.member)
	if member_info.is_binded:
		member_info.phone =  '%s****%s' % (member_info.phone_number[:3],member_info.phone_number[-4:])

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'绑定信息',
		'member': request.member,
		'member_info': member_info
	})
	return render_to_response('%s/binding_info.html' % request.template_dir, c)


def get_refueling_page(request):
	member = Member.objects.get(id=request.member.id)
	webapp_user = request.webapp_user
	member_refuelings = MemberRefueling.objects.filter(member=member)

	#product_id = Product.objects.filter(owner_id=request.webapp_owner_id)[0].id
	product = mall_api.get_product_detail(request.webapp_owner_id, 2565, webapp_user, member.grade_id)
	can_buy = False
	cookie_fid = request.COOKIES.get('fid', '')
	member_fid = cookie_fid
	member_refueling = None
	member_refueling_infos = None
	friend_member = None
	current_member = False
	refuelinged = False
	if cookie_fid:
		if cookie_fid == str(member.id):
			"""
				当前会员信息
			"""
			current_member = True
			if member_refuelings.count() == 0:
				"""
				 还没有参加活动
				"""
				pass
			else:
				member_refueling = member_refuelings[0]
				member_refueling_infos = MemberRefuelingInfo.objects.filter(member_refueling=member_refueling)
				if member_refueling_infos.count() >= 15:
					"""
						已经符合活动要求
					"""
					can_buy = True
					for member_refueling_has_order in MemberRefuelingHasOrder.objects.filter(member_refueling=member_refueling):
						if member_refueling_has_order.order_id and Order.objects.get(id=member_refueling_has_order.order_id).status >=3:
							can_buy = False
							break
		else:
			"""
				给好友集赞页面
			"""
			friend_member = Member.objects.get(id=cookie_fid)
			member_refuelings = MemberRefueling.objects.filter(member=friend_member)

			if member_refuelings.count() > 0:
				"""
					好友分享链接成功
				"""
				member_refueling = member_refuelings[0]
			else:
				"""
					好友分享链接失败 创建链接
				"""
				try:
					member_refueling = MemberRefueling.objects.create(member=friend_member)
				except :
					member_refueling = MemberRefueling.objects.filter(member=friend_member)[0]


			member_refueling_infos = MemberRefuelingInfo.objects.filter(member_refueling=member_refueling)[:15]

			"""
				判断是否加油
			"""
			refuelinged = True if MemberRefuelingInfo.objects.filter(member_refueling=member_refueling, follow_member=member).count() > 0 else False

	# if member_refuelings.count() > 0:
	# 	"""
	# 		已经分享活动
	# 	"""
	# 	member_refueling = member_refuelings[0]
	# 	member_refueling_infos = MemberRefuelingInfo.objects.filter(member_refueling=member_refueling)
	# 	if member_refueling_infos.count() >= 15:
	# 		"""
	# 			已经符合活动要求
	# 		"""

	# 		can_buy = True
	# 		for member_refueling_has_order in MemberRefuelingHasOrder.objects.filter(member_refueling=member_refueling):
	# 			if member_refueling_has_order.order_id and Order.objects.get(id=member_refueling_has_order.order_id):
	# 				can_buy = False
	# 				break
	# 	else:
	# 		pass
	# else:
	# 	"""
	# 		未分享活动
	# 	"""
	# 	pass
	# if fid:
	# 	"""
	# 	点击好友分享链接而来：显示集赞新
	# 	"""
	# 	member_fid = Member.objects.get(id=fid)
	# 	member_refueling_fms = MemberRefueling.objects.filter(member=member_fid)
	# 	if member_refueling_fms.count() > 0:
	# 		member_refueling_fm_infos = MemberRefuelingInfo.objects.filter(member_refueling=member_refueling_fms[0])
	# else:
	# 	"""
	# 	不是通过链接而来 显示普通活动
	# 	"""
	# 	pass

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': False,
		'page_title': u'找小伙伴帮你加油',
		'member': request.member,
		'product': product,
		'can_buy': can_buy,
		'member_fid':member_fid,
		'hide_non_member_cover':True,
		'member_refueling':member_refueling,
		'member_refueling_infos':member_refueling_infos,
		'refueling_count':member_refueling_infos.count() if member_refueling_infos else 0,
		'cookie_fid':cookie_fid,
		'member_refuelings':member_refuelings,
		#'member_refueling_fm_infos': member_refueling_fm_infos,
		'friend_member':friend_member,
		'current_member':current_member,
		'refuelinged': refuelinged
	})
	return render_to_response('%s/refueling_page.html' % request.template_dir, c)

