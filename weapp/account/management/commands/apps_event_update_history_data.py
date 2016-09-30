# -*- coding: utf-8 -*-

import pymongo
from bson.objectid import ObjectId

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from termite import pagestore as pagestore_manager
from apps.customerized_apps.event import models as app_models
from apps_survey_update_history_data import create_page

class Command(BaseCommand):
    help = ''
    args = ''

    def handle(self, *args, **options):
        """
        处理线上微信投票活动历史数据
        """
        print 'update event history data start...'
        old_events = app_models.event.objects()
        record_id2related_page_id = {str(event.id): str(event.related_page_id) for event in old_events}
        related_page_ids = [str(event.related_page_id) for event in old_events]
        related_page_ids_object = [ObjectId(event.related_page_id) for event in old_events]
        record_ids = [str(event.id) for event in old_events]
        old_event_participances = app_models.eventParticipance.objects(belong_to__in=record_ids)
        pagestore = pagestore_manager.get_pagestore('mongo')

        # #通过pymongo链接新的数据库market_app_data
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
            db_market_app_data.event_event.remove({'is_old': True})
            db_market_app_data.page_html.remove({'is_old': True, 'related_page_id': {'$in': related_page_ids}})
            db_market_app_data.event_event_participance.remove({'is_old': True})

            #复制termite里的page到market_app_page
            db_termite.market_app_page.remove({'_id': {'$in': related_page_ids_object}})
            for page in db_termite.page.find({'_id': {'$in': related_page_ids_object}}):
                # 更新market_app_page里description中静态资源地址
                model = page['component']['components'][0]['model']
                page['component']['components'][0]['model']['description'] = model['description'].replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                if page['component']['components'][1]['model'].get('description2', ''):
                    page['component']['components'][1]['model']['description2'] = page['component']['components'][1]['model']['description2'].replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                db_termite.market_app_page.insert(page)

            #然后将老数据写入新数据库
            for event in old_events:
                related_page_id = event.related_page_id
                page = pagestore.get_page(related_page_id, 1)
                page_details = page['component']['components'][0]['model']
                description = page_details['description'].replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                description2 = ''
                if page['component']['components'][1]['model'].get('description2', ''):
                    description2 = page['component']['components'][1]['model']['description2'].replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                db_market_app_data.event_event.insert({
                    'owner_id': event.owner_id,
                    'name': event.name,
                    'start_time': event.start_time,
                    'end_time': event.end_time,
                    'status': event.status,
                    'participant_count': event.participant_count,
                    'related_page_id': event.related_page_id,
                    'created_at': event.created_at,
                    'subtitle': page_details['subtitle'],
                    'description': description,
                    'description2': description2,
                    'prize': page_details['prize'],
                    'permission': page_details['permission'],
                    'is_old': True
                })

                project_id = 'new_app:event:%s' % related_page_id
                html = create_page(project_id).replace('xa-submitTermite', 'xa-submitWepage')
                html = html.replace('/static/', 'http://' + settings.DOMAIN + '/static/')

                db_market_app_data.page_html.insert({
                    'related_page_id': related_page_id,
                    'html': html,
                    'is_old': True
                })

            #构造活动报名related_page_id与活动id映射
            related_page_id2record_id = {str(event['related_page_id']): str(event['_id']) for event in db_market_app_data.event_event.find({'is_old': True})}
            for par in old_event_participances:
                related_page_id = record_id2related_page_id[str(par.belong_to)]
                db_market_app_data.event_event_participance.insert({
                    'member_id': par.member_id,
                    'belong_to': related_page_id2record_id[related_page_id],
                    'related_page_id': related_page_id,
                    'tel': par.tel,
                    'termite_data': par.termite_data,
                    'prize': par.prize,
                    'created_at': par.created_at,
                    'is_old': True
                })

        except Exception, e:
            print ('error!!!!!!!!!!!!',e)

        print 'update event history data end...'