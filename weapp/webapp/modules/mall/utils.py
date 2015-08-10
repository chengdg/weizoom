# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
from datetime import datetime

from mall import module_api as mall_api
from mall import models as mall_models
from mall.promotion import models as promotion_models


def get_user_member_grade_id(request):
    """得到用户会员等级

    Return:
      int - 如果用户是会员， 将返回对应的会员级别ID，
      None - 如果用户不是会员
    """
    member_grade_id = None
    if hasattr(request, 'member') and request.member:
        member_grade_id = request.member.grade_id
    return member_grade_id


def get_vip_discount(request):
    """得到会员折扣(0.000~1.000), 1.000 表示伟打折.

    Return:
      discount(float): 如果请求用户是会员返回对应折扣， 否则返回1.00

    """
    grade_id = get_user_member_grade_id(request)
    if not grade_id:
        return 1.00
    member_grade = filter(lambda x: x.id == grade_id,
                          request.webapp_owner_info.member_grades)
    return (member_grade[0].shop_discount / 100.00)


def get_product_member_discount(discount, product):
    """判断商品是否参加会员折扣，返回对应折扣(0.000~1.000), 1.000 表示伟打折.


    Return:
      fload: 如果商品参加会员折扣， 返回对应的折扣 否则返回1.000
    """
    # 商品是否参加会员折扣
    if product.is_member_product:
        return discount
    return 1.000


def get_product_member_price(request, product):
    """如果商品参加会员折扣， 得到商品的会员价格， 否这得到商品原价.

    Return:
      fload - 商品价格
    """
    member_discount = get_vip_discount(request)
    product_member_discount = get_product_member_discount(member_discount, product)
    return product.display_price * product_member_discount


def get_processed_products(request, products):
    """按需求处理商品

    Return:
      products

    """
    # 得到商品的会员价
    # discount = get_vip_discount(request)
    # member_grade_id = get_user_member_grade_id(request)
    # new_products = []
    # for p in products:
    #     new_products.append(get_display_price(discount, member_grade_id, p))
    return products


def get_processed_product(request, product):
    """按需求处理商品

    Return:
      product
    """
    # 得到商品的会员价
    discount = get_vip_discount(request)
    product.price_info['vip_price'] = product.price_info['display_price'] * discount
    return product


def has_promotion(user_member_grade_id=None, promotion_member_grade_id=0):
    """判断促销是否对用户开放.

    Args:
      user_member_grade_id(int): 用户会员等价
      promotion_member_grade_id(int): 促销制定的会员等级

    Return:
      True - if 促销对用户开放
      False - if 促销不对用户开放
    """
    if promotion_member_grade_id == 0:
        return True
    elif promotion_member_grade_id == user_member_grade_id:
        return True
    else:
        return False


def get_display_price(discount, member_grade_id, product):
    """商品促销类型，更新商品价格

    Return:
      product
    """
    # 如果用户不是会员
    if not member_grade_id:
        return product
    # 如果用户是会员
    else:
        # 商品参加促销
        if hasattr(product, 'promotion') and product.promotion:
            promotion_type = int(product.promotion.get('type'))
            # 限时抢购
            if promotion_type == promotion_models.PROMOTION_TYPE_FLASH_SALE:
                # user是否满足限时抢购条件
                if has_promotion(member_grade_id, int(product.promotion['member_grade_id'])):
                    product.display_price = product.promotion['detail']['promotion_price']
                    return product
            # 买赠
            elif promotion_type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
                if has_promotion(member_grade_id, int(product.promotion['member_grade_id'])):
                    return product
            # 满减
            elif promotion_type == promotion_models.PROMOTION_TYPE_PRICE_CUT:
                pass
            # 优惠券
            elif promotion_type == promotion_models.PROMOTION_TYPE_COUPON:
                pass
            # 积分抵扣
            elif promotion_type == promotion_models.PROMOTION_TYPE_INTEGRAL_SALE:
                if has_promotion(member_grade_id, int(product.integral_sale['member_grade_id'])):
                    return product
        # 商品是否参加会员折扣
        if product.is_member_product:
            product.display_price = product.display_price * discount
            return product
        else:
            return product


