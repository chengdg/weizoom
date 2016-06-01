# -*- coding: utf-8 -*-

import urllib2
from webapp import models as webapp_models
from django.conf import settings
from celery import task


def request_url(url2method):
    if url2method:
        for key, value in url2method.items():
            print value,">>>>>>>key_url:",key
            request = urllib2.Request(key)
            request.get_method = lambda: value
            x = urllib2.urlopen(request)

@task(bind=True, max_retries=2)
def purge_webapp_page_from_varnish_cache(self, woid, project_id=0):

    if settings.EN_VARNISH:
        url2method = {}
        if project_id == 0:
            #首先清理首页varnish
            home_project = webapp_models.Project.objects.filter(owner=woid, is_active=True)[0]
            url = "http://{}/termite2/webapp_page/?workspace_id=home_page&webapp_owner_id={}&workspace_id={}&project_id=0".format(settings.DOMAIN, woid,home_project.workspace_id)
            url2method[url] = "BAN"
            

            url = "http://{}/termite2/webapp_page/?workspace_id={}&webapp_owner_id={}&project_id=0".format(settings.DOMAIN, home_project.workspace_id, woid)
            url2method[url] = "PURGE"

        else:
            project = webapp_models.Project.objects.get(id=project_id)
            if project.is_active:
                home_project = webapp_models.Project.objects.filter(owner=woid, is_active=True)[0]
                url = "http://{}/termite2/webapp_page/?workspace_id=home_page&webapp_owner_id={}&workspace_id={}&project_id=0".format(settings.DOMAIN, woid, home_project.workspace_id)
                url2method[url] = "PURGE"
             
            url = "http://{}/termite2/webapp_page/?workspace_id=home_page&project_id={}&webapp_owner_id={}".format(settings.DOMAIN, project.id, woid)
            url2method[url] = "PURGE"
          

            url = "http://{}/termite2/webapp_page/?workspace_id=home_page&pwebapp_owner_id={}&roject_id={}".format(settings.DOMAIN,  woid, project.id)
            url2method[url] = "PURGE"

            url = "http://{}/termite2/webapp_page/?workspace_id={}&webapp_owner_id={}&project_id=0".format(settings.DOMAIN, project.workspace_id, woid)
            url2method[url] = "PURGE"

        request_url(url2method)

