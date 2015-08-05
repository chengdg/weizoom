# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response

from core import resource
import export
from mall.module_api import update_promotion_status_by_member_grade
from modules.member.models import MemberGrade, IntegralStrategySttings, Member
from core.jsonresponse import create_response


class MemberGradeList(resource.Resource):
    app = "mall2"
    resource = "member_grade_list"

    @login_required
    def get(request):
        webapp_id = request.user_profile.webapp_id

        member_grades = MemberGrade.get_all_grades_list(webapp_id)

        for grade in member_grades:
            grade.shop_discount /= 10.0

        is_all_conditions = IntegralStrategySttings.objects.get(webapp_id=webapp_id).is_all_conditions

        if request.method == "GET":
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
        webapp_id = request.user_profile.webapp_id
        member_grades = MemberGrade.get_all_grades_list(webapp_id).exclude(name = u'普通会员')
        member_grade_ids = [grade.id for grade in member_grades]
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

            elif grade_id in member_grade_ids:
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


        delete_ids = list(set(member_grade_ids).difference(set(post_ids)))

        Member.objects.filter(grade_id__in=delete_ids).update(grade=default_grade)

        MemberGrade.objects.filter(id__in=delete_ids).delete()
        if delete_ids:
            update_promotion_status_by_member_grade(delete_ids)

        response = create_response(200)
        return response.get_response()


def _is_auto(grade_id):
    return MemberGrade.objects.get(id=grade_id).is_auto_upgrade
