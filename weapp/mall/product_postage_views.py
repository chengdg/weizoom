# -*- coding: utf-8 -*-
"""@package mall.product_postage_views
商品运费模板模块的页面的实现文件

一个运费模板包括以下三部分：
    - 默认运费：首重，首重价格，续重，续重价格
    - 特殊地区运费：地域，首重，首重价格，续重，续重价格
    - 指定地区包邮条件：地域，包邮条件

其中，“默认运费”必填，而“特殊地区运费”和“指定地区包邮条件”可以选填，而且一个运费模板中可以有多个“特殊地区运费”和多个“指定地区包邮条件”
"""


from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from models import *
import export
from core.restful_url_route import *


COUNT_PER_PAGE = 20
FIRST_NAV = export.MALL_CONFIG_FIRST_NAV


@view(app='mall', resource='postage_templates', action='get')
@login_required
def get_postage_templates(request):
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


@view(app='mall', resource='postage_template', action='create')
@login_required
def create_postage_template(request):
    """
    创建运费模板页面
    """
    c = RequestContext(request, {
        'first_nav_name': FIRST_NAV,
        'second_navs': export.get_config_second_navs(request),
        'second_nav_name': export.MALL_CONFIG_POSTAGE_NAV,
        'postage_config': None
    })
    return render_to_response('mall/editor/edit_postage_config.html', c)


@view(app='mall', resource='postage_template', action='edit')
@login_required
def edit_postage_template(request):
    """
    编辑运费模板页面

    @param id 运费模板id
    """
    id = request.GET['id']
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
    return render_to_response('mall/editor/edit_postage_config.html', c)
