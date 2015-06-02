# -*- coding: utf-8 -*-


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core.restful_url_route import api
from core.jsonresponse import create_response

from . import models as red_models


COUNT_PER_PAGE = 10


@api(app='mall_promotion', resource='red_enevlop_record', action='get')
@login_required
def get_red_enevlop_record(request):
    """
    获取红包记录的集合
    """
    # name = request.GET.get('name', '')
    # type_str = request.GET.get('type', 'all')
    # start_date = request.GET.get('startDate', '')
    # end_date = request.GET.get('endDate', '')

    # is_fetch_all_promotions = (not name) and (not type_str == 'all') and (not start_date) and (not end_date)
    # if is_fetch_all_promotions:
    #     """
    #     TODO:处理筛选
    #     """
    #     pass
    # else:
    #     records = [record for record in list(mall_models.RedEnvelop.objects.filter(owner=request.manager).order_by('-id'))]

    #     count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
    #     cur_page = int(request.GET.get('page', '1'))
    #     pageinfo, records = paginator.paginate(records, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

    # item = []
    # record2coupon_rules = dict([(record, record.coupon_rule_id for record in records)])
    # coupon_rule_ids = record2coupon_rules.values()
    # coupon_rules = mall_models.CouponRule.objects.filter(id__in=coupon_rule_ids)

    # for record in records:
    return create_response(200).get_response()


@api(app='mall_promotion', resource='red_enevlop_record', action='create')
@login_required
def create_red_enevlop(request):
    owners = request.POST.get('owners', None)  # 获取 得到放优惠券的用户
    if owners:
        coupon_rule_id = request.POST.get('coupon_rule_id')  # 优惠券规则
        pre_person_count = int(request.POST.get('pre_person_count'))  #
        person_count = len(owners)
        coupon_count = pre_person_count * person_count
        send_time = request.POST.get('send_time')
        for i in owners:
            red_models.RedEnvelop(owner=User.objects.get(pk=i),
                                  coupon_rule_id=coupon_rule_id,
                                  pre_person_count=person_count,
                                  coupon_count=coupon_count,
                                  send_time=send_time,
                                  ).save()
    else:
        assert("Error with no owners")
