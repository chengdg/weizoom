# -*- coding: utf-8 -*-

__author__ = "chuter"

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.conf import settings
from django.shortcuts import render_to_response

from account.models import *

def map(request, webapp_id):
    try:
        loc_name = request.GET["loc_name"]
        mapapi = request.GET["mapapi"]
        targetlat = request.GET["targetlat"]
        targetlng = request.GET["targetlng"]
        page_title = request.GET["page_title"]

        profile = UserProfile.objects.get(webapp_id=webapp_id)

        c = RequestContext(request, {
            'loc_name': loc_name,
            'page_title': page_title,
            'webapp_id' : webapp_id,
            'template_name' : profile.webapp_template,
            'targetlat' : targetlat,
            'targetlng' : targetlng,
            'mapapi' : mapapi,
        })

        return render_to_response('map/map.html', c)
    except:
        import traceback
        traceback.print_exc(c)

        raise Http404(u'Not Found')