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


##########################################多进程处理数据更新############################################################
def update_info(index_start,index_stop):
  print index_start,index_stop,'>>>>>>>>>> asd'
  relations = mall_models.OrderHasProduct.objects.filter(id__range=[index_start,index_stop])
  print len(relations),'>>>>>>>>>> asd11111'
  product_ids = [r.product_id for r in relations]
  id2product = dict([(product.id, product) for product in mall_models.Product.objects.filter(id__in=product_ids)])
  for relation in relations:
      product = id2product[relation.product_id]
      product.fill_specific_model(relation.product_model_name)
      l = []
      if product.custom_model_properties:
          for pro in product.custom_model_properties:
              l.append(pro['property_value'])
      mall_models.OrderHasProduct.objects.filter(id=relation.id).update(
          weight=product.weight,
          thumbnail_url=product.thumbnails_url,
          product_model_name_texts=json.dumps(l)
      )


if __name__ == "__main__":
    from multiprocessing import Pool
    pool = Pool(processes=130)
    n = 1
    result = []
    for i in range(130):
        if n>=641877:
            result.append(pool.apply_async(update_info, (n-5000,641877)))
        else:
            result.append(pool.apply_async(update_info, (n,n+5000)))
        n+=5000
    pool.close()
    pool.join()
    m = 0
    for res in result:
        print m,"============================="
        m+=1
    print "Sub-process(es) done."
######################################################################################################
