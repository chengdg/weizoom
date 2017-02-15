# -*- coding: utf-8 -*-

import json
import requests
import MySQLdb

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group


from account.models import UserProfile
from mall.models import *

class Command(BaseCommand):
    help = "update account_type from fans"
    args = ''

    def handle(self, *args, **options):
        """
        计算零售返点类型供货商的商品的结算价
        """
        conn= MySQLdb.connect(
            host='127.0.0.1',
            port = 3306,
            user='panda',
            passwd='weizoom',
            db ='panda',
            charset="utf8"
            )
        cur = conn.cursor()
        #获取所有零售返点类型的panda用户
        cur.execute(u"select id, points, purchase_method from account_user_profile where purchase_method in(2,3)")
        rows = cur.fetchall()  
        for row in rows:
            #获取account_user_profile的id和返点数
            account_id = row[0]
            points = row[1]
            purchase_method = row[2]
            print 'account_id is', account_id, 'points:', points , 'purchase_method:', purchase_method

            #获取对应供货商在weapp中的id
            cur.execute(u"select supplier_id from account_has_supplier where account_id='%d'" % account_id)
            supplier = cur.fetchone()
            if supplier:
                supplier_id = supplier[0]
            else:
                continue
            if supplier_id and int(purchase_method) == 3:
                # 五五分成历史供货商
                info = SupplierDivideRebateInfo.objects.filter(supplier_id=supplier_id,
                                                               is_deleted=False).first()
                if info:
                    points = info.basic_rebate
                else:
                    points = 0
                
            #根据供货商，获取该供货商下全部的商品
            # supplier = Supplier.objects.get(id=supplier_id)
            products = Product.objects.filter(supplier=supplier_id)
            #
            # #修改mall_product中的结算价
            # for product in products:
            #     print product.name
            #     product.purchase_price = "%.2f" % (product.price * (100 - points)/100)
            #     product.save()
            produst_ids = [p.id for p in products]
            
            print '--------------'
            
            #修改mall_product_model中的结算价
            product_models = ProductModel.objects.filter(product_id__in=produst_ids)
            for model in product_models:
                print model.name
                model.purchase_price = "%.2f" % (model.price * (100 - points)/100)
                model.save()


