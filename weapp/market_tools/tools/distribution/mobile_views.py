# -*- coding: utf-8 -*-

__author__ = 'aix'

import os

from django.template import Context, RequestContext
from django.shortcuts import render_to_response
import models
from modules.member.models import Member
template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

COUNT_PER_PAGE = 15
def get_page(request):
	"""
	手机端推广分销页面
	"""
	webapp_id = request.user_profile.webapp_id
	member_id = request.member.id
	user_icon = request.member.user_icon
	propotion_data = models.ChannelDistributionQrcodeSettings.objects.get(bing_member_id=member_id)
	total_return = propotion_data.total_return   #已提取
	commission_return_standard = propotion_data.commission_return_standard  #佣金返现标准（即最低取现标准）
	will_return_reward = propotion_data.will_return_reward  #已获得奖励
	total_earn = total_return + will_return_reward  #收入
	diff_reward = commission_return_standard - will_return_reward  #还差多少元可以取现
	if diff_reward < 0:
		diff_reward = 0
	return_standard = propotion_data.return_standard  #多少天的计算方式
	status = propotion_data.status  # 取现进度
	valid = will_return_reward >= commission_return_standard
	if valid:
		state = 1
	else:
		state = 2
	if status != 0:
		state = 3
	# if status != 0:
	# 	state = 3
	# elif state = 2
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
		'state': state,
		'member_id': member_id
	})

	return render_to_response('%s/distribution/webapp/m_my_promotion.html' % TEMPLATE_DIR, c)

def get_process(request):
	"""
	获取提取进度页面
	"""
	member_id = request.member.id
	cur_list = models.ChannelDistributionQrcodeSettings.objects.get(bing_member_id=member_id)
	prev_datas = models.ChannelDistributionDetail.objects.filter(member_id=member_id, order_id=0).order_by('-created_at')[0:20]
	if cur_list or prev_datas:
		prev_lists = []
		for prev_data in prev_datas:
			prev_list = {
				'created_at': prev_data.created_at
			}
			prev_lists.append(prev_list)

		c = RequestContext(request, {
			"cur_list": cur_list,
			"prev_lists": prev_lists
		})
	else:
		c = RequestContext(request, {
		})

	return render_to_response('%s/distribution/webapp/m_process.html' % TEMPLATE_DIR, c)

	

def get_vip_message(request):
	"""
	获取已有会员页面
	"""
	webapp_id = request.user_profile.webapp_id
	member_id = request.member.id
	vip_member_id = models.ChannelDistributionQrcodeSettings.objects.get(bing_member_id=member_id).id
	vip_datas = models.ChannelDistributionQrcodeHasMember.objects.filter(channel_qrcode_id=vip_member_id, commission__gt=0)
	if vip_datas:
		vip_lists = []
		for vip_data in vip_datas:
			vip_list = {
				'nick_name': Member.objects.get(id=vip_data.member_id).username_for_html,
				'cost_money': vip_data.cost_money,  #消费金额
				'commission': vip_data.commission,  #带来的佣金
				'buy_times': vip_data.buy_times,  #购买次数
				'created_at': vip_data.created_at  #关注时间
			}
			vip_lists.append(vip_list)

		c = RequestContext(request, {
			'vip_lists': vip_lists
		})
	else:
		c = RequestContext(request, {
		})

	return render_to_response('%s/distribution/webapp/m_vip.html' % TEMPLATE_DIR, c)

def get_details(request):
	"""
	获取交易明细页面
	"""
	member_id = request.member.id
	ChannelDistributionQrcodeSettings = models.ChannelDistributionQrcodeSettings.objects.get(bing_member_id=member_id)
	will_return_reward = ChannelDistributionQrcodeSettings.will_return_reward  #已获得奖励
	channel_qrcode_id = ChannelDistributionQrcodeSettings.id  #提取进度的会员的id
	details_datas = models.ChannelDistributionDetail.objects.filter(channel_qrcode_id=channel_qrcode_id)[0:20] #提取记录
	if details_datas:
		details_lists = []
		for details_data in details_datas:
			details_list = {			
				'order_id': details_data.order_id,  #订单id，id为0，则为提取
				'money': details_data.money,  #操作金额
				'created_at': details_data.created_at,  #添加时间
				'commission_rate': ChannelDistributionQrcodeSettings.commission_rate  #利率
			}
			details_lists.append(details_list)

		for details_list in details_lists:
			if details_list['order_id'] == 0:
				details_list['money'] = details_list['money'] * details_list['commission_rate']

		c = RequestContext(request, {
			'will_return_reward': will_return_reward,
			'details_lists': details_lists
		})
	else:
		c = RequestContext(request, {
			'will_return_reward': will_return_reward
		})

	return render_to_response('%s/distribution/webapp/m_details.html' % TEMPLATE_DIR, c)

def get_weixin_code(request):
	"""
	获取二维码推广页面
	"""
	member_id = request.member.id
	ChannelDistributionQrcodeSettings = models.ChannelDistributionQrcodeSettings.objects.get(bing_member_id=member_id)
	nick_name = ChannelDistributionQrcodeSettings.bing_member_title  #当前登入用户的关联会员头衔
	weixin_code = ChannelDistributionQrcodeSettings.ticket  #二维码
	weixin_code = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=' + weixin_code #二维码url
	c = RequestContext(request, {
		'nick_name': nick_name,
		'weixin_code': weixin_code
	})

	return render_to_response('%s/distribution/webapp/m_weixin_promotion.html' % TEMPLATE_DIR, c)

