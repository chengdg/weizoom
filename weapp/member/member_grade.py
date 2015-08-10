# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from core import resource
import export
import mall.module_api
from modules.member.models import MemberGrade, IntegralStrategySttings, Member, WebAppUser
from core.jsonresponse import create_response
from mall.models import Order
import mall.models as mall_models


class MemberGradeList(resource.Resource):
    app = "mall2"
    resource = "member_grade_list"

    @login_required
    def get(request):
        webapp_id = request.user_profile.webapp_id
        print(webapp_id)
        member_grades = MemberGrade.get_all_grades_list(webapp_id)

        for grade in member_grades:
            grade.shop_discount /= 10.0

        is_all_conditions = IntegralStrategySttings.objects.get(webapp_id=webapp_id).is_all_conditions

        c = RequestContext(request, {
            'first_nav_name': export.MEMBER_FIRST_NAV,
            'second_navs': export.get_second_navs(request),
            'second_nav_name': export.MEMBER_GRADE,
            'member_grades': member_grades,
            'is_all_conditions': is_all_conditions,
        })
        return render_to_response('member/editor/member_grades.html', c)

    @login_required
    def api_post(request):

        post_grades = json.loads(request.POST.get('grades', []))
        if not post_grades:
            return HttpResponseRedirect('/mall2/member_grade_list/')

        webapp_id = request.user_profile.webapp_id
        original_member_grades = MemberGrade.get_all_grades_list(webapp_id)
        original_member_grade_ids = [grade.id for grade in original_member_grades]
        default_grade = MemberGrade.get_default_grade(webapp_id)

        is_all_conditions = request.POST.get('is_all_conditions', '0')
        IntegralStrategySttings.objects.filter(webapp_id=webapp_id).update(is_all_conditions=int(is_all_conditions))

        post_ids = []
        for grade in post_grades:
            grade_id = int(grade.get("id", '0'))
            if grade_id > 0:
                post_ids.append(grade_id)

            name = grade.get("name", 'get none value')
            is_auto_upgrade = bool(int(grade.get("is_auto_upgrade", 0)))
            pay_money = grade.get("money", 0)
            pay_times = grade.get("paytimes", 0)
            upgrade_lower_bound = grade.get("bound", 0)
            shop_discount = grade.get("discount", '10')

            shop_discount = int(float(shop_discount) * 10)

            if grade_id == default_grade.id:

                MemberGrade.objects.filter(id=grade_id).update(name=name, shop_discount=shop_discount)

            elif grade_id in original_member_grade_ids:
                if is_auto_upgrade:
                    MemberGrade.objects.filter(id=grade_id).update(pay_money=pay_money, pay_times=pay_times,
                                                                   upgrade_lower_bound=upgrade_lower_bound, name=name,
                                                                   is_auto_upgrade=is_auto_upgrade,
                                                                   shop_discount=shop_discount)
                else:
                    MemberGrade.objects.filter(id=grade_id).update(name=name,
                                                                   is_auto_upgrade=is_auto_upgrade,
                                                                   shop_discount=shop_discount)
            else:
                if is_auto_upgrade:
                    MemberGrade.objects.create(pay_money=pay_money, pay_times=pay_times,
                                               upgrade_lower_bound=upgrade_lower_bound, name=name,
                                               is_auto_upgrade=is_auto_upgrade,
                                               shop_discount=shop_discount, webapp_id=webapp_id)

                else:
                    MemberGrade.objects.create(name=name, is_auto_upgrade=is_auto_upgrade,
                                               shop_discount=shop_discount, webapp_id=webapp_id)

        delete_ids = list(set(original_member_grade_ids).difference(set(post_ids)))

        if delete_ids:
            if default_grade.id in delete_ids:
                delete_ids.remove(default_grade.id)

            members = Member.objects.filter(grade_id__in=delete_ids)

            for member in members:
                auto_update_grade(member=member, delete=True)


            # MemberGrade.objects.filter(id__in=delete_ids).delete()

            mall.module_api.update_promotion_status_by_member_grade(delete_ids)

        response = create_response(200)
        return response.get_response()


def auto_update_grade(webapp_user_id=None, member=None, delete=False, **kwargs):
    """

    :param member:
    :return:bool,等级是否更新
    """

    is_change = False

    if webapp_user_id:
        print("webapp_user_id", webapp_user_id)
        member = WebAppUser.get_member_by_webapp_user_id(webapp_user_id)
    elif member:
        print("member", member.id)

    if not member.grade.is_auto_upgrade and not delete:
        return is_change

    webapp_id = member.webapp_id
    # webapp_owner_id = webapp_models.WebApp.objects.get(appid=webapp_id).owner_id
    webapp_user_ids = member.get_webapp_user_ids

    # 获取会员数据
    paid_orders = Order.objects.filter(status=mall_models.ORDER_STATUS_SUCCESSED, webapp_user_id__in=webapp_user_ids)
    pay_times = paid_orders.count()
    bound = member.experience
    pay_money = 0
    for order in paid_orders:
        pay_money += order.get_final_price(webapp_id) + order.weizoom_card_money

    if delete:
        grades_list = MemberGrade.objects.filter(webapp_id=webapp_id, is_auto_upgrade=True).exclude(
            id=member.grade_id).order_by('-id')
    else:
        grades_list = MemberGrade.objects.filter(webapp_id=webapp_id, is_auto_upgrade=True,
                                                 id__gt=member.grade_id).order_by('-id')

    is_all_conditions = IntegralStrategySttings.objects.get(webapp_id=webapp_id).is_all_conditions
    # is_all_conditions = webapp_owner_cache.get_webapp_owner_info(webapp_owner_id).is_all_conditions
    print("is_all_conditions:", is_all_conditions)

    # 计算条件

    print("conditions:", pay_money, pay_times, bound)

    print("len:", len(grades_list))

    if is_all_conditions:
        for grade in grades_list:
            if pay_money >= grade.pay_money and pay_times >= grade.pay_times and bound >= grade.upgrade_lower_bound:
                is_change = True
                member.grade = grade
                break
    else:
        print "here----------------------"
        for grade in grades_list:
            print("one grade:", grade.name, grade.pay_money, grade.pay_times, grade.upgrade_lower_bound)
            if pay_money >= grade.pay_money or pay_times >= grade.pay_times or bound >= grade.upgrade_lower_bound:
                is_change = True
                member.grade = grade
                break
    if is_change:
        print(member.grade.name)
        print("changed")
        member.save()
    else:
        print("not changed")

    return is_change



    ############################################


# def update_grade_from_order(**kwargs):
#     if 'model' in kwargs:
#         for order in kwargs['instance']:
#             auto_update_grade(webapp_user_id=order.webapp_user_id)
#     else:
#         auto_update_grade(webapp_user_id=kwargs['instance'].webapp_user_id)
#
#
# def update_grade_from_member(**kwargs):
#     if 'model' in kwargs:
#         print("update")
#         for member in kwargs['instance']:
#             auto_update_grade(member=member)
#     else:
#         print('save')
#         auto_update_grade(member=kwargs['instance'])
#
#
# signals.post_save.connect(update_grade_from_order, sender=Order, dispatch_uid="member_grade.order_save")
# post_update_signal.connect(update_grade_from_order,
#                            sender=Order, dispatch_uid="member_grade.order_update")
#
# signals.post_save.connect(update_grade_from_member, sender=Member, dispatch_uid="member_grade.member_save")
# #
# post_update_signal.connect(update_grade_from_member,
#                            sender=Member, dispatch_uid="member_grade.member_update")
