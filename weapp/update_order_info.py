# -*- coding: utf-8 -*-
import sys
import datetime
import copy
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

import json
from mall import models as mall_models
from eaglet.utils.resource_client import Resource

# 执行脚本前需要先把数据库中表结构里面加上四个字段，SQL语句如下：
# alter table mall_order_has_product add weight float(12) default 0,add thumbnail_url varchar(1024) default '',add product_model_name_texts varchar(1024) default '[]',add product_model_id integer(12) default 0;


# 一共需要更新四个字段，其中三个字段是通过下面的update_info()函数进行更新，另外一个字段product_model_id是通过sql语句进行更新，语句如下：
# update mall_order_has_product re join mall_product_model m on re.product_id = m.product_id and re.product_model_name = m.name set re.product_model_id= m.id；

##########################################处理数据更新############################################################
def update_info():
    relations = mall_models.OrderHasProduct.objects.filter(created_at__gte='2016-12-01 00:00:00')
    product_ids = [r.product_id for r in relations]
    id2product = dict([(product.id, product) for product in mall_models.Product.objects.filter(id__in=product_ids)])
    n = 0
    for relation in relations:
        product = id2product[relation.product_id]
        product.fill_specific_model(relation.product_model_name)
        l = []
        if product.custom_model_properties:
            for pro in product.custom_model_properties if product.custom_model_properties else []:
                l.append(pro['property_value'])
        mall_models.OrderHasProduct.objects.filter(id=relation.id).update(
            weight=product.weight,
            thumbnail_url=product.thumbnails_url,
            product_model_name_texts=json.dumps(l)
        )
        n += 1
        print n,"===================================",product.id

    # =================================更新productmodel_id的sql
    # update mall_order_has_product re join mall_product_model m on re.product_id = m.product_id and re.product_model_name = m.name set re.product_model_id= m.id
    

if __name__ == "__main__":
    update_info()
    print "=============================done"

######################################################################################################
