# -*- coding: utf-8 -*-

import json
import requests

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from account.models import UserProfile

class Command(BaseCommand):
    help = "update account_type from fans"
    args = ''

    def handle(self, *args, **options):
        """
        同步fans中账户类型(正式/体验)到weapp中
        """
        user_profiles = UserProfile.objects.exclude(store_name='')
        store_names = ','.join([user.store_name for user in user_profiles])

        url = '%s/account/get_account_type_by_store_name/' % settings.FAN_HOST
        param = {
            'store_names': store_names
        }
        resp = requests.post(url, data=param)
        text = json.loads(resp.text)
        store_name2account_type = text['data']

        for user in user_profiles:
            user.is_formal = int(store_name2account_type.get(user.store_name, 1))
            user.save()

