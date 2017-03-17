# -*- coding: utf-8 -*-

import json
import requests
import MySQLdb

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group


from account.models import UserProfile, CorpInfo
from mall.models import *

class Command(BaseCommand):
    help = "update account_type from fans"
    args = ''

    def handle(self, *args, **options):
        """
        同步panda中账户类型(正式/体验)到weapp中
        weapp库user的id即为corp_id
        """
        f = open('weapp_exists_users.txt', 'rb')
        weapp_exists_users = []
        for username in f.readlines():
            weapp_exists_users.append(username.strip())
        print weapp_exists_users

        conn= MySQLdb.connect(
            host='rm-bp18wbhgz1493ad8to.mysql.rds.aliyuncs.com',
            port = 3306,
            user='panda',
            passwd='Weizoom@',
            db ='panda',
            charset="utf8"
            )
        cur = conn.cursor()
        # cur.execute(u"select user_id,supplier_id from account_has_supplier where user_id in (329)")
        cur.execute(u"select user_id,supplier_id from account_has_supplier where user_id>0")
        relations = cur.fetchall()

        for relation in relations:
            panda_id = relation[0]
            cur_owner_id = panda_id
            supplier_id = relation[1]
            print supplier_id, panda_id
            supplier = Supplier.objects.get(id=supplier_id)
            try:
                print '>>>%s supplier start<<<' % supplier.name
            except:
                print '>>>%s supplier start<<<' % supplier.id
            cur.execute(u"select id,username from auth_user where id='%s'" % panda_id)
            panda_user = cur.fetchone()
            username = panda_user[1]
            # print panda_id, 'panda_id', username

            if not User.objects.filter(username=username):
                user = User.objects.create_user(username, 'none@weizoom.com', '123456')
                user.first_name = supplier.name
                user.save()
                profile = user.get_profile()
                profile.store_name = supplier.name
                profile.webapp_type = 4 #供货商类型帐号
                profile.note = supplier.id
                profile.save()
            else:
                # continue
                if username in weapp_exists_users:
                    username = username + '_317new'
                    if User.objects.filter(username=username):
                        continue
                    user = User.objects.create_user(username, 'none@weizoom.com', '123456')
                    user.first_name = supplier.name
                    user.save()
                    profile = user.get_profile()
                    profile.store_name = supplier.name
                    profile.webapp_type = 4 #供货商类型帐号
                    profile.note = supplier.id
                    profile.save()
                    print username
                else:
                    continue
                user = User.objects.get(username=username)
                # print 'already exists panda_id', panda_id

            #供货商配置
            if not CorpInfo.objects.filter(corp_id=user.id):
                cur.execute(u"select name,company_name,purchase_method,points,settlement_period,customer_from,max_product,company_type,contacter,phone,note,status,pre_sale_tel,after_sale_tel,customer_service_tel,customer_service_qq_first,customer_service_qq_second from account_user_profile where user_id='%d'" % (cur_owner_id)) 
                panda_user_info = cur.fetchone()
                CorpInfo.objects.create(
                    corp_id = user.id,
                    name = panda_user_info[0],
                    company_name = panda_user_info[1],
                    settlement_type = panda_user_info[2],
                    divide_rebate = panda_user_info[3],
                    clear_period = panda_user_info[4],
                    customer_from = panda_user_info[5],
                    max_product_count = panda_user_info[6],
                    classification_ids = panda_user_info[7],
                    contact = panda_user_info[8],
                    contact_phone = panda_user_info[9],
                    note = panda_user_info[10],
                    status = panda_user_info[11],
                    pre_sale_tel = panda_user_info[12],
                    after_sale_tel = panda_user_info[13],
                    service_tel = panda_user_info[14],
                    service_qq_first = panda_user_info[15],
                    service_qq_second = panda_user_info[16],
                    )

            #更新在售商品
            Product.objects.filter(supplier=supplier.id).update(owner=user.id)

            #订单数据处理
            Order.objects.filter(supplier=supplier.id).update(supplier=user.id)
            
            #运费模版
            cur.execute(u"select weapp_config_relation_id from postage_config_relation inner join postage_config on postage_config_relation.postage_config_id = postage_config.id and postage_config.owner_id='%d' " % (cur_owner_id)) 
            weapp_config_relation_ids = cur.fetchall()
            for weapp_config_relation_id in weapp_config_relation_ids:
                PostageConfig.objects.filter(id=weapp_config_relation_id[0]).update(owner = user.id)
                SpecialPostageConfig.objects.filter(postage_config_id=weapp_config_relation_id[0]).update(owner = user.id)
                FreePostageConfig.objects.filter(postage_config_id=weapp_config_relation_id[0]).update(owner = user.id)

            #仅售禁售
            cur.execute(u"select weapp_template_id from product_limit_zone_template_relation inner join product_limit_zone_template on product_limit_zone_template_relation.template_id = product_limit_zone_template.id and product_limit_zone_template.owner_id='%s'" %(cur_owner_id))
            weapp_template_ids = cur.fetchall()
            for weapp_template_id in weapp_template_ids:
                ProductLimitZoneTemplate.objects.filter(id=weapp_template_id[0]).update(owner = user.id)
            
            #
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

            #发货人
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
            
            #商品规格
            cur.execute(u"select weapp_property_id from product_model_property_relation inner join product_model_property on product_model_property_relation.model_property_id = product_model_property.id and product_model_property.owner_id='%s'" %(cur_owner_id))
            model_property_ids = cur.fetchall()
            for model_property_id in model_property_ids:
                ProductModelProperty.objects.filter(id=model_property_id[0]).update(owner = user.id)



