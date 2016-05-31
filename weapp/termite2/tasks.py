# -*- coding: utf-8 -*-

import urllib2
from webapp import models as webapp_models
from django.conf import settings
from celery import task


@task(bind=True, max_retries=2)
def purge_webapp_page_from_varnish_cache(self, woid, project_id=0):
    if settings.EN_VARNISH:
        if project_id == 0:
            #首先清理首页varnish

            #try:
            home_project = webapp_models.Project.objects.filter(owner=woid, is_active=True)[0]
            url = "http://{}/termite2/webapp_page/?ngx_rd=1workspace_id=home_page&webapp_owner_id={}&workspace_id={}&project_id=0".format(settings.DOMAIN, woid,home_project.workspace_id)
            print "home_page_url++++>>>>>", url
            request = urllib2.Request(url)
            request.get_method = lambda: 'BAN'
            x = urllib2.urlopen(request)
            # except:
            #     pass
            # for project in webapp_models.Project.objects.filter(owner=woid):
            #     #try:
            #     url = "http://{}/termite2/webapp_page/?ngx_rd=1workspace_id=home_page&webapp_owner_id={}&project_id={}".format(settings.DOMAIN, woid, project.id)
            #     print "project1++++>>>>>", url
            #     request = urllib2.Request(url)
            #     #request.get_method = lambda: 'BAN'
            #     x = urllib2.urlopen(request)
            #     # except:
            #     #     pass
        else:
            project = webapp_models.Project.objects.get(id=project_id)
            if project.is_active:
                home_project = webapp_models.Project.objects.filter(owner=woid, is_active=True)[0]
                url = "http://{}/termite2/webapp_page/?ngx_rd=1workspace_id=home_page&webapp_owner_id={}&workspace_id={}&project_id=0".format(settings.DOMAIN, woid, home_project.workspace_id)
                print "home_page_url++++>>>>>", url
                request = urllib2.Request(url)
                request.get_method = lambda: 'PURGE'
                x = urllib2.urlopen(request)
                url = "http://{}/termite2/webapp_page/?ngx_rd=1workspace_id=home_page&project_id={}&webapp_owner_id={}".format(settings.DOMAIN, project.id, woid)
                print "project++++>>>>>", url
                request = urllib2.Request(url)
                request.get_method = lambda: 'PURGE'
                x = urllib2.urlopen(request)

