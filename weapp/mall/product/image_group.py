# -*- coding: utf-8 -*-
import json
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


from mall import models as mall_models
from core import resource
from mall import export
from core.jsonresponse import create_response


class ImageGroupList(resource.Resource):
    app = 'mall2'
    resource = 'image_group_list'

    @login_required
    def get(request):
        """图片分组列表页面

        Note 每个图片分组最多显示8张图片
        """
        # 获取image group
        image_groups = mall_models.ImageGroup.objects.filter(
            owner=request.manager
        )
        group_ids = []
        id2group = {}
        for image_group in image_groups:
            image_group.images = []
            group_ids.append(image_group.id)
            id2group[image_group.id] = image_group

        # 向group中填充image
        target_image_groups = mall_models.Image.objects.filter(
            group_id__in=group_ids
        )
        for image in target_image_groups:
            id2group[image.group_id].images.append(image)
        for image_group in image_groups:
            if len(image_group.images) > 8:
                image_group.images = image_group.images[:8]

        c = RequestContext(request, {
            'first_nav_name': export.PRODUCT_FIRST_NAV,
            'second_navs': export.get_mall_product_second_navs(request),
            'second_nav_name': export.PRODUCT_MANAGE_IMAGE_NAV,
            'image_groups': image_groups
        })
        return render_to_response('mall/editor/image_groups.html', c)

    @login_required
    def api_get(request):
        """获取图片分组信息
        Return json:
          data
            [{
                "id": 1,
                "name": "图片分组1"
            }, {
                "id": 2,
                "name": "图片分组2"
            }, {
                ......
            }]
        """
        image_groups = []
        target_image_groups = mall_models.ImageGroup.objects.filter(
            owner=request.manager
        )
        for image_group in target_image_groups:
            image_groups.append({
                "id": image_group.id,
                "name": image_group.name
            })

        response = create_response(200)
        response.data = image_groups
        return response.get_response()


class ImageGroup(resource.Resource):
    app = 'mall2'
    resource = 'image_group'

    @login_required
    def api_get(request):
        """获取图片分组中的图片集合

          Args:
            id: 图片分组id

          Return json:
            data(list):
              [{
                "id": 1,
                "src": "http://upyun.com/a/1.jpg",
                "width": "100",
                "height": "100,
              }, {
                "id": 2,
                "src": "http://upyun.com/a/2.jpg",
                "width": "100",
                "height": "100,
              }, {
                ......
              }]

        """
        group_id = request.GET['id']
        images = []
        for image in mall_models.Image.objects.filter(group_id=group_id):
            images.append({
                "id": image.id,
                "src": image.url,
                "width": image.width,
                "height": image.height
            })

        response = create_response(200)
        response.data = images
        return response.get_response()

    @login_required
    def api_put(request):
        """创建图片分组.

        Args:
          name: 图片分组名.
          images: 分组中的图片集合. id为-1，表示该图片需要新建.
        """
        name = request.POST['name']
        images = json.loads(request.POST.get('images', '[]'))

        image_group = mall_models.ImageGroup.objects.create(
            owner=request.manager,
            name=name
        )

        for image in images:
            mall_models.Image.objects.create(
                owner=request.manager,
                group=image_group,
                url=image['path'],
                width=image['width'],
                height=image['height']
            )

        response = create_response(200)
        return response.get_response()

    @login_required
    def api_post(request):
        """更新图片分组.
        Args:
          id: imagegroup id, 不存在则创建.
          name: 图片分组名.
          images: 分组中的图片集合

        """
        id = request.POST['id']
        name = request.POST['name']
        images = json.loads(request.POST.get('images', '[]'))

        image_group = mall_models.ImageGroup.objects.get(owner=request.manager, id=id)
        if image_group.name != name:
            mall_models.ImageGroup.objects.filter(id=id).update(name=name)

        # 更新image
        image_ids = set([image['id'] for image in images])
        existed_image_ids = set([
            image.id for image in mall_models.Image.objects.filter(group_id=id)
        ])
        for image in images:
            if int(image['id']) < 0:
                mall_models.Image.objects.create(
                    owner=request.manager,
                    group=image_group,
                    url=image['path'],
                    width=image['width'],
                    height=image['height']
                )
        ids_to_be_delete = existed_image_ids - image_ids
        mall_models.Image.objects.filter(id__in=ids_to_be_delete).delete()

        response = create_response(200)
        return response.get_response()

    @login_required
    def api_delete(request):
        """删除图片分组
        Args:
          id: ImageGroup id
        """
        id = request.POST['id']
        mall_models.ImageGroup.objects.filter(id=id).delete()

        response = create_response(200)
        return response.get_response()

