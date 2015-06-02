# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date

from apps.customerized_apps.shengjing.models import *
from apps.customerized_apps.shengjing.crm_api.models import *

from django.db.models.loading import get_model
from django.db.models import Q
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_alert, watchdog_fatal

import crm_settings

#######################################################################
# getmodelfield: 获取model所有字段
#######################################################################
def getmodelfield(model):
    columns=[]
    for field in model._meta.fields:
        columns.append(field.column)
    return columns

#######################################################################
# get_account_attr_ids: 获取手机号获取客户附属表中的account_id
#######################################################################
def get_account_attr_ids(phone_number):
    account_ids = []
    account_ids = [account_attr.account_id for account_attr in CRMAccountAttr.objects.using(crm_settings.SHENGJINGD_DB).filter(acct_char14__icontains=phone_number)]
    return account_ids

#######################################################################
# get_userinfo_by_phone_number: 通过手机号，获取联系人资料
#######################################################################
def get_userinfo_by_phone_number(phone_number):
    account_ids = get_account_attr_ids(phone_number)
    contact_name = ''
    # 获取公司名、学员姓名
    contact_infos = get_contact_by_phone_number(phone_number)
    for contact_info in contact_infos:
        contact_name = contact_info[crm_settings.CONTACT_NAME]
        account_ids.append(contact_info[crm_settings.ACCOUNT_ID])

    accounts = CRMAccount.objects.using(crm_settings.SHENGJINGD_DB).filter(acct_int02=1004)\
        .filter(Q(account_mobile_phone__icontains=phone_number) | Q(account_id__in=account_ids))
    decision_maker = False
    companys = []
    # 判断是否为决策人、决策人姓名
    if accounts:
        decision_maker = True
        for account in accounts:
            companys.append(account.account_name)
            lader_name = accounts[0].acct_char01.strip()
            if len(lader_name) > 0:
                contact_name = lader_name

    # 获取公司名
    # if account_ids:
    #     # 1004 是已购池
    #     accounts = CRMAccount.objects.using(crm_settings.SHENGJINGD_DB).filter(account_id__in=account_ids, acct_int02=1004)

    # for account in accounts:
    #     companys.append(account.account_name)

    companys = list(set(companys))
    
    # 组织数据
    items = {}
    # 判断身份
    if companys:
        items[crm_settings.IDENTIFY] = STAFF
    else:
        # 如果没有获取到公司，可以认定为没有数据，返回空。
        return items
        # items[crm_settings.IDENTIFY] = OUTSIDER
    if decision_maker:
        items[crm_settings.IDENTIFY] = LEADER
    items[crm_settings.CONTACT_NAME] = contact_name
    items[crm_settings.COMPANYS] = companys
    items[crm_settings.PHONE] = phone_number

    return items


#######################################################################
# is_leader: 通过手机号与公司名判断是否为决策人
#######################################################################
def is_leader(phone_number, company):
    account_ids = get_account_attr_ids(phone_number)
    accounts = CRMAccount.objects.using(crm_settings.SHENGJINGD_DB).filter(account_id__in=account_ids, account_name=company)
    if accounts:
        return True
    accounts = CRMAccount.objects.using(crm_settings.SHENGJINGD_DB).filter(account_mobile_phone__icontains=phone_number, account_name=company)
    if accounts:
        return True
    return False


#######################################################################
# get_contact_by_phone_number: 通过手机号，获取所关联的学员名字、客户ID与角色
#######################################################################
def get_contact_by_phone_number(phone_number):
    account_ids = []
    if phone_number:
        try:
            contacts = CRMContact.objects.using(crm_settings.SHENGJINGD_DB).filter(Q(mobile__icontains=phone_number) | Q(cnct_char03__icontains=phone_number))
        except:
            return account_ids

        for contact in contacts:
            account_ids.append({
                crm_settings.CONTACT_NAME: contact.contact_name,
                crm_settings.ACCOUNT_ID: contact.account_id
                #crm_settings.ROLE: contact.cnct_int01
            })
        return account_ids
    else:
        return account_ids

#######################################################################
# get_account_ids_by_phone_number: 通过手机号，获取所关联的所有客户ID
#######################################################################
def get_account_ids_by_phone_number(phone_number):
    contact_infos = get_contact_by_phone_number(phone_number)
    account_ids = []
    for contact_info in contact_infos:
        account_ids.append(contact_info[crm_settings.ACCOUNT_ID])
    return account_ids


