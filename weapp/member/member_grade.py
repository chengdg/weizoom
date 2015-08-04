# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from core import resource
import export
from mall.module_api import update_promotion_status_by_member_grade
from modules.member.models import *
from core.jsonresponse import create_response
import json


class MemberGradeList(resource.Resource):
    app = "mall2"
    resource = "member_grade_list"

    @login_required
    def get(request):
        webapp_id = request.user_profile.webapp_id

        member_grades = MemberGrade.get_all_grades_list(webapp_id)
        if request.method == "GET":
            c = RequestContext(request, {
                'first_nav_name': export.MEMBER_FIRST_NAV,
                'second_navs': export.get_second_navs(request),
                'second_nav_name': export.MEMBER_GRADE,
                'member_grades': member_grades,
            })
            return render_to_response('member/editor/member_grades.html', c)

    @login_required
    def api_post(request):
        # print(request)
        post_grades = json.loads(request.POST.get('json', []))
        # print(post_grades)
        webapp_id = request.user_profile.webapp_id
        member_grades = MemberGrade.get_all_grades_list(webapp_id)
        member_grade_ids = [grade.id for grade in member_grades]
        default_grade = MemberGrade.get_default_grade(webapp_id)

        print(webapp_id)
        print(default_grade.id)
        print("-----------")

        post_ids = []
        for grade in post_grades:
            grade_id = int(grade.get("id", None))

            post_ids.append(grade_id)

            name = grade.get("name", None)
            is_auto_upgrade = grade.get("is_auto_upgrade", False)
            pay_money = grade.get("money", None)
            pay_times = grade.get("paytimes", None)
            upgrade_lower_bound = grade.get("bound", None)
            shop_discount = grade.get("discount", None)


            print(grade_id, name,is_auto_upgrade,pay_money,pay_times,upgrade_lower_bound,shop_discount)

            if grade_id == default_grade.id:
                print("default")
                MemberGrade.objects.filter(id=grade_id).update(name=name, is_auto_upgrade=is_auto_upgrade,
                                                               shop_discount=shop_discount)

            elif grade_id in member_grade_ids:
                MemberGrade.objects.filter(id=grade_id).update(pay_money=pay_money, pay_times=pay_times,
                                                               upgrade_lower_bound=upgrade_lower_bound, name=name,
                                                               is_auto_upgrade=is_auto_upgrade,
                                                               shop_discount=shop_discount, )
            else:
                MemberGrade.objects.create(pay_money=pay_money, pay_times=pay_times,
                                           upgrade_lower_bound=upgrade_lower_bound, name=name,
                                           is_auto_upgrade=is_auto_upgrade,
                                           shop_discount=shop_discount, webapp_id=webapp_id)

        # delete_ids = list(set(member_grade_ids).difference(set(post_ids)))
        # MemberGrade.objects.filter(id__in=delete_ids).delete()
        # if delete_ids:
        #     update_promotion_status_by_member_grade(delete_ids)

        # post_ids = []
        # for key, value in request.POST.dict().items():
        #     if key.startswith('grade_id_'):
        #         post_ids.append(int(key.split('_')[2]))
        # post_ids.sort()
        # for grade_id in post_ids:
        #     grade_name = request.POST.get('grade_id_%s' % grade_id, 'get none value')
        #     grade_experience_term = request.POST.get('grade_experience_term_%s' % grade_id, 0)
        #     grade_money_term = request.POST.get('grade_money_term_%s' % grade_id, 0)
        #     grade_paytimes_term = request.POST.get('grade_paytimes_term_%s' % grade_id, 0)
        #     shop_discount = request.POST.get('shop_discount_%s' % grade_id, 100)
        #     if grade_id == default_grade.id:
        #         MemberGrade.objects.filter(id=grade_id).update(shop_discount=shop_discount, name=grade_name)
        #     elif grade_id in member_grade_ids:
        #         MemberGrade.objects.filter(id=grade_id).update(pay_money=grade_money_term, pay_times=grade_paytimes_term,
        #                                                  experience=grade_experience_term, name=grade_name,
        #                                                  shop_discount=shop_discount, )
        #     else:
        #         MemberGrade.objects.create(pay_money=grade_money_term, pay_times=grade_paytimes_term,
        #                                    experience=grade_experience_term, name=grade_name, webapp_id=webapp_id,
        #                                    upgrade_lower_bound=0, shop_discount=shop_discount, )
        #
        # delete_ids = list(set(member_grade_ids).difference(set(post_ids)))
        # MemberGrade.objects.filter(id__in=delete_ids).delete()
        # if delete_ids:
        #     update_promotion_status_by_member_grade(delete_ids)
        # return HttpResponseRedirect('/member/member_grades/get/')

        response = create_response(200)
        return response.get_response()
