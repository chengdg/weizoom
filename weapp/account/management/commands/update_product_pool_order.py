#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
import time
import json

from django.core.management.base import BaseCommand, CommandError

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning
from mall.promotion import models as promotion_models
from mall.models import *
from weixin.user.models import ComponentAuthedAppid
from market_tools.tools.template_message import models as template_message_model
from market_tools.tools.template_message import module_api as template_message_api

class Command(BaseCommand):
    help = "update_product_pool_order"
    args = ''

    def handle(self, **options):
        
        # x = {"458": ["404", "404", "404"], "459": ["405", "405", "405"], "450": ["396", "396", "396"], "451": ["397", "397", "397"], "452": ["398", "398", "398"], "453": ["399", "399", "399"], "454": ["400", "400", "400"], "455": ["401", "401", "401"], "456": ["402", "402", "402"], "457": ["403", "403", "403"], "475": ["421", "421", "421"], "438": ["384", "384", "384"], "428": ["374", "374", "374"], "429": ["375", "375", "375"], "465": ["411", "411", "411"], "464": ["410", "410", "410"], "466": ["412", "412", "412"], "467": ["413", "413", "413"], "427": ["373", "373", "373"], "449": ["395", "395", "395"], "448": ["394", "394", "394"], "469": ["415", "415", "415"], "468": ["414", "414", "414"], "443": ["389", "389", "389"], "442": ["388", "388", "388"], "441": ["387", "387", "387"], "440": ["386", "386", "386"], "447": ["393", "393", "393"], "446": ["392", "392", "392"], "445": ["391", "391", "391"], "444": ["390", "390", "390"], "463": ["409", "409", "409"], "461": ["407", "407", "407"], "474": ["420", "420", "420"], "462": ["408", "408", "408"], "478": ["11", "11", "11"], "11": ["425", "425", "425"], "472": ["418", "418", "418"], "473": ["419", "419", "419"], "470": ["416", "416", "416"], "471": ["417", "417", "417"], "476": ["422", "422", "422"], "477": ["423", "423", "423"], "460": ["406", "406", "406"], "439": ["385", "385", "385"], "436": ["382", "382", "382"], "437": ["383", "383", "383"], "434": ["380", "380", "380"], "435": ["381", "381", "381"], "432": ["378", "378", "378"], "433": ["379", "379", "379"], "430": ["376", "376", "376"], "431": ["377", "377", "377"]}

        # for index,value in x.items():
        #     print index, "," , value
        #     new_product = Product.objects.get(id=index)
        #     supplier = Supplier.objects.get(id=new_product.supplier)
        #     order_has_products = OrderHasProduct.objects.filter(product_id__in=value)
            
        #     print "update order_has_product count", order_has_product.count()
        #     for order_has_product in order_has_products:
        #         order_has_product.product = index
        #         order_has_product.save()
        #         #如果是子订单
        #         if order_has_product.origin_order_id > 0:
        #             order = order_has_product.order
        #             new_order_id =  order.order_id.split("^")[0]+'^'+str(supplier.id)+ 's'
        #             order.supplier = supplier.id
        #             order.order_id = new_order_id
        #             order.save()
        #     MemberProductWishlist.objects.filter(product_id__in=value).update(product_id=index)

        #     #处理营销工具相关
        #     promotion_models.ProductHasPromotion.objects.filter(product_id__in=value).update(product_id=index)
        #     promotion_models.ForbiddenCouponProduct.objects.filter(product_id__in=value).update(product_id=index)
