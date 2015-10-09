# -*- coding: utf-8 -*-
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

from django.conf import settings
from django.db.models.aggregates import Sum
from django.db.models.aggregates import Count
from django.contrib.auth.models import User, Group, Permission

from modules.member.models import *
from account.models import UserProfile

webapp_ids = [user_profile.webapp_id for user_profile in UserProfile.objects.filter(is_active=True)]

#添加默认分组
for webapp_id in webapp_ids:
    if MemberTag.objects.filter(name='未分组', webapp_id=webapp_id).count() == 0:
        MemberTag.objects.create(name='未分组', webapp_id=webapp_id)

webapp_id2default_tag_id = dict([(tag.webapp_id, tag.id) for tag in MemberTag.objects.filter(webapp_id__in=webapp_ids) if tag.name == '未分组'])

member_id2webapp_id = dict([(m.id, m.webapp_id) for m in Member.objects.filter(webapp_id__in=webapp_ids)])

all_member_ids = member_id2webapp_id.keys()

has_tag_member_ids = [r.member_id for r in MemberHasTag.objects.all()]

need_add_default_tag_member = list(set(all_member_ids).difference(set(has_tag_member_ids)))

#把没有添加任何分组的会员添加到相应的‘未分组’当中
for member in need_add_default_tag_member:
    member_webapp_id = member_id2webapp_id[member.id]
    default_tag_id = webapp_id2default_tag_id[member_webapp_id]
    MemberHasTag.objects.created(member_id=member.id, tag_id=default_tag_id)