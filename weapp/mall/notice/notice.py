# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import Http404

from core import resource, paginator
from core.jsonresponse import create_response
from mall import export, notices_models


class NoticeList(resource.Resource):
    app = 'mall2'
    resource = 'notice_list'

    @login_required
    def get(request):
        """
        """
        notice_list = notices_models.Notice.objects.all()
        paginator = Paginator(notice_list, 4)
        page = request.GET.get('page')
        try:
            notices = paginator.page(page)
        except PageNotAnInteger:
            notices = paginator.page(1)
        except EmptyPage:
            notices = Paginator.page(paginator.num_pages)
        c = RequestContext(request, {
            'first_nav_name': export.MALL_HOME_FIRST_NAV,
            'second_navs': export.get_mall_home_second_navs(request),
            'second_nav_name': export.MALL_HOME_NOTICES_NAV,
            'notice_list': notices,
        })
        return render_to_response('mall/editor/notice_list.html', c)

    @login_required
    def api_get(request):
        """
        """
        notices = notices_models.Notice.objects.all().order_by('-id')
        notices_json = []
        # 进行分页
        count_per_page = int(request.GET.get('count_per_page', 4))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, notices = paginator.paginate(
            list(notices),
            cur_page,
            count_per_page,
            query_string=request.META['QUERY_STRING']
        )
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


class Notice(resource.Resource):
    app = 'mall2'
    resource = 'notice'

    @login_required
    def get(request):
        """
        """
        notice_pk = request.GET['pk']
        try:
            notice = notices_models.Notice.objects.get(pk=notice_pk)
            notice.created_at = notice.created_at.strftime('%Y-%m-%d')
        except:
            return Http404
        c = RequestContext(request, {
            'first_nav_name': export.MALL_HOME_FIRST_NAV,
            'second_navs': export.get_mall_home_second_navs(request),
            'second_nav_name': export.MALL_HOME_NOTICES_NAV,
            'notice': notice,
        })
        return render_to_response('mall/editor/notice_detail.html', c)
