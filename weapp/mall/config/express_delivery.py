# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from mall.models import ExpressDelivery
from mall import export
from core import resource
from core import paginator
from core.jsonresponse import create_response
from tools.express import util as tools_express_util

COUNT_PER_PAGE = 20
FIRST_NAV = export.MALL_CONFIG_FIRST_NAV


class ExpressDeliveryInfo(resource.Resource):
    app = "mall2"
    resource = "express_delivery"

    @login_required
    def api_post(request):
        try:
            ExpressDelivery.objects.filter(id=request.POST.get('id')).update(
                name=request.POST.get('name'),
                express_number=request.POST.get('express_number'),
                express_value=request.POST.get('express_value'),
                remark=request.POST.get('remark')
            )
            response = create_response(200)
        except:
            response = create_response(500)

        return response.get_response()

    @login_required
    def api_put(request):
        express_deliverys = ExpressDelivery.objects.filter(owner_id=request.manager.id).order_by('-display_index')
        if express_deliverys.count() > 0:
            display_index = express_deliverys[0].display_index + 1
        else:
            display_index = 1

        express_delivery = ExpressDelivery.objects.create(
            owner=request.manager,
            name=request.POST.get('name'),
            express_number=request.POST.get('express_number'),
            express_value=request.POST.get('express_value'),
            remark=request.POST.get('remark'),
            display_index=display_index
        )
        response = create_response(200)
        return response.get_response()

    @login_required
    def api_delete(request):
        express_delivery_id = request.POST['id']
        ExpressDelivery.objects.filter(id=express_delivery_id).delete()

        response = create_response(200)
        return response.get_response()


########################################################################
# get_express_delivery: 获得快递公司列表
########################################################################

class ExpressDeliveryList(resource.Resource):
    app = "mall2"
    resource = "express_delivery_list"

    @login_required
    def get(request):
        """
        配置管理-物理名称管理页面
        """

        has_express_delivery = (ExpressDelivery.objects.filter(owner_id=request.manager.id).count() > 0)
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_config_second_navs(request),
            'second_nav_name': export.MALL_CONFIG_EXPRESS_COMOANY_NAV,
            'has_express_delivery': has_express_delivery
        })
        return render_to_response('mall/editor/express_deliverys.html', c)

    @login_required
    def api_get(request):
        cur_page = int(request.GET.get('page', '1'))
        count_per_page = 50
        # 处理排序
        sort_attr = request.GET.get('sort_attr', None);
        if not sort_attr:
            sort_attr = '-display_index'

        express_deliverys = list(ExpressDelivery.objects.filter(owner_id=request.manager.id).order_by('-display_index'))

        pageinfo, express_deliverys = paginator.paginate(express_deliverys, cur_page, count_per_page,
                                                         query_string=request.META['QUERY_STRING'])
        result_express_deliverys = []
        for express_delivery in express_deliverys:
            result_express_deliverys.append({
                "id": express_delivery.id,
                "name": express_delivery.name,
                "express_number": express_delivery.express_number,
                "express_value": express_delivery.express_value,
                "display_index": express_delivery.display_index,
                "remark": express_delivery.remark
            })

        response = create_response(200)
        response.data = {
            'items': result_express_deliverys,
            'pageinfo': paginator.to_dict(pageinfo),
            'sortAttr': sort_attr
        }
        return response.get_response()


class ExpressDeliverysCompany(resource.Resource):
    """
    获得下拉列表中的快递公司信息
    """
    app = "mall2"
    resource = "express_delivery_company"

    @login_required
    def api_get(request):
        source = request.GET['source']
        # 配置管理-五六名称管理
        if source == 'init_express_deliverys':
            data = tools_express_util.get_express_company_json()
            express_deliverys = ExpressDelivery.objects.filter(owner_id=request.manager.id)

            # 过滤已有的快递公司
            result_express_deliverys = []
            if express_deliverys.count() == 0:
                result_express_deliverys = data
            else:
                express_values = [e.express_value for e in express_deliverys]
                for item in data:
                    if item['value'] in express_values:
                        continue
                    result_express_deliverys.append(item)

            response = create_response(200)
            response.data = result_express_deliverys
            return response.get_response()
        # 订单管理发货时获得物流公司信息
        else:
            express_deliverys = list(
                ExpressDelivery.objects.filter(owner_id=request.manager.id).order_by('-display_index'))
            if len(express_deliverys) > 0:
                # 获取 物流名称管理  中的物流信息
                result_express_deliverys = []
                for express_delivery in express_deliverys:
                    result_express_deliverys.append({
                        "name": express_delivery.name,
                        "id": express_delivery.express_number,
                        "value": express_delivery.express_value,
                    })
            else:
                # 获取 全部的物流信息
                result_express_deliverys = tools_express_util.get_express_company_json()

            response = create_response(200)
            response.data = result_express_deliverys
            return response.get_response()


class ExpressDeliveryDisplayIndex(resource.Resource):
    """
    排序
    """
    app = "mall2"
    resource = "express_delivery_display_index"

    @login_required
    def api_post(request):
        src_id = request.REQUEST.get('src_id', None)
        dst_id = request.REQUEST.get('dst_id', None)

        if not src_id or not dst_id:
            response = create_response(500)
            response.errMsg = u'invalid arguments: src_id(%s), dst_id(%s)' % (src_id, dst_id)
            return response.get_response()

        src_id = int(src_id)
        dst_id = int(dst_id)
        if dst_id == 0:
            # dst_id = 0, 将src_product的display_index设置得比第一个product的display_index大即可
            first_delivery = ExpressDelivery.objects.filter(owner=request.manager).order_by('-display_index')[0]
            if first_delivery.id != src_id:
                ExpressDelivery.objects.filter(id=src_id).update(display_index=first_delivery.display_index + 1)
        else:
            # dst_id不为0，交换src_product, dst_product的display_index
            id2delivery = dict([(p.id, p) for p in ExpressDelivery.objects.filter(id__in=[src_id, dst_id])])
            ExpressDelivery.objects.filter(id=src_id).update(display_index=id2delivery[dst_id].display_index)
            ExpressDelivery.objects.filter(id=dst_id).update(display_index=id2delivery[src_id].display_index)

        response = create_response(200)
        return response.get_response()