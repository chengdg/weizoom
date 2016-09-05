# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from watchdog.utils import watchdog_warning, watchdog_error
from core.exceptionutil import unicode_full_stack
from core import resource
from core.jsonresponse import create_response

from mall import models as mall_models
from tools.regional.models import City, Province

from .. import export

ZONE_NAMES = [u'直辖市', u'华北-东北', u'华东地区', u'华南-华中', u'西北-西南', u'其它']

PROVINCE_ID2ZONE = {
    1: u'直辖市',
    2: u'直辖市',
    3: u'华北-东北',
    4: u'华北-东北',
    5: u'华北-东北',
    6: u'华北-东北',
    7: u'华北-东北',
    8: u'华北-东北',
    9: u'直辖市',
    10: u'华东地区',
    11: u'华东地区',
    12: u'华东地区',
    13: u'华东地区',
    14: u'华东地区',
    15: u'华东地区',
    16: u'华南-华中',
    17: u'华南-华中',
    18: u'华南-华中',
    19: u'华南-华中',
    20: u'华南-华中',
    21: u'华南-华中',
    22: u'直辖市',
    23: u'西北-西南',
    24: u'西北-西南',
    25: u'西北-西南',
    26: u'西北-西南',
    27: u'西北-西南',
    28: u'西北-西南',
    29: u'西北-西南',
    30: u'西北-西南',
    31: u'西北-西南',
    32: u'其它',
    33: u'其它',
    34: u'其它',
}

class ProductLimitZone(resource.Resource):
    app = 'mall2'
    resource = 'product_limit_zone'

    @login_required
    def get(request):
        """
        商品限购区域列表
        @return:
        """
        template_models = mall_models.ProductLimitZoneTemplate.objects.filter(owner=request.user).order_by('-id')
        all_cities = City.objects.all()
        all_provinces = Province.objects.all()
        templates = []
        for temp in template_models:
            city_ids = temp.cities.split(',')
            province_ids = temp.provinces.split(',')
            template_cities = filter(lambda city: str(city.id) in city_ids, all_cities)
            template_provinces = filter(lambda province: str(province.id) in province_ids, all_provinces)
            id2province = dict([(p.id, p) for p in template_provinces])

            provinces = []
            zone_names = []
            for id in sorted(id2province.keys()):
                province_has_city = {
                    'provinceId': id,
                    'provinceName': id2province[id].name,
                    'cities': []
                }
                province_has_city = rename_zone(province_has_city)
                for city in filter(lambda city: city.province_id == id, template_cities):
                    province_has_city['cities'].append({
                        'cityId': city.id,
                        'cityName': city.name
                    })
                provinces.append(province_has_city)
                if PROVINCE_ID2ZONE[id] not in zone_names:
                    zone_names.append(PROVINCE_ID2ZONE[id])
            zones = []
            for zone_name in zone_names:
                zones.append({
                    'zoneName': zone_name,
                    'provinces': filter(lambda province: PROVINCE_ID2ZONE[province['provinceId']] == zone_name,
                                        provinces)
                })
            templates.append({
                'templateId': temp.id,
                'templateName': temp.name,
                'zones': zones
            })
        c = RequestContext(request, {
            'first_nav_name': export.PRODUCT_FIRST_NAV,
            'second_navs': export.get_mall_product_second_navs(request),
            'second_nav_name': export.PRODUCT_LIMIT_ZONE,
            'templates': templates
        })

        return render_to_response('mall/editor/product_limit_zone.html', c)

    @login_required
    def api_get(request):
        pass

    @login_required
    def api_delete(request):
        template_id = request.POST.get('template_id', 0)
        owner = request.user
        if template_id:
            try:
                mall_models.ProductLimitZoneTemplate.objects.filter(owner=owner, id=template_id).delete()
                mall_models.Product.objects.filter(limit_zone=template_id).update(limit_zone_type=0, limit_zone=0)
                return create_response(200).get_response()
            except:
                return create_response(500).get_response()
        else:
            error_msg = u"删除商品限购区域模板失败, cause:\n{}".format(unicode_full_stack())
            watchdog_error(error_msg)
            return create_response(500).get_response()

