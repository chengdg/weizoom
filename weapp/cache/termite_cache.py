# -*- coding: utf-8 -*-
from __future__ import absolute_import


from utils import cache_util
from modules.member import models as member_models
from account.social_account import models as social_account_models
from django.db.models import signals
from datetime import datetime
from webapp import models as webapp_models
from weapp.hack_django import post_update_signal

def get_termite_project_for_cache(workspace_id):
    def inner_func():
        workspace = webapp_models.Workspace.objects.get(id=workspace_id)
        project = webapp_models.Project.objects.get(workspace=workspace, type='wepage', is_active=True)
        return {
            'value': {
                'workspace': workspace.to_dict(),
                'project': project.to_dict()
            }
        }

    return inner_func

class Object(object):
    def __init__(self):
        pass

def get_termite_project(project):
    key = 'termite_{workspace_id:%s}' % workspace_id
    data = cache_util.get_from_cache(key, get_termite_project_for_cache(openid, webapp_id))
    

    obj = Object()
    obj.workspace = webapp_models.Workspace.from_dict(data['workspace'])
    obj.project =  webapp_models.Project.from_dict(data['project'])
    return  obj

def delete_termite_project_cache(workspace_id):
    key = 'termite_{workspace_id:%s}' % workspace_id
    cache_util.delete_pattern(key)


# def update_termite_project_cache_for_workspace(instance, **kwargs):
#     """
#     Workspace save时触发信号回调函数

#     @param instance Member的实例
#     @param kwargs   其他参数，包括'sender'、'created'、'signal'、'raw'、'using'


#     """
#     #print("in update_webapp_order_cache(), kwargs: %s" % kwargs)
#     if isinstance(instance, webapp_models.Workspace):
#         try:
#             delete_termite_project_cache(instance.id)
#             #get_accounts(openid, webapp_id)
#         except:
#             pass
#     else:
#         instances = list(instance)
#         for workspace in instances:
#             try:

#                 delete_termite_project_cache(workspace.id)
#                 #get_accounts(openid, webapp_id)
#             except:
#                 pass
#     return

# post_update_signal.connect(update_termite_project_cache_for_workspace, sender=webapp_models.Workspace, dispatch_uid = "webapp_models.Workspace.update")
# signals.post_save.connect(update_termite_project_cache_for_workspace, sender=webapp_models.Workspace, dispatch_uid = "webapp_models.Workspace.save")


def update_termite_project_cache_for_project(instance, **kwargs):
    """
    Workspace save时触发信号回调函数

    @param instance Member的实例
    @param kwargs   其他参数，包括'sender'、'created'、'signal'、'raw'、'using'


    """
    if isinstance(instance, webapp_models.Project):
        try:
            delete_termite_project_cache(instance.workspace_id)
            #get_accounts(openid, webapp_id)
        except:
            pass
    else:
        instances = list(instance)
        for project in instances:
            try:

                delete_termite_project_cache(project.workspace_id)
                #get_accounts(openid, webapp_id)
            except:
                pass
    return

post_update_signal.connect(update_termite_project_cache_for_project, sender=webapp_models.Project, dispatch_uid = "webapp_models.Project.update")
signals.post_save.connect(update_termite_project_cache_for_project, sender=webapp_models.Project, dispatch_uid = "webapp_models.Project.save")





#signals.post_save.connect(update_webapp_product_cache, sender=mall_models.ProductCategory, dispatch_uid = "product_category.save")
#signals.post_save.connect(update_webapp_product_cache, sender=mall_models.CategoryHasProduct, dispatch_uid = "category_has_product.save")