def get_user_product_saved_price(discount, member_grade_id, product):
    """根据用户的类别（会员/非会员）等级以及商品的促销返回商品优惠了多少钱.
         比如商品原价100， 促销价80， 这优惠了20元

       Args:
         user - 购物者
         product - 包含促销信息的商品

       Return:
         float - 优惠了多少钱
    """
    if not member_grade_id:
        # 如果用户不是会员
        return 0.000
    else:
        # 如果用户是会员
        if hasattr(product, 'promotion') and product.promotion:
            # 商品参加促销
            promotion_type = int(product.promotion.get('type'))
            if promotion_type == promotion_models.PROMOTION_TYPE_FLASH_SALE:
                # 限时抢购
                if has_promotion(member_grade_id, int(product.promotion['member_grade_id'])):
                    # 是否是指定的对象
                    if hasattr(product, 'display_price'):
                        # TODO 临时避免BDD报错
                        return product.display_price - product.promotion['detail']['promotion_price']
                    else:
                        return 0.00

        if product.is_member_product:
            # 商品是否参加会员折扣
            if hasattr(product, 'display_price'):
                # TODO 临时避免BDD报错
                return product.display_price * (1.000 - discount)
            return 0.00
        else:
            return 0.000


NO_PROMOTION_ID = -1


