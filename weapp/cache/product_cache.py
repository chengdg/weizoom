# -*- coding: utf-8 -*-
from __future__ import absolute_import

from utils import cache_util
from product.models import *

__author__ = 'victor'


def _get_user_product_from_db(key, **kwargs):
    """
    用于缓存用户产品的函数
    """

    def inner_func():
        # print "in get_user_product_from_db.inner_func()"
        try:
            user_has_product = UserHasProduct.objects.get(**kwargs)
            ret = {
                'keys': [key],
                'value': user_has_product.product.to_dict()
            }
            return ret
        except:
            return None
    return inner_func


def get_user_product(user):
    """
    获取用户对应的产品

    @param user User对象

    """
    key = 'webapp_user_product_{wo:%s}' % user.id
    # print "user in get_user_product(): %s %s" % (user.id, user)
    # 如果没有缓存的数据，则调用_get_user_product_from_db()的函数获取数据库中的数据
    data = cache_util.get_from_cache(key, _get_user_product_from_db(key, owner=user))
    #print("data: {}".format(data))
    return UserHasProduct.from_dict(data)
