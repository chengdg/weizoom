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
        同步panda中账户类型(正式/体验)到weapp中
        """
        suppliers = Supplier.objects.all()
        print '==============='
        print suppliers.count()

        conn= MySQLdb.connect(
            host='127.0.0.1',
            port = 3306,
            user='panda',
            passwd='weizoom',
            db ='panda',
            charset="utf8"
            )
        cur = conn.cursor()
        for supplier in suppliers:
            print supplier.name
            cur.execute(u"select id,username from auth_user where first_name='%s'" % supplier.name)
            panda_user = cur.fetchone()
            cur_owner_id = panda_user[0]
            username = panda_user[1]
            print cur_owner_id, 'cur_owner_id'

            if not User.objects.filter(username=username):
                user = User.objects.create_user(username, 'none@weizoom.com', '123456')
                user.first_name = supplier.name
                user.save()
                profile = user.get_profile()
                profile.store_name = supplier.name
                profile.save()
            else:
                continue

            Product.objects.filter(supplier=supplier.id).update(owner=user.id)

            #TODO: 订单数据处理
			#Order.objects.filter(XXX).update(owner=user.id)
        
            cur.execute(u"select id,owner_id,name,first_weight,first_weight_price,is_enable_added_weight,added_weight,added_weight_price,is_used,created_at,is_enable_special_config,is_enable_free_config,is_deleted from postage_config where owner_id = '%d' " % (cur_owner_id)) 
            postage_config_rows = cur.fetchall()
            for postage_config_row in postage_config_rows:
                p = PostageConfig.objects.create(
                    owner_id = user.id,
                    name = postage_config_row[2],
                    first_weight = postage_config_row[3],
                    first_weight_price = postage_config_row[4],
                    added_weight = postage_config_row[6],
                    added_weight_price = postage_config_row[7],
                    is_enable_special_config = postage_config_row[10],
                    is_enable_free_config = postage_config_row[11],
                    is_enable_added_weight = postage_config_row[5],
                    is_used = postage_config_row[8],
                    is_deleted = postage_config_row[12]
                ) 
                postage_config_id = postage_config_row[0]
                cur.execute(u"select id,owner_id,postage_config_id,first_weight_price,added_weight_price,created_at,destination,first_weight,added_weight from postage_config_special where postage_config_id ='%d' " %(postage_config_id))
                postage_config_special_rows = cur.fetchall()
                for postage_config_special_row in postage_config_special_rows:
                    if postage_config_special_row[6].isdigit():
                        postage_config_special_destination = '[' + str(postage_config_special_row[6]) + ']'
                    else:
                        postage_config_special_destination=[]
                        for x in postage_config_special_row[6].split(','):
                            postage_config_special_destination.append(int(x))
                    SpecialPostageConfig.objects.create(
                        owner_id = user.id,
                        postage_config_id = p.id,
                        first_weight_price = postage_config_special_row[3],
                        added_weight_price = postage_config_special_row[4],
                        #created_at = postage_config_special_row[5],
                        destination = postage_config_special_destination,
                        first_weight = postage_config_special_row[7],
                        added_weight = postage_config_special_row[8]
                    )  

                cur.execute(u"select id,owner_id,postage_config_id,destination,condition,condition_value,created_at from free_postage_config where postage_config_id ='%s' " %(postage_config_id))
                free_postage_config_rows = cur.fetchall()
                for free_postage_config_row in free_postage_config_rows:
                    if free_postage_config_row[3].isdigit():
                        free_postage_config_destination = '[' + str(free_postage_config_row[3]) + ']'
                    else:
                        free_postage_config_destination=[]
                        for x in free_postage_config_row[3].split(','):
                            free_postage_config_destination.append(int(x))
                    FreePostageConfig.objects.create(
                        owner_id = user.id,
                        postage_config_id = p.id,
                        destination = free_postage_config_destination,
                        condition = free_postage_config_row[4],
                        condition_value = free_postage_config_row[5],
                        #created_at = free_postage_config_row[6],
                    )

            #TODO: ProductLimitZoneTemplate无法辨识所属关系
			#ProductLimitZoneTemplate.objects.filter(owner_id=cur_owner_id).update(owner = user.id)
            
            cur.execute(u"select id,owner_id,express_name,customer_name,customer_pwd,logistics_number,remark,is_deleted,sendsite from express_bill_accounts where owner_id ='%s' " %(cur_owner_id))
            express_bill_account_rows = cur.fetchall()
            for express_bill_account_row in express_bill_account_rows:
                ExpressBillAccount.objects.create(
                    owner_id = user.id,
                    express_name = express_bill_account_row[2],
                    customer_name = express_bill_account_row[3],
                    customer_pwd = express_bill_account_row[4],
                    logistics_number = express_bill_account_row[5],
                    sendsite = express_bill_account_row[8],
                    remark = express_bill_account_row[6],
                    is_deleted = express_bill_account_row[7],
                )

            cur.execute(u"select id,owner_id,shipper_name,tel_number,province,city,district,address,postcode,company_name,remark,is_active,is_deleted from shipper_messages where owner_id ='%s' " %(cur_owner_id))
            shipper_message_rows = cur.fetchall()
            for shipper_message_row in shipper_message_rows:
                Shipper.objects.create(
                    owner_id = user.id,
                    name = shipper_message_row[2],
                    tel_number = shipper_message_row[3],
                    province = shipper_message_row[4][0:-1],
                    city = shipper_message_row[5][0:-1],
                    district = shipper_message_row[6],
                    address = shipper_message_row[7],
                    postcode = shipper_message_row[8],
                    company_name = shipper_message_row[9],
                    remark = shipper_message_row[10],
                    is_active = shipper_message_row[11],
                    is_deleted = shipper_message_row[12],
                )    
            
            #TODO: ProductModelProperty无法辨识所属关系
			#ProductModelProperty.objects.filter(owner_id=cur_owner_id).update(owner = user.id)
                

