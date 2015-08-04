# -*- coding: utf-8 -*-

from modules.member.models import Member
from weixin2.models import FanHasCategory
from utils.string_util import byte_to_hex

def get_members(request, filter_value, sort_attr):
    filter_data_args = {}
    filter_data_args['webapp_id'] = request.user_profile.webapp_id
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
