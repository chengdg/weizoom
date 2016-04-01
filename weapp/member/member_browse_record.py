# -*- coding: utf-8 -*-

from core import resource

from modules.member.models import *
from core import paginator
from core.jsonresponse import create_response

COUNT_PER_PAGE = 6


class MemberBrowseRecords(resource.Resource):
	app = "member"
	resource = "member_browse_record"

	def api_get(request):
		member_id = request.GET.get('id', None)

		if member_id is None:
			response = create_response(500)
			response.errMsg = 'Member id is required'
			return response.get_response()

		member_browse_records = MemberBrowseRecord.objects.filter(member_id=member_id).exclude(title="").order_by('-id')
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		current_page = int(request.GET.get('page', '1'))
		pageinfo, member_browse_records = paginator.paginate(member_browse_records, current_page, count_per_page, 
														query_string=request.META['QUERY_STRING'])
		items = []

		for record in member_browse_records:
			# if record.title == "":
			# 	continue
			items.append({
				'id': record.id,
				'member_id': record.member_id,
				'tittle': record.title,
				'url': record.url,
				'create_at': record.created_at.strftime("%Y-%m-%d %H:%M")
			})

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'data': {}
		}

		return response.get_response()