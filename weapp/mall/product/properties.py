# -*- coding: utf-8 -*-
import json
from django.template import RequestContext
from django.shortcuts import render_to_response
from eaglet.utils.resource_client import Resource

from core import resource
from core.jsonresponse import create_response
from mall import export
from weapp.settings import ZEUS_HOST
from weapp.settings import ZEUS_SERVICE_NAME as SERVICE_NAME


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
        params = {
            'owner_id': request.manager.id,
            'title': title
        }
        # 创建模板
        resp = Resource.use(SERVICE_NAME, ZEUS_HOST).put({
            'resource': 'mall.product_property_template',
            'data': params
        })
        if resp and resp['code'] == 200:

            template = resp['data']
            properties_params = {
                'template_id': template['id'],
                'owner_id': request.manager.id,
                'properties': json.dumps(new_properties)
            }
            # 创建模板的属性
            property_resp = Resource.use(SERVICE_NAME, gateway_host=ZEUS_HOST).put({
                'resource': 'mall.template_property',
                'data': properties_params
            })
            if property_resp and property_resp['code'] == 200:

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

        # 更新template
        template_params = {
            "id": template_id,
            'title': title
        }
        template_update = Resource.use(SERVICE_NAME, ZEUS_HOST).post({
            'resource': 'mall.product_property_template',
            'data': template_params
        })
        if template_update and template_update['code'] == 200:

            # 创建新的property
            if new_properties:
                create_new_properties_params = {
                    "owner_id": request.manager.id,
                    'properties': json.dumps(new_properties),
                    'template_id': template_id,
                }
                Resource.use(SERVICE_NAME, ZEUS_HOST).put({
                    'resource': 'mall.template_property',
                    'data': create_new_properties_params
                })
            if update_properteis:
                # 更新已有的property
                update_properties_params = {
                    'properties': json.dumps(update_properteis),
                }
                Resource.use(SERVICE_NAME, ZEUS_HOST).post({
                    'resource': 'mall.template_property',
                    'data': update_properties_params
                })

            # 删除property
            if deleted_property_ids:
                delete_properties_params = {
                    'ids': json.dumps(deleted_property_ids),
                }
                Resource.use(SERVICE_NAME, ZEUS_HOST).delete({
                    'resource': 'mall.template_property',
                    'data': delete_properties_params
                })
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
        params = {
            'id': template_id,
        }
        resp = Resource.use(SERVICE_NAME, ZEUS_HOST).delete({
            'resource': 'mall.product_property_template',
            'data': params
        })

        if resp:
            if resp['code'] == 200:
                response = create_response(200)
                return response.get_response()
            else:
                response = create_response(resp['code'])
                return response.get_response()


class PropertyList(resource.Resource):
    app = 'mall2'
    resource = "property_list"

    def get(request):
        """商品属性模板列表页面.

        """

        user_id = request.manager.id
        params = {
            'owner_id': user_id
        }
        resp = Resource.use(SERVICE_NAME, gateway_host=ZEUS_HOST).get(
            {
                'resource': 'mall.template_list',
                'data': params
            }
        )
        templates = None
        if resp:
            code = resp['code']
            if code == 200:
                templates = resp['data']['templates']

        c = RequestContext(request, {
            'first_nav_name': export.PRODUCT_FIRST_NAV,
            'second_navs': export.get_mall_product_second_navs(request),
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
            params = {
                'template_id': template_id
            }
            resp = Resource.use(SERVICE_NAME, ZEUS_HOST).get(
                {
                    'resource': 'mall.template_property',
                    'data': params
                }
            )
            if resp and resp['code'] == 200:
                    properties = resp['data']['properties']
            else:
                properties = []
        response = create_response(200)
        response.data = properties
        return response.get_response()