#######################################################################
# get_learning_plan: 根据状态（未开课，己开课，全部）获取学习计划数据
# status: 0：未开课、1：已开课、2：全部
#######################################################################
def get_learning_plan(phone_number, company, status=0):
    account_ids = get_account_ids_by_phone_number(phone_number)
    items = []
    try:
        account_ids = [account.account_id for account in CRMAccount.objects.using(SHENGJINGD_DB).filter(Q(account_mobile_phone__icontains=phone_number) | Q(account_id__in=account_ids), account_name=company)]
        learning_plans = CRMLearnplan.objects.using(SHENGJINGD_DB).filter(account_id__in=account_ids, learnplan_type=FORMAL_LEARNING_PLAN) # 只取正式计划
        if int(status) == 0:
            # 当选择未开课时，参课判定为已参加才显示
            learning_plans = learning_plans.filter(learnplan_int07=HAVING_JOINED)
        elif int(status) == 1: 
            # 当选择已开课时，签到人数大于0时才显示
            learning_plans = learning_plans.filter(learnplan_dec04__gt=0)
        else:
            pass
    except:
        return items
    jiaoxplan_ids = []
    jiaoxplanid2plan_count = {}
    jiaoxplanid2learnplanid = {}
    for plan in learning_plans:
        if plan.learnplan_refid02 not in jiaoxplanid2plan_count:
            # 存在一个客户选同一个教学计划多次，且其中一个学习计划签到人数为0的情况
            if int(status) != 0 and int(plan.learnplan_dec04) == 0:
                continue
            jiaoxplanid2plan_count[plan.learnplan_refid02] = plan.learnplan_dec04
            jiaoxplan_ids.append(plan.learnplan_refid02)
            jiaoxplanid2learnplanid[plan.learnplan_refid02] = plan.learnplan_id # 学习计划ID
        else:
            pass

    try:
        teachplans = CRMTeachplan.objects.using(SHENGJINGD_DB).filter(jiaoxplan_id__in=jiaoxplan_ids)
    except:
        return items
    # 根据status过滤； 
    today = date.today()
    if int(status) == 0:
        teachplans = teachplans.filter(jiaoxplan_date02__gt=today)
    elif int(status) == 1: 
        teachplans = teachplans.filter(jiaoxplan_date02__lt=today)
    else:
        pass
    
    for teachplan in teachplans:
        if teachplan.jiaoxplan_date01:
            # 如果有签到人员，增加签到人员列表。
            plan_count = int(jiaoxplanid2plan_count[teachplan.jiaoxplan_id])
            students = []
            # 在传入状态为2时，返回状态区分是否开课
            if int(status) == 2:
                if teachplan.jiaoxplan_date02 > today:
                    state = 0
                else:
                    state = 1
            else:
                state = int(status)
            # 在已开课与全部中过滤签到人数为0的学习计划，没有签到的不显示
            if state != 0:
                if plan_count == 0:
                    continue

            if int(jiaoxplanid2learnplanid[teachplan.jiaoxplan_id]) > 0:
                sgnin_ids = [ls.yckb_id for ls in CRMLearnplanSgnin.objects.using(SHENGJINGD_DB).filter(ref_1=jiaoxplanid2learnplanid[teachplan.jiaoxplan_id])]
                contact_ids = [sgnin.yckb_refid01 for sgnin in CRMSgnin.objects.using(SHENGJINGD_DB).filter(yckb_int03=1002,yckb_id__in=sgnin_ids)]
                contacts = CRMContact.objects.using(SHENGJINGD_DB).filter(contact_id__in=contact_ids)
                for contact in contacts:
                    students.append(contact.contact_name)

            items.append({
                'status': state,
                'id': int(teachplan.jiaoxplan_id),
                'course_name': teachplan.jiaoxplan_name,
                'curricula_time': teachplan.jiaoxplan_date01.strftime('%Y-%m-%d'),
                'stop_time': teachplan.jiaoxplan_date02.strftime('%Y-%m-%d'),
                'students': students,
                'plan_count': plan_count
            })
    if items:
        if int(status) == 1:
            items = sorted(items, key=lambda x:x['curricula_time'],reverse=True)
        else:
            items = sorted(items, key=lambda x:x['curricula_time'])
    return items

