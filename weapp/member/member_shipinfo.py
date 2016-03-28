# -*- coding: utf-8 -*-
from core import resource
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from modules.member.models import *
from core import paginator
from core.jsonresponse import create_response

COUNT_PER_PAGE = 6


class MemberShipInfo(resource.Resource):
	app = "member"
	resource = "member_shipinfo"

	def api_get(request):
		member_id = request.GET.get('id', None)

		if member_id is None:
			response = create_response(500)
			response.errMsg = 'Member id is required'
			return response.get_response()

		member = Member.objects.get(id=member_id)
		member_ships = ShipInfo.objects.filter(webapp_user_id__in=member.get_webapp_user_ids)
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		current_page = int(request.GET.get('page', '1'))
		pageinfo, member_ships = paginator.paginate(member_ships, current_page, count_per_page, 
														query_string=request.META['QUERY_STRING'])
		items = []

		for ship in member_ships:
			items.append({
				'id': ship.id,
				'ship_name': ship.ship_name,
				'ship_tel': ship.ship_tel,
				'ship_address': ship.ship_address,
				'area': ship.get_str_area,
				'is_selected': ship.is_selected,
				'is_deleted': ship.is_deleted
			})

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'data': {}
		}

		return response.get_response()