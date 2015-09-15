# -*- coding: utf-8 -*-

#import json

#from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

#from datetime import datetime, timedelta

from core import emotion, resource, paginator
from core.jsonresponse import create_response, JsonResponse
from core.dateutil import get_datetime_before_by_hour, get_datetime_from_timestamp, get_timestamp_from_datetime
#from core.exceptionutil import unicode_full_stack

from weixin.mp_decorators import mp_required
from weixin.user.module_api import get_mp_head_img, get_mp_nick_name
from weixin2 import export
from weixin2.models import *

from modules.member.models import *
from account.social_account.models import SocialAccount

COUNT_PER_PAGE = 20
FIRST_NAV = export.MESSAGE_FIRST_NAV
DATETIME_BEFORE_HOURS = 48

class RealtimeMessagesDetail(resource.Resource):
    """
    实时消息详情
    """
    app = 'new_weixin'
    resource = 'realtime_messages_detail'

    @login_required
    def get(request):
        """
        获取实时消息页面
        """
        session_id = request.GET.get('session_id', '')
        try:
            could_replied = int(request.GET.get('replied', 0))
        except:
            could_replied = 0

        try:
            session = Session.objects.get(id=session_id)
            session.unread_count = 0
            session.save()
            if 'replied' not in request.GET:
                member_latest_created_at = get_datetime_from_timestamp(int(session.member_latest_created_at))
                datetime_before = get_datetime_before_by_hour(DATETIME_BEFORE_HOURS)
                if member_latest_created_at <= datetime_before:
                    could_replied = 0
                else:
                    could_replied = 1
                webapp_id = request.user_profile.webapp_id
                member = get_social_member(webapp_id, session.member_user_username)
                if not member.is_subscribed:
                    could_replied = 0
        except:
            session = None


        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_message_second_navs(request),
            'second_nav_name': export.MESSAGE_REALTIME_MESSAGE_NAV,
            'session_id': session_id,
            'could_replied': could_replied,
            'session':session
        })

        return render_to_response('weixin/message/realtime_messages_detail.html', c)

    @login_required
    @mp_required
    def api_get(request):
        """
        获取实时消息详情集合json数据
        """
        #获取当前页数
        cur_page = int(request.GET.get('page', '1'))
        #获取每页个数
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        #过滤条件
        session_id = request.GET.get('session_id', '')
        replied = int(request.GET.get('replied', 0))

        pageinfo, realtime_messages, member = get_messages(request.user, request.user_profile, session_id, replied, cur_page, count_per_page, request.META['QUERY_STRING'])

        response = create_response(200)
        response.data = {
            'items': realtime_messages,
            'pageinfo': paginator.to_dict(pageinfo),
            'session_id': session_id,
            'member': member
        }

        return response.get_response()

    @login_required
    def api_post(request):
        """
        修改用户基本资料操作
        """
        response = create_response(200)
        try:
            if 'member_id' in request.POST:
                member_id = request.POST['member_id']
                if 'category_id' in request.POST:
                    category_id = request.POST['category_id']
                    member_categories = FanHasCategory.objects.filter(fan_id=member_id)
                    if len(member_categories) > 0:
                        member_category = member_categories[0]
                    else:
                        member_category = FanHasCategory()
                        member_category.fan_id = member_id
                    member_category.category_id = category_id
                    member_category.save()
                else:
                    member= Member.objects.get(id=member_id)
                    if 'integral' in request.POST:
                        integral = request.POST['integral']
                        member.integral = integral
                    if 'grade_id' in request.POST:
                        grade_id = request.POST['grade_id']
                        member.grade_id = grade_id
                    member.save()
            elif 'member_info_id' in request.POST:
                member_info_id = request.POST['member_info_id']
                member_info = MemberInfo.objects.get(id=member_info_id)
                if 'sex' in request.POST:
                    sex = request.POST['sex']
                    member_info.sex = sex
                if 'remark_name' in request.POST:
                    remark_name = request.POST['remark_name']
                    member_info.name = remark_name
                member_info.save()
        except:
            response = create_response(500)
            response.errMsg = u'修改用户基本资料失败'

        return response.get_response()


def get_social_member(webapp_id, username):
    member = {}
    #会员相关信息
    try:
        accounts = SocialAccount.objects.filter(webapp_id=webapp_id, openid=username)
        member_has_accounts = MemberHasSocialAccount.objects.filter(webapp_id=webapp_id, account=accounts[0])
        social_member = Member.objects.get(id=member_has_accounts[0].member_id)
        try:
            social_member_info = MemberInfo.objects.get(member=social_member)
        except:
            social_member_info = MemberInfo.objects.create(
                member = social_member,
                name = ''
            )
        member['member_info_id'] = social_member_info.id
        member['remark_name'] = social_member_info.name
        member['sex'] = social_member_info.sex
        member['phone'] = social_member_info.phone_number

        fan_has_categories = FanHasCategory.objects.filter(fan=social_member)
        categories = FanCategory.objects.filter(webapp_id=webapp_id)

        member_categories = []
        member_category = {}
        member_category['id'] = -1
        member_category['name'] = u'请选择分组'
        member_categories.append(member_category)
        for category in categories:
            member_category = {}
            member_category['id'] = category.id
            member_category['name'] = category.name
            member_categories.append(member_category)

        member['categories'] = member_categories
        if len(fan_has_categories) > 0:
            member['category_id'] = fan_has_categories[0].category_id

        grades = MemberGrade.objects.filter(webapp_id=webapp_id)
        member_grades = []
        member_grade = {}
        member_grade['id'] = -1
        member_grade['name'] = u'请选择等级'
        member_grades.append(member_grade)
        for grade in grades:
            member_grade = {}
            member_grade['id'] = grade.id
            member_grade['name'] = grade.name
            member_grades.append(member_grade)
        member['grades'] = member_grades
        member['grade_id'] = social_member.grade_id

        member['id'] = social_member.id

        member['location'] = ''
        if social_member.country:
            member['location'] = social_member.country
        if social_member.province:
            member['location'] += ' ' + social_member.province
        if social_member.city:
            member['location'] += ' ' + social_member.city
        if member['location']:
            member['location'] = member['location'].strip()
        member['integral'] = social_member.integral

        member['follow_created_at'] = social_member.created_at.strftime('%Y-%m-%d %H:%M:%S')
        member['last_buy_created_at'] = social_member.last_pay_time.strftime('%Y-%m-%d %H:%M:%S')
        member['buy_times'] = social_member.pay_times
        member['average_price'] = social_member.unit_price
        member['total_price'] = social_member.pay_money
        member['openid'] = username
        member['is_subscribed'] = social_member.is_subscribed
    except:
        pass

    return member


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


