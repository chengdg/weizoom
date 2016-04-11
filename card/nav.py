# -*- coding: utf-8 -*-
__author__ = 'robert'

FIRST_NAV = 'card'
CARD_ORDINARY_NAV = 'ordinary_rules'
CARD_LIMIT_NAV = 'limit_cards'

SECOND_NAVS = [{
	'name': CARD_ORDINARY_NAV,
	'displayName': '通用卡',
	'href': '/card/ordinary_rules/'
}, {
	'name': CARD_LIMIT_NAV,
	'displayName': '限制卡',
	'href': '/card/limit_rules/'
}]

def get_second_navs():
	return SECOND_NAVS