def group_product_by_promotion(request, products):
    """根据商品促销类型对商品进行分类
    Args:
      products -

    Return:
      list - [
                  {'id': ,
                   'uid': ,
                   'products':,
                   'promotion':,
                   'promotion_type': (str),
                   'promotion_result':,
                   'integral_sale_rule':,
                   'can_use_promotion': }
                  ...
               ]
    """
    member_grade_id = get_user_member_grade_id(request)
    group_id = 0
    #按照促销对product进行聚类
    global NO_PROMOTION_ID
    NO_PROMOTION_ID = -1  # 负数的promotion id表示商品没有promotion
    product_groups = []
    promotion2products = {}
    print 'jz---2', len(products)
    for product in products:
        #对于满减，同一活动中不同规格的商品不能分开，其他活动，需要分开
        group_id += 1
        default_products = {"group_id": group_id, "products": []}
        promotion_name = _get_promotion_name(product)
        print 'jz-----3', promotion_name
        promotion2products.setdefault(promotion_name, default_products)['products'].append(product)

    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    items = promotion2products.items()
    items.sort(lambda x, y: cmp(x[1]['group_id'], y[1]['group_id']))
    print 'jz----', len(items)
    for promotion_id, group_info in items:
        products = group_info['products']
        group_id = group_info['group_id']
        group_unified_id = __get_group_name(products)
        integral_sale_rule = __collect_integral_sale_rules(member_grade_id, products) if member_grade_id != -1 else None

        # 商品没有参加促销
        if not promotion_id:
            product_groups.append({
                "id": group_id,
                "uid": group_unified_id,
                'products': products,
                'promotion': {},
                "promotion_type": '',
                'promotion_result': '',
                'integral_sale_rule': integral_sale_rule,
                'can_use_promotion': False
            })
            continue

        promotion = products[0].promotion
        promotion_type = promotion.get('type', 0)
        if promotion_type == 0:
            type_name = 'none'
        else:
            type_name = promotion_models.PROMOTION2TYPE[promotion_type]['name']

        # #判断promotion状态
        # 促销活动还未开始，或已结束
        if promotion['start_date'] > now or promotion['end_date'] < now:
            promotion['status'] = promotion_models.PROMOTION_STATUS_NOT_START if promotion['start_date'] > now else promotion_models.PROMOTION_STATUS_FINISHED

            product_groups.append({
                "id": group_id,
                "uid": group_unified_id,
                "promotion_type": '',
                'products': products,
                'promotion': promotion,
                'promotion_result': None,
                'integral_sale_rule': integral_sale_rule,
                'can_use_promotion': promotion['status'] == promotion_models.PROMOTION_STATUS_STARTED,
                'promotion_json': json.dumps(promotion)
            })
            continue
        # 限时抢购
        if promotion_type == promotion_models.PROMOTION_TYPE_FLASH_SALE:
            product = products[0]
            promotion_result = {
                "saved_money": get_user_product_saved_price(product.member_discount, member_grade_id, product),
                "subtotal": product.purchase_count * promotion['detail']['promotion_price']
            }
            product_groups.append({
                "id": group_id,
                "uid": group_unified_id,
                "promotion_type": type_name,
                'products': products,
                'promotion': promotion,
                'promotion_result': promotion_result,
                'integral_sale_rule': integral_sale_rule,
                'can_use_promotion': promotion['status'] == promotion_models.PROMOTION_STATUS_STARTED,
                #'promotion_json': json.dumps(promotion)
            })
        # 买赠
        elif promotion_type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
            first_product = products[0]
            promotion = first_product.promotion
            promotion_detail = promotion['detail']
            can_use_promotion = (promotion['status'] == promotion_models.PROMOTION_STATUS_STARTED)

            total_purchase_count = 0
            total_product_price = 0.0
            for product in products:
                total_purchase_count += product.purchase_count
                total_product_price += product.price * product.purchase_count

            if total_purchase_count < promotion_detail['count']:
                can_use_promotion = False
            else:
                #如果满足循环满赠，则调整赠品数量
                if promotion_detail['is_enable_cycle_mode']:
                    premium_round_count = total_purchase_count / promotion['detail']['count']
                    for premium_product in promotion_detail['premium_products']:
                        premium_product['original_premium_count'] = premium_product['premium_count']
                        premium_product['premium_count'] = premium_product['premium_count'] * premium_round_count

            product_groups.append({
                "id": group_id,
                "uid": group_unified_id,
                "promotion_type": type_name,
                'products': products,
                'promotion': promotion,
                'promotion_result': {"subtotal": total_product_price},
                'integral_sale_rule': integral_sale_rule,
                'can_use_promotion': can_use_promotion,
                #'promotion_json': json.dumps(promotion)
            })
        # 满减
        elif promotion_type == promotion_models.PROMOTION_TYPE_PRICE_CUT:
            promotion = products[0].promotion
            promotion_detail = promotion['detail']
            if promotion['status'] == promotion_models.PROMOTION_STATUS_STARTED:
                total_price = 0.0
                for product in products:
                    total_price += product.price * product.purchase_count
                can_use_promotion = (total_price - promotion_detail['price_threshold']) >= 0
                promotion_round_count = 1  # 循环满减执行的次数
                if promotion_detail['is_enable_cycle_mode']:
                    promotion_round_count = int(total_price / promotion_detail['price_threshold'])
                if can_use_promotion:
                    subtotal = total_price - promotion_detail['cut_money']*promotion_round_count
                else:
                    subtotal = total_price
                promotion_result = {
                    "subtotal": subtotal,
                    "price_threshold": promotion_round_count*promotion_detail['price_threshold']
                }
                product_groups.append({
                    "id": group_id,
                    "uid": group_unified_id,
                    "promotion_type": type_name,
                    'products': products,
                    'promotion': promotion,
                    'promotion_result': promotion_result,
                    'integral_sale_rule': integral_sale_rule,
                    'can_use_promotion': can_use_promotion,
                    #'promotion_json': json.dumps(promotion)
                })
            else:
                product_groups.append({
                    "id": group_id,
                    "uid": group_unified_id,
                    "promotion_type": type_name,
                    'products': products,
                    'promotion': None,
                    'promotion_result': None,
                    'integral_sale_rule': integral_sale_rule,
                    'can_use_promotion': False,
                    #'promotion_json': json.dumps(promotion)
                })
        else:
            #非促销商品
            product_groups.append({
                "id": group_id,
                "uid": group_unified_id,
                "promotion_type": type_name,
                'products': products,
                'promotion': None,
                'promotion_result': None,
                'integral_sale_rule': integral_sale_rule,
                'can_use_promotion': False
            })
    return product_groups


