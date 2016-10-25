# -*- coding: utf-8 -*-

import pymongo
from bson.objectid import ObjectId

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# from termite import pagestore as pagestore_manager
from apps.customerized_apps.powerme import models as app_models
from apps_survey_update_history_data import create_page

class Command(BaseCommand):
    help = ''
    args = ''

    def handle(self, *args, **options):
        """
        处理线上微助力活动历史数据
        """
        print ('update powerme history data start...')
        old_powermes = app_models.PowerMe.objects()
        record_id2related_page_id = {str(powerme.id): str(powerme.related_page_id) for powerme in old_powermes}
        related_page_ids = [str(powerme.related_page_id) for powerme in old_powermes]
        related_page_ids_object = [ObjectId(powerme.related_page_id) for powerme in old_powermes]
        record_ids = [str(powerme.id) for powerme in old_powermes]
        old_powerme_participances = app_models.PowerMeParticipance.objects(belong_to__in=record_ids)
        old_powerme_relations = app_models.PowerMeRelations.objects(belong_to__in=record_ids)
        old_powerme_powered_logs = app_models.PowerLog.objects(belong_to__in=record_ids)
        old_powerme_powered_details = app_models.PoweredDetail.objects(belong_to__in=record_ids)
        old_powerme_powered_limit_relations = app_models.PoweredLimitRelation.objects(belong_to__in=record_ids)
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
            db_market_app_data.powerme_powerme.remove({'is_old': True})
            db_market_app_data.page_html.remove({'is_old': True, 'related_page_id': {'$in': related_page_ids}})
            db_market_app_data.powerme_powerme_participance.remove({'is_old': True})
            db_market_app_data.powerme_powerme_relations.remove({'is_old': True})
            db_market_app_data.powerme_powered_log.remove({'is_old': True})
            db_market_app_data.powerme_powered_detail.remove({'is_old': True})
            db_market_app_data.powerme_powered_limit_relation.remove({'is_old': True})

            # 复制termite里的page到market_app_page
            db_termite.market_app_page.remove({'_id': {'$in': related_page_ids_object}})
            for page in db_termite.page.find({'_id': {'$in': related_page_ids_object}}):
                model = page['component']['components'][0]['model']
                page['component']['components'][0]['model']['background_image'] = model['background_image'].replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                page['component']['components'][0]['model']['material_image'] = model['material_image'].replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                db_termite.market_app_page.insert(page)

            # #然后将老数据写入新数据库
            for powerme in old_powermes:
                related_page_id = powerme.related_page_id
                db_market_app_data.powerme_powerme.insert({
                    'owner_id': powerme.owner_id,
                    'name': powerme.name,
                    'start_time': powerme.start_time,
                    'end_time': powerme.end_time,
                    'status': powerme.status,
                    'related_page_id': related_page_id,
                    'timing': powerme.timing,
                    'reply_content': powerme.reply_content,
                    'material_image': powerme.material_image.replace('/static/', 'http://' + settings.DOMAIN + '/static/'),
                    'qrcode': powerme.qrcode,
                    'created_at': powerme.created_at,
                    'is_old': True
                })
                project_id = 'new_app:powerme:%s' % related_page_id
                html = create_page(project_id).replace('xa-submitTermite', 'xa-submitWepage').replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                db_market_app_data.page_html.insert({
                    'related_page_id': related_page_id,
                    'html': html,
                    'is_old': True
                })

            # 构造活动报名related_page_id与活动id映射
            related_page_id2record_id = {str(powerme['related_page_id']): str(powerme['_id']) for powerme in db_market_app_data.powerme_powerme.find({'is_old': True})}

            for par in old_powerme_participances:
                related_page_id = record_id2related_page_id[str(par.belong_to)]
                db_market_app_data.powerme_powerme_participance.insert({
                    'member_id': par.member_id,
                    'belong_to': related_page_id2record_id[related_page_id],
                    'has_join': par.has_join,
                    'power': par.power,
                    'powered_member_id': par.powered_member_id,
                    'created_at': par.created_at,
                    'is_old': True
                })

            for relation in old_powerme_relations:
                related_page_id = record_id2related_page_id[str(relation.belong_to)]
                db_market_app_data.powerme_powerme_relations.insert({
                    'member_id': relation.member_id,
                    'belong_to': related_page_id2record_id[related_page_id],
                    'powered_member_id': relation.powered_member_id,
                    'is_old': True
                })

            for log in old_powerme_powered_logs:
                related_page_id = record_id2related_page_id[str(log.belong_to)]
                db_market_app_data.powerme_powered_log.insert({
                    'belong_to': related_page_id2record_id[related_page_id],
                    'powered_member_id': log.powered_member_id,
                    'be_powered_member_id': log.be_powered_member_id,
                    'created_at': log.created_at,
                    'is_old': True
                })

            for detail in old_powerme_powered_details:
                related_page_id = record_id2related_page_id[str(detail.belong_to)]
                db_market_app_data.powerme_powered_detail.insert({
                    'belong_to': related_page_id2record_id[related_page_id],
                    'owner_id': detail.owner_id,
                    'power_member_id': detail.power_member_id,
                    'power_member_name': detail.power_member_name,
                    'has_powered': detail.has_powered,
                    'created_at': detail.created_at,
                    'is_old': True
                })

            for limit in old_powerme_powered_limit_relations:
                related_page_id = record_id2related_page_id[str(limit.belong_to)]
                db_market_app_data.powerme_powered_limit_relation.insert({
                    'belong_to': related_page_id2record_id[related_page_id],
                    'powered_member_id': limit.powered_member_id,
                    'created_at': limit.created_at,
                    'is_old': True
                })

        except Exception, e:
            print ('error!!!!!!!!!!!!',e)

        print ('update powerme history data end...')