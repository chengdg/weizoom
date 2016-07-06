# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from core import resource
from modules.member.models import MemberGrade, IntegralStrategySttings, Member, WebAppUser
from core.jsonresponse import create_response


class exSignMemberGradeList(resource.Resource):
	app = "apps/exsign"
	resource = "member_grade_list"

	@login_required
	def api_get(request):
		webapp_id = request.user_profile.webapp_id
		member_grades = MemberGrade.get_all_grades_list(webapp_id)
		member_grade_list = [{
			"id": -1,
			"name": u"全部"
		}]
		for grade in member_grades:
			member_grade_list.append({
				"id": grade.id,
				"name": grade.name
			})

		response = create_response(200)
		response.data = member_grade_list
		return response.get_response()