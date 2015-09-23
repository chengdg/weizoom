# -*- coding: utf-8 -*-

import re
import json
import weixin2.module_api as weixin_module_api

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import F

from datetime import datetime, timedelta

from core import emotion, resource, paginator
from core.jsonresponse import create_response, JsonResponse
from core.dateutil import get_datetime_before_by_hour, get_datetime_from_timestamp, get_timestamp_from_datetime
from core.wxapi.weixin_api import WeixinApiError
from core.wxapi import get_weixin_api, weixin_error_codes
from core.wxapi.custom_message import TextCustomMessage, NewsCustomMessage
from core.exceptionutil import unicode_full_stack

from weixin.mp_decorators import mp_required
from weixin.user.module_api import get_mp_head_img
from weixin2 import export
from weixin2.models import *

from modules.member.models import MemberHasSocialAccount, Member,MemberHasTag
from account.social_account.models import SocialAccount
from watchdog.utils import *

from utils.string_util import byte_to_hex

COUNT_PER_PAGE = 20
FIRST_NAV = export.MESSAGE_FIRST_NAV
DATETIME_BEFORE_HOURS = 48

STATUS_ALL = -1
STATUS_UNREAD = 0
STATUS_UNREPLY = 1
STATUS_REMARK = 2
STATUS_COLLECT = 3

class SignUnreadMessages(resource.Resource):
    """
    标记消息为已读
    """
    app = 'new_weixin'
    resource = 'sign_unread_message'

    @login_required
    def api_post(request):
        try:
            response = create_response(200)
            session_ids = json.loads(request.POST['sessionIds'])
            Session.objects.filter(id__in=session_ids).update(unread_count=0)
            return response.get_response()
        except:
            response = create_response(500)
            return response.get_response()

