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
    help = "create weizoom product pool"
    args = ''

    def handle(self, *args, **options):
        classifications = Classification.objects.filter(level=2)
        weizoom_corp_id = UserProfile.objects.get(webapp_type=2).user_id
        pooled_product_ids = set([pooled_product.product_id for pooled_product in ProductPool.objects.filter(type=1)])
        products = Product.objects.filter(id__in=pooled_product_ids, is_accepted=True)
        product_ids = [p.id for p in products]
        for classification in classifications:
            relations = ClassificationHasProduct.objects.filter(classification=classification, product_id__in=product_ids)
            cur_product_ids = set([r.product_id for r in relations])
            classification.product_count = len(cur_product_ids)
            classification.save()
        classifications = Classification.objects.filter(level=1)
        for classification in classifications:
            child_classifications = Classification.objects.filter(level=2, father_id=classification.id)
            child_classification_ids = [c.id for c in child_classifications]
            relations = ClassificationHasProduct.objects.filter(classification__in=child_classification_ids, product_id__in=product_ids)
            cur_product_ids = set([r.product_id for r in relations])
            classification.product_count = len(cur_product_ids)
            classification.save()


        
                

