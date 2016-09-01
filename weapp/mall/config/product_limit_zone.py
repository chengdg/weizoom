# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from mall.models import ProductLimitZoneTemplate
from tools.regional.models import City, Province

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

    def get(request):
        pass

class ProvincialCity(resource.Resource):
    app = 'mall2'
    resource = 'provincial_city'

    @login_required
    def api_get(request):
        template_id = int(request.GET.get('templateId', '0'))
        select_province_ids = []
        select_city_ids = []
        if ProductLimitZoneTemplate.objects.filter(id=template_id).count() > 0:
            template = ProductLimitZoneTemplate.objects.filter(id=template_id).first()
            select_province_ids = template.provinces.split(',')
            select_city_ids = template.cities.split(',')
        all_cities = City.objects.all()
        all_provinces = Province.objects.all()
        id2province = dict([(p.id, p) for p in all_provinces])

        provinces = []
        for id in id2province.keys():
            province_has_city = {
                    'province_id': id,
                    'province_name': id2province[id].name,
                    'is_selected': True if id in select_province_ids else False,
                    'cities': []
                    }
            for city in filter(lambda city: city.province_id == id, all_cities):
                province_has_city['cities'].append({
                        'city_id': city.id,
                        'city_name': city.name,
                        'is_selected': True if city.id in select_city_ids else False
                    })
            provinces.append(province_has_city)

        zones = []
        for zone_name in ZONE_NAMES:
            zones.append({
                'zone_name': zone_name,
                'provinces': filter(lambda province: PROVINCE_ID2ZONE[province['province_id']] == zone_name, provinces)
                })

        response = create_response(200)
        response.data = {'zones': zones}
        return response.get_response()