# -*- coding: utf-8 -*-

__author__ = 'aix'

import os

from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from market_tools.tools.distribution import models
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
		'member_id': member_id
	})

	return render_to_response('%s/distribution/webapp/m_my_promotion.html' % TEMPLATE_DIR, c)

def get_process(request):
	"""
	获取提取进度页面
	"""
	member_id = request.member_id
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
