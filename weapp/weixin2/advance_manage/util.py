# -*- coding: utf-8 -*-
import time

from modules.member.models import Member,SUBSCRIBED,CANCEL_SUBSCRIBED, MemberHasTag
from weixin2.models import FanHasCategory
from utils.string_util import byte_to_hex
from weixin2.models import get_opid_from_session
from modules.member import module_api


def get_members(request, filter_value, sort_attr):
    filter_data_args = {}
    filter_data_args['webapp_id'] = request.user_profile.webapp_id
    filter_data_args['status__in'] = [SUBSCRIBED, CANCEL_SUBSCRIBED]
    filter_data_args['is_for_test'] = False
    exclude_data_args = {}

    if filter_value:
        filter_data_dict = {}

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
            elif key == 'category_id':
                value = int(value)
                #如果value是-1则不进行处理，获取全部数据
                if value != -1:
                    if value == 0:
                        #获取未分组数据
                        exclude_member_ids = [fan_id_dict['fan_id'] for fan_id_dict in FanHasCategory.objects.values('fan_id').distinct()]
                        exclude_data_args["id__in"] = exclude_member_ids
                    else:
                        #获取指定组数据
                        member_ids = [member.id for member in  FanHasCategory.get_fans_list_by_category_id(value)]
                        filter_data_args["id__in"] = member_ids
            elif key == 'status':
                filter_data_args["is_subscribed"] = True if value == '1' else False
            elif key == 'sex':
                filter_data_args['memberinfo__sex'] = int(value)
    members = Member.objects.filter(**filter_data_args).exclude(**exclude_data_args).order_by(sort_attr)
    return members

def new_get_members(request, filter_value):
    filter_data_args = {}
    last_message_time = {}
    filter_data_args['webapp_id'] = request.user_profile.webapp_id
    filter_data_args['status__in'] = [SUBSCRIBED, CANCEL_SUBSCRIBED]
    filter_data_args['is_for_test'] = False

    if filter_value:
        filter_data_dict = {}

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
                if value in ['-1', 0]:
                    pass
                else:
                    filter_data_args["source"] = value
            if key in ['pay_times', 'pay_money', 'friend_count', 'unit_price']:
                if value.find('-') > -1:
                    val1,val2 = value.split('-')
                    if float(val1) > float(val2):
                        filter_data_args['%s__gte' % key] = float(val2)
                        filter_data_args['%s__lte' % key] = float(val1)
                    else:
                        filter_data_args['%s__gte' % key] = float(val1)
                        filter_data_args['%s__lte' % key] = float(val2)
                else:
                    filter_data_args['%s__gte' % key] = value

            if key in ['first_pay', 'sub_date', 'integral'] :
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
                last_message_time['member_latest_created_at__gte'] = time.strptime(val1,'%Y-%m-%d %H:%M')
                last_message_time['member_latest_created_at__lte'] = time.strptime(val2,'%Y-%m-%d %H:%M')

                opids = get_opid_from_session(session_filter)
                session_member_ids = module_api.get_member_ids_by_opid(opids)
                if filter_data_args.has_key('id__in'):
                    member_ids = filter_data_args['id__in']
                    member_ids = list(set(member_ids).intersection(set(session_member_ids)))
                    filter_data_args['id__in'] = member_ids
                else:
                    filter_data_args['id__in'] = session_member_ids

    members = Member.objects.filter(**filter_data_args)
    return members, filter_data_args, last_message_time