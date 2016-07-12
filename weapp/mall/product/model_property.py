# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from eaglet.utils.resource_client import Resource

from core import resource
from core.jsonresponse import create_response
from mall import models as mall_models
from mall import export, signals
from weapp.settings import ZEUS_HOST
from weapp.settings import ZEUS_SERVICE_NAME as SERVICE_NAME


class ModelPropertyList(resource.Resource):
    app = 'mall2'
    resource = 'model_property_list'

    @login_required
    def get(request):
        """
        商品规格列表页面.
        """
        params = {
            'owner_id': request.manager.id,
        }
        # 创建模板
        resp = Resource.use(SERVICE_NAME, ZEUS_HOST).get({
            'resource': 'mall.product_model_property_list',
            'data': params
        })
        result = []
        if resp and resp['code'] == 200:

            model_properties = resp['data']['product_models']
            # 重新操作页面方便
            for model_property in model_properties:
                product_model = model_property['product_model']
                property_values = model_property['properties']

                product_model['shot_name'] = product_model.get('name')[:6] \
                    if len(product_model.get('name')) > 6 else product_model.get('name')
                product_model['type'] = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT \
                    if product_model.get('type') == 'text' \
                    else mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE

                for value in property_values:
                    value['shot_name'] = value.get('name')[:10] if len(value.get('name')) > 10 else value.get('name')
                    value['is_image_property_value'] = product_model.get('type') \
                                                             == mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE \
                                                       and product_model.get('pic_url')
                product_model['property_values'] = property_values
                result.append(product_model)

        c = RequestContext(request, {
            'first_nav_name': export.PRODUCT_FIRST_NAV,
            'second_navs': export.get_mall_product_second_navs(request),
            'second_nav_name': export.PRODUCT_MANAGE_MODEL_NAV,
            'model_properties': result
        })
        return render_to_response('mall/editor/model_properties.html', c)

    @login_required
    def api_get(request):
        """
        获取全部规格属性集合

        Return json:

          Example:
            [{
                id: 1,
                name: "颜色",
                type: "text",
                values: [{
                    id: 1,
                    full_id: "1:1", //full_id表示${property.id}:${value.id}
                    name: "红",
                    image: ""
                }, {
                    id: 2,
                    name: "白"
                    image: ""
                }, {
                    ......
                }]
            }, {
                ......
            }]
        """
        properties = []
        user_pmp = mall_models.ProductModelProperty.objects.filter(
            owner=request.manager,
            is_deleted=False
        )
        for property in user_pmp:
            values = []
            pro_pmp = mall_models.ProductModelPropertyValue.objects.filter(
                property=property,
                is_deleted=False
            )
            for value in pro_pmp:
                shot_name = value.name
                if len(shot_name) > 9:
                    shot_name = shot_name[:9]+'...'
                values.append({
                    "id": value.id,
                    "fullId": '%s:%s' % (property.id, value.id),
                    "name": value.name,
                    "shot_name": shot_name,
                    "image": value.pic_url
                })

            properties.append({
                "id": property.id,
                "name": property.name,
                "type": "text" if property.type ==mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT else "image",
                "values": values
            })

        response = create_response(200)
        response.data = properties
        return response.get_response()


class ModelProperty(resource.Resource):
    app = 'mall2'
    resource = 'model_property'

    @login_required
    def api_put(request):
        """
        创建一个空的规格属性

        Return json:
          data: %d

        """
        params = {
            'owner_id': request.manager.id,
            'name': '',
            'type': 'text'
        }
        # 创建模板
        resp = Resource.use(SERVICE_NAME, ZEUS_HOST).put({
            'resource': 'mall.product_model_property',
            'data': params
        })
        if resp and resp['code'] == 200:
            _property = resp['data'].get('product_model')

            response = create_response(200)
            response.data = _property.get('id')
            return response.get_response()

    @login_required
    def api_post(request):
        """
        更新规格属性.

        Args:
          id: 规格id
          filed: 指定更新规格的哪个属性: name or type
            name -> 新的规格名,
            type -> 新的规格类型. text或image
        """
        model_id = request.POST['id']
        field = request.POST['field']
        get_params = {
            'id': model_id
        }
        resp = Resource.use(SERVICE_NAME, ZEUS_HOST).get({
            'resource': 'mall.product_model_property',
            'data': get_params
        })
        if resp:
            if resp.get('code') == 200:
                _model = resp.get('data').get('product_model')
                if _model:
                    name = _model.get('name')
                    model_type = _model.get('type')
                    if field == 'name':
                        name = request.POST['name']
                    if field == 'type':
                        model_type = request.POST.get('type')
                    params = {
                        'id': model_id,
                        'name': name,
                        'type': model_type
                    }
                    post_resp = Resource.use(SERVICE_NAME, ZEUS_HOST).post({
                        'resource': 'mall.product_model_property',
                        'data': params
                    })
                    if post_resp and post_resp.get('code') == 200:
                        response = create_response(200)
                        return response.get_response()
            else:
                response = create_response(resp.get('code'))
                return response.get_response()

    @login_required
    def api_delete(request):
        """删除规格属性

        Args:
          id: 规格id

        Note: 删除规格属性后，会send pre_delete_product_model_property signal，
          处理由于规格变化引起的商品状态的变化.
        """
        property_id = request.POST['id']
        # TODO 怎么改造 --------------start------------------
        model_property = mall_models.ProductModelProperty.objects.get(
            owner=request.manager,
            id=property_id)

        signals.pre_delete_product_model_property.send(
            sender=mall_models.ProductModelProperty,
            model_property=model_property,
            request=request)
        # TODO 怎么改造 --------------end ------------------

        params = {
            'id': property_id,
            # 'name': name,
            # 'type': model_type
        }
        resp = Resource.use(SERVICE_NAME, ZEUS_HOST).delete({
            'resource': 'mall.product_model_property',
            'data': params
        })

        if resp:
            if resp.get('code') == 200:

                response = create_response(200)
                return response.get_response()
            else:
                response = create_response(resp.get('code'))
                return response.get_response()