def get_collect_message_dict(session_message_ids):
    collect_messages = CollectMessage.objects.filter(message_id__in=session_message_ids)
    message2collect = {}
    for collect_message in collect_messages:
        message_id = collect_message.message_id
        if message2collect.has_key(message_id):
            return
        message2collect[message_id] = collect_message

    return message2collect


#获取微信message
def get_messages(user, user_profile, session_id, replied, cur_page, count, query_string=None):
    mpuser = get_system_user_binded_mpuser(user)
    if mpuser is None:
        return []

    messages = Message.objects.filter(mpuser=mpuser, session=session_id).order_by('-weixin_created_at', '-id')
    pageinfo, messages = paginator.paginate(messages, cur_page, count, query_string=query_string)

    weixin_user_usernames = []
    for message in messages:
        weixin_user_usernames.append(message.from_weixin_user_username)
        weixin_user_usernames.append(message.to_weixin_user_username)
        break
    weixin_users = WeixinUser.objects.filter(username__in=weixin_user_usernames)
    username2weixin_user = dict([(u.username, u) for u in weixin_users])

    #会员相关信息
    webapp_id = user_profile.webapp_id
    username2weixin_account, account2member, id2member = get_social_member_dict(webapp_id, weixin_user_usernames)

    datetime_before = get_datetime_before_by_hour(DATETIME_BEFORE_HOURS)

    items = []
    message_ids = []
    sender_username = None
    name = None
    for message in messages:
        weixin_user = username2weixin_user[message.from_weixin_user_username]
        one_message = {}
        one_message['id'] = message.id
        one_message['session_id'] = message.session_id
        one_message['message_id'] = message.id
        one_message['sender_username'] = weixin_user.username
        if not sender_username:
            if message.is_reply:
                one_weixin_user = username2weixin_user[message.to_weixin_user_username]
                sender_username = one_weixin_user.username
                name = one_weixin_user.nickname_for_html
            else:
                sender_username = weixin_user.username
                name = weixin_user.nickname_for_html
        one_message['name'] = weixin_user.nickname_for_html
        if message.is_reply:
            head_img = get_mp_head_img(user.id)
            mp_username = get_mp_nick_name(user.id)
            one_message['mp_username'] = mp_username
            if head_img:
                one_message['user_icon'] = head_img
            else:
                one_message['user_icon'] = DEFAULT_ICON

        else:
            if weixin_user.weixin_user_icon:
                one_message['user_icon'] = weixin_user.weixin_user_icon if len(weixin_user.weixin_user_icon.strip()) > 0 else DEFAULT_ICON
            else:
                one_message['user_icon'] =  DEFAULT_ICON

        one_message['text'] = emotion.new_change_emotion_to_img(message.content)
        from_index = one_message['text'].find('<a href=')
        if from_index > -1:
            from_text = one_message['text'][0:from_index]

            middle_index = one_message['text'][from_index:].find('>')
            remain_text = one_message['text'][from_index:middle_index] + ' target="_blank"' + one_message['text'][middle_index:]

            one_message['text'] = from_text + remain_text
        try:
            one_message['created_at'] = message.weixin_created_at.strftime('%Y-%m-%d %H:%M:%S')
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

        message_ids.append(message.id)

        items.append(one_message)

        try:
            account = username2weixin_account[webapp_id + '_' + weixin_user.username]
            member_id = account2member[account.id]
            member = id2member[member_id]
            if member:
                one_message['member_id'] = member.id
        except:
            one_message['member_id'] = ''

    #会员相关信息
    webapp_id = user_profile.webapp_id
    member = get_social_member(webapp_id, sender_username)
    member['name'] = name
    member['could_replied'] = replied

    member_info = None
    if member and member.has_key('id'):
        member_id =  member['id']
        from modules.member.module_api import get_member_info_by
        member_info = get_member_info_by(member_id)
    member["member_info"] = member_info


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

        try:
            msginfo = MessageRemarkMessage.objects.filter(status=1).all()
            for msg in msginfo:
                if message_id == msg.message_id:
                    one_message['remark'] = msg.message_remark
        except:
            one_message['remark'] = False

    return pageinfo, items, member