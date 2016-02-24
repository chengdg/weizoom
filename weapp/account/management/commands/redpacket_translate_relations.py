# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from apps.customerized_apps.red_packet import models as redpacket_models


class Command(BaseCommand):
    help = 'start redpacket translation task'
    args = ''

    def handle(self, *args, **options):
        """
        转换RedPacketParticipance-->RedPacketRelations
        """
        print 'Redpacket collections are translating...'

        all_redpacket = redpacket_models.RedPacket.objects()
        id2all_redpacket = {}
        for one_redpacket in all_redpacket:
            id2all_redpacket[unicode(one_redpacket.id)] = one_redpacket

        all_control_data = redpacket_models.RedPacketAmountControl.objects()

        all_control_data_dic = {}
        for one_control in all_control_data:
            belong_to = one_control.belong_to
            red_packet_amount = one_control.red_packet_amount
            if belong_to in all_control_data_dic:
                all_control_data_dic[belong_to].append(red_packet_amount)
            else:
                all_control_data_dic[belong_to] =[red_packet_amount]

        all_control_remain_dic = {}
        for one_control in all_control_data_dic:
            one_amount_list = all_control_data_dic[one_control]
            if len(one_amount_list)==2:
                one_remain_amount = max(one_amount_list)-min(one_amount_list)-1
                all_control_remain_dic[one_control] = one_remain_amount
            else:
                print "[!!!!]Brocken Record:"+one_control


        print 'all:   length:%d'%(len(id2all_redpacket))
        print id2all_redpacket

        print 'all_control_data_dic   length:%d'%(len(all_control_data_dic))
        print all_control_data_dic

        print 'add_control_remain_dic   length:%d'%(len(all_control_remain_dic))
        print all_control_remain_dic

        Error_Msg = []
        for one_redpacket in all_control_remain_dic:
            belong_to = one_redpacket
            one_remain_amount = all_control_remain_dic[one_redpacket]

            if belong_to in id2all_redpacket:
                redpacket_record = id2all_redpacket[belong_to]
                print '-----Translation-------'
                print "belong_to:"
                print belong_to
                print "RedPacket_id:"
                print redpacket_record.id
                print "remain_amount:"
                print one_remain_amount
                redpacket_record.update(set__red_packet_remain_amount=one_remain_amount)
            else:
                err_msg = "[!!!] >>> Not Fund Redpacket:"+belong_to
                Error_Msg.append(err_msg)

        if Error_Msg:
            print '>>>>>>>>>>>> Error_Msg >>>>>>>>>'
            for msg in Error_Msg:
                print msg

