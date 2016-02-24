# -*- coding: utf-8 -*-

import datetime
from django.core.management.base import BaseCommand, CommandError
from apps.customerized_apps.powerme import models as powerme_models
from collections import OrderedDict
from mongoengine.errors import NotUniqueError
import pymongo
import json


class Command(BaseCommand):
    help = 'start powerme translation task'
    args = ''

    def handle(self, *args, **options):
        """
        转换PowerMeParticipance-->PowerMeRelations
        6min
        """
        timeA = datetime.datetime.now()
        print '---------Translating-----------'
        print 'Powerme collections are translating...'
        print 'Start Time:',timeA

        all_data = powerme_models.PowerMeParticipance.objects()
        print '--------------------'
        print 'loading...'
        if all_data.count() > 0:
            print 'Total Count:',all_data.count()
            powerme_models.PowerMeRelations.objects.all().delete()
            all_relations_list = []
            for data in all_data:
                if data.powered_member_id:
                    cur_member_id = data.member_id
                    cur_belong_to = data.belong_to
                    cur_powered_member_id_list = set(data.powered_member_id)

                    for cur_powered_member_id in cur_powered_member_id_list:
                        relation_dic = OrderedDict()
                        relation_dic['member_id'] = cur_member_id
                        relation_dic['belong_to'] = cur_belong_to
                        relation_dic['powered_member_id'] = cur_powered_member_id
                        all_relations_list.append(relation_dic)

            need_create_docs=[]
            for relation in all_relations_list:
                need_create_docs.append(powerme_models.PowerMeRelations(
                    belong_to = str(relation['belong_to']),
                    member_id = str(relation['member_id']),
                    powered_member_id = str(relation['powered_member_id'])
                ))

            count = 5000
            n = len(need_create_docs)//count +1

            for i in range(n):
                tmp_docs = need_create_docs[:count]
                need_create_docs = need_create_docs[count:]
                try:
                    powerme_models.PowerMeRelations.objects.insert(tmp_docs)
                except NotUniqueError,e:
                    pass
                except Exception,e:
                    print '[!!!Error]:',e

            print 'Total Relations Count:',powerme_models.PowerMeRelations.objects().count()
            print '--------------------'
            print 'Powerme Collections Translation is finished.'
            timeB = datetime.datetime.now()
            print 'End Time:',timeB
            print 'Total Time:'
            print '%s s'%(str((timeB-timeA).seconds))
            print '------ Translating End ----------'

        else:
            print 'There is no data needed to be translated.'