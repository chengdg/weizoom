# -*- coding: utf-8 -*-
import json
from django.template import RequestContext
from django.shortcuts import render_to_response

from core import resource
from core.jsonresponse import create_response
from mall import export
from mall import models as mall_models


class Property(resource.Resource):
    app = 'mall2'
    resource = "property"

    def api_put(request):
        """创建属性模板

        Args:
          title: 属性模板标题
          newProperties 属性模板中需要新建的property信息的json字符串

        Example:
          {
            'title': 'aaa',
            'newProperties':[
                {
                    id: -1, //id=-1, 代表需要新建的属性
                    name: "属性1",
                    value: "属性1的描述"
                },
                ...
            ]
          }
        """
        title = request.POST['title']
        new_properties = json.loads(request.POST.get('newProperties', "[]"))

        template = mall_models.ProductPropertyTemplate.objects.create(
            owner=request.manager,
            name=title
        )

        # 创建新的property
        for property in new_properties:
            if property['id'] < 0:
                # 需要新建property
                mall_models.TemplateProperty.objects.create(
                    owner=request.manager,
                    template=template,
                    name=property['name'],
                    value=property['value']
                )

        response = create_response(200)
        return response.get_response()

    def api_post(request):
        """更新属性模板

        Args:
          id: 属性模板id
          title: 属性模板标题
          newProperties: 属性模板中需要新建的property信息的json字符串
          updateProperties: 属性模板中需要更新的property信息的json字符串
          deletedIds: 属性模板中需要删除的property的id数据的json字符串

        """
        template_id = request.POST['id']
        title = request.POST['title']
        new_properties = json.loads(request.POST.get('newProperties', "[]"))
        update_properteis = json.loads(request.POST.get('updateProperties', "[]"))
        deleted_property_ids = json.loads(request.POST.get('deletedIds', "[]"))

        mall_models.ProductPropertyTemplate.objects.filter(
            id=template_id
        ).update(name=title)

        # 创建新的property
        for property in new_properties:
            if property['id'] < 0:
                # 需要新建property
                mall_models.TemplateProperty.objects.create(
                    owner=request.manager,
                    template_id=template_id,
                    name=property['name'],
                    value=property['value']
                )

        # 更新已有的property
        for property in update_properteis:
                mall_models.TemplateProperty.objects.filter(
                    id=property['id']
                ).update(
                    name=property['name'],
                    value=property['value']
                )
        #删除property
        mall_models.TemplateProperty.objects.filter(
            id__in=deleted_property_ids
        ).delete()

        response = create_response(200)
        return response.get_response()

    def api_delete(request):
        """删除属性模板

        Args:
          id: 属性模板id

        Raise:
          DoesNotExist: if id is not provided
        """
        template_id = request.POST.get('id')

        mall_models.ProductPropertyTemplate.objects.filter(
            owner=request.manager,
            id=template_id
        ).delete()

        response = create_response(200)
        return response.get_response()


class PropertyList(resource.Resource):
    app = 'mall2'
    resource = "property_list"

    def get(request):
        """商品属性模板列表页面.

        """
        templates = mall_models.ProductPropertyTemplate.objects.filter(
            owner=request.manager)
        for template in templates:
            template.properties = []
        id2templates = dict(
            [(template.id, template) for template in templates]
        )

        template_ids = [template.id for template in templates]
        properties = mall_models.TemplateProperty.objects.filter(
            template_id__in=template_ids
        )
        for property in properties:
            template = id2templates.get(property.template_id, None)
            if template:
                template.properties.append(property)

        c = RequestContext(request, {
            'first_nav_name': export.PRODUCT_FIRST_NAV,
            'second_navs': export.get_second_navs(request),
            'second_nav_name': export.PRODUCT_MANAGE_MODEL_NAV,
            'templates': templates
        })
        return render_to_response('mall/editor/property_templates.html', c)

    def api_get(request):
        """ 获得属性模板中的属性集合

        Args:
          id: 属性模板id

        Return json:
          Example:
            [{
                id: 1,
                name: "属性1",
                value: "属性1的描述"
            }, {
                ......
            }]

        """
        template_id = int(request.GET['id'])
        if template_id == -1:
            properties = []
        else:
            properties = mall_models.TemplateProperty.objects.filter(
                template_id=template_id)

        result_properties = []
        for property in properties:
            result_properties.append({
                "id": property.id,
                "name": property.name,
                "value": property.value
            })

        response = create_response(200)
        response.data = result_properties
        return response.get_response()
