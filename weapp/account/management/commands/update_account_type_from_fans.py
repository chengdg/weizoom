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
        user_profiles = UserProfile.objects.all()
        usernames = ','.join([user.user.username for user in user_profiles])

        url = '%s/account/get_account_type_by_user_name/' % settings.FAN_HOST
        param = {
            'usernames': usernames
        }
        resp = requests.post(url, data=param)
        username2account_type = json.loads(resp.text)['data']

        for user in user_profiles:
            user.is_formal = int(username2account_type.get(user.user.username, 0))
            user.save()