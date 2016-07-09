# -*- coding: utf-8 -*-

import json
from datetime import datetime
import datetime as dt_datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from termite import pagestore as pagestore_manager
from django.template.loader import render_to_string


from core import resource
from core.jsonresponse import create_response

import models as app_models
from termite2 import pagecreater
from utils.cache_util import GET_CACHE, SET_CACHE

class exMSign(resource.Resource):
    app = 'apps/exsign'
    resource = 'm_exsign'

    def get(request):
        """
        响应GET
        """
        p_id = request.GET.get('id','id')

        isPC = request.GET.get('isPC',0)
        webapp_owner_id = request.GET.get('webapp_owner_id', None)
        prize_info = {}


        if 'new_app' in p_id:
            project_id = p_id
            activity_status = u"未开始"
            record_id = 0
            exsign_description = ""
            record = None
        else:
            if not webapp_owner_id:
                c = RequestContext(request, {
                        'is_deleted_data': True
                    })
                return render_to_response('exsign/templates/webapp/m_exsign.html', c)

            cache_key = 'apps_exsign_%s_html' % webapp_owner_id
            if not isPC:
                #从redis缓存获取静态页面
                cache_data = GET_CACHE(cache_key)
                if cache_data:
                    #存入全局变量
                    print 'redis---return'
                    return HttpResponse(cache_data)

            record = app_models.exSign.objects(owner_id=webapp_owner_id)
            if record.count() > 0:
                record = record[0]
                prize_settings = record.prize_settings

                pagestore = pagestore_manager.get_pagestore('mongo')
                page = pagestore.get_page(record.related_page_id, 1)
                exsign_description = page['component']['components'][0]['model']['description']

                activity_status = record.status_text

                project_id = 'new_app:exsign:%s' % record.related_page_id
                record_id = record.id

                prize_rules = {}

                for name in sorted(map(lambda x: (int(x),x), prize_settings.keys())):
                    setting = prize_settings[name[1]]
                    name = name[0]
                    if setting['integral']:
                        p_integral = setting['integral']
                    else:
                        p_integral = 0
                    p_coupon = []
                    if setting['coupon']:
                        for coupon in setting['coupon']:
                            p_coupon.append({
                                "coupon_name": coupon['name']
                            })
                    prize_rules[name] = {'integral': p_integral,'coupon': p_coupon}

                prize_info = {
                    'prize_rules':prize_rules
                }

            else:
                c = RequestContext(request, {
                    'is_deleted_data': True
                })
                return render_to_response('exsign/templates/webapp/m_exsign.html', c)

        request.GET._mutable = True
        request.GET.update({"project_id": project_id})
        request.GET._mutable = False
        html = pagecreater.create_page(request, return_html_snippet=True)
        c = RequestContext(request, {
            'record_id': record_id,
            'activity_status': activity_status,
            'page_title': u"签到",
            'page_html_content': html,
            'app_name': "sign",
            'resource': "sign",
            'hide_non_member_cover': True, #非会员也可使用该页面
            'isPC': False if not isPC else True,
            'prize_info': json.dumps(prize_info),
            'share_page_title': record.share['desc'] if record else '',
            'share_img_url': record.share['img'] if record else '',
            'share_page_desc': u"签到",
            'exsign_description': exsign_description,

        })
        response = render_to_string('exsign/templates/webapp/m_exsign.html', c)
        if not isPC:
            SET_CACHE(cache_key, response)
        return HttpResponse(response)

    def api_get(request):

        p_id = request.GET.get('id',None)

        webapp_owner_id = request.GET.get('webapp_owner_id', None)
        member_info = {}
        prize_info = {}

        member = request.member

        response = create_response(500)
        if not p_id or not member:
            response.errMsg = u"活动信息出错"
            return response.get_response()

        isMember = member.is_subscribed
        member_id = member.id
        record = app_models.exSign.objects(owner_id=webapp_owner_id)
        status = u'未签到'
        activity_status =  u'未开始'
        if record.count()<=0:
            response.errMsg = "is_deleted"
            return response.get_response()

        if record.count() > 0:
            record = record[0]
            prize_settings = record.prize_settings

            activity_status = record.status_text

            record_id = record.id

            #检查当前用户签到情况
            cur_daily_prize = prize_settings['0']
            temp_daily_coupon = []
            if cur_daily_prize["coupon"]:
                for c in cur_daily_prize["coupon"]:
                    if request.member.grade_id == int(c["grade_id"]):
                        temp_daily_coupon.append({
                            "name": c["name"]
                        })
                    elif int(c["grade_id"]) == 0:
                        temp_daily_coupon.append({
                            "name": c["name"]
                         })

            daily_prize = {
                "integral": cur_daily_prize["integral"],
                "coupon": temp_daily_coupon
            }
            serial_prize = {}
            next_serial_prize = {}
            prize_rules = {}

            #设置的最大连续签到天数
            max_setting_count = sorted(map(lambda x: int(x), prize_settings.keys()), reverse=True)[0]

            member_info = {
                'user_name': member.username_for_html if member.username_for_html else u'未知',
                'user_icon': member.user_icon if member.user_icon else '/static/img/user-1.jpg',
                'user_integral': member.integral
            }

            signers = app_models.exSignParticipance.objects(belong_to=str(record_id), member_id=member_id)
            participance_data_count = signers.count()
            signer = signers[0] if participance_data_count > 0 else None

            if signer:
                #检查是否已签到
                nowDate = datetime.now().strftime('%Y-%m-%d')
                if signer.latest_date:
                    latest_sign_date = signer.latest_date.strftime('%Y-%m-%d')
                    #首先检查是否断掉了连续签到条件，状态重置serial_count为1
                    if latest_sign_date == (datetime.now() - dt_datetime.timedelta(days=1)).strftime('%Y-%m-%d'):
                        temp_serial_count = signer.serial_count
                    else:
                        temp_serial_count = 0
                    #如果已达到最大设置天数则重置签到
                    if (signer.serial_count == max_setting_count and latest_sign_date != nowDate) or (max_setting_count!=0 and signer.serial_count > max_setting_count):
                        temp_serial_count = 0
                        signer.update(set__serial_count=0, set__latest_date=None)
                        signer.reload()
                else:
                    temp_serial_count = 0
                latest_sign_date = signer.latest_date
                if not latest_sign_date:
                     pass
                elif (latest_sign_date.strftime('%Y-%m-%d') == nowDate and signer.serial_count != 0) or (latest_sign_date.strftime('%Y-%m-%d') == nowDate and temp_serial_count != 0):
                    status = u'已签到'
                    for name in sorted(map(lambda x: (int(x),x), prize_settings.keys())):
                        setting = prize_settings[name[1]]
                        temp_serial_coupon = {
                            "integral": setting["integral"],
                            "coupon": []
                        }
                        for c in setting["coupon"]:
                            if request.member.grade_id == int(c["grade_id"]):
                                temp_serial_coupon["coupon"].append({
                                    "name": c["name"]
                                })
                            elif int(c["grade_id"]) == 0:
                                temp_serial_coupon["coupon"].append({
                                    "name": c["name"]
                                })
                        name = name[0]
                        if int(name) > signer.serial_count:
                            next_serial_prize = {
                                'count': int(name),
                                'prize': temp_serial_coupon
                            }
                            break
                elif temp_serial_count >=1:
                    flag = False
                    for name in sorted(map(lambda x: (int(x),x), prize_settings.keys())):
                        setting = prize_settings[name[1]]
                        temp_serial_coupon = {
                            "integral": setting["integral"],
                            "coupon": []
                        }
                        for c in setting["coupon"]:
                            if request.member.grade_id == int(c["grade_id"]):
                                temp_serial_coupon["coupon"].append({
                                    "name": c["name"]
                                })
                            elif int(c["grade_id"]) == 0:
                                 temp_serial_coupon["coupon"].append({
                                    "name": c["name"]
                                })

                        name = int(name[0])
                        if flag or name>signer.serial_count + 1:
                            next_serial_prize = {
                                'count': name,
                                'prize': temp_serial_coupon
                            }
                            break
                        if name == signer.serial_count + 1:
                            serial_prize = {
                                'count': name,
                                'prize': temp_serial_coupon
                            }
                            flag = True

            prize_info = {
                'serial_count': signer.serial_count if signer else 0,
                'daily_prize': daily_prize,
                'serial_prize': serial_prize,
                'next_serial_prize': next_serial_prize,
                'prize_rules':prize_rules
            }

        response = create_response(200)
        response.data = {
            "status":status,
            "activity_status": activity_status,
            "isMember":isMember,
            "member_info":member_info,
            "prize_info":prize_info
        }

        return response.get_response()
