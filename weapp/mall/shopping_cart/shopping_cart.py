# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning
from core.exceptionutil import unicode_full_stack

from mall.models import ShoppingCart

class ShoppingCartCount(resource.Resource):
    """
    用户购物车的数量
    """
    app = "mall2"
    resource = "shopping_cart_count"

    @login_required
    def api_get(request):
        webapp_user_id = request.GET.get('webapp_user_id', None)
        if webapp_user_id:
            try:
                shopping_cart = ShoppingCart.objects.filter(webapp_user_id=webapp_user_id)
                if shopping_cart.count() > 0:
                    shopping_cart_count = shopping_cart.first().count
                else:
                    shopping_cart_count = 0
            except:
                notify_message = u"购物车数量函数出错，cause:\n{}".format(unicode_full_stack())
                watchdog_error(notify_message)
                return create_response(500).get_response()

            response = create_response(200)
            response.data = {'count': shopping_cart_count}
            return response.get_response()
        else:
            notify_message = u"参数webapp_user_id确实或者错误！"
            watchdog_error(notify_message)
            return create_response(500).get_response()