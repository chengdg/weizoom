# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from apps.customerized_apps.powerme import models as powerme_models


class Command(BaseCommand):
    help = 'start powerme translation task'
    args = ''

    def handle(self, *args, **options):
        """
        转换PowerMeParticipance-->PowerMeRelations
        """
        print 'Powerme collections are translating...'
        all_data = powerme_models.PowerMeParticipance.objects()
        if all_data:
            all_data_list = []
            for data in all_data:
                data_dic = {}
                data_dic['member_id'] = data.member_id
                data_dic['belong_to'] = data.belong_to
                data_dic['powered_member_id'] = data.powered_member_id
                all_data_list.append(data_dic)

            for one_data in all_data_list:
                one_member_id = one_data['member_id']
                one_belong_to = one_data['belong_to']
                one_powered_member_id_list = one_data['powered_member_id']
                if one_powered_member_id_list:
                    for member_id in one_powered_member_id_list:
                        one_record = powerme_models.PowerMeRelations(
                            belong_to = str(one_belong_to),
                            member_id = str(one_member_id),
                            powered_member_id = str(member_id)
                            )
                        one_record.save()
            print 'Powerme Collections Translation is finished.'

        else:
            print 'There is no data needed to be translated.'