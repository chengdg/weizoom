# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404

# local
from core.restful_url_route import view
from . import export
from .notices_models import Notice


@view(app='mall', resource='notice_list', action='get')
@login_required
def get_notice_list(request):
    notice_list = Notice.objects.all()
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
        'second_navs': export.get_home_second_navs(request),
        'second_nav_name': export.MALL_HOME_NOTICES_NAV,
        'notice_list': notices,
    })
    return render_to_response('mall/editor/notice_list.html', c)


@view(app='mall', resource='notice_detail', action='get')
@login_required
def get_notice_detail(request):
    notice_pk = request.GET['pk']
    try:
        notice = Notice.objects.get(pk=notice_pk)
        notice.created_at = notice.created_at.strftime('%Y-%m-%d')
    except:
        return Http404
    c = RequestContext(request, {
        'first_nav_name': export.MALL_HOME_FIRST_NAV,
        'second_navs': export.get_home_second_navs(request),
        'second_nav_name': export.MALL_HOME_NOTICES_NAV,
        'notice': notice,
    })
    return render_to_response('mall/editor/notice_detail.html', c)
