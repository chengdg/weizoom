# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from core.restful_url_route import api
from core.jsonresponse import create_response
from core import paginator
from .notices_models import Notice


@api(app='mall', resource="notice_list", action='get')
@login_required
def get_notices_list(request):
    notices = Notice.objects.all()[::-1]
    notices_json = []
    # 进行分页
    count_per_page = int(request.GET.get('count_per_page', 4))
    cur_page = int(request.GET.get('page', '1'))
    pageinfo, notices = paginator.paginate(list(notices), cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
    for notice in notices:
        dict_notice = notice.to_dict()
        dict_notice['created_at'] = notice.created_at.strftime('%Y-%m-%d')
        notices_json.append(dict_notice)

    response = create_response(200)

    response.data = {
        'items': notices_json,
        'pageinfo': paginator.to_dict(pageinfo),
        'sortAttr': '',
        'data': {},
    }
    return response.get_response()
