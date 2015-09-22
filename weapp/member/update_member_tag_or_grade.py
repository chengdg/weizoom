# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

import export
from core import resource
from core import paginator
from modules.member.models import *
from core.jsonresponse import create_response
from webapp import models as webapp_models
from weixin.user.models import DEFAULT_ICON, get_system_user_binded_mpuser

COUNT_PER_PAGE = 20

def get_request_members_list(request):
    """
    获取会员列表
    """
    #获取当前页数
    cur_page = int(request.GET.get('page', '1'))
    #获取每页个数
    count = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
    #处理排序
    sort_attr = request.GET.get('sort_attr', '-id')
    #会员过滤
    filter_value = request.GET.get('filter_value', None)

    filter_data_args = {}
    filter_data_args['webapp_id'] = request.user_profile.webapp_id
    filter_data_args['is_for_test'] = False
    filter_data_args['status__in'] = [SUBSCRIBED, CANCEL_SUBSCRIBED]

    #处理已经被选的会员
    selected_member_ids_str = request.GET.get('selectedMemberIds',"")
    selected_member_ids = []
    if selected_member_ids_str:
        selected_member_ids = selected_member_ids_str.split(",")

    #处理当前选择的会员
    current_member_id = int(request.GET.get('currentMemberId',"0"))
    #处理来自“数据罗盘-会员分析-关注会员链接”过来的查看关注会员的请求
    #add by duhao 2015-07-13
    status = request.GET.get('status', '-1')
    if not filter_value and status == '1':
        filter_data_args['is_subscribed'] = True

    if filter_value:
        filter_data_dict = {}
        #session_member_ids:通过最后对话时间而获取到会员id的list，先默认为false
        session_member_ids = False

        for filter_data_item in filter_value.split('|'):
            try:
                key, value = filter_data_item.split(":")
            except:
                key = filter_data_item[:filter_data_item.find(':')]
                value = filter_data_item[filter_data_item.find(':')+1:]

            filter_data_dict[key] = value
            if key == 'name':
                query_hex = byte_to_hex(value)
                filter_data_args["username_hexstr__contains"] = query_hex
            if key == 'grade_id':
                filter_data_args["grade_id"] = value

            if key == 'tag_id':
                member_ids = [member.id for member in  MemberHasTag.get_member_list_by_tag_id(value)]
                filter_data_args["id__in"] = member_ids

            if key == 'status':
                #无论如何这地方都要带有status参数，不然从“数据罗盘-会员分析-关注会员链接”过来的查询结果会有问题
                if value == '1':
                    filter_data_args["is_subscribed"] = True
                elif value == '0':
                    filter_data_args["is_subscribed"] = False

            if key == 'source':
                if value in ['-1']:
                    filter_data_args['source__in'] = [0,-1,1,2]
                elif value in ['0']:
                    filter_data_args['source__in'] = [0,-1]
                else:
                    filter_data_args["source"] = value

            if key in ['pay_times', 'pay_money', 'friend_count', 'unit_price', 'integral']:
                if value.find('-') > -1:
                    val1,val2 = value.split('--')
                    if float(val1) > float(val2):
                        filter_data_args['%s__gte' % key] = float(val2)
                        filter_data_args['%s__lte' % key] = float(val1)
                    else:
                        filter_data_args['%s__gte' % key] = float(val1)
                        filter_data_args['%s__lte' % key] = float(val2)
                else:
                    filter_data_args['%s__gte' % key] = value

            if key in ['first_pay', 'sub_date'] :
                if value.find('-') > -1:
                    val1,val2 = value.split('--')
                    if key == 'first_pay':
                        filter_data_args['last_pay_time__gte'] = val1
                        filter_data_args['last_pay_time__lte'] =  val2
                    elif key == 'sub_date':

                        filter_data_args['created_at__gte'] = val1
                        filter_data_args['created_at__lte'] = val2
                    else:
                        filter_data_args['integral__gte'] = val1
                        filter_data_args['integral__lte'] = val2

            if key  == 'last_message_time':
                val1,val2 = value.split('--')
                session_filter = {}
                session_filter['mpuser__owner_id'] = request.manager.id
                session_filter['member_latest_created_at__gte'] = time.mktime(time.strptime(val1,'%Y-%m-%d %H:%M'))
                session_filter['member_latest_created_at__lte'] = time.mktime(time.strptime(val2,'%Y-%m-%d %H:%M'))

                opids = get_opid_from_session(session_filter)
                session_member_ids = module_api.get_member_ids_by_opid(opids)
        #最后对话时间和分组的处理：1、都存在，做交集运算2、最后对话时间存在，将它赋值给filter_data_args['id__in']，
        #3、最后对话时间存在，上面做了处理，不处理了。4、都不存在，pass
        if filter_data_args.has_key('id__in') and session_member_ids:
            member_ids = filter_data_args['id__in']
            member_ids = list(set(member_ids).intersection(set(session_member_ids)))
            filter_data_args['id__in'] = member_ids
        elif session_member_ids:
            filter_data_args['id__in'] = session_member_ids
        #最后对话时间和分组的处理

    members = Member.objects.filter(**filter_data_args).order_by(sort_attr)
    total_count = members.count()
    pageinfo, members = paginator.paginate(members, cur_page, count, query_string=request.GET.get('query', None))
    for member in members:
        if str(member.id) in selected_member_ids:
            member.is_selected = True
        else:
            member.is_selected = False

        if member.id == current_member_id:
            member.is_current_select = True
        else:
            member.is_current_select = False

        if request.user.username == 'shengjing360':
            try:
                sj_binding_id = ShengjingBindingMember.objects.get(member_id=member.id).id
                sj_binding_member_info= ShengjingBindingMemberInfo.objects.get(binding_id=sj_binding_id)
                sj_name = sj_binding_member_info.name
                member.sj_name = sj_name
                member.sj_status = sj_binding_member_info.status_name
            except:
                # TODO 检查非学员是否正常
                member.sj_name = None
                member.sj_status = None
        else:
            member.sj_name = None
            member.sj_status = None

    return pageinfo, list(members), total_count


