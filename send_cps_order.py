# -*- coding: utf-8 -*-
import sys


reload(sys)
sys.setdefaultencoding("utf-8")
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)
import logging

#邮件部分
from core.sendmail import sendmail


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from tools.regional.models import *
from mall.models import *
from account.models import UserProfile
import xlsxwriter

from datetime import datetime,timedelta,date

product_names = [u"【润绿源】马铃薯鲜粉条(细、宽、韭叶)300g*3袋",u"淘老西儿 超大枣夹核桃内夹四片核桃", u"淘老西儿红枣夹核桃仁  单枣500克包邮", u"宝宝米婴幼儿食用米宝宝辅食500g包邮", u"母婴套装3KG礼盒装", u"蜜果恋 黄桃蜜桔杨梅时尚果罐 425g*8罐 包邮可混合卖", u"金圪达碗团 礼盒 纯荞麦 健康粗粮包邮", u"楼恒泰 手剥巴西松子168g罐装新货", u"楼恒泰 焦糖味/山核桃葵瓜子黑瓜子150g*4包 壳薄肉大", u"秋冬双面>立领羊绒大衣 毛呢外套", u"【红双阳】高邮咸鸭蛋 地方特产65克*20只简装", u"【红双阳】高邮咸鸭蛋  地方特产 65克*20只礼盒装", u"VISON雨萱玫瑰按摩香膏120g", u"vison雨萱活泉创水候保湿霜50g", u"洁柔（C&S）卫生纸布艺倍柔系列3层140g卷纸*16卷", u"6828顺清柔纯净系列4层200g*12>卷有芯卷纸", u"中粮山萃每日坚果随手包 混合坚果休闲零食25g*7包", u"露兰姬娜全效缤纷美白补水紧致面膜16片", u"露兰姬娜八倍补水美白尊享套装六件套 明星产品 保湿 温泉水", u"泉林本色 母婴专用纸巾卫生纸3层110抽15包定制箱装", u"爱仕达家系列两件套装ZQ02CJ2", u"奔腾省空间魔术>衣架裤架黑色", u"POVOS奔腾PW602电吹风机", u"天际 DDG-7A 宝宝煮粥小炖锅0.6LBB锅煲汤锅", u"万家美 男士套装 纯棉 圆领V领打底套装 5码6色", u"万家美男士保暖内衣套装纯色保暖内衣套装 中等厚度不加绒", u"宝家丽床宝天生一对紫外线杀菌床铺吸尘器家用除螨仪", u"国际牌柚子茶/枣茶/姜茶", u"皇族无糖各种酥", u"拉菲原味/红枣味麦片+2盒奶酪威化夹心饼干组合下单备注口味", u"香港威夫力特话梅2种口味（原味VS炭烧）", u"香>港拉菲核桃糊/杏仁糊/椰子糊", u"马来西亚进口福多牌Fudo盒装瑞士卷", u"台湾进口好祺烤虾/烧烤/芝士味花生豆150g休闲食品", u"澳洲进口拉菲营养早餐原味养生燕麦片 免煮即食休闲营养早餐饮品", u"新疆若羌大红枣 新疆优质产品 大红枣480g绿袋", u"阿克苏纸皮核桃 核桃500g/袋" ]

#products = Product.objects.filter(name__in=product_names,owner_id=1127)

product_ids = []
error_names = [[26367L, 62180L, 62138L, 61314L, 61312L, 62959L, 62088L, 28045L, 67756L, 65672L, 27728L, 27732L, 29051L, 29050L, 64912L, 66289L, 63599L, 60935L, 29702L, 67866L, 61265L, 67954L, 61447L, 59151L, 60168L, 59804L, 62098L, 28121L, 28376L, 28360L, 28361L, 28366L, 28374L, 28127L, 28371L, 59710L, 59709L]
for name in product_names:
        products = Product.objects.filter(owner_id=1127,name=name, is_deleted=False)
        ids = [p.id for p in products]
        if not ids:
                print name
        product_ids.extend(list(set(ids)))
print error_names
print len(product_ids), len(product_names)
assert len(product_ids) == len(product_names)

#product_ids = [p.id for p in products]

sales_order_status = [ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED]
file_path = 'product_cps_sales.xlsx'
workbook   = xlsxwriter.Workbook(file_path)
table = workbook.add_worksheet()
alist = [u'商品', u'113销量数量', u'113订单数量',u'113销售金额',  u'114销量数量', u'114订单数量',u'114销售金额', u'115销量数量', u'115订单数量',u'115销售金额',  u'116销量数量', u'116订单数量',u'116销售金额']
table.write_row('A1',alist)
tmp_line = 1
products = Product.objects.filter(id__in=product_ids)
for product in products:
        tmp_line += 1
        tmp_list = [product.name]
        for d in ["2016-11-03", "2016-11-04", "2016-11-05", "2016-11-06"]:
                order_has_products = OrderHasProduct.objects.filter(product_id=product.id, order__origin_order_id__lte=0, order__status__in=sales_order_status, order__payment_time=d)
                order_counts = order_has_products.count()
                product_sales = order_has_products.aggregate(Sum('number'))['number__sum']
                product_sales = product_sales if product_sales else 0
                product_price_sum = order_has_products.aggregate(Sum('total_price'))['total_price__sum']
                product_price_sum = product_price_sum if product_price_sum else 0.0
                tmp_list.extend([order_counts, product_sales, product_price_sum])


	table.write_row('A{}'.format(tmp_line),tmp_list)
workbook.close()
mode = ''
receivers = ['guoyucheng@weizoom.com']
if len(args) == 1:
	if args[0] == 'test':
		mode = 'test'
title = u'微众自运营CPS商品销量{}'.format(current_time)
content = u'您好'

sendmail(receivers, title, content, mode, file_path)
