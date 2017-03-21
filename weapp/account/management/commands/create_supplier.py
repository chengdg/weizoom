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
        conn= MySQLdb.connect(
            host='rm-bp18wbhgz1493ad8to.mysql.rds.aliyuncs.com',
            port = 3306,
            user='panda',
            passwd='Weizoom@',
            db ='panda',
            charset="utf8"
            )
        cur = conn.cursor()
        # cur.execute(u"select user_id,supplier_id from account_has_supplier where user_id in (4)")
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
            cur.execute(u"select id,username,password from auth_user where id='%s'" % panda_id)
            panda_user = cur.fetchone()
            username = panda_user[1]
            password = panda_user[2]
            username = username + '_for_ghs'
            print panda_id, 'panda_id', username

            if not User.objects.filter(username=username):
                user = User.objects.create_user(username, 'none@weizoom.com', '123456')
                user.first_name = supplier.name
                user.password = password
                user.save()
                profile = user.get_profile()
                profile.store_name = supplier.name
                profile.webapp_type = 4 #供货商类型帐号
                profile.note = supplier.id
                profile.save()
            else:
                # continue
                user = User.objects.get(username=username)
                print 'already exists panda_id', panda_id

            #供货商配置
            if not CorpInfo.objects.filter(corp_id=user.id):
                cur.execute(u"select name,company_name,purchase_method,points,settlement_period,customer_from,max_product,company_type,contacter,phone,note,status,pre_sale_tel,after_sale_tel,customer_service_tel,customer_service_qq_first,customer_service_qq_second,valid_time_from,valid_time_to from account_user_profile where user_id='%d'" % (cur_owner_id)) 
                panda_user_info = cur.fetchone()
                if not CorpInfo.objects.filter(corp_id = user.id):
                    corp_info = CorpInfo.objects.create(
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
                        valid_time_from = panda_user_info[17],
                        valid_time_to = panda_user_info[18],
                        )
                    corp_info.valid_time_from = panda_user_info[17]
                    corp_info.valid_time_to = panda_user_info[18]
                    corp_info.save()


            #更新在售商品
            Product.objects.filter(supplier=supplier.id).update(owner=user.id, supplier=user.id)

            #订单数据处理
            Order.objects.filter(supplier=supplier.id).update(supplier=user.id)
            
            #运费模版
            cur.execute(u"select weapp_config_relation_id from postage_config_relation inner join postage_config on postage_config_relation.postage_config_id = postage_config.id and postage_config.owner_id='%d' " % (cur_owner_id)) 
            weapp_config_relation_ids = cur.fetchall()
            for weapp_config_relation_id in weapp_config_relation_ids:
                PostageConfig.objects.filter(id=weapp_config_relation_id[0]).update(owner=user.id, supplier_id=user.id)
                SpecialPostageConfig.objects.filter(postage_config_id=weapp_config_relation_id[0]).update(owner = user.id)
                FreePostageConfig.objects.filter(postage_config_id=weapp_config_relation_id[0]).update(owner = user.id)
            #删除创建默认模版
            PostageConfig.objects.filter(owner=user.id,name = u'免运费',added_weight="0.0",is_used=True).delete()

            #仅售禁售
            cur.execute(u"select weapp_template_id from product_limit_zone_template_relation inner join product_limit_zone_template on product_limit_zone_template_relation.template_id = product_limit_zone_template.id and product_limit_zone_template.owner_id='%s'" %(cur_owner_id))
            weapp_template_ids = cur.fetchall()
            for weapp_template_id in weapp_template_ids:
                ProductLimitZoneTemplate.objects.filter(id=weapp_template_id[0]).update(owner = user.id)
            
            #
            cur.execute(u"select id,owner_id,express_name,customer_name,customer_pwd,logistics_number,remark,is_deleted,sendsite from express_bill_accounts where owner_id ='%s' " %(cur_owner_id))
            express_bill_account_rows = cur.fetchall()
            if not ExpressBillAccount.objects.filter(owner_id = user.id):
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
            if not Shipper.objects.filter(owner_id = user.id):
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


            #未审核商品
            if Product.objects.filter(owner=user, is_accepted=False):
                continue
            cur.execute(u"select id,product_name,promotion_title,product_price,clear_price,product_weight,product_store,product_status,remark,valid_time_from,valid_time_to,limit_clear_price,has_limit_time,created_at,has_product_model,catalog_id,is_update,is_refused,refuse_reason,is_deleted ,limit_zone_type,limit_zone,has_same_postage,postage_money,postage_id from product_product where is_deleted=0 and owner_id='%s' and id not in (select product_id from product_has_relation_weapp)" %(cur_owner_id))
            products = cur.fetchall()
            for product in products:
                cur.execute(u"select weapp_config_relation_id from postage_config_relation where postage_config_id = '%s'" % product[24]) 
                weapp_config_relation_ids = cur.fetchall()
                if weapp_config_relation_ids:
                    weapp_config_relation_id = weapp_config_relation_ids[0][0]
                else:
                    weapp_config_relation_id = 0

                cur.execute(u"select weapp_template_id from product_limit_zone_template_relation where template_id = '%s'" % product[21])
                weapp_template_ids = cur.fetchall()
                if weapp_template_ids:
                    weapp_template_id = weapp_template_ids[0][0]
                else:
                    weapp_template_id = 0
                p = Product.objects.create(
                    owner = user,
                    name= product[1],
                    promotion_title= product[2],
                    bar_code= '',
                    thumbnails_url='',
                    pic_url='',
                    detail=product[8],
                    type= 'object',
                    is_use_online_pay_interface=False,
                    is_use_cod_pay_interface=False,
                    postage_type= 'custom_postage_type' if product[22] else 'unified_postage_type' ,
                    postage_id=weapp_config_relation_id,
                    unified_postage_money= product[23],
                    stocks= 0,
                    is_member_product= False,
                    supplier= user.id,
                    purchase_price= product[23],
                    is_enable_bill= False,
                    is_delivery= False,
                    limit_zone_type= product[20],
                    limit_zone= weapp_template_id,

                    status= product[7],
                    is_pre_product= False,
                    is_accepted= False
                )

                #分类
                cur.execute(u"select weapp_catalog_id from product_catalog_relation inner join product_catalog on product_catalog_relation.catalog_id = product_catalog.id and product_catalog.id='%s'" % product[15])
                classification_ids = cur.fetchall()
                classification_id = classification_ids[0][0]
                classification = Classification.objects.get(id=classification_id)
                ClassificationHasProduct.objects.create(
                    classification =  classification,
                    product_id = p.id,
                    woid = user.id,
                    display_index = 0
                )
                classification = Classification.objects.get(id=classification_id)
                classification.product_count += 1
                classification.save()

                cur.execute(u"select path from resource_image where id in (select image_id from product_image where product_id ='%s')" % product[0])
                product_images = cur.fetchall()
                for product_image in product_images:
                    ProductSwipeImage.objects.create(
                        product_id = p.id,
                        url = product_image[0]
                    )

                if product[14] == 0:
                    ProductModel.objects.create(
                        owner = user,
                        product = p,
                        name = 'standard',
                        is_standard = True,
                        price = product[3],
                        purchase_price = product[4],
                        weight = product[5],
                        stock_type = 1 if product[6]>1 else 0,
                        stocks = product[6],
                        user_code = '',
                        is_deleted = False
                    )
                else:
                    ProductModel.objects.create(
                        owner = user,
                        product = p,
                        name ='standard',
                        is_standard = True,
                        price = 0.0,
                        purchase_price = 0.0,
                        weight = 0,
                        stock_type = 0,
                        stocks = 0,
                        user_code = '',
                        is_deleted = True
                    )

                cur.execute(u"select id,name,is_standard,price,market_price,weight,stocks,user_code from product_model where is_deleted = 0 and product_id = '%s'" % product[0])
                product_models = cur.fetchall()
                for product_model in product_models:
                    single_model_properties = product_model[1].split('_')
                    weapp_model_properties = []
                    for single_model_property in single_model_properties:
                        temp_list = single_model_property.split(':')

                        cur.execute(u"select weapp_property_id from product_model_property_relation where model_property_id = '%s' " % temp_list[0])
                        weapp_property_ids = cur.fetchall()
                        weapp_property_id = weapp_property_ids[0][0]

                        cur.execute(u"select weapp_property_value_id from product_model_property_value_relation where property_value_id = '%s' " % temp_list[1])
                        weapp_property_value_ids = cur.fetchall()
                        weapp_property_value_id = weapp_property_value_ids[0][0]

                        weapp_model_properties.append(str(weapp_property_id) + ':' + str(weapp_property_value_id))

                    name = '_'.join(weapp_model_properties)

                    ProductModel.objects.create(
                        owner = user,
                        product = p,
                        name = name,
                        is_standard = False,
                        price = product_model[3],
                        purchase_price = product_model[4],
                        weight = product_model[5],
                        stock_type = 1,
                        stocks = product_model[6],
                        user_code = product_model[7],
                        is_deleted = False
                    )