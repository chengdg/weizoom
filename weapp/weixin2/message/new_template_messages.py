# -*- coding: utf-8 -*-

import json

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from watchdog.utils import watchdog_alert, watchdog_warning
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from weixin2 import export
import weixin2.models as weixin_models
from core import resource
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from core.wxapi import get_weixin_api

FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

class NewTemplateMessages(resource.Resource):
    """
    模板式消息
    """
    app = 'new_weixin'
    resource = 'new_template_messages'

    @login_required
    def get(request):
        """
        获取商家的模板消息
        """
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_weixin_second_navs(request),
            'second_nav_name': export.WEIXIN_MESSAGE_SECOND_NAV,
            'third_nav_name': export.MESSAGE_TEMPLATE_MESSAGE_NAV,
            # 'has_templates': weixin_models.UserTemplateSettings.objects.filter(owner_id=request.manager.id).count() > 0
            'has_templates': True
        })

        return render_to_response('weixin/message/new_template_messages.html', c)

    @login_required
    def api_get(request):
        """
                获取模板消息详情集合json数据
        """
        templates = weixin_models.UserHasTemplateMessages.objects.filter(owner_id=request.manager.id)
        template_ids = [t.template_id for t in templates]

        id2template = {t.template_id: t for t in weixin_models.UserTemplateSettings.objects.filter(id__in=template_ids)}

        items = []
        for template in templates:
            template_id = template.template_id
            item = {
                'status': False,
                'first': '',
                'remark': '',
                'industry_name': '%s-%s' % (template.primary_industry, template.deputy_industry),
                'title': template.title,
                'template_id': template_id,
                'example': template.example
            }

            setting = id2template.get(template_id, None)
            if setting:
                item['status'] = template.status
                item['first'] = setting.first
                item['remark'] = setting.remark

            items.append(item)
        response = create_response(200)
        response.data = items
        return response.get_response()

    @login_required
    def api_put(request):
        """
        配置模版消息内容
        """
        response = create_response(200)
        return response.get_response()

    @login_required
    def api_post(request):
        """
        同步模版
        从微信获取商家在公众号中配置的所有模板消息
        """
        mpuser_access_token = _get_mpuser_access_token(request.manager)
        response = create_response(500)
        if mpuser_access_token:
            weixin_api = get_weixin_api(mpuser_access_token)
            user_id = request.manager.id
            try:
                curr_template_info = {t.template_id: t for t in weixin_models.UserHasTemplateMessages.objects.filter(owner_id=user_id)}
                result = weixin_api.get_all_template_messages(True)
                template_list = result['template_list']
                need_create_list = [] #商家新配置的模版
                changed_template_info = [] #有变化的模版，包括新增的和先删除后新增同一个模版后，template_id发生变化的模版
                deleted_template_info = [] #商家删除的模版
                all_sync_ids = [] #商家配置的所有模版id
                need_delete_ids = [] #商家删除的模版id
                for t in template_list:
                    template_id = t['template_id']
                    all_sync_ids.append(template_id)
                    title = t['title']
                    if template_id not in curr_template_info.keys():
                        need_create_list.append(weixin_models.UserHasTemplateMessages(
                            owner_id = user_id,
                            template_id = template_id,
                            title = title,
                            primary_industry = t['primary_industry'],
                            deputy_industry = t['deputy_industry'],
                            content = t['content'],
                            example = t['example']
                        ))
                        changed_template_info.append({
                            'template_id': template_id,
                            'title': title
                        })
                for t_id in curr_template_info.keys(): #如果当前库里的template_id不在获取的信息之中，那么就是商家已删除的
                    if t_id not in all_sync_ids:
                        template = curr_template_info[t_id]
                        need_delete_ids.append(t_id)
                        deleted_template_info.append({
                            'template_id': template.template_id,
                            'title': template.title
                        })
                #删除模板库中的记录
                weixin_models.UserHasTemplateMessages.objects.filter(owner_id=user_id, template_id__in=need_delete_ids).delete()
                #同时删除已配置过的模版
                weixin_models.UserTemplateSettings.objects.filter(owner_id=user_id, template_id__in=need_delete_ids).delete()
                #新增模版
                weixin_models.UserHasTemplateMessages.objects.bulk_create(need_create_list)
                #提醒用户这些模版已经发生变化
                response = create_response(200)
                response.data = {
                    'created': changed_template_info,
                    'deleted': deleted_template_info
                }
                return response.get_response()
            except Exception, e:
                print e
                notify_message = u"获取模板列表异常, cause:\n{}".format(unicode_full_stack())
                watchdog_alert(notify_message)
                response.errMsg = e
                return response.get_response()
        else:
            response.errMsg = u'微信接口异常'
            return response.get_response()


def _get_mpuser_access_token(user):
    mp_user = get_binding_weixin_mpuser(user)
    if mp_user:
        mpuser_access_token = get_mpuser_accesstoken(mp_user)
    else:
        return False

    if mpuser_access_token is None:
        return False

    if mpuser_access_token.is_active:
        return mpuser_access_token
    else:
        return None