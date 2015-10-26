# -*- coding: utf-8 -*-

import re
from weixin2.models import *
from core.jsonresponse import create_response
from core import emotion
import json
from modules.member.models import *
from utils.json_util import string_json

def package_rule(rule, should_change_emotion=False):
    """
    封装rule为json response
    """
    response = create_response(200)
    response.data = dict()
    response.data['id'] = rule.id
    response.data['material_id'] = rule.material_id
    response.data['type'] = rule.type
    response.data['patterns'] = rule.patterns
    if should_change_emotion:
        response.data['answer'] = emotion.change_emotion_to_img(rule.answer)
    else:
        response.data['answer'] = rule.answer

    return response.get_response()

def get_newses(newses):
    newses_object = []
    news_count = len(newses)
    for news in newses:
        one_news = {}
        one_news['id'] = news.id
        one_news['title'] = string_json(news.title)
        one_news['display_index'] = news.display_index
        one_news['type'] = 'news'
        if news_count > 0:
            one_news['text'] = string_json(news.text.encode("utf-8"))
        one_news['date'] = news.created_at.strftime('%m月%d日').strip('0')
        one_news['url'] = news.url
        one_news['pic_url'] = news.pic_url
        one_news['summary'] = string_json(news.summary)
        if news.display_index == 1:
            one_news['metadata'] = {'autoSelect':'true'}
        else:
            one_news['metadata'] = {}
        newses_object.append(one_news)
    return newses_object

#@login_required
def check_duplicate_patterns(request):
    """
    检查pattern是否有重复
    """
    patterns = request.POST['patterns']
    ignore_rule_id = request.POST.get('id', None)
    has_duplicate, duplicate_patterns = has_duplicate_pattern(request.manager, patterns, ignore_rule_id)

    if has_duplicate:
        response = create_response(601)
        response.errMsg = u'下列关键词已经存在: %s' % duplicate_patterns[0]
        return response.get_response()
    else:
        return create_response(200).get_response()

def get_member_groups(webapp_id):
    groups = []
    member_tags = MemberTag.get_member_tags(webapp_id)
    for member_tag in member_tags:
        group_id2name = {}
        group_id2name['id'] = member_tag.id
        group_id2name['name'] = member_tag.name
        groups.append(group_id2name)
    return groups

def get_fans_groups(webapp_id):
    groups = []
    fan_categorys = FanCategory.get_fan_categorys(webapp_id)
    for fan_category in fan_categorys:
        group_id2name = {}
        group_id2name['id'] = fan_category.id
        group_id2name['name'] = fan_category.name
        groups.append(group_id2name)
    return groups

def is_valid_time(time_str):
    """
    校验时间格式是否正确，23:59
    """
    if time_str and  len(time_str) == 5:
        (hour, minute) = time_str.split(':')
        if hour and minute:
            if len(hour) == 2 and len(minute) == 2:
                try:
                    hour = int(hour)
                    minute = int(minute)
                    if hour >= 0 and hour <= 23 and minute >= 0 and minute <= 59:
                        return True
                except Exception, e:
                    return False
    return False


#处理消息中的特殊字符
def translate_special_characters(message_text):
    a_pattern = re.compile(r'<a.+?href=.+?>.+?</a>')
    all_a_html = a_pattern.findall(message_text)
    
    for html in all_a_html:
        message_text = message_text.replace(html, "%s")
    message_text = message_text.replace('<', "&lt;")
    message_text = message_text.replace('>', "&gt;")
    if all_a_html:
        message_text = message_text % tuple(all_a_html)
    return message_text