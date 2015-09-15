# -*- coding: utf-8 -*-
__author__ = 'zhaolei'

from core import resource
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from core.jsonresponse import create_response
from mall.models import Supplier,Product
from mall.models import PRODUCT_SHELVE_TYPE_ON,PRODUCT_SHELVE_TYPE_OFF
from core import paginator
from mall import export
from datetime import datetime
from excel_response import ExcelResponse


FIRST_NAV = export.MALL_CONFIG_FIRST_NAV
class SupplierInfo(resource.Resource):
    app = "mall2" # 资源所属的app名称
    resource = "supplier_info" # 资源名称

    @login_required
    def get(request):
        id = request.GET.get('id', None)
        supplier = None
        if id:
            supplier = Supplier.objects.get(id=id)

        # 该dict中所需要传的值取决于base_nav.html
        c = RequestContext(request,{
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_config_second_navs(request),
            'second_nav_name': export.MAIL_CONFIG_SUPPLIER_NAV,
            'supplier': supplier,
        })
        return render_to_response('mall/editor/edit_supplier.html', c)

    @login_required
    def api_put(request):
        """
            创建供货商
        """
        name = request.POST.get('name')
        if len(name) > 16:
            response = create_response(500)
            response.data = {'msg':"供货商名称过长，请控制在8个字以内"}
            return response.get_response()
        supplier = Supplier.objects.create(
            owner=request.manager,
            name=name,
            responsible_person=request.POST.get('responsible_person'),
            supplier_tel=request.POST.get('supplier_tel'),
            supplier_address=request.POST.get('supplier_address'),
            remark=request.POST.get('remark')
        )
        response = create_response(200)
        return response.get_response()

    @login_required
    def api_post(request):
        """
            更新供货商
        """
        try:
            name = request.POST.get('name')
            if len(name) > 16:
                response = create_response(500)
                response.data = {'msg':"供货商名称过长，请控制在8个字以内"}
                return response.get_response()
            Supplier.objects.filter(id=request.POST.get('id')).update(
                name=request.POST.get('name'),
                responsible_person=request.POST.get('responsible_person'),
                supplier_tel=request.POST.get('supplier_tel'),
                supplier_address=request.POST.get('supplier_address'),
                remark=request.POST.get('remark')
            )
            response = create_response(200)
        except:
            response = create_response(500)

        return response.get_response()

    @login_required
    def api_delete(request):
        supplier_id = request.POST['id']

        # 若存在“在售”商品，删除供货商时提示：请先下架与该供货商有关的在售商品
        on_products = Product.objects.filter(supplier=supplier_id).filter(is_deleted=False)
        if on_products:
            # 若只存在“待售”商品，删除供货商时提示：删除该供货商后，与该供货商有关的商品将都被删除。
            response=create_response(200)
            response.data = {'msg':"请先删除与该供货商有关的商品"}
        else:
            Supplier.objects.filter(id=supplier_id).update(is_delete=True)
            response = create_response(200)

        return response.get_response()

class SupplierList(resource.Resource):

    app = "mall2" # 资源所属的app名称
    resource = "supplier_list" # 资源名称

    @login_required
    def get(request):
        has_supplier = (Supplier.objects.filter(owner_id = request.manager.id).count() > 0 )
        # 该dict中所需要传的值取决于base_nav.html
        c = RequestContext(request,{
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_config_second_navs(request),
            'second_nav_name': export.MAIL_CONFIG_SUPPLIER_NAV,
            'has_supplier': has_supplier
        })
        return render_to_response('mall/editor/supplier_list.html',c)

    @login_required
    def api_get(request):
        cur_page = int(request.GET.get('page', '1'))
        count_per_page = 10
        # 处理排序
        sort_attr = request.GET .get('sort_attr', None);
        name = request.GET.get('name', None);
        if not sort_attr:
            sort_attr = '-created_at'
        if not name:
            suppliers = list(Supplier.objects.filter(owner_id=request.manager.id).filter(is_delete=False).order_by('-id'))
        else:
            suppliers = list(Supplier.objects.filter(owner_id=request.manager.id).filter(name__contains=name).filter(is_delete=False).order_by('-id'))

        pageinfo, part_suppliers = paginator.paginate(suppliers, cur_page, count_per_page,
                                                         query_string=request.META['QUERY_STRING'])
        result_supplier = []
        for supplier in part_suppliers:
            result_supplier.append({
                "id": supplier.id,
                "name": supplier.name,
                "responsible_person": supplier.responsible_person,
                "supplier_tel": supplier.supplier_tel,
                "supplier_address": supplier.supplier_address,
                "create_at": datetime.strftime(supplier.created_at, '%Y-%m-%d %H:%M'),
                "remark": supplier.remark
            })


        response = create_response(200)
        response.data = {
            'items': result_supplier,
            'pageinfo': paginator.to_dict(pageinfo),
            'sortAttr': sort_attr
        }
        return response.get_response()

class SupplierExport(resource.Resource):
    app = "mall2"
    resource = "supplier_export"

    @login_required
    def get(request):
        # 处理排序

        name = request.GET.get('name', None)
        if not name:
            suppliers = Supplier.objects.filter(owner_id=request.manager.id).filter(is_delete=False).order_by('-id')
        else:
            suppliers = Supplier.objects.filter(owner_id=request.manager.id).filter(name__contains=name).filter(is_delete=False).order_by('-id')
        # 得到所有该用户的所有满足条件的供货商
        cloumn_name = [u'供货商名称',u'客户负责人',u'供货商电话',u'供货商地址',u'备注']
        supplier_data = [
             cloumn_name
        ]
        for su in suppliers:
            supplier_data.append([su.name,su.responsible_person,
                                   su.supplier_tel,su.supplier_address,su.remark])
        return ExcelResponse(supplier_data, output_name=u'供货商列表'.encode('utf8'), force_csv=False)