class RealtimeMessages(resource.Resource):
    """
    实时消息
    """
    app = 'new_weixin'
    resource = 'realtime_messages'

    @login_required
    @mp_required
    def get(request):
        """
                        获取实时消息页面
        """
        status = request.GET.get('status', -1)
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_message_second_navs(request),
            'second_nav_name': export.MESSAGE_REALTIME_MESSAGE_NAV,
            'status': status
        })

        return render_to_response('weixin/message/realtime_messages.html', c)

    @login_required
    @mp_required
    def api_get(request):
        """
                        获取实时消息集合json数据
        """

        #获取当前页数
        cur_page = int(request.GET.get('page', '1'))
        #获取每页个数
        count_per_page = int(request.GET.get('count', COUNT_PER_PAGE))
        #过滤条件
        filter_value = request.GET.get('filter_value', '')
        #时间条件
        date_interval = request.GET.get('date_interval', '')

        is_debug = (request.GET.get('dbg', '0') == '1')

        #解析过滤条件
        #消息状态
        status = STATUS_ALL
        #消息内容
        content = ''
        nick_name = ''
        grade_id = '-1'
        tag_id = '-1'
        filter_value_items = filter_value.split('|')
        for filter_value_item in filter_value_items:
            filter_items = filter_value_item.split(':')
            try:
                if filter_items[0].find('status') >= 0:
                    status = int(filter_items[1])
                if filter_items[0].find('content') >= 0:
                    content = filter_items[1]
                if filter_items[0].find('tag_id') >= 0:
                    tag_id = filter_items[1]
                if filter_items[0].find('grade_id') >= 0:
                    grade_id = filter_items[1]
                if filter_items[0].find('name') >= 0:
                    nick_name = filter_items[1]
            except:
                pass
        #解析时间条件
        start_time = ''
        end_time = ''
        if date_interval:
            try:
                date_items = date_interval.split('|')
                start_time = date_items[0].strip()
                end_time = date_items[1].strip()
            except:
                pass
        if content or (start_time and end_time) or nick_name or grade_id != '-1' or tag_id != '-1':
            status = STATUS_ALL
            pageinfo, realtime_messages = get_messages_from_messages(request.user, request.user_profile, cur_page, count_per_page, content, start_time, end_time, filter_value_items,request.META['QUERY_STRING'])
        elif status == STATUS_COLLECT:
            pageinfo, realtime_messages = get_messages_from_collected(request.user, request.user_profile, cur_page, count_per_page, request.META['QUERY_STRING'])
        elif status == STATUS_REMARK:
            pageinfo, realtime_messages = get_messages_from_remarked(request.user, request.user_profile, cur_page, count_per_page, request.META['QUERY_STRING'])
        else:
            pageinfo, realtime_messages = get_sessions(request.user, request.user_profile, cur_page, count_per_page, status, request.META['QUERY_STRING'])

        response = create_response(200)
        response.data = {
            'items': realtime_messages,
            'pageinfo': paginator.to_dict(pageinfo),
            'status': status,
            'query_string': request.META['QUERY_STRING']
        }

        return response.get_response()

    @login_required
    @mp_required
    def api_put(request):
        """
                        回复实时消息
        """
        pattern = re.compile(r'_src=".*"')
        answer = request.POST['answer']
        src_str = pattern.findall(answer, re.S)
        if src_str:
            answer = answer.replace(src_str[0], "")
        material_id = request.POST['material_id']
        type = request.POST['type']
        openid_sendto = request.POST['openid']

        mpuser = get_system_user_binded_mpuser(request.user)
        if mpuser is None:
            response = create_response(500)
            response.errMsg = u'请先进行公众号的绑定'
        else:
            #进行实际消息的发送
            try:
                sessions = get_weixinuser_sessions(openid_sendto)
                if openid_sendto and sessions.count() > 0:
                    session = sessions[0]
                    is_active =  True if datetime.now() < session.latest_contact_created_at + timedelta(hours=DATETIME_BEFORE_HOURS) and datetime.now() > session.latest_contact_created_at else False
                    if is_active:
                        if type == u'text':
                            #文本消息
                            custom_message = TextCustomMessage(answer)
                        else:
                            #图文消息
                            newses = weixin_module_api.get_material_news_info(material_id)
                            articles = weixin_module_api.get_articles_object(newses)
                            custom_message = NewsCustomMessage(articles)

                        _send_custom_message(mpuser, openid_sendto, custom_message)
                        response = create_response(200)
                    else:
                        response = create_response(501)
                        response.errMsg = u'互动已经超时'
                else:
                    response = create_response(501)
                    response.errMsg = u'互动已经超时'
            except WeixinApiError, error:
                response = create_response(500)
                error_code = error.error_response.errcode
                response.errMsg = weixin_error_codes.code2msg.get(error_code, error.error_response.errmsg)
                response.innerErrMsg = error.error_response.detail
            except:
                response = create_response(500)
                response.errMsg = u'发送消息失败'
                response.innerErrMsg = unicode_full_stack()

        error_msg = u'weixin reply, stage:[weixin reply], result:\n{}'.format(response.get_response())
        watchdog_info(error_msg)

        return response.get_response()

    @login_required
    @mp_required
    def api_post(request):
        """
                        回复实时消息后回写操作
        """
        session_id = request.POST['session_id']
        pattern = re.compile(r'_src=".*"')
        content = request.POST['content']
        src_str = pattern.findall(content, re.S)
        if src_str:
            content = content.replace(src_str[0], "")
        receiver_username = request.POST['receiver_username']
        material_id = request.POST['material_id']

        mpuser = get_system_user_binded_mpuser(request.user)
        if mpuser is None:
            response = create_response(500)
            response.errMsg = u'请先进行公众号的绑定'

        message = Message.objects.create(
            mpuser=mpuser,
            session_id=session_id,
            from_weixin_user_username=mpuser.username,
            to_weixin_user_username=receiver_username,
            content=content,
            material_id=material_id,
            is_reply=True
        )
        latest_contact_created_at = datetime.today()
        Session.objects.filter(id=session_id).update(latest_contact_content=content, latest_contact_created_at=datetime.today(),
                                                     is_latest_contact_by_viper=True, unread_count=0, is_replied=True, message_id=message.id)
        response = create_response(200)
        data = {}
        data['created_at'] = latest_contact_created_at.strftime('%Y-%m-%d %H:%M:%S')

        data['text'] = emotion.new_change_emotion_to_img(content)
        from_index = data['text'].find('<a href=')
        if from_index > -1:
            from_text = data['text'][0:from_index]

            middle_index = data['text'][from_index:].find('>')
            remain_text = data['text'][from_index:middle_index] + ' target="_blank"' + data['text'][middle_index:]

            data['text'] = from_text + remain_text

        if material_id and int(material_id) > 0:
            newses = list(News.objects.filter(material_id=message.material_id))
            if len(newses) > 0:
                news = newses[0]
                news_title = news.title
                if len(news_title) > 21:
                    news_title = news.title[0:18] + '...'

                data['news_title'] = news_title
            data['is_news_type'] = True
        else:
            data['news_title'] = ''
        data['material_id'] = message.material_id

        response.data = data

        return response.get_response()


