# -*- coding: utf-8 -*-

import pymongo
from bson.objectid import ObjectId

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from termite import pagestore as pagestore_manager
from apps.customerized_apps.group import models as app_models
from apps_survey_update_history_data import create_page

class Command(BaseCommand):
    help = ''
    args = ''

    def handle(self, *args, **options):
        """
        处理线上团购历史数据
        """
        print ('update group history data start...')
        old_groups = app_models.Group.objects()
        record_id2related_page_id = {str(group.id): str(group.related_page_id) for group in old_groups}
        related_page_ids = [str(group.related_page_id) for group in old_groups]
        related_page_ids_object = [ObjectId(group.related_page_id) for group in old_groups]
        record_ids = [str(group.id) for group in old_groups]
        old_group_relations = app_models.GroupRelations.objects(belong_to__in=record_ids)

        relation_ids = [str(relation.id) for relation in old_group_relations]
        old_group_details = app_models.GroupDetail.objects(relation_belong_to__in=relation_ids)
        # pagestore = pagestore_manager.get_pagestore('mongo')

        #通过pymongo链接新的数据库market_app_data
        l = len(args)
        if l > 0 and args[0] == 'deploy':
            host = 'mongodb://app:weizoom@dds-bp1502411213f1e41.mongodb.rds.aliyuncs.com:3717,dds-bp1502411213f1e42.mongodb.rds.aliyuncs.com:3717/market_app_data?replicaSet=mgset-1211291'
        else:
            host = settings.APP_MONGO['HOST']
        connection = pymongo.Connection(host, 27017)
        connection_termite = pymongo.Connection('mongo.weapp.com', 27017)
        db_market_app_data = connection.market_app_data
        db_termite = connection_termite.termite

        try:
            #跑脚本之前先把新数据库中的老数据删除
            db_market_app_data.group_group.remove({'is_old': True})
            db_market_app_data.page_html.remove({'is_old': True, 'related_page_id': {'$in': related_page_ids}})
            db_market_app_data.group_group_relations.remove({'is_old': True})
            db_market_app_data.group_group_detail.remove({'is_old': True})

            # 复制termite里的page到market_app_page
            db_termite.market_app_page.remove({'_id': {'$in': related_page_ids_object}})
            for page in db_termite.page.find({'_id': {'$in': related_page_ids_object}}):
                db_termite.market_app_page.insert(page)

            #然后将老数据写入新数据库
            for group in old_groups:
                related_page_id = group.related_page_id
                db_market_app_data.group_group.insert({
                    'owner_id': group.owner_id,
                    'related_page_id': related_page_id,
                    'name': group.name,
                    'start_time': group.start_time,
                    'end_time': group.end_time,
                    'status': group.status,
                    'is_use': group.is_use,
                    'handle_status': group.handle_status,
                    'created_at': group.created_at,
                    'group_dict': group.group_dict,
                    'product_id': group.product_id,
                    'product_img': group.product_img,
                    'product_name': group.product_name,
                    'product_price': group.product_price,
                    'product_socks': group.product_socks,
                    'product_sales': group.product_sales,
                    'product_usercode': group.product_usercode,
                    'product_create_at': group.product_create_at,
                    'rules': group.rules,
                    'material_image': group.material_image,
                    'share_description': group.share_description,
                    'visited_member': group.visited_member,
                    'is_old': True
                })

                project_id = 'new_app:group:%s' % related_page_id
                html = create_page(project_id).replace('xa-submitTermite', 'xa-submitWepage')
                html = html.replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                db_market_app_data.page_html.insert({
                    'related_page_id': related_page_id,
                    'html': html,
                    'is_old': True
                })

            # 构造团购related_page_id与活动id映射
            related_page_id2record_id = {str(group['related_page_id']): str(group['_id']) for group in db_market_app_data.group_group.find({'is_old': True})}

            old_relation_id2new_relation_id = {}
            for relation in old_group_relations:
                related_page_id = record_id2related_page_id[str(relation.belong_to)]
                new_relation = db_market_app_data.group_group_relations.insert({
                    'belong_to': related_page_id2record_id[related_page_id],
                    'member_id': relation.member_id,
                    'group_leader_name': relation.group_leader_name,
                    'product_id': relation.product_id,
                    'group_type': relation.group_type,
                    'group_days': relation.group_days,
                    'group_price': relation.group_price,
                    'group_status': relation.group_status,
                    'grouped_number': relation.grouped_number,
                    'grouped_member_ids': relation.grouped_member_ids,
                    'success_time': relation.success_time,
                    'created_at': relation.created_at,
                    'is_old': True
                })
                old_relation_id2new_relation_id[str(relation.id)] = str(new_relation)

            for detail in old_group_details:
                db_market_app_data.group_group_detail.insert({
                    'relation_belong_to': old_relation_id2new_relation_id[str(detail.relation_belong_to)],
                    'owner_id': detail.owner_id,
                    'grouped_member_id': detail.grouped_member_id,
                    'grouped_member_name': detail.grouped_member_name,
                    'is_already_paid': detail.is_already_paid,
                    'order_id': detail.order_id,
                    'created_at': detail.created_at,
                    'msg_api_status': detail.msg_api_status,
                    'msg_api_failed_members_info': detail.msg_api_failed_members_info,
                    'is_old': True
                })

        except Exception, e:
            print ('error!!!!!!!!!!!!',e)

        print ('update group history data end...')