#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'kuki'

from behave import *
from test import bdd_util
from collections import OrderedDict

from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
import termite.pagestore as pagestore_manager
from apps.customerized_apps.red_packet.models import RedPacket, RedPacketParticipance, RedPacketControl,RedPacketLog,RedPacketDetail
from weixin.message.material import models as material_models
from modules.member.models import Member, SOURCE_MEMBER_QRCODE
from utils.string_util import byte_to_hex
import json
import re

import time
from django.core.management.base import BaseCommand, CommandError
from utils.cache_util import SET_CACHE
from modules.member.models import Member

def __get_red_packet_rule_name(title):
	material_url = material_models.News.objects.get(title=title).url
	red_packet_rule_name = material_url.split('-')[1]
	return red_packet_rule_name

def __get_red_packet_rule_id(red_packet_rule_name):
	return RedPacket.objects.get(name=red_packet_rule_name).id

def __get_channel_qrcode_name(red_packet_rule_id):
	return RedPacket.objects.get(id=red_packet_rule_id).qrcode['name']