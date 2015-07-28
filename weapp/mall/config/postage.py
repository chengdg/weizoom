# -*- coding: utf-8 -*-
"""@package mall.product_postage_views
商品运费模板模块的页面的实现文件

一个运费模板包括以下三部分：
    - 默认运费：首重，首重价格，续重，续重价格
    - 特殊地区运费：地域，首重，首重价格，续重，续重价格
    - 指定地区包邮条件：地域，包邮条件

其中，“默认运费”必填，而“特殊地区运费”和“指定地区包邮条件”可以选填，而且一个运费模板中可以有多个“特殊地区运费”和多个“指定地区包邮条件”
"""

import json

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from core import resource
from core.jsonresponse import create_response

from mall.models import PostageConfig, SpecialPostageConfig, FreePostageConfig
from mall import export

COUNT_PER_PAGE = 20
FIRST_NAV = export.MALL_CONFIG_FIRST_NAV

class Postage(resource.Resource):
    app = 'mall2'
    resource = 'postage'

    @login_required
    def get(request):
        """
        创建、编辑运费模板页面

        @param id 运费模板id
        """
        id = request.GET.get('id', None)
        if id:
            postage_config = PostageConfig.objects.get(id=id)

            jsons = []
            special_configs = []
            for special_config in SpecialPostageConfig.objects.filter(postage_config=postage_config):
                special_configs.append({
                    "id": special_config.id,
                    "destination": special_config.destination,
                    "destination_str": special_config.destination_str,
                    "first_weight": special_config.first_weight,
                    "first_weight_price": special_config.first_weight_price,
                    "added_weight": special_config.added_weight,
                    "added_weight_price": special_config.added_weight_price
                })

            free_configs = list(FreePostageConfig.objects.filter(postage_config=postage_config))

            jsons = [{
                "name": "special_configs", "content": special_configs
            }]
            c = RequestContext(request, {
                'first_nav_name': FIRST_NAV,
                'second_navs': export.get_config_second_navs(request),
                'second_nav_name': export.MALL_CONFIG_POSTAGE_NAV,
                'postage_config': postage_config,
                'free_configs': free_configs,
                'jsons': jsons
            })
        else:
            c = RequestContext(request, {
                'first_nav_name': FIRST_NAV,
                'second_navs': export.get_config_second_navs(request),
                'second_nav_name': export.MALL_CONFIG_POSTAGE_NAV,
                'postage_config': None
            })
        return render_to_response('mall/editor/edit_postage_config.html', c)


    @login_required
    def api_put(request):
        """

        创建运费模板

        Method: POST

        @param name 运费模板名
        @param firstWeight  默认运费的首重
        @param firstWeightPrice  默认运费的首重价格
        @param addedWeight  默认运费的续重
        @param addedWeightPrice  默认运费的续重价格
        @param isEnableSpecialConfig 是否启用“特殊地区运费”
        @param specialConfigs 特殊地区运费信息的json字符串
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
                [{
                        destination: [上海, 北京, ...],
                        firstWeight: 1.0,
                        firstWeightPrice: 5.5,
                        addedWeight: 0.5,
                        addedWeightPrice: 3.0
                }, {
                        ......
                }]
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        @param isEnableFreeConfig 是否启用“特殊地区包邮条件”
        @param freeConfigs 特殊地区包邮条件的json字符串
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
                [{
                        destination: [上海, 北京, ...],
                        condition: 'count', //count代表数量，price代表价格
                        value: 3 //condition条件需要满足的值
                }, {
                        ......
                }]
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        name = request.POST['name']
        first_weight = round(float(request.POST['firstWeight']), 1)
        first_weight_price = round(float(request.POST['firstWeightPrice']), 2)
        added_weight = round(float(request.POST['addedWeight']), 1)
        added_weight_price = round(float(request.POST['addedWeightPrice']), 2)
        is_enable_special_config = (request.POST.get('isEnableSpecialConfig', 'false') == 'true')
        special_configs = json.loads(request.POST.get('specialConfigs', '[]'))
        is_enable_free_config = (request.POST.get('isEnableFreeConfig', 'false') == 'true')
        free_configs = json.loads(request.POST.get('freeConfigs', '[]'))

        #更新当前被使用的postage config状态
        PostageConfig.objects.filter(owner=request.manager, is_used=True).update(is_used=False)

        postage_config = PostageConfig.objects.create(
            owner=request.manager,
            name=name,
            first_weight=first_weight,
            first_weight_price=first_weight_price,
            added_weight=added_weight,
            added_weight_price=added_weight_price,
            is_enable_special_config=is_enable_special_config,
            is_enable_free_config=is_enable_free_config,
            is_used=True
        )

        if is_enable_special_config:

            for special_config in special_configs:
                special_config = SpecialPostageConfig.objects.create(
                    owner=request.manager,
                    postage_config=postage_config,
                    destination=','.join(special_config.get('destination', [])),
                    first_weight= round(float(special_config.get('firstWeight', 0.0)), 1),
                    first_weight_price= round(float(special_config.get('firstWeightPrice', 0.0)), 2),
                    added_weight = round(float(special_config.get('addedWeight', 0.0)), 1),
                    added_weight_price = round(float(special_config.get('addedWeightPrice', 0.0)), 2)
                )
        if is_enable_free_config:
            for free_config in free_configs:
                free_config = FreePostageConfig.objects.create(
                    owner=request.manager,
                    postage_config=postage_config,
                    destination = ','.join(free_config.get('destination', [])),
                    condition = free_config.get('condition', 'count'),
                    condition_value = free_config.get('value', 1)
                )

        response = create_response(200)
        return response.get_response()


    @login_required
    def api_post(request):
        """
        更新运费模板

        Method: POST

        @param id 运费模板id
        @param name 运费模板名
        @param firstWeight  默认运费的首重
        @param firstWeightPrice  默认运费的首重价格
        @param addedWeight  默认运费的续重
        @param addedWeightPrice  默认运费的续重价格
        @param isEnableSpecialConfig 是否启用“特殊地区运费”
        @param specialConfigs 特殊地区运费信息的json字符串
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
                [{
                        id: 1, //如果id < 0，则表示要新建；否则，表示需要更新
                        destination: [上海, 北京, ...],
                        firstWeight: 1.0,
                        firstWeightPrice: 5.5,
                        addedWeight: 0.5,
                        addedWeightPrice: 3.0
                }, {
                        ......
                }]
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        @param isEnableFreeConfig 是否启用“特殊地区包邮条件”
        @param freeConfigs 特殊地区包邮条件的json字符串
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
                [{
                        id: 1, //如果id < 0，则表示要新建；否则，表示需要更新
                        destination: [上海, 北京, ...],
                        condition: 'count', //count代表数量，price代表价格
                        value: 3 //condition条件需要满足的值
                }, {
                        ......
                }]
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        id = request.POST.get('id', None)
        if not id:
            response = create_response(200)
            return response.get_response()

        is_used = request.POST.get('is_used', None)
        name = request.POST.get('name', None)
        if is_used and not name:
            PostageConfig.objects.filter(owner=request.manager, is_used=True).update(is_used=False)
            PostageConfig.objects.filter(owner=request.manager, id=id).update(is_used=True)
            response = create_response(200)
            return response.get_response()

        name = request.POST['name']
        first_weight = request.POST['firstWeight']
        first_weight_price = request.POST['firstWeightPrice']
        added_weight = request.POST['addedWeight']
        added_weight_price = request.POST['addedWeightPrice']
        is_enable_special_config = (
            request.POST.get(
                'isEnableSpecialConfig',
                'false') == 'true')
        special_configs = json.loads(request.POST.get('specialConfigs', '[]'))
        is_enable_free_config = (
            request.POST.get(
                'isEnableFreeConfig',
                'false') == 'true')
        free_configs = json.loads(request.POST.get('freeConfigs', '[]'))

        PostageConfig.objects.filter(id=id).update(
            name=name,
            first_weight=first_weight,
            first_weight_price=first_weight_price,
            added_weight=added_weight,
            added_weight_price=added_weight_price,
            is_enable_special_config=is_enable_special_config,
            is_enable_free_config=is_enable_free_config
        )

        # 更新special config
        if is_enable_special_config:
            special_config_ids = set([config['id'] for config in special_configs])
            existed_special_config_ids = set(
                [config.id
                for config in
                SpecialPostageConfig.objects.filter(postage_config_id=id)])
            for special_config in special_configs:
                config_id = special_config['id']
                if config_id < 0:
                    special_config = SpecialPostageConfig.objects.create(
                        owner=request.manager,
                        postage_config_id=id,
                        destination=','.join(special_config.get('destination', [])),
                        first_weight=special_config.get('firstWeight', 0.0),
                        first_weight_price=special_config.get('firstWeightPrice', 0.0),
                        added_weight=special_config.get('addedWeight', 0.0),
                        added_weight_price=special_config.get('addedWeightPrice', 0.0)
                    )
                else:
                    SpecialPostageConfig.objects.filter(id=config_id).update(
                        destination=','.join(special_config.get('destination', [])),
                        first_weight=special_config.get('firstWeight', 0.0),
                        first_weight_price=special_config.get('firstWeightPrice', 0.0),
                        added_weight=special_config.get('addedWeight', 0.0),
                        added_weight_price=special_config.get('addedWeightPrice', 0.0)
                    )
            ids_to_be_delete = existed_special_config_ids - special_config_ids
            SpecialPostageConfig.objects.filter(id__in=ids_to_be_delete).delete()

        # 更新free config
        if is_enable_free_config:
            free_config_ids = set([config['id'] for config in free_configs])
            existed_free_config_ids = set(
                [config.id
                for config in
                FreePostageConfig.objects.filter(
                    postage_config_id=id)])
            for free_config in free_configs:
                config_id = free_config['id']
                if config_id < 0:
                    free_config = FreePostageConfig.objects.create(
                        owner=request.manager,
                        postage_config_id=id,
                        destination=','.join(free_config.get('destination', [])),
                        condition=free_config.get('condition', 'count'),
                        condition_value=free_config.get('value', 1)
                    )
                else:
                    FreePostageConfig.objects.filter(id=config_id).update(
                        destination=','.join(free_config.get('destination', [])),
                        condition=free_config.get('condition', 'count'),
                        condition_value=free_config.get('value', 1)
                    )
            ids_to_be_delete = existed_free_config_ids - free_config_ids
            FreePostageConfig.objects.filter(id__in=ids_to_be_delete).delete()

        response = create_response(200)
        return response.get_response()

    @login_required
    def api_delete(request):
        """

        删除运费模板

        Method: POST

        @param id 运费模板id

        """
        postage_config_id = request.POST.get('id', None)
        if postage_config_id:
            PostageConfig.objects.filter(owner=request.manager, id=postage_config_id).update(is_used=False, is_deleted=True)
            PostageConfig.objects.filter(owner=request.manager, is_system_level_config=True).update(is_used=True)

        response = create_response(200)
        return response.get_response()


class PostageList(resource.Resource):
    app = 'mall2'
    resource = 'postage_list'

    @login_required
    def get(request):
        """
        运费模板列表页面
        """
        postage_configs = [config for config in PostageConfig.objects.filter(owner=request.manager) if not config.is_deleted]
        config_ids = []
        id2config = {}
        for config in postage_configs:
            config.special_configs = []
            id2config[config.id] = config
            if config.is_enable_special_config:
                config_ids.append(config.id)

        for special_config in SpecialPostageConfig.objects.filter(postage_config_id__in=config_ids):
            config_id = special_config.postage_config_id
            id2config[config_id].special_configs.append(special_config)

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_config_second_navs(request),
            'second_nav_name': export.MALL_CONFIG_POSTAGE_NAV,
            'postage_configs': postage_configs
        })
        return render_to_response('mall/editor/postage_configs.html', c)