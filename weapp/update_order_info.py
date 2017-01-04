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

print('----start...')
relations = mall_models.OrderHasProduct.objects.all()
product_ids = [r.product_id for r in relations]
id2product = dict([(product.id, product) for product in mall_models.Product.objects.filter(id__in=product_ids)])
for relation in relations:
    product = id2product[relation.product_id]
    product.fill_specific_model(relation.product_model_name)
    l = []
    if product.custom_model_properties:
        for pro in product.custom_model_properties:
            l.append(pro['name'])
    mall_models.OrderHasProduct.objects.filter(id=relation.id).update(
        weight=product.weight,
        thumbnail_url=product.thumbnails_url,
        product_model_name_texts=json.dumps(l)
    )
print('end...')