def get_social_member_dict(webapp_id, weixin_user_usernames):
    #会员相关信息
    accounts = SocialAccount.objects.filter(webapp_id=webapp_id, openid__in=weixin_user_usernames)
    username2weixin_account = dict([(a.webapp_id + '_' + a.openid, a) for a in accounts])
    member_has_accounts = MemberHasSocialAccount.objects.filter(account__in=accounts)
    member_ids = []
    account2member = {}
    for member_has_account in member_has_accounts:
        account_id = member_has_account.account_id
        member_id = member_has_account.member_id
        member_ids.append(member_id)
        if account2member.has_key(account_id):
           continue
        account2member[account_id] = member_id
    members = Member.objects.filter(id__in=member_ids)
    id2member = {}
    for member in members:
        if id2member.has_key(member.id):
            continue
        id2member[member.id] = member

    return username2weixin_account, account2member, id2member

def get_weixin_user_names_from(webapp_id, weixin_user_usernames, tag_id, grade_id, nick_name):
    accounts = SocialAccount.objects.filter(webapp_id=webapp_id, openid__in=weixin_user_usernames)
    username2weixin_account = dict([(a.webapp_id + '_' + a.openid, a) for a in accounts])
    filter_data = {}
    filter_data['webapp_id'] = webapp_id
    if accounts:
        filter_data['account__in'] = accounts

    if grade_id != '-1':
        filter_data['member__grade_id'] = grade_id
    if tag_id != '-1':
        member_ids = [member_tag.member_id for member_tag in MemberHasTag.objects.filter(member_tag_id=tag_id)]
        filter_data['member_id__in'] = member_ids
    if nick_name:
        query_hex = byte_to_hex(nick_name)
        filter_data['member__username_hexstr__icontains'] = query_hex

    member_has_accounts = MemberHasSocialAccount.objects.filter(**filter_data)
    now_weixin_user_usernames = [member_has_account.account.openid for member_has_account in member_has_accounts]
    return now_weixin_user_usernames

def get_collect_message_dict(session_message_ids):
    collect_messages = CollectMessage.objects.filter(message_id__in=session_message_ids)
    message2collect = {}
    for collect_message in collect_messages:
        message_id = collect_message.message_id
        if message2collect.has_key(message_id):
            return
        message2collect[message_id] = collect_message

    return message2collect

