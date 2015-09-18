#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.jsonresponse import create_response
from mall.models import Order, ORDER_STATUS_PAYED_NOT_SHIP
from market_tools.tools.channel_qrcode.models import *
import mall.module_api as mall_api
from watchdog.utils import watchdog_warning
from core.exceptionutil import unicode_full_stack
from core import resource
from django.contrib.auth.decorators import login_required

class BulkShipment(resource.Resource):
    """
    批量发货
    """
    app = "mall2"
    resource = "bulk_shipment"

    @login_required
    def api_post(request):
        response = create_response(200)
        file_url = request.POST.get('file_url', '')
        # 读取文件
        json_data, error_rows = _read_file(file_url[1:])

        # 批量处理订单
        success_data, error_items = mall_api.batch_handle_order(json_data, request.manager)
        # print '------------------'
        # print json_data
        # print u'成功处理订单'
        # print success_data
        # print u'失败处理订单'
        # print 'error_rows'
        # print error_rows
        # print 'error_items'
        # print error_items

        # __clean_file(file_url[1:])
        response.data = {
            'success_count': len(success_data),
            'error_count': len(error_rows) + len(error_items),
            'error_items': error_items
        }
        return response.get_response()


def _read_file(file_url):
    data = []
    error_rows = []

    import csv

    file_path = os.path.join(settings.PROJECT_HOME, '..', file_url)

    with open(file_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=':', quotechar='|')
        for row in reader:
            try:
                if len(row) > 0:
                    item = dict()
                    row = row[0].split(',')
                    if not (len(row[0]) or len(row[1]) or len(row[2])):
                        continue
                    item['order_id'] = row[0]
                    item['express_company_name'] = row[1].decode('gbk')
                    item['express_number'] = row[2]
                    data.append(item)
            except:
                error_rows.append(', '.join(row))
            # print(', '.join(row))

        csvfile.close()

    if len(error_rows) > 0:
        alert_message = u"bulk_shipments批量发货 读取文件错误的行, error_rows:{}".format(error_rows)
        watchdog_warning(alert_message)

    return data, error_rows


def __clean_file(file_url):
    import os

    try:
        file_path = os.path.join(settings.PROJECT_HOME, '..', file_url)
        os.remove(file_path)
    except:
        alert_message = u"__clean_file cause:\n{}".format(unicode_full_stack())
        watchdog_warning(alert_message)


class Delivery(resource.Resource):
    """
    单个订单发货
    """
    app = "mall2"
    resource = "delivery"

    @login_required
    def api_post(request):
        order_id = request.POST.get('order_id', None)
        express_company_name = request.POST.get('express_company_name')
        express_number = request.POST.get('express_number')
        leader_name = request.POST.get('leader_name')
        is_update_express = request.POST.get('is_update_express')
        is_update_express = True if is_update_express == 'true' else False

        try:
            order = Order.objects.get(id=order_id)
            if not is_update_express and order.status != ORDER_STATUS_PAYED_NOT_SHIP:
                response = create_response(500)
                response.errMsg = u'该订单已取消'
                return response.get_response()
        except:
            pass
        is_success = mall_api.ship_order(order_id, express_company_name, express_number, request.manager.username,
                                         leader_name=leader_name, is_update_express=is_update_express)
        if is_success:
            response = create_response(200)
        else:
            response = create_response(500)
        return response.get_response()

