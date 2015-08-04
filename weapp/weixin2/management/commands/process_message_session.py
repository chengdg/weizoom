# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from core.dateutil import get_timestamp_from_datetime

from weixin2.models import Session, Message, WeixinUser

class Command(BaseCommand):
    help = "process message session"
    args = ''
    
    def handle(self, **options):
        sessions = Session.objects.filter(Q(member_latest_created_at=None) | Q(member_latest_created_at=''))
        print 'total message session ', len(sessions)
        
        process_count = 0
        for session in sessions:
            messages = Message.objects.filter(session=session, is_reply=False).order_by('-id')
            try:
                message = messages[0]
                session.member_user_username = message.from_weixin_user_username
                session.member_message_id = message.id
                session.member_latest_content = message.content
                session.member_latest_created_at = get_timestamp_from_datetime(message.weixin_created_at)
                session.save()
                
                process_count += 1
                if process_count % 100 == 0:
                    print 'process message session ', process_count
            except:
                pass
            
        print 'process message session ', process_count