# -*- coding: utf-8 -*-

import pymongo
from bson.objectid import ObjectId

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from termite import pagestore as pagestore_manager
from apps.customerized_apps.sign import models as app_models
from apps_survey_update_history_data import create_page

class Command(BaseCommand):
    help = ''
    args = ''

    def handle(self, *args, **options):
        """
        处理线上签到活动历史数据
        """
        print ('update sign history data start...')
        old_signs = app_models.Sign.objects()
        record_id2related_page_id = {str(sign.id): str(sign.related_page_id) for sign in old_signs}
        related_page_ids = [str(sign.related_page_id) for sign in old_signs]
        related_page_ids_object = [ObjectId(sign.related_page_id) for sign in old_signs]
        record_ids = [str(sign.id) for sign in old_signs]
        old_sign_participances = app_models.SignParticipance.objects(belong_to__in=record_ids)
        old_sign_details = app_models.SignDetails.objects(belong_to__in=record_ids)

        pagestore = pagestore_manager.get_pagestore('mongo')

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
            db_market_app_data.sign_sign.remove()
            db_market_app_data.page_html.remove({'is_old': True, 'related_page_id': {'$in': related_page_ids}})
            db_market_app_data.sign_sign_participance.remove({'is_old': True})
            db_market_app_data.sign_sign_details.remove({'is_old': True})

            # 复制termite里的page到market_app_page
            db_termite.market_app_page.remove({'_id': {'$in': related_page_ids_object}})
            for page in db_termite.page.find({'_id': {'$in': related_page_ids_object}}):
                model = page['component']['components'][0]['model']
                page['component']['components'][0]['model']['image'] = model['image'].replace('/static/', 'http://' + settings.DOMAIN + '/static/').replace('/termite_static/', 'http://' + settings.DOMAIN + '/termite_static/')
                db_termite.market_app_page.insert(page)

            # #然后将老数据写入新数据库
            for sign in old_signs:
                related_page_id = sign.related_page_id
                page = pagestore.get_page(related_page_id, 1)
                page_details = page['component']['components'][0]['model']
                description = page_details['description']
                db_market_app_data.sign_sign.insert({
                    'owner_id': sign.owner_id,
                    'name': sign.name,
                    'status': sign.status,
                    'related_page_id': related_page_id,
                    'description': description,
                    'share': sign.share,
                    'reply': sign.reply,
                    'prize_settings': sign.prize_settings,
                    'participant_count': sign.participant_count,
                    'created_at': sign.created_at,
                    'is_old': True
                })
                project_id = 'new_app:sign:%s' % related_page_id
                html = create_page(project_id).replace('xa-submitTermite', 'xa-submitWepage').replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                db_market_app_data.page_html.insert({
                    'related_page_id': related_page_id,
                    'html': html,
                    'is_old': True
                })

            # 构造活动报名related_page_id与活动id映射
            related_page_id2record_id = {str(sign['related_page_id']): str(sign['_id']) for sign in db_market_app_data.sign_sign.find({'is_old': True})}

            for par in old_sign_participances:
                related_page_id = record_id2related_page_id[str(par.belong_to)]
                db_market_app_data.sign_sign_participance.insert({
                    'webapp_user_id': par.webapp_user_id,
                    'member_id': par.member_id,
                    'belong_to': related_page_id2record_id[related_page_id],
                    'tel': par.tel,
                    'prize': par.prize,
                    'latest_date': par.latest_date,
                    'total_count': par.total_count,
                    'serial_count': par.serial_count,
                    'top_serial_count': par.top_serial_count,
                    'created_at': par.created_at,
                    'is_old': True
                })

            for detail in old_sign_details:
                related_page_id = record_id2related_page_id[str(detail.belong_to)]
                db_market_app_data.sign_sign_details.insert({
                    'member_id': detail.member_id,
                    'belong_to': related_page_id2record_id[related_page_id],
                    'type': detail.type,
                    'prize': detail.prize,
                    'created_at': detail.created_at,
                    'is_old': True
                })


        except Exception, e:
            print ('error!!!!!!!!!!!!',e)

        print ('update sign history data end...')