def sorted_product_groups_by_promotioin(product_groups):
    '''按商品促销信息排序，先按促销id升序排，再按促销类型升序排，无促销信息的排到后面
    供获取订单商品、显示购物车详情调用.
    '''
    product_groups = sorted(
        product_groups,
        cmp=lambda x, y: cmp(x['promotion']['id'] if x['promotion'] else 0, y['promotion']['id'] if y['promotion'] else 0))
    product_groups = sorted(
        product_groups, cmp=lambda x, y:
        cmp(x['promotion']['type'] if x['promotion'] else 9, y['promotion']['type'] if y['promotion'] else 9))
    return product_groups


def format_product_group_price_factor(product_groups):
    factors = []
    for product_group in product_groups:
        product_factors = []
        for product in product_group['products']:
            product_factors.append({
                "id": product.id,
                "model": product.model_name,
                "count": product.purchase_count,
                "price": product.price,
                "weight": product.weight,
                "active_integral_sale_rule": getattr(product, 'active_integral_sale_rule', None),
                "postageConfig": product.postage_config if hasattr(product, 'postage_config') else {}
            })

        factor = {
            'id': product_group['id'],
            'uid': product_group['uid'],
            'products': product_factors,
            'promotion': product_group['promotion'],
            'promotion_type': product_group['promotion_type'],
            'promotion_result': product_group['promotion_result'],
            'integral_sale_rule': product_group['integral_sale_rule'],
            'can_use_promotion': product_group['can_use_promotion']
        }
        factors.append(factor)

    return factors


def get_products(request):
    '''获取订单商品，根据request参数返回商品列表，以及是否有已失效商品
    供下单、购物车页面调用
    '''
    member_discount = get_vip_discount(request)
    product_ids, promotion_ids, product_counts, product_model_names = get_product_param(request)

    #id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])
    products = []
    product_infos = []
    product2count = {}
    product2promotion = {}

    for i in range(len(product_ids)):
        product_id = int(product_ids[i])
        product_model_name = product_model_names[i]
        product_infos.append({"id": product_id, "model_name": product_model_name})
        product_model_id = '%s_%s' % (product_id, product_model_name)
        product2count[product_model_id] = int(product_counts[i])
        product2promotion[product_model_id] = promotion_ids[i] if promotion_ids[i] else 0

    postage_configs = request.webapp_user.webapp_owner_info.mall_data['postage_configs']
    system_postage_config = filter(lambda c: c.is_used, postage_configs)[0]
    products = mall_api.get_product_details_with_model(request.webapp_owner_id, request.webapp_user, product_infos)
    for product in products:
        product_model_id = '%s_%s' % (product.id, product.model['name'])
        product.member_discount = get_product_member_discount(member_discount, product)
        product.purchase_count = product2count[product_model_id]
        product.used_promotion_id = int(product2promotion[product_model_id])
        product.total_price = float(product.price)*product.purchase_count

        # 确定商品的运费策略
        if product.postage_type == mall_models.POSTAGE_TYPE_UNIFIED:
            #使用统一运费
            product.postage_config = {
                "id": -1,
                "money": product.unified_postage_money,
                "factor": None
            }
        else:
            if isinstance(system_postage_config.created_at, datetime):
                system_postage_config.created_at = system_postage_config.created_at.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(system_postage_config.update_time, datetime):
                system_postage_config.update_time = system_postage_config.update_time.strftime('%Y-%m-%d %H:%M:%S')
            product.postage_config = system_postage_config.to_dict('factor')
            # postage_config.to_dict('factor')
    return products


