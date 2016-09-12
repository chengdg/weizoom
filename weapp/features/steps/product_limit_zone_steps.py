#-*- coding:utf-8 -*-
import json
import types

from behave import *
from test import bdd_util
from features.testenv.model_factory import *
from django.test.client import Client
from django.contrib.auth.models import User

from mall.models import ProductLimitZoneTemplate
from tools.regional.models import City, Province

@then(u"{user}能获得限定区域列表")
def step_impl(context, user):
    url = '/mall2/product_limit_zone/'

    response = context.client.get(url)
    templates = response.context['templates']
    expected = json.loads(context.text)
    actual = []
    for template in templates:
        template_data = {}
        template_data['name'] = template['templateName']
        limit_area = []
        for zone in template['zones']:
            zone_data = {}
            if zone['zoneName'] in [u'直辖市', u'其它']:
                zone_data['area'] = zone['zoneName']
                province_list = []
                for province in zone['provinces']:
                    province_list.append(province['provinceName'])
                zone_data['province'] = province_list
                limit_area.append(zone_data)
            else:
                for province in zone['provinces']:
                    zone_data = {}
                    zone_data['area'] = province['zoneName']
                    zone_data['province'] = province['provinceName']
                    zone_data['city'] = []
                    for city in province['cities']:
                        zone_data['city'].append(city['cityName'])
                    limit_area.append(zone_data)
        template_data['limit_area'] = limit_area
        template_data["actions"] = [u"修改", u"删除"]
        actual.append(template_data)

    bdd_util.assert_list(expected, actual)

@when(u"{user}添加限定区域配置")
def step_impl(context, user):
    data = json.loads(context.text)
    url = '/mall2/api/product_limit_zone_template/?_method=put'

    template_name = data['name']
    provinces = []
    cities = []
    for limit_area in data['limit_area']:
        if type(limit_area['province']) is types.UnicodeType:
            provinces.append(limit_area['province'])
        if type(limit_area['province']) is types.ListType:
            provinces += limit_area['province']
        if limit_area.has_key('city'):
            cities += limit_area['city']
    province_ids = []

    for province in provinces:
        province_ids.append(str(Province.objects.filter(name__contains=province).first().id))
    city_ids = City.objects.filter(name__in=cities).values_list('id', flat=True)
    args = {
        'template_name': template_name,
        'province_ids': json.dumps(province_ids),
        'city_ids': json.dumps([str(id) for id in city_ids])
    }
    response = context.client.post(url, args)
    bdd_util.assert_api_call_success(response)

@when(u"{user}修改'{template_name}'限定区域配置")
def step_impl(context, user, template_name):
    user = User.objects.filter(username=user)
    template_id = ProductLimitZoneTemplate.objects.filter(owner=user, name=template_name).first().id

    data = json.loads(context.text)
    url = '/mall2/api/product_limit_zone_template/'

    template_name = data['name']
    provinces = []
    cities = []
    for limit_area in data['limit_area']:
        if type(limit_area['province']) is types.UnicodeType:
            provinces.append(limit_area['province'])
        if type(limit_area['province']) is types.ListType:
            provinces += limit_area['province']
        if limit_area.has_key('city'):
            cities += limit_area['city']
    province_ids = []

    for province in provinces:
        province_ids.append(str(Province.objects.filter(name__contains=province).first().id))
    city_ids = City.objects.filter(name__in=cities).values_list('id', flat=True)
    args = {
        'template_id': template_id,
        'template_name': template_name,
        'province_ids': json.dumps(province_ids),
        'city_ids': json.dumps([str(id) for id in city_ids])
    }
    response = context.client.post(url, args)
    bdd_util.assert_api_call_success(response)

@when(u"{user}删除'{template_name}'限定区域配置")
def step_impl(context, user, template_name):
    user = User.objects.filter(username=user)
    template_id = ProductLimitZoneTemplate.objects.filter(owner=user, name=template_name).first().id
    url = "/mall2/api/product_limit_zone/?_method=delete"

    response = context.client.post(url, {'template_id': template_id})
    bdd_util.assert_api_call_success(response)