#获取微信session
def get_sessions(user, user_profile, cur_page, count, status=STATUS_ALL, query_string=None, is_debug=False):
    mpuser = get_system_user_binded_mpuser(user)
    if mpuser is None:
        return None, None

    if is_debug:
        sessions = Session.objects.select_related().filter(mpuser=mpuser)
    else:
        sessions = Session.objects.select_related().filter(mpuser=mpuser, is_show=True)

    #未读信息
    if status == STATUS_UNREAD:
        sessions = sessions.filter(unread_count__gt=0)
    #未回复
    datetime_before = get_datetime_before_by_hour(DATETIME_BEFORE_HOURS)
    if status == STATUS_UNREPLY:
        sessions = sessions.filter(latest_contact_created_at__gte=datetime_before, is_replied=False)

    sessions = sessions.order_by('-latest_contact_created_at')
    pageinfo, sessions = paginator.paginate(sessions, cur_page, count, query_string=query_string)

    weixin_user_usernames = [s.weixin_user_id for s in sessions]
    weixin_users = WeixinUser.objects.filter(username__in=weixin_user_usernames)
    username2weixin_user = dict([(u.username, u) for u in weixin_users])

    #会员相关信息
    webapp_id = user_profile.webapp_id
    username2weixin_account, account2member, id2member = get_social_member_dict(webapp_id, weixin_user_usernames)

    #备注相关信息
    msginfo = MessageRemarkMessage.objects.filter(owner = user, status = 1)
    msgid2remark = {}
    for msg in msginfo:
        msgid2remark[msg.message_id] = msg.message_remark

    items = []
    session_message_ids = []
    for session in sessions:
        weixin_user = username2weixin_user[session.weixin_user_id]
        one_session = {}
        one_session['id'] = session.id
        one_session['session_id'] = session.id
        one_session['message_id'] = session.message_id
        one_session['sender_username'] = weixin_user.username
        one_session['name'] = weixin_user.nickname_for_html
        if weixin_user.weixin_user_icon:
            one_session['user_icon'] = weixin_user.weixin_user_icon if len(weixin_user.weixin_user_icon.strip()) > 0 else DEFAULT_ICON
        else:
            one_session['user_icon'] =  DEFAULT_ICON
        one_session['text'] = emotion.new_change_emotion_to_img(session.latest_contact_content)
        from_index = one_session['text'].find('<a href=')
        if from_index > -1:
            from_text = one_session['text'][0:from_index]

            middle_index = one_session['text'][from_index:].find('>')
            remain_text = one_session['text'][from_index:middle_index] + ' target="_blank"' + one_session['text'][middle_index:]

            one_session['text'] = from_text + remain_text
        try:
            latest_contact_created_at = session.latest_contact_created_at
            one_session['created_at'] = latest_contact_created_at.strftime('%Y-%m-%d %H:%M:%S')
            if latest_contact_created_at <= datetime_before:
                one_session['could_replied'] = 0
            else:
                one_session['could_replied'] = 1
        except:
            print unicode_full_stack()
            one_session['created_at'] = ''
        one_session['unread_count'] = session.unread_count

        if session.message_id != 0:
            session_message_ids.append(session.message_id)

        try:
            reply_message = Message.objects.filter(session=session, is_reply=True).order_by('-id')[0]
            one_session['latest_reply_at'] = reply_message.weixin_created_at.strftime('%Y-%m-%d %H:%M:%S')
        except:
            one_session['latest_reply_at'] = ''

        try:
            account = username2weixin_account[webapp_id + '_' + weixin_user.username]
            member_id = account2member[account.id]
            member = id2member[member_id]
            if member:
                one_session['member_id'] = member.id
                one_session['is_subscribed'] = member.is_subscribed
                if not member.is_subscribed:
                    one_session['could_replied'] = 0
        except:
            one_session['member_id'] = ''

        items.append(one_session)
    #星标消息
    message2collect = get_collect_message_dict(session_message_ids)
    #消息类型
    messages = Message.objects.filter(id__in=session_message_ids)
    id2message = dict([(m.id, m) for m in messages])
    for one_session in items:
        session_message_id = one_session['message_id']
        try:
            if id2message.has_key(session_message_id):
                message = id2message[session_message_id]
                one_session['message_type'] = message.message_type
                one_session['pic_url'] = message.pic_url
                one_session['audio_url'] = message.audio_url

                if message.is_news_type:
                    newses = list(News.objects.filter(material_id=message.material_id))
                    if len(newses) > 0:
                        news = newses[0]
                        news_title = news.title
                        if len(news_title) > 21:
                            news_title = news.title[0:18] + '...'

                        one_session['news_title'] = news_title
                else:
                    one_session['news_title'] = ''
                one_session['is_news_type'] = message.is_news_type
                one_session['material_id'] = message.material_id
            else:
                one_session['message_type'] = 'text'
                one_session['pic_url'] = ''
                one_session['audio_url'] = ''
        except:
            one_session['message_type'] = 'text'
            one_session['pic_url'] = ''
            one_session['audio_url'] = ''

        try:
            if message2collect.has_key(session_message_id):
                one_session['is_collected'] = message2collect[session_message_id].status
            else:
                one_session['is_collected'] = False
        except:
            one_session['is_collected'] = False

        if msgid2remark.has_key(session_message_id):
            one_session['remark'] = msgid2remark[session_message_id]
        else:
            one_session['remark'] = ''

    return pageinfo, items


