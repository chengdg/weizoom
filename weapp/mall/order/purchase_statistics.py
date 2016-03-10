# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from core import resource
from mall.models import *
from core.jsonresponse import create_response, JsonResponse
import mall.module_api as mall_api
from datetime import datetime,timedelta
from tools.regional.models import Province
from utils.dateutil import get_date_after_days, date2string


class PurchaseStatistics(resource.Resource):
    app = "mall2"
    resource = "purchase_statistics"

    def api_get(request):
        #将省份处理成dict
        id2province ={}
        provinces = Province.objects.all()
        for province in provinces:
            id2province[province.id] = province.name
        #将省份处理成dict

        result=[]

        days = int(request.GET.get("days", "30"))
        today = datetime.now()
        pre_date = date2string(get_date_after_days(today, -days))
        webapp_id = request.GET.get('webapp_id', None)

        orders = Order.objects.filter(webapp_id=webapp_id, payment_time__gte=pre_date, status__in=[3,4,5]).order_by('-payment_time')
        webapp_user_ids = set([order.webapp_user_id for order in orders])
        from modules.member.models import Member
        webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

        for order in orders:
            # 获取order对应的member的显示名
            member = webappuser2member.get(order.webapp_user_id, None)
            if member:
                order.buyer_name = member.username_for_html
                order.member_id = member.id
            else:
                order.buyer_name = u'未知'
                order.member_id = 0
            order.province_id =order.area.split('_')[0]
            #根据订单获取商品
            products = mall_api.get_order_products(order)
            order.province_id =order.area.split('_')[0]
            if len(order.province_id) > 0:
                order.province_name = id2province[int(order.province_id)]

                infor_dict = {}
                infor_dict["province_name"] = order.province_name
                infor_dict["username"] = order.buyer_name
                infor_dict["products"] = []
                for product in products:
                    if product["promotion"] and product["promotion"].has_key("type") and product["promotion"]["type"] == "premium_sale:premium_product":
                        infor_dict["products"].append({"promotion_name":product["name"],"count":product["count"]})
                    else:
                        infor_dict["products"].append({"name":product["name"],"count":product["count"]})
                result.append(infor_dict)

        response = create_response(200)
        response.data = {'items': result}
        #return response.get_response()
        return response.get_jsonp_response(request)


class PurchaseStatistics(resource.Resource):
    app = "mall2"
    resource = "test"

    def api_get(request):
        import random
        pids = request.GET.get('pids')
        pids = pids.split("_")
        #pids =json.loads(pids)
        pid2is_in_group_buy = []
        if len(pids)>1:
            for pid in pids:
                pid2is_in_group_buy.append({
                      'pid': int(pid),
                      #'is_in_group_buy': random.choice([True,False]),
                      'is_in_group_buy': False,
                      })
        else:
            for pid in pids:
                pid2is_in_group_buy.append({
                      'pid': int(pid),
                      'is_in_group_buy': False,
                      })
        response = create_response(200)
        response.data = {
            'pid2is_in_group_buy': pid2is_in_group_buy
        }
        return response.get_response()