class ModelPropertyValue(resource.Resource):
    app = 'mall2'
    resource = 'model_property_value'

    @login_required
    def api_put(request):
        """创建规格属性值

        Args:
          id: 规格id
          name: 规格值的名字
          pic_url: 规格值的图片地址
        """
        property_id = request.POST['id']
        pic_url = request.POST['pic_url']
        name = request.POST['name']
        params = {
            'id': property_id,
            'name': name,
            'pic_url': pic_url
        }
        resp = Resource.use(SERVICE_NAME, ZEUS_HOST).put({
            'resource': 'mall.model_property_value',
            'data': params
        })

        if resp:
            if resp.get('code') == 200:
                property_value = resp.get('data').get('product_model_value')
                response = create_response(200)
                response.data = property_value.get('id')
                return response.get_response()

    @login_required
    def api_post(request):
        """修改规格属性值

        Args:
          id: 属性值id
          name: 规格值的名字
          pic_url: 规格值的图片地址
        """
        property_value_id = request.POST['id']
        pic_url = request.POST['pic_url']
        name = request.POST['name']

        params = {
            'id': property_value_id,
            'name': name,
            'pic_url': pic_url
        }
        resp = Resource.use(SERVICE_NAME, ZEUS_HOST).post({
            'resource': 'mall.model_property_value',
            'data': params
        })

        if resp and resp.get('code') == 200:
            response = create_response(200)
            return response.get_response()

    @login_required
    def api_delete(request):
        """删除规格属性值

        Args:
          id: 规格值id

        Note: 删除规格值后，会处理由于规格值变化引起的商品状态的改变

        Raise:
          DoesNotExist: if id is not provided
        """
        property_value_id = request.POST.get('id')
        # TODO　其他变化接口暂时未提供
        mall_models.ProductModelPropertyValue.objects.filter(
            id=property_value_id
        ).update(is_deleted=True)

        mhpv = mall_models.ProductModelHasPropertyValue.objects.filter(
            property_value_id=property_value_id
        )
        model_ids = [relation.model_id for relation in mhpv]
        mall_models.ProductModel.objects.filter(
            id__in=model_ids
        ).update(is_deleted=True)

        product_ids = set(
            mall_models.ProductModel.objects.filter(
                id__in=model_ids
            ).values_list('product_id', flat=True)
        )
        shelve_type = mall_models.PRODUCT_SHELVE_TYPE_OFF
        mall_models.Product.objects.record_cache_args(
            ids=product_ids
        ).filter(
            id__in=product_ids
        ).update(shelve_type=shelve_type)
        # 发送商品下架信号
        signals.products_not_online.send(sender=mall_models.Product, product_ids=product_ids, request=request)

        # 处理商品无规格的情况，恢复基础规格并设置基础规格为0库存
        # 获取仍然有规格的商品id
        ok_product_ids = product_models = set(mall_models.ProductModel.objects.filter(
            product_id__in=product_ids, is_deleted=False
        ).values_list('product_id', flat=True))
        need_update_stock = product_ids - ok_product_ids
        mall_models.ProductModel.objects.filter(product_id__in=need_update_stock, is_standard=True).update(
            is_deleted=False, stock_type=mall_models.PRODUCT_STOCK_TYPE_LIMIT, stocks=0)

        response = create_response(200)
        return response.get_response()