#######################################################################
# list_course: 获取课程列表
#######################################################################
def list_course(page=1, page_size=20, days=60):
    page = int(page)
    page_size = int(page_size)
    start_page = (page - 1) * page_size
    end_page = page * page_size
    items = []
    from datetime import timedelta, datetime
    try:
        today = datetime.today()
        if days == -1:
            teachplans = CRMTeachplan.objects.using(crm_settings.SHENGJINGD_DB).filter(jiaoxplan_date01__gt=today).order_by('jiaoxplan_date01')[start_page: end_page]
            page_count = CRMTeachplan.objects.using(crm_settings.SHENGJINGD_DB).filter(jiaoxplan_date01__gt=today).count()
        else:
            after_two_months = datetime.today() + timedelta(days=days)
            teachplans = CRMTeachplan.objects.using(crm_settings.SHENGJINGD_DB).filter(jiaoxplan_date01__lt=after_two_months, jiaoxplan_date01__gt=today).order_by('jiaoxplan_date01')[start_page: end_page]
            page_count = CRMTeachplan.objects.using(crm_settings.SHENGJINGD_DB).filter(jiaoxplan_date01__lt=after_two_months, jiaoxplan_date01__gt=today).count()
    except:
        return items, False
    if page_count > page * page_size:
        has_next = True
    else:
        has_next = False
    
    for teachplan in teachplans:
        if teachplan.jiaoxplan_date01 and teachplan.jiaoxplan_date02:
            items.append({
                'id': teachplan.jiaoxplan_id,
                'course_name': teachplan.jiaoxplan_name,
                'start_date': teachplan.jiaoxplan_date01.strftime('%Y-%m-%d'),
                'end_date': teachplan.jiaoxplan_date02.strftime('%Y-%m-%d'),
                'pic': '/static/...',
                'description': ''
            })

    return items, has_next

#######################################################################
# get_course: 获取课程详细信息
#######################################################################
def get_course(id):
    result = {}
    if int(id):
        try:
            teachplan = CRMTeachplan.objects.using(crm_settings.SHENGJINGD_DB).get(jiaoxplan_id=int(id))
        except:
            return result
        if teachplan.jiaoxplan_date01 and teachplan.jiaoxplan_date02:
            result['id'] =teachplan.jiaoxplan_id
            result['course_name'] = teachplan.jiaoxplan_name
            result['start_date'] = teachplan.jiaoxplan_date01.strftime('%Y-%m-%d')
            result['end_date']=  teachplan.jiaoxplan_date02.strftime('%Y-%m-%d')
            result['pic'] = '/static/...'
            result['content'] = u'暂无介绍内容。'

    return result


#######################################################################
# get_time_person_cards: 获取时间卡、人次卡信息
#######################################################################
def get_time_person_cards(phone_number, company, status=0):
    try:
        if not CRMAccount.has_account(phone_number, company):
            return None

        #1、根据公司信息和手机号获取到account_id
        account_ids = get_account_attr_ids(phone_number)
        crm_accounts = CRMAccount.objects.using(crm_settings.SHENGJINGD_DB).filter(Q(account_mobile_phone__icontains=phone_number) | Q(account_id__in=account_ids), account_name=company)
        if crm_accounts.count() == 0:
            fatal_message = u'账单(获取时间卡、人次卡信息),未获取到CRMAccount phone:{}; account_ids: {}, company:{}'.format(phone_number, account_ids, company)
            watchdog_fatal(fatal_message, user_id=211)
            return None
        crm_account = crm_accounts[0]

        #2、根据account_id获取到所有的订单
        crm_contracts = None
        if CRMContract.exist_office_order(crm_account.account_id):
            crm_contracts = CRMContract.objects.using(crm_settings.SHENGJINGD_DB).filter(account_id=crm_account.account_id, contract_type=OFFICIAL_CONTRACT, close_flag=0, is_deleted=0)
        else:
            fatal_message = u'账单(获取时间卡、人次卡信息),未获取到账单 phone:{}; account_id: {}, company:{}'.format(phone_number, crm_contract.account_id, company)
            watchdog_fatal(fatal_message, user_id=211)
            return None

        #对订单信息进行封装
        cards = []
        for crm_contract in crm_contracts:
            try:
                #对状态进行判断
                is_time_card = False
                card = {}
                if status == ALL_STATUS:
                    is_time_card, card = crm_contract.fill_order()
                else:                    
                    order_status = crm_contract.get_order_status()
                    if order_status == status:
                        is_time_card, card = crm_contract.fill_order()
                    else:
                        continue
                cards.append(card)
            except:
                alert_message = u'封装时间卡:contract_id {} 信息失败.\n couse: {}'.format(crm_contract.contract_id, unicode_full_stack())
                watchdog_alert(alert_message, user_id=211)

        print 'cards size: ', len(cards)
        if len(cards) > 0:
            cards = sorted(cards, cmp=lambda x, y: cmp(y['order_time'], x['order_time']))

        return cards
    except:
        raise ValueError, u'获取时间卡信息失败.\n couse: {}'.format(unicode_full_stack())

#######################################################################
# get_companys: 获取公司信息
#######################################################################
def get_companys(phone_number):
    items = []
    account_ids = get_account_ids_by_phone_number(phone_number)
    try:
        accounts = CRMAccount.objects.using(crm_settings.SHENGJINGD_DB).filter(account_id__in=account_ids)
    except:
        accounts = {}
    for account in accounts:
        items.append(account.account_name)

    return items