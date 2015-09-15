#coding: utf8
"""
微商城访问接口(通过WAPI)
"""

import os,sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wglass.settings')
#for path in sys.path:	print("{}".format(path))


#from core.exceptionutil import unicode_full_stack

from utils.api_client import wapi


def get_order_stats(webapp_id, start_date=None, end_date=None):
	"""
	获取多项品牌价值
	"""
	results = wapi().get('mall', 'order_stats', {
		'wid': webapp_id,
		'date_start': start_date,
		'date_end': end_date
	})
	return results


def get_webapp_id(username):
	results = wapi().get_json('mall', 'webapp_id', {
		'username': username
	})
	return results.get('webapp_id')


def get_member_count(webapp_id, date_start=None, date_end=None):
	"""
	获取会员总数
	"""
	results = wapi().get_json('mall', 'member_stats', {
		'wid': webapp_id,
		'date_start': date_start,
		'date_end': date_end
	})
	return results.get('member_count')


def get_product_categories(uid):
	"""
	获取商品分组列表
	"""
	results = wapi().get_json('mall', 'product_categories', {
		'uid': uid
	})
	return results['categories']


def get_product_category(category_id):
	"""
	获取一个分类详情
	"""
	category = wapi().get_json('mall', 'product_category', {
		'id': category_id
	})
	return category


def update_product_category(category_id, name):
	"""
	获取商品分组列表
	"""
	wapi().post('mall', 'product_category', {
		'id': category_id,
		'name': name
	})
	return


def add_product_category(uid, name):
	"""
	创建商品分类
	"""
	response = wapi().put('mall', 'product_category', {
		'uid': uid,
		'name': name
	})
	#print("RESPONSE: {}".format(response))
	return



if __name__ == "__main__":
	idlist = [
	"ainicoffee",
	"aliguo",
	"wugutang",
	"judou",
	"heshibaineng",
	"zhonghaitou",
	"tianmashengwu",
	"guangruishipin",
	"yingguan",
	"LaRhea",
	"hanjin",
	"fxkj",
	"tianreyifang",
	"amigo",
	"hongfan",
	"gangshanxigu",

	"changjiufangzhi",


	"tide",

	"tianreyifang",

	"heruntiancheng",
	"dongfangwodeming",
	"huajitang"
	]

	print("USERNAME\tMEMBER_CNT\tORDER_CNT\tPAIED_MEMBER\tTOTAL_PAYMENT")
	for username in idlist:
		webapp_id = get_webapp_id(username)
		results = get_order_stats(webapp_id, "2015-08-01", "2015-08-31")
		member_count = get_member_count(webapp_id, "2015-08-01", "2015-08-31")

		#print("results: {}".format(results))
		print("{}\t{}\t{}\t{}\t{}".format(username, member_count, results['order_count'], results['member_count'], results['total_payment']))
