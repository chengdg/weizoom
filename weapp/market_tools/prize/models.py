# -*- coding: utf-8 -*-

__author__ = 'chuter'

import random

from django.db import models
from modules.member.models import Member
from watchdog.utils import watchdog_fatal, watchdog_error

#########################################################################
# Prize: 奖品
#########################################################################
class Prize(models.Model):
	name = models.CharField(max_length=32, verbose_name=u'奖品名称')
	level = models.IntegerField(verbose_name=u'奖品等级')
	odds = models.IntegerField(default=0, verbose_name=u'中奖概率')
	image_url = models.CharField(max_length=256, null=True, blank=True, default='')
	detail = models.TextField(verbose_name=u'奖品详情', null=True, blank=True, default='')
	count = models.IntegerField(verbose_name=u'奖品个数')
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'market_tool_prizes'
		verbose_name = '奖品'
		verbose_name_plural = '奖品'

	@staticmethod
	def create(name, level, odds, count, image_url='', detail=''):
		return Prize.objects.create(
			name = name,
			level = level,
			odds = odds,
			count = count,
			image_url = image_url,
			detail = detail
			)

	@staticmethod
	def decrease_count(prize, decrease_count):
		from django.db import connection, transaction
		cursor = connection.cursor()
		cursor.execute('update market_tool_prizes set count=count-%d where id = %d' % (decrease_count, prize.id))
		transaction.commit_unless_managed()

#########################################################################
# 获取默认的采样空间大小，默认大小为所有会员的数量*2
#########################################################################
def __get_default_sample_space_size(webapp_id):
	return Member.count(webapp_id) * 2

#########################################################################
# 生成是否中奖的采样集合，其中sample_space_size为总的采样集合大小，
# 中奖样品的数量为奖品列表prizes_list中的个数总和
#########################################################################
MAX_PRIZE_COUNT = 1000
def __generate_whether_hint__sample_list(prizes_list, sample_space_size):
	total_prize_count = 0
	for prize in prizes_list:
		if prize is None:
			continue

		if prize.count > MAX_PRIZE_COUNT:
			total_prize_count += MAX_PRIZE_COUNT
		else:
			total_prize_count += prize.count


	sample_list = []
	for i in xrange(total_prize_count):
		sample_list.append(True)

	remain_space_size = sample_space_size - total_prize_count
	if remain_space_size > 0:
		for i in xrange(remain_space_size):
			sample_list.append(False)

	random.shuffle(sample_list)
	return sample_list

#########################################################################
# 默认抽奖策略，先根据奖品数量和采样空间大小构造是否中奖的
# 样品集合，然后随机采样，看是否中奖
# 如果没有中奖那么直接返回None
# 否则，根据每个奖品（还有剩余的）的中奖概率填充奖品列表，然后
# 随机抓阄，返回所抓到的奖品
#########################################################################
def default_draw_lottery_strategy(prizes_list, webapp_id, sample_space_size=None):
	if sample_space_size is None:
		sample_space_size = __get_default_sample_space_size(webapp_id)

	if (prizes_list is None) or (len(prizes_list) == 0) or (sample_space_size <= 0):
		return None

	hint_sample_list = __generate_whether_hint__sample_list(prizes_list, sample_space_size)

	assert (len(hint_sample_list) > 0)
	random_index = random.randint(0, len(hint_sample_list)-1)
	is_hint = hint_sample_list[random_index]

	if not is_hint:
		return None

	prize_sample_list = []
	for prize in prizes_list:
		if (prize is None) or (prize.count <= 0):
			continue

		for i in xrange(prize.odds):
			prize_sample_list.append(prize)

	if len(prize_sample_list) <= 0:
		return None
	elif len(prize_sample_list) == 1:
		return prize_sample_list[0]

	random.shuffle(prize_sample_list)
	random_index = random.randint(0, len(prize_sample_list)-1)
	return prize_sample_list[random_index]

def draw_lottery(
	prizes_list,
	webapp_id,
	draw_lottery_strategy=default_draw_lottery_strategy,
	sample_space_size=None
	):

	if (prizes_list is None) or (len(prizes_list) == 0):
		return None

	return draw_lottery_strategy(prizes_list, webapp_id, sample_space_size)


#########################################################################
# 创建一个大小为100的样本池，讲奖品根据概率放入池中，不足100则使用None补充
# 从奖品池中随机选择一个元素，进行判断。
# 如果是None或者相应的奖品个数小于0，返回None
# 否则返回相应的prize对象
#########################################################################
def draw_lottery_new(prizes, webapp_id):
	prize_list = []
	for prize in prizes:
		for i in xrange(prize.odds):
			prize_list.append(prize)

	length = len(prize_list)
	for i in xrange(100 - length):
		prize_list.append(None)
	prize = random.choice(prize_list)
	if prize:
		if prize.count <= 0:
			return None
		else:
			return prize
	else:
		return None
