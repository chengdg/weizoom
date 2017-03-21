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
        for classification in classifications:
            count = ClassificationHasProduct.objects.filter(classification=classification, product_id__in=pooled_product_ids).count()
            classification.product_count = count
            classification.save()
        classifications = Classification.objects.filter(level=1)
        for classification in classifications:
            count = 0
            child_classifications = Classification.objects.filter(level=2, father_id=classification.id)
            for child_classification in child_classifications:
                count += child_classification.product_count
            classification.product_count = count
            classification.save()


        
                

