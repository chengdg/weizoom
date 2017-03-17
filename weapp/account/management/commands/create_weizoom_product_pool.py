# -*- coding: utf-8 -*-

import json
import requests
import MySQLdb

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group


from account.models import UserProfile, CorpInfo
from mall import models as mall_models

class Command(BaseCommand):
    help = "create weizoom product pool"
    args = ''

    def handle(self, *args, **options):
        weizoom_corp_id = UserProfile.objects.get(webapp_type=2).user_id
        pooled_product_ids = set([pooled_product.product_id for pooled_product in mall_models.ProductPool.objects.filter(type=1)])
        weizoom_pooled_product_ids = set([pooled_product.product_id for pooled_product in mall_models.ProductPool.objects.filter(woid=weizoom_corp_id)])
        need_add_product_ids = pooled_product_ids - weizoom_pooled_product_ids
        for product in mall_models.Product.objects.filter(is_deleted=False,id__in=need_add_product_ids):
            # try:
            #     print 'add %s' % product.name
            # except:
            #     print 'add %s' % product.id
            mall_models.ProductPool.objects.create(
                woid=weizoom_corp_id,
                product_id=product.id,
                status=mall_models.PP_STATUS_ON,
                display_index=1,
                type=1,
                sync_at=product.created_at
            )
                