#根据weixin_message_message表获取微信信息
def get_messages_from_messages(user, user_profile, cur_page, count, content=None, start_time=None, end_time=None,  filter_items=None,query_string=None):
    mpuser = get_system_user_binded_mpuser(user)
    if mpuser is None:
        return []

    messages = Message.objects.filter(mpuser=mpuser)
    if content:
        messages = messages.filter(content__contains=content)
    if start_time and end_time:
        messages = messages.filter(weixin_created_at__gte=start_time, weixin_created_at__lte=end_time)
    messages = messages.filter(is_reply=False)
    messages =  get_message_detail_items(user, user_profile.webapp_id, messages, filter_items)
    pageinfo, messages = paginator.paginate(messages, cur_page, count, query_string=query_string)

    return pageinfo, messages


#更新weixin_collect_message表获取微信信息
def get_messages_from_collected(user, user_profile, cur_page, count, query_string=None):
    collected_ids = CollectMessage.get_message_ids(user)
    messages = Message.objects.filter(id__in=collected_ids)
    pageinfo, messages = paginator.paginate(messages, cur_page, count, query_string=query_string)

    return pageinfo, get_message_detail_items(user, user_profile.webapp_id, messages)


#更新weixin_collect_message表获取备注信息
def get_messages_from_remarked(user, user_profile, cur_page, count, query_string=None):
    collected_ids = MessageRemarkMessage.get_message_ids(user)
    messages = Message.objects.filter(id__in=collected_ids)
    pageinfo, messages = paginator.paginate(messages, cur_page, count, query_string=query_string)

    return pageinfo, get_message_detail_items(user, user_profile.webapp_id, messages)


