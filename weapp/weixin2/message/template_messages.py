# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import F

from weixin2 import export
import weixin2.models as weixin_models
from market_tools.tools.template_message.models import *
from core import resource
from core import paginator
from core.jsonresponse import create_response

COUNT_PER_PAGE = 20
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV


class MessageIndustry(resource.Resource):
    """
    模板消息的“行业”
    """
    app = 'new_weixin'
    resource = 'message_industry'

    @login_required
    def api_get(request):
        """
        获取行业列表
        """
        response = create_response(200)
        industries = MarketToolsIndustry.objects.all()

        items = []
        for industry in industries:
            item = {}
            item['type'] = industry.industry_type
            item['name'] = industry.industry_name
            items.append(item)
        response.data.items = items

        return response.get_response()

    @login_required
    def api_post(request):
        """
        修改行业
        """
        response = create_response(200)
        major_type = request.POST.get('major_type')
        if major_type == 'None' or len(major_type) == 0:
            return response.get_response()
        industries = []
        major_templates = []
        try:
            major_type = int(major_type)
            majors = MarketToolsTemplateMessageDetail.objects.filter(owner=request.user, industry=major_type)
            if len(majors) > 0:
                majors.update(type=MAJOR_INDUSTRY_TYPE)
            else:
                major_templates = MarketToolsTemplateMessage.objects.filter(industry=major_type)
            industries.append(major_type)
        except:
            pass
        deputy_templates = []
        try:
            deputy_type = int(request.POST.get('deputy_type'))
            deputies = MarketToolsTemplateMessageDetail.objects.filter(owner=request.user, industry=deputy_type)
            if len(deputies) > 0:
                deputies.update(type=DEPUTY_INDUSTRY_TYPE)
            else:
                deputy_templates = MarketToolsTemplateMessage.objects.filter(industry=deputy_type)
            industries.append(deputy_type)
        except:
            pass
        MarketToolsTemplateMessageDetail.objects.filter(owner=request.user).exclude(industry__in=industries).delete()
        if major_templates:
            for template in major_templates:
                MarketToolsTemplateMessageDetail.objects.create(
                    owner = request.user,
                    template_message = template,
                    industry = major_type,
                    type = MAJOR_INDUSTRY_TYPE
                )
        if deputy_templates:
            for template in deputy_templates:
                MarketToolsTemplateMessageDetail.objects.create(
                    owner = request.user,
                    template_message = template,
                    industry = deputy_type,
                    type = DEPUTY_INDUSTRY_TYPE
                )


        return response.get_response()



class TemplateMessages(resource.Resource):
    """
    模板式消息
    """
    app = 'new_weixin'
    resource = 'template_messages'

    @login_required
    def get(request):
        """
        获取“模板消息”的页面
        """

        industries = MarketToolsTemplateMessageDetail.objects.filter(owner=request.user).values('industry', 'type').distinct()
        industry = {}
        for indus in industries:
            industry_name = TYPE2INDUSTRY.get(indus['industry'], '')
            if indus['type'] == MAJOR_INDUSTRY_TYPE:
                industry['major'] = industry_name
            elif indus['type'] == DEPUTY_INDUSTRY_TYPE:
                industry['deputy'] = industry_name

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_weixin_second_navs(request),
            'second_nav_name': export.WEIXIN_MESSAGE_SECOND_NAV,
            'third_nav_name': export.MESSAGE_TEMPLATE_MESSAGE_NAV,
            'industry': industry,
        })

        return render_to_response('weixin/message/template_messages.html', c)

    @login_required
    def api_get(request):
        """
                获取模板消息详情集合json数据
        """

        templates = [{
            "id": 1,
            "title": "TM00938-付款成功通知",
            "industry": "IT科技",
            "state": 1, # 未启用，已启用
        }, {
            "id": 2,
            "title": "订单标记发货通知",
            "industry": "消费品",
            "state": 2, # 未启用，已启用
        }]
        
        #获取当前页数
        cur_page = int(request.GET.get('page', '1'))
        #获取每页个数
        count_per_page = int(request.GET.get('count', COUNT_PER_PAGE))

        templates = MarketToolsTemplateMessageDetail.objects.filter(owner=request.user).order_by('type')
        pageinfo, templates = paginator.paginate(templates, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
        template_ids = [t.template_message_id for t in templates]
        messages = MarketToolsTemplateMessage.objects.filter(id__in=template_ids)
        id2template = {}
        for message in messages:
            id2template[message.id] = message
        items = []
        for template in templates:
            item = {}
            template_message_id = template.template_message_id
            item['template_detail_id'] = template.id
            item['template_id'] = template.template_id
            item['title'] = id2template[template_message_id].title
            item['industry_name'] = TYPE2INDUSTRY.get(id2template[template_message_id].industry, '')
            item['status'] = template.status

            if template.template_id:
                item['edit_status'] = 1
            else:
                item['edit_status'] = 0
            if template.type == 0:
                item['type'] = u'主营行业'
            else:
                item['type'] = u'副营行业'
            items.append(item)
        response = create_response(200)
        response.data.items = items
        response.data.pageinfo = paginator.to_dict(pageinfo)
        response.data.sortAttr = 'title'

        response = create_response(200)
        response.data = {
            'items': items,
            'pageinfo': paginator.to_dict(pageinfo),
            'data': {}
        }

        return response.get_response()

    @login_required
    def api_post(request):
        """
        修改模板消息的启用状态
        """
        id = request.POST.get('id')
        status = request.POST.get('status')
        status = '1' if status == '0' else '0'

        message_detail = MarketToolsTemplateMessageDetail.objects.get(id=id)
        message_detail.status = status
        message_detail.save()
        response = create_response(200)
        return response.get_response()

