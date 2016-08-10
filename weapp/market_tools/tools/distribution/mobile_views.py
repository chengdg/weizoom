# -*- coding: utf-8 -*-

__author__ = 'aix'

import os

from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from market_tools.tools.distribution import models
from static.modules.member import models as member_models
template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

COUNT_PER_PAGE = 15
def get_page(request):
	"""
	手机端推广分销页面
	"""
	webapp_id = request.user_profile.webapp_id
	member_id = request.member.id
	propotion_data = models.ChannelDistributionQrcodeSettings.objects.get(bing_member_id=member_id)
	total_return = propotion_data.total_return   #已提取
	commission_return_standard = propotion_data.commission_return_standard  #佣金返现标准（即最低取现标准）
	will_return_reward = propotion_data.will_return_reward  #已获得奖励
	total_earn = total_return + will_return_reward  #收入
	diff_reward = commission_return_standard - will_return_reward  #还差多少元可以取现
	return_standard = propotion_data.return_standard  #多少天的计算方式
	user_icon = request.member.user_icon
	valid = will_return_reward >= commission_return_standard

	c = RequestContext(request, {
		'propotion_data': propotion_data,
		'total_return': total_return,
		'commission_return_standard': commission_return_standard,
		'will_return_reward': will_return_reward,
		'total_earn': total_earn,
		'diff_reward': diff_reward,
		'return_standard': return_standard,
		'user_icon': user_icon,
		'webapp_id': webapp_id,
		'member_id': member_id,
		'valid': valid,
		'member_id': member_id
	})

	return render_to_response('%s/distribution/webapp/m_my_promotion.html' % TEMPLATE_DIR, c)

def get_process(request):
	"""
	获取提取进度页面
	"""
	member_id = request.member.id
	cur_list = models.ChannelDistributionQrcodeSettings.objects.get(bing_member_id=member_id)
	prev_datas = models.ChannelDistributionDetail.objects.get(member_id=member_id, order_id=0).order_by('-created_at')[0:10]
	prev_lists = []
	for prev_data in prev_datas:
		prev_list={
			'created_at': prev_data.created_at
		}
		prev_lists.append(prev_list)

	c = RequestContext(request, {
		"cur_list": cur_list,
		"prev_lists": prev_lists
	})
	return render_to_response('%s/distribution/webapp/m_process.html' % TEMPLATE_DIR, c)

def get_vip_message(request):
	"""
	获取已有会员页面
	"""
	webapp_id = request.user_profile.webapp_id
	member_id = request.member.id
	vip_lists = models.ChannelDistributionQrcodeHasMember.objects.get(member_id=member_id)
	for vip_list in vip_lists:
		vip_list={
			'nick_name': member_models.Member.objects.get(id=member_id).username_for_html,
			'cost_money': vip_list.cost_money,  #消费金额
			'commission': vip_list.commission,  #带来的佣金
			'buy_times': vip_list.buy_times,  #购买次数
			'created_at': vip_list.created_at  #关注时间
		}
		vip_lists.append(vip_list)

	c = RequestContext(request, {
		'vip_lists': vip_lists
	})
	return render_to_response('%s/distribution/webapp/m_vip.html' % TEMPLATE_DIR, c)

def get_details(request):
	"""
	获取交易明细页面
	"""
	member_id = request.member.id
	will_return_reward = models.ChannelDistributionQrcodeSettings.objects.get(bing_member_id=member_id).will_return_reward  #已获得奖励
	details_lists = models.ChannelDistributionDetail.objects.get(member_id=member_id)
	for details_list in details_lists:
		details_list={
			'will_return_reward': will_return_reward,
			'order_id': details_list.order_id  #订单id，id为0，则为提取
			'money': details_list.money  #操作金额
			'created_at': details_list.created_at  #添加时间
		}
		details_lists.append(details_list)

	c = RequestContext(request, {
		'details_lists': details_lists
	})
	return render_to_response('%s/distribution/webapp/m_details.html' % TEMPLATE_DIR, c)

def get_weixin_code(request):
	"""
	获取二维码推广页面
	"""
	member_id = request.member.id
	nick_name = request.member.username_for_html  #当前登入用户的昵称
	weixin_code = models.ChannelDistributionQrcodeSettings.objects.get(bing_member_id=member_id).ticket  #二维码
	c = RequestContext(request, {
		'nick_name': nick_name,
		'weixin_code': weixin_code
	})
	return render_to_response('%s/distribution/webapp/m_weixin_promotion.html' % TEMPLATE_DIR, c)

