# -*- coding: utf-8 -*-

__author__ = 'chuter'

import json

class PrizeInfo(object):
	SCORE_PRIZE_INFO_NAME = '_score-prize_'
	REAL_PRIZE_INFO_NAME = '_real-prize_'

	REAL_PRIZE_INFO_ID = 0

	def __init__(self, id, name, type):
		self.id = id
		self.name = name
		self.type = type

	#是否是积分奖励
	@property
	def is_score_prize(self):
		return self.name == self.SCORE_PRIZE_INFO_NAME

	#是否是无奖励
	@property
	def is_non_prize(self):
		return self.id == -1

	#是否是实物奖励
	@property
	def is_real_prize(self):
		return self.id == 0

	@property
	def prize_type(self):
		if self.is_score_prize:
			return SCORE_PRIZE_TYPE
		elif self.is_non_prize:
			return NON_PRIZE_TYPE_NAME
		else:
			return self.type

	@staticmethod
	def build_from(object, prize_type):
		if object is None:
			return None

		if isinstance(object, unicode) or isinstance(object, str):
			return PrizeInfo.from_json(object)

		#奖品信息只需要作为奖品的对象的id和name属性
		return PrizeInfo(object.id, object.name, prize_type)

	@staticmethod
	def from_json(jsonobj):
		if isinstance(jsonobj, unicode):
			jsonobj = jsonobj.encode('utf-8')

		if isinstance(jsonobj, str):
			jsonobj = json.loads(jsonobj)


		prize_type = PRIZE_TYPE_NAMES_2_TYPES.get(jsonobj['type'], None)
		return PrizeInfo(jsonobj['id'], jsonobj['name'], prize_type)

	def to_json(self):
		if self.is_non_prize:
			return {'id':-1, 'name':'non-prize', 'type':NON_PRIZE_TYPE_NAME}
		elif self.is_score_prize:
			#如果是积分奖励时，id代表积分额度
			return {'id':self.id, 'name':self.SCORE_PRIZE_INFO_NAME, 'type':SCORE_PRIZE_TYPE_NAME}
		elif self.is_real_prize:
			return {'id':self.REAL_PRIZE_INFO_ID, 'name':self.name, 'type':REAL_PRIZE_TYPE_NAME}
		else:
			return {'id':self.id, 'name':self.name, 'type':self.type.name}

	def __str__(self):
		return json.dumps(self.to_json())

class PrizeType(object):
	def __init__(self, prize_type_name, 
		get_all_prizes_func=None, award_to_func=None):
		self.prize_type_name = prize_type_name
		self.get_all_prizes_func = get_all_prizes_func
		self.award_to_func = award_to_func

	@property
	def name(self):
		return self.prize_type_name

	def get_all_prizes(self, user):
		return self.get_all_prizes_func(user)

	def award_to(self, prize_info, member):
		return self.award_to_func(prize_info, member)

#内置奖品类别
#积分奖品，对于积分奖品发奖操作直接是直接调用
#member.integral@increase_member_integral对会员增加积分
SCORE_PRIZE_TYPE_NAME = u'积分'
SCORE_PRIZE_TYPE = PrizeType(SCORE_PRIZE_TYPE_NAME)

#没有任何奖品
NON_PRIZE_TYPE_NAME = u'无奖励'
NON_PRIZE_TYPE = PrizeType(NON_PRIZE_TYPE_NAME)

#没有任何奖品
REAL_PRIZE_TYPE_NAME = u'实物奖励'
REAL_PRIZE_TYPE = PrizeType(REAL_PRIZE_TYPE_NAME)

PRIZE_TYPES = [
	NON_PRIZE_TYPE,
	SCORE_PRIZE_TYPE,
	REAL_PRIZE_TYPE,
]

PRIZE_TYPE_NAMES_2_TYPES = {
	NON_PRIZE_TYPE_NAME : NON_PRIZE_TYPE,
	SCORE_PRIZE_TYPE_NAME : SCORE_PRIZE_TYPE,
	REAL_PRIZE_TYPE_NAME : REAL_PRIZE_TYPE,
}

def register_prize_type(prize_type):
	if prize_type is None:
		return

	if PRIZE_TYPE_NAMES_2_TYPES.has_key(prize_type.name):
		raise ValueError(u"Duplicate prize type name({})".format(prize_type.name))
	else:
		PRIZE_TYPE_NAMES_2_TYPES[prize_type.name] = prize_type
		PRIZE_TYPES.append(prize_type)

def get_request_prize_type(prize_type_name):
	if prize_type_name is None:
		return None

	return PRIZE_TYPE_NAMES_2_TYPES.get(prize_type_name, None)

def award(prize_info, member, event_type):
	if (member is None) or (prize_info is None):
		return None

	if not isinstance(prize_info, PrizeInfo):
		prize_info = PrizeInfo.build_from(prize_info.__str__())

	if prize_info.is_score_prize:
		from modules.member.integral import increase_member_integral
		
		increase_member_integral(member, prize_info.id, event_type)
	elif prize_info.is_non_prize or prize_info.is_real_prize:
		return
	else:
		prize_type = get_request_prize_type(prize_info.type.name)
		return prize_type.award_to(prize_info, member)