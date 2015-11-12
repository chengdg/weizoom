# -*- coding: utf-8 -*-
from mall import module_api as mall_api
from mall import models as mall_models
from utils import cache_util

def test():
    webapp_owner_id = 3
    webapp_id = 3181
    c_id = 0
    c,products = mall_api.get_products_in_webapp(webapp_id, 0, webapp_owner_id, c_id)
    categories = mall_models.ProductCategory.objects.filter(owner_id=3)

    key_infos = []
    # for pid in [p.id for p in products]:
    #     key_infos.append({
    #         'key': 'webapp_product_detail_{wo:%s}_{pid:%s}' % (webapp_owner_id, pid),
    #         'on_miss': mall_api.get_product_detail_for_cache(webapp_owner_id, pid)
    #     })

    zset_all_products_key_name = 'webapp_products_{wo:%s}' % webapp_owner_id
    zset_all_products_key_name_m = 'webapp_products_{wo:%s}_m' % webapp_owner_id
    count = 0
    for product in products:

        if count <=4 :
            print "zl---------",product.id,count
            cache_util.add_zdata_to_redis(zset_all_products_key_name,product.id,0)
            count+=1
            # 单个写

    #批量写
    data_list = []
    for product in products:
        data_list.append(product.id)
        data_list.append(0)
    print data_list

    cache_util.add_zdata_to_redis(zset_all_products_key_name_m,*data_list)
    for categorie in categories:
        zset_category_products_key_name = 'webapp_products_{wo:%s}_{co:%s}' % (webapp_owner_id,categorie.id)
        category_has_product = mall_models.CategoryHasProduct.objects.filter(
                    category_id=categorie.id)
        cache_util.add_zdata_to_redis(zset_category_products_key_name,0,product.id)

    result = cache_util.get_zset_from_redis(zset_all_products_key_name)
    # 获取，类型为list
    print result,type(result)
    result_m = cache_util.get_zset_from_redis(zset_all_products_key_name_m)
    # 获取，类型为list
    print result_m,type(result_m)

    #单个和多个删除
    # 其中返回值代表成功删除的个数
    r  =cache_util.rem_zset_member_from_redis(zset_all_products_key_name_m,1)
    print "zl------------r",r
    result_m = cache_util.get_zset_from_redis(zset_all_products_key_name_m)
    # 获取，类型为list
    print result_m,type(result_m)
    r_m  =cache_util.rem_zset_member_from_redis(zset_all_products_key_name_m,1,2,3,4)
    print "zl------------r_m",r_m
    result_m = cache_util.get_zset_from_redis(zset_all_products_key_name_m)
    # 获取，类型为list
    print result_m,type(result_m)

    #添加已存在元素，但是改变 score 值,也就相当于更改某个元素的score的值
    result = cache_util.get_zrange_from_redis(zset_all_products_key_name_m,0,3)
    print "normal-----------",result
    #倒叙
    result = cache_util.get_zrange_from_redis(zset_all_products_key_name_m,0,3,desc=True)
    print "normal-----------desc=true",result
    #倒叙并且返回score
    result = cache_util.get_zrange_from_redis(zset_all_products_key_name_m,0,3,desc=True,withscores=True)
    print "normal-----------desc=true,with=true",result



