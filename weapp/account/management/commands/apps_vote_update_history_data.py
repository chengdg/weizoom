# -*- coding: utf-8 -*-

import pymongo
from bson.objectid import ObjectId

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from termite import pagestore as pagestore_manager
from apps.customerized_apps.vote import models as app_models
from apps_survey_update_history_data import create_page

class Command(BaseCommand):
    help = ''
    args = ''

    def handle(self, *args, **options):
        """
        处理线上微信投票活动历史数据
        """
        print 'update vote history data start...'
        old_votes = app_models.vote.objects()
        record_id2related_page_id = {str(vote.id): str(vote.related_page_id) for vote in old_votes}
        related_page_ids = [str(vote.related_page_id) for vote in old_votes]
        related_page_ids_object = [ObjectId(vote.related_page_id) for vote in old_votes]
        record_ids = [str(vote.id) for vote in old_votes]
        old_vote_participances = app_models.voteParticipance.objects(belong_to__in=record_ids)
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
            #泡脚本之前先把新数据库中的老数据删除
            db_market_app_data.vote_vote.remove({'is_old': True})
            db_market_app_data.page_html.remove({'is_old': True, 'related_page_id': {'$in': related_page_ids}})
            db_market_app_data.vote_vote_participance.remove({'is_old': True})

            #复制termite里的page到market_app_page
            db_termite.market_app_page.remove({'_id': {'$in': related_page_ids_object}})
            for page in db_termite.page.find({'_id': {'$in': related_page_ids_object}}):
                # 更新market_app_page里description中静态资源地址
                model = page['component']['components'][0]['model']
                page['component']['components'][0]['model']['description'] = model['description'].replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                page['component']['components'][0]['model']['image'] = model['image'].replace('/static_v2/', 'http://' + settings.DOMAIN + '/static_v2/')
                components = page['component']['components']
                for i in range(0, len(page['component']['components'])):
                    if components[i]['components']:
                        for j in range(0, len(components[i]['components'])):
                            if components[i]['components'][j]['model'].get('image', ''):
                                page['component']['components'][i]['components'][j]['model']['image'] = components[i]['components'][j]['model']['image'].replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                db_termite.market_app_page.insert(page)

            #然后将老数据写入新数据库
            for vote in old_votes:
                related_page_id = vote.related_page_id
                page = pagestore.get_page(related_page_id, 1)
                page_details = page['component']['components'][0]['model']
                description = page_details['description']
                description = description.replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                db_market_app_data.vote_vote.insert({
                    'owner_id': vote.owner_id,
                    'name': vote.name,
                    'start_time': vote.start_time,
                    'end_time': vote.end_time,
                    'status': vote.status,
                    'participant_count': vote.participant_count,
                    'related_page_id': vote.related_page_id,
                    'image': vote.image,
                    'created_at': vote.created_at,
                    'subtitle': page_details['subtitle'],
                    'description': description,
                    'prize': page_details['prize'],
                    'permission': page_details['permission'],
                    'is_old': True
                })

                project_id = 'new_app:vote:%s' % related_page_id
                html = create_page(project_id).replace('xa-submitTermite', 'xa-submitWepage')

                html = html.replace('/static/', 'http://' + settings.DOMAIN + '/static/')

                db_market_app_data.page_html.insert({
                    'related_page_id': related_page_id,
                    'html': html,
                    'is_old': True
                })

            #构造投票活动related_page_id与活动id映射
            related_page_id2record_id = {str(vote['related_page_id']): str(vote['_id']) for vote in db_market_app_data.vote_vote.find({'is_old': True})}
            for par in old_vote_participances:
                related_page_id = record_id2related_page_id[str(par.belong_to)]
                termite_data = par.termite_data
                for key, value in termite_data.items():
                    if value['type'] == 'appkit.imageselection' and value['value']:
                        for img_title, img_value in value['value'].items():
                            image_url = img_value['image'].replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                            termite_data[key]['value'][img_title]['image'] = image_url

                db_market_app_data.vote_vote_participance.insert({
                    'member_id': par.member_id,
                    'belong_to': related_page_id2record_id[related_page_id],
                    'related_page_id': related_page_id,
                    'tel': par.tel,
                    'termite_data': termite_data,
                    'prize': par.prize,
                    'created_at': par.created_at,
                    'is_old': True
                })

        except Exception, e:
            print ('error!!!!!!!!!!!!',e)

        print 'update vote history data end...'