def get_product_param(request):
    '''获取订单商品id，数量，规格
    供_get_products调用
    '''
    if hasattr(request, 'redirect_url_query_string'):
        query_string = get_query_string_dict_to_str(request.redirect_url_query_string)
    else:
        query_string = request.REQUEST

    if 'product_ids' in query_string:
        product_ids = query_string.get('product_ids', None)
        if product_ids:
            product_ids = product_ids.split('_')
        promotion_ids = query_string.get('promotion_ids', None)
        if promotion_ids:
            promotion_ids = promotion_ids.split('_')
        else:
            promotion_ids = [0] * len(product_ids)
        product_counts = query_string.get('product_counts', None)
        if product_counts:
            product_counts = product_counts.split('_')
        product_model_names = query_string.get('product_model_names', None)
        if product_model_names:
            if '$' in product_model_names:
                product_model_names = product_model_names.split('$')
            else:
                product_model_names = product_model_names.split('%24')
        product_promotion_ids = query_string.get('product_promotion_ids', None)
        if product_promotion_ids:
            product_promotion_ids = product_promotion_ids.split('_')
        product_integral_counts = query_string.get('product_integral_counts', None)
        if product_integral_counts:
            product_integral_counts = product_integral_counts.split('_')
    else:
        product_ids = [query_string.get('product_id', None)]
        promotion_ids = [query_string.get('promotion_id', None)]
        product_counts = [query_string.get('product_count', None)]
        product_model_names = [query_string.get('product_model_name', 'standard')]
        product_promotion_ids = [query_string.get('product_promotion_id', None)]
        product_integral_counts = [query_string.get('product_integral_count', None)]

    return product_ids, promotion_ids, product_counts, product_model_names


def get_query_string_dict_to_str(str):
    data = dict()
    for item in str.split('&'):
        values = item.split('=')
        data[values[0]] = values[1]
    return data


def __get_group_name(group_products):
    items = []
    for product in group_products:
        items.append('%s_%s' % (product.id, product.model['name']))
    items.sort()
    return '-'.join(items)


def _get_promotion_name(product):
    """判断商品是否促销， 没有返回None, 有返回促销ID与商品的规格名.

    Args:
      product -

    Return:
      False - 商品没有促销
      'int_str' - 商品有促销
    """

    if not product.promotion:
        print 'jz----4'
        return None
    else:
        promotion = product.promotion
        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        # 已过期或未开始活动的商品，做为 普通商品
        if promotion['start_date'] > now or promotion['end_date'] < now:
            return '%d_%s' % (promotion['id'], product.model['name'])
        elif promotion['type'] == promotion_models.PROMOTION_TYPE_PRICE_CUT or promotion['type'] == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
            return promotion['id']
        else:
            return '%d_%s' % (promotion['id'], product.model['name'])


def __collect_integral_sale_rules(target_member_grade_id, products):
    """收集product_group积分规则抵扣规则

    Args:
      target_member_grade_id(int): 用户会员等级id
      products:

    Return:
      dict - {'member_grade_id':
              'product_model_names': (list),
              ?'rule':
             }
    """
    merged_rule = {
        "member_grade_id": target_member_grade_id,
        "product_model_names": []
    }
    for product in products:
        product.active_integral_sale_rule = None
        product_model_name = '%s_%s' % (product.id, product.model['name'])
        #判断积分应用是否不可用
        if not product.integral_sale_model:
            continue
        if not product.integral_sale_model.is_active:
            if product.integral_sale['detail']['is_permanant_active']:
                pass
            else:
                continue

        for rule in product.integral_sale['detail']['rules']:
            member_grade_id = int(rule['member_grade_id'])
            if member_grade_id < 0 or member_grade_id == target_member_grade_id:
                # member_grade_id == -1则为全部会员等级
                merged_rule['product_model_names'].append(product_model_name)
                product.active_integral_sale_rule = rule
                merged_rule['rule'] = rule

    if len(merged_rule['product_model_names']) > 0:
        return merged_rule
    else:
        return None
