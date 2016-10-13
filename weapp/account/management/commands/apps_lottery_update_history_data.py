# -*- coding: utf-8 -*-

import pymongo
from bson.objectid import ObjectId

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from termite import pagestore as pagestore_manager
from apps.customerized_apps.lottery import models as app_models
from apps_survey_update_history_data import create_page

class Command(BaseCommand):
    help = ''
    args = ''

    def handle(self, *args, **options):
        """
        处理线上微信抽奖活动历史数据
        """
        print ('update lottery history data start...')
        old_lotteries = app_models.lottery.objects()
        record_id2related_page_id = {str(lottery.id): str(lottery.related_page_id) for lottery in old_lotteries}
        related_page_ids = [str(lottery.related_page_id) for lottery in old_lotteries]
        related_page_ids_object = [ObjectId(lottery.related_page_id) for lottery in old_lotteries]
        record_ids = [str(lottery.id) for lottery in old_lotteries]
        old_lottery_participances = app_models.lotteryParticipance.objects(belong_to__in=record_ids)
        old_lottery_records = app_models.lottoryRecord.objects(belong_to__in=record_ids)
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
            db_market_app_data.lottery_lottery.remove({'is_old': True})
            db_market_app_data.page_html.remove({'is_old': True, 'related_page_id': {'$in': related_page_ids}})
            db_market_app_data.lottery_lottery_participance.remove({'is_old': True})
            db_market_app_data.lottery_lottery_record.remove({'is_old': True})

            # 复制termite里的page到market_app_page
            db_termite.market_app_page.remove({'_id': {'$in': related_page_ids_object}})
            for page in db_termite.page.find({'_id': {'$in': related_page_ids_object}}):
                for i in range(3):
                    page['component']['components'][0]['components'][i]['model']['image'] = page['component']['components'][0]['components'][i]['model']['image'].replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                db_termite.market_app_page.insert(page)

            #然后将老数据写入新数据库
            for lottery in old_lotteries:
                related_page_id = lottery.related_page_id
                db_market_app_data.lottery_lottery.insert({
                    'owner_id': lottery.owner_id,
                    'name': lottery.name,
                    'lottery_type': lottery.lottery_type,
                    'start_time': lottery.start_time,
                    'end_time': lottery.end_time,
                    'status': lottery.status,
                    'participant_count': lottery.participant_count,
                    'winner_count': lottery.winner_count,
                    'related_page_id': related_page_id,
                    'expend': lottery.expend,
                    'delivery': lottery.delivery,
                    'delivery_setting': lottery.delivery_setting,
                    'limitation': lottery.limitation,
                    'chance': lottery.chance,
                    'allow_repeat': lottery.allow_repeat,
                    'prize': lottery.prize,
                    'created_at': lottery.created_at,
                    'is_old': True
                })

                project_id = 'new_app:lottery:%s' % related_page_id
                html = create_page(project_id).replace('xa-submitTermite', 'xa-submitWepage')
                html = html.replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                db_market_app_data.page_html.insert({
                    'related_page_id': related_page_id,
                    'html': html,
                    'is_old': True
                })

            # 构造活动报名related_page_id与活动id映射
            related_page_id2record_id = {str(lottery['related_page_id']): str(lottery['_id']) for lottery in db_market_app_data.lottery_lottery.find({'is_old': True})}

            for par in old_lottery_participances:
                related_page_id = record_id2related_page_id[str(par.belong_to)]
                db_market_app_data.lottery_lottery_participance.insert({
                    'webapp_user_id': par.webapp_user_id,
                    'member_id': par.member_id,
                    'belong_to': related_page_id2record_id[related_page_id],
                    'has_prize': par.has_prize,
                    'total_count': par.total_count,
                    'can_play_count': par.can_play_count,
                    'lottery_date': par.lottery_date,
                    'is_old': True
                })

            for rec in old_lottery_records:
                related_page_id = record_id2related_page_id[str(rec.belong_to)]
                db_market_app_data.lottery_lottery_record.insert({
                    'webapp_user_id': rec.webapp_user_id,
                    'member_id': rec.member_id,
                    'belong_to': related_page_id2record_id[related_page_id],
                    'lottery_name': rec.lottery_name,
                    'prize_type': rec.prize_type,
                    'prize_title': rec.prize_title,
                    'prize_name': rec.prize_name,
                    'prize_data': rec.prize_data,
                    'tel': rec.tel,
                    'status': rec.status,
                    'created_at': rec.created_at,
                    'is_old': True
                })

        except Exception, e:
            print ('error!!!!!!!!!!!!',e)

        print ('update lottery history data end...')