class ProductLimitZoneTemplate(resource.Resource):
    app = 'mall2'
    resource = 'product_limit_zone_template'

    @login_required
    def get(request):
        """
        商品限购区域列表
        @return:
        """
        template_id = request.GET.get('template_id', 0)
        zones = []
        template_name = ''
        provinces = []
        cities = []
        if template_id:
            template_model = mall_models.ProductLimitZoneTemplate.objects.filter(id=template_id).first()
            if template_model.provinces:
                provinces = Province.objects.filter(id__in=template_model.provinces.split(','))
            if template_model.cities:
                cities = City.objects.filter(id__in=template_model.cities.split(','))
            template_name = template_model.name
            for province in provinces:
                zone = {
                    'provinceId': province.id,
                    'provinceName': province.name,
                    'zoneName': PROVINCE_ID2ZONE[province.id],
                    'cities': []
                }
                zone = rename_zone(zone)
                for city in filter(lambda city: city.province_id == province.id, cities):
                    zone['cities'].append({
                            'cityId': city.id,
                            'cityName': city.name
                        })
                zones.append(zone)
        c = RequestContext(request, {
            'first_nav_name': export.PRODUCT_FIRST_NAV,
            'second_navs': export.get_mall_product_second_navs(request),
            'second_nav_name': export.PRODUCT_LIMIT_ZONE,
            'templateId' : template_id,
            'templateName': template_name,
            'zones': zones
        })

        return render_to_response('mall/editor/product_limit_zone_template.html', c)

    @login_required
    def api_put(request):
        try:
            owner = request.user
            province_ids = json.loads(request.POST.get('province_ids', '[]'))
            city_ids = json.loads(request.POST.get('city_ids', '[]'))
            template_name = request.POST.get('template_name', '')
            mall_models.ProductLimitZoneTemplate.objects.create(
                    owner=owner,
                    name=template_name,
                    provinces=','.join(province_ids),
                    cities=','.join(city_ids)
                )
            return create_response(200).get_response()
        except:
            error_msg = u"创建商品限购区域模板失败, cause:\n{}".format(unicode_full_stack())
            watchdog_error(error_msg)
            return create_response(500).get_response()

    @login_required
    def api_post(request):
        template_id = int(request.POST.get('template_id', '0'))
        template_name = request.POST.get('template_name', '')

        province_ids = json.loads(request.POST.get('province_ids', '[]'))
        city_ids = json.loads(request.POST.get('city_ids', '[]'))

        if template_id and template_name:
            mall_models.ProductLimitZoneTemplate.objects.filter(
                    owner=request.user,
                    id=template_id
                ).update(
                    name=template_name,
                    provinces=','.join(province_ids),
                    cities=','.join(city_ids)
                )
            return create_response(200).get_response()
        else:
            return create_response(500).get_response()

class ProvincialCity(resource.Resource):
    app = 'mall2'
    resource = 'provincial_city'

    @login_required
    def api_get(request):
        all_cities = City.objects.all()
        all_provinces = Province.objects.all()
        id2province = dict([(p.id, p) for p in all_provinces])

        provinces = []
        for id in id2province.keys():
            province_has_city = {
                    'provinceId': id,
                    'provinceName': id2province[id].name,
                    'cities': []
                    }
            province_has_city = rename_zone(province_has_city)

            for city in filter(lambda city: city.province_id == id, all_cities):
                province_has_city['cities'].append({
                        'cityId': city.id,
                        'cityName': city.name,
                    })
            provinces.append(province_has_city)

        zones = []
        for zone_name in ZONE_NAMES:
            zones.append({
                'zoneName': zone_name,
                'provinces': filter(lambda province: PROVINCE_ID2ZONE[province['provinceId']] == zone_name, provinces)
                })

        response = create_response(200)
        response.data = {'items': zones}
        return response.get_response()

def rename_zone(zone):
    if zone['provinceId'] == 5:
        zone['provinceName'] = u'内蒙古'
    elif zone['provinceId'] == 20:
        zone['provinceName'] = u'广西'
    elif zone['provinceId'] == 26:
        zone['provinceName'] = u'西藏'
    elif zone['provinceId'] == 30:
        zone['provinceName'] = u'宁夏'
    elif zone['provinceId'] == 31:
        zone['provinceName'] = u'新疆'
    elif zone['provinceId'] == 32:
        zone['provinceName'] = u'香港'
    elif zone['provinceId'] == 33:
        zone['provinceName'] = u'澳门'
    elif zone['provinceId'] == 34:
        zone['provinceName'] = u'台湾'
    return zone