# -*- coding: utf-8 -*-
"""@package mall.product_postage_api_views
商品运费模块的API的实现文件
"""

import json

from django.contrib.auth.decorators import login_required

from models import PostageConfig, SpecialPostageConfig, FreePostageConfig
from core.restful_url_route import api
from core.jsonresponse import create_response


@api(app='mall', resource='postage_template', action='create')
@login_required
def create_postage_template(request):
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


@api(app='mall', resource='postage_template', action='update')
@login_required
def update_postage_template(request):
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
    id = request.POST['id']
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


@api(app='mall', resource='postage_template', action='delete')
@login_required
def delete_postage_template(request):
    """

    删除运费模板

    Method: POST

    @param id 运费模板id

    """
    postage_config_id = request.POST['id']
    PostageConfig.objects.filter(id=postage_config_id).update(is_used=False, is_deleted=True)
    PostageConfig.objects.filter(owner=request.manager, is_system_level_config=True).update(is_used=True)

    response = create_response(200)
    return response.get_response()


@api(app='mall', resource='used_postage_template', action='create')
@login_required
def create_used_postage_template(request):
    """
    切换运费模板

    Method: POST

    @param id 运费模板id
    """
    id = request.POST['id']
    PostageConfig.objects.filter(owner=request.manager, is_used=True).update(is_used=False)
    PostageConfig.objects.filter(id=id).update(is_used=True)

    response = create_response(200)
    return response.get_response()