class UpdateMemberTagOrGrade(resource.Resource):
    """
    修改单个会员分组或者会员等级
    """
    app = "member"
    resource = "update_member_tag_or_grade"

    @login_required
    def api_get(request):
        webapp_id = request.user_profile.webapp_id
        tags = []
        for tag in MemberTag.get_member_tags(webapp_id):
            if tag.name == '未分组':
                tags = [{"id": tag.id,"name": tag.name}] + tags
            else:
                tags.append({
                    "id": tag.id,
                    "name": tag.name
                })

        grades = []
        for grade in MemberGrade.get_all_grades_list(webapp_id):
            grades.append({
                "id": grade.id,
                "name": grade.name
            })

        response = create_response(200)
        response.data = {
            'tags': tags,
            'grades': grades
        }

        return response.get_response()

    @login_required
    def api_post(request):
        webapp_id = request.user_profile.webapp_id
        type = request.POST.get('type', None)
        checked_ids = request.POST.get('checked_ids', None)
        member_id = request.POST.get('member_id', None)

        if type and member_id:
            member = Member.objects.get(id=member_id)
            if member.webapp_id == webapp_id:
                if type == 'tag':
                    tag_ids = checked_ids.split('_')
                    MemberHasTag.delete_tag_member_relation_by_member(member)
                    tag_ids = [id for id in tag_ids if id]
                    if tag_ids:
                        MemberHasTag.add_tag_member_relation(member, tag_ids)
                    else:
                        tag_ids.append(MemberTag.get_default_tag(webapp_id).id)
                        MemberHasTag.add_tag_member_relation(member, tag_ids)
                elif type == 'grade':
                    member.grade = MemberGrade.objects.get(id=checked_ids)
                    member.save()

        response = create_response(200)
        return response.get_response()

class BatchUpdateMemberTag(resource.Resource):
    """
    批量修改会员分组
    """
    app = "member"
    resource = "batch_update_member_tag"

    @login_required
    def api_post(request):
        webapp_id = request.user_profile.webapp_id
        tag_id = request.POST.get('tag_id', None)
        post_ids = request.POST.get('ids', None)

        status = request.POST.get('update_status', 'selected')
        if status == 'all':
            filter_value = request.POST.get('filter_value', '')
            request.GET = request.GET.copy()
            request.GET['filter_value'] = filter_value
            request.GET['count_per_page'] = 999999999
            _, request_members, _ = get_request_members_list(request)
            post_ids = [m.id for m in request_members]
        else:
            post_ids = post_ids.split('-')
        tag = MemberTag.objects.get(id=tag_id)
        if tag.webapp_id == webapp_id and post_ids:
            default_tag_id = MemberTag.get_default_tag(webapp_id).id
            MemberHasTag.add_members_tag(default_tag_id, tag_id, post_ids)

        response = create_response(200)
        return response.get_response()

class BatchUpdateMemberGrade(resource.Resource):
    """
    批量修改会员等级
    """
    app = "member"
    resource = "batch_update_member_Grade"

    @login_required
    def api_post(request):
        webapp_id = request.user_profile.webapp_id
        grade_id = request.POST.get('grade_id', None)
        post_ids = request.POST.get('ids', None)
        grade = MemberGrade.objects.get(id=grade_id)

        status = request.POST.get('update_status', 'selected')
        if status == 'all':
            filter_value = request.POST.get('filter_value', '')
            request.GET = request.GET.copy()
            request.GET['filter_value'] = filter_value
            request.GET['count_per_page'] = 999999999
            _, request_members, _ = get_request_members_list(request)
            post_ids = [m.id for m in request_members]
        else:
            post_ids = post_ids.split('-')

        if grade.webapp_id == webapp_id and post_ids:
            Member.objects.filter(id__in=post_ids).update(grade=grade)

        response = create_response(200)
        response.data.post_ids = post_ids
        return response.get_response()

class MemberIds(resource.Resource):
    """
    获取会员id集(取消关注除外)
    """

    app = "member"
    resource = "member_ids"

    @login_required
    def api_get(request):
        pageinfo, request_members, total_count = get_request_members_list(request)

        # 构造返回数据
        member_ids = []
        response = create_response(200)
        for member in request_members:
            if member.is_subscribed:
                member_ids.append(member.id)

        response.data = {
            'member_ids': member_ids,
        }
        return response.get_response()