#获取微信message
def get_message_detail_items(user, webapp_id, messages, filter_items=None):
    weixin_user_usernames = [m.from_weixin_user_username for m in messages]
    weixin_users = WeixinUser.objects.filter(username__in=weixin_user_usernames)
    username2weixin_user = dict([(u.username, u) for u in weixin_users])

    #会员相关信息
    username2weixin_account, account2member, id2member = get_social_member_dict(webapp_id, weixin_user_usernames)

    tag_id = '-1'
    grade_id = '-1'
    name = ''
    if filter_items:
        for filter_value_item in filter_items:
            filter_items = filter_value_item.split(':')
            try:
                if filter_items[0].find('tag_id') >= 0:
                    tag_id = filter_items[1]
                if filter_items[0].find('grade_id') >= 0:
                    grade_id = filter_items[1]
                if filter_items[0].find('name') >= 0:
                    name = filter_items[1]
            except:
                pass

    if tag_id != '-1' or grade_id != '-1' or name != '':
        weixin_user_usernames = get_weixin_user_names_from(webapp_id,weixin_user_usernames, tag_id, grade_id, name)
        messages = messages.filter(from_weixin_user_username__in=weixin_user_usernames)

    #备注相关信息
    msginfo = MessageRemarkMessage.objects.filter(owner = user, status = 1)
    msgid2remark = {}
    for msg in msginfo:
        msgid2remark[msg.message_id] = msg.message_remark

    datetime_before = get_datetime_before_by_hour(DATETIME_BEFORE_HOURS)

    items = []
    message_ids = []
    for message in messages:
        weixin_user = username2weixin_user[message.from_weixin_user_username]
        one_message = {}
        one_message['id'] = message.id
        one_message['session_id'] = message.session_id
        one_message['message_id'] = message.id
        one_message['sender_username'] = weixin_user.username
        one_message['name'] = weixin_user.nickname_for_html

        one_message['text'] = emotion.new_change_emotion_to_img(message.content)
        try:
            one_message['created_at'] = message.weixin_created_at.strftime('%Y-%m-%d %H:%M:%S')
            if message.weixin_created_at <= datetime_before:
                one_message['could_replied'] = 0
            else:
                one_message['could_replied'] = 1
        except:
            one_message['created_at'] = ''
        one_message['unread_count'] = 0

        try:
            one_message['message_type'] = message.message_type
            one_message['pic_url'] = message.pic_url
            one_message['audio_url'] = message.audio_url
        except:
            one_message['message_type'] = 'text'
            one_message['pic_url'] = ''
            one_message['audio_url'] = ''

        try:
            one_message['fast_reply'] = message.is_reply
        except:
            one_message['fast_reply'] = True

        if msgid2remark.has_key(message.id):
            one_message['remark'] = msgid2remark[message.id]
        else:
            one_message['remark'] = ''

        if message.is_news_type:
            newses = list(News.objects.filter(material_id=message.material_id))
            if len(newses) > 0:
                news = newses[0]
                news_title = news.title
                if len(news_title) > 21:
                    news_title = news.title[0:18] + '...'

                one_message['news_title'] = news_title
        else:
            one_message['news_title'] = ''
        one_message['is_news_type'] = message.is_news_type
        one_message['material_id'] = message.material_id

        try:
            reply_message = Message.objects.filter(session=message.session_id, is_reply=True).order_by('-id')[0]
            one_message['latest_reply_at'] = reply_message.weixin_created_at.strftime('%Y-%m-%d %H:%M:%S')

        except:
            one_message['latest_reply_at'] = ''

        message_ids.append(message.id)

        try:
            account = username2weixin_account[webapp_id + '_' + weixin_user.username]
            member_id = account2member[account.id]
            member = id2member[member_id]
            one_message['user_icon'] =  DEFAULT_ICON
            if member:
                one_message['member_id'] = member.id
                one_message['is_subscribed'] = member.is_subscribed
                one_message['user_icon'] =  member.user_icon
                if not member.is_subscribed:
                    one_message['could_replied'] = 0
        except:
            one_message['member_id'] = ''

        if message.is_reply:
            head_img = get_mp_head_img(user.id)
            if head_img:
                one_message['user_icon'] = head_img
            else:
                one_message['user_icon'] = DEFAULT_ICON

        items.append(one_message)

    #星标消息
    message2collect = get_collect_message_dict(message_ids)
    for one_message in items:
        message_id = one_message['id']
        try:
            if message2collect.has_key(message_id):
                one_message['is_collected'] = message2collect[message_id].status
            else:
                one_message['is_collected'] = False
        except:
            one_message['is_collected'] = False

    return items


#回复微信实时消息
def _send_custom_message(mpuser, send_to, custom_message):
    mpuser_access_token = get_mpuser_access_token_for(mpuser)
    wxapi = get_weixin_api(mpuser_access_token)
    wxapi.send_custom_msg(send_to, custom_message)