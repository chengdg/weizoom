# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

from core import resource
from core.jsonresponse import create_response
from mall import models as mall_models
from mall import export, signals


class ModelPropertyList(resource.Resource):
    app = 'mall2'
    resource = 'model_property_list'

    @login_required
    def get(request):
        """
        商品规格列表页面.
        """
        model_properties = mall_models.ProductModelProperty.objects.filter(
            owner=request.manager,
            is_deleted=False)
        id2property = {}
        for model_property in model_properties:
            model_property.property_values = []
            t_name = model_property.name
            model_property.shot_name = t_name[:6]+'...' if len(t_name) > 6 else t_name
            id2property[model_property.id] = model_property

        property_ids = [property.id for property in model_properties]
        mpv = mall_models.ProductModelPropertyValue.objects.filter(
            property_id__in=property_ids)
        for property_value in mpv:
            if property_value.is_deleted:
                continue
            property_id = property_value.property_id
            property = id2property[property_id]
            property_value.is_image_property_value = (
                property.is_image_property and property_value.pic_url)
            t_name = property_value.name
            property_value.shot_name = t_name[:10]+'...' if len(t_name) > 10 else t_name
            property.property_values.append(property_value)

        c = RequestContext(request, {
            'first_nav_name': export.PRODUCT_FIRST_NAV,
            'second_navs': export.get_second_navs(request),
            'second_nav_name': export.PRODUCT_MANAGE_MODEL_NAV,
            'model_properties': model_properties
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
        _property = mall_models.ProductModelProperty.objects.create(
            owner=request.manager,
            name=''
        )

        response = create_response(200)
        response.data = _property.id
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
        id = request.POST['id']
        field = request.POST['field']
        if 'name' == field:
            name = request.POST['name']
            mall_models.ProductModelProperty.objects.filter(
                id=id
            ).update(name=name)
        elif 'type' == field:
            _type = request.POST.get('type')
            if _type and _type == 'text':
                _type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT
            else:
                _type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE

            mall_models.ProductModelProperty.objects.filter(
                id=id
            ).update(type=_type)
        response = create_response(200)
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
        model_property = mall_models.ProductModelProperty.objects.get(
            id=property_id)
        signals.pre_delete_product_model_property.send(
            sender=mall_models.ProductModelProperty,
            model_property=model_property,
            request=request)

        mall_models.ProductModelPropertyValue.objects.filter(
            property_id=property_id
        ).update(is_deleted=True)
        mall_models.ProductModelProperty.objects.filter(
            id=property_id
        ).update(is_deleted=True)

        response = create_response(200)
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
        property_value = mall_models.ProductModelPropertyValue.objects.create(
            property_id=property_id,
            name=name,
            pic_url=pic_url
        )

        response = create_response(200)
        response.data = property_value.id
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

        try:
            mall_models.ProductModelPropertyValue.objects.filter(id=property_value_id).update(
                name=name,
                pic_url=pic_url
            )
            response = create_response(200)
        except:
            response = create_response(500)

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
        ).update(shelve_type=shelve_type, weshop_status=shelve_type)
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
