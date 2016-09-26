# -*- coding: utf-8 -*-
import json
import os
import re
import pymongo
from bson.objectid import ObjectId

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template
from django.template import Context, RequestContext

from termite import pagestore as pagestore_manager
from apps.customerized_apps.survey import models as app_models
from webapp import models as webapp_models
from core.exceptionutil import unicode_full_stack

type2template = {}

STRIPPER_ENABLED =  getattr(settings, 'STRIPPER_ENABLED', True)
STRIPPER_TAG = getattr(settings, 'STRIPPER_TAG', '__STRIPPER_TAG__')
DELETE_TAG = ''
FIND_START_BLANK_LINE = r'^(\s*)\n'
DELETE_START_BLANK_LINE = ''
FIND_BLANK_LINE = r'\n(\s*)\n'
DELETE_BLANK_LINE = '\n'

class Command(BaseCommand):
    help = ''
    args = ''

    def handle(self, *args, **options):
        """
        处理线上调研活动历史数据
        """
        print 'update survey history data start...'
        old_surveies = app_models.survey.objects()
        record_id2related_page_id = {str(survey.id): str(survey.related_page_id) for survey in old_surveies}
        related_page_ids = [str(survey.related_page_id) for survey in old_surveies]
        related_page_ids_object = [ObjectId(survey.related_page_id) for survey in old_surveies]
        record_ids = [str(survey.id) for survey in old_surveies]
        old_survey_participances = app_models.surveyParticipance.objects(belong_to__in=record_ids)
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
            db_market_app_data.survey_survey.remove({'is_old': True})
            db_market_app_data.page_html.remove({'is_old': True, 'related_page_id': {'$in': related_page_ids}})
            db_market_app_data.survey_survey_participance.remove({'is_old': True})

            #复制termite里的page到market_app_page
            db_termite.market_app_page.remove({})
            for page in db_termite.page.find({'_id': {'$in': related_page_ids_object}}):
                # 更新market_app_page里description中静态资源地址
                description = page['component']['components'][0]['model']['description']
                page['component']['components'][0]['model']['description'] = description.replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                db_termite.market_app_page.insert(page)

            #然后将老数据写入新数据库
            for survey in old_surveies:
                related_page_id = survey.related_page_id
                page = pagestore.get_page(related_page_id, 1)
                page_details = page['component']['components'][0]['model']
                description = page_details['description']
                description = description.replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                db_market_app_data.survey_survey.insert({
                    'owner_id': survey.owner_id,
                    'name': survey.name,
                    'start_time': survey.start_time,
                    'end_time': survey.end_time,
                    'status': survey.status,
                    'participant_count': survey.participant_count,
                    'tag_id': survey.tag_id,
                    'related_page_id': survey.related_page_id,
                    'created_at': survey.created_at,
                    'subtitle': page_details['subtitle'],
                    'description': description,
                    'prize': page_details['prize'],
                    'permission': page_details['permission'],
                    'is_old': True
                })

                project_id = 'new_app:survey:%s' % related_page_id
                html = create_page(project_id).replace('xa-submitTermite', 'xa-submitWepage')

                html = html.replace('/static/', 'http://' + settings.DOMAIN + '/static/')

                db_market_app_data.page_html.insert({
                    'related_page_id': related_page_id,
                    'html': html,
                    'is_old': True
                })

            #构造调研活动related_page_id与活动id映射
            related_page_id2record_id = {str(survey['related_page_id']): str(survey['_id']) for survey in db_market_app_data.survey_survey.find({'is_old': True})}
            for par in old_survey_participances:
                related_page_id = record_id2related_page_id[str(par.belong_to)]
                termite_data = par.termite_data
                for key, value in termite_data.items():
                    if value['type'] == 'appkit.uploadimg' and value['value']:
                        img_list = []
                        for img in value['value']:
                            if img:
                                if 'http://' not in img:
                                    img = img.replace('/static/', 'http://' + settings.DOMAIN + '/static/')
                                img_list.append(img)
                        termite_data[key]['value'] = img_list

                db_market_app_data.survey_survey_participance.insert({
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

        print 'update survey history data end...'

########################################################################
#
########################################################################
def create_page(project_id):
    project, page = __preprocess_page(project_id)
    # 将page的class放入request，解决design page下无法为data-role=page设置class的问题
    # TODO: 优化解决方案
    # request.page_model = page['component']['model']
    html = create_mobile_page_html_content(page, page['component'], project)

    return html

def __preprocess_page(project_id):
    display_info = __get_display_info(project_id)
    project = display_info['project']
    page = display_info['page']

    #填充page.component
    page_component = page['component']
    if not 'components' in page_component:
        page_component['components'] = []

    return project, page

def __get_display_info(project_id):
    pagestore = pagestore_manager.get_pagestore('mongo')

    project = None
    is_app_project = False
    app_name = ''
    if project_id.startswith('new_app:'):
        _, app_name, project_id = project_id.split(':')
        is_app_project = True
    else:
        project_id = 0

    if is_app_project:
        project = webapp_models.Project()
        project.id = project_id
        project.type = 'appkit'

    page_id = 1
    page = pagestore.get_page(project_id, page_id)

    if page_id != 'preview':
        try:
            #使用project中的site_title作为真正的site_title
            #因为在page列表页面直接更新page site_title时是不会更新mongo中page数据中的site_title的
            page['component']['model']['site_title'] = project.site_title
        except:
            pass

    display_info = {
        'project': project,
        'page_id': page_id,
        'page': page
    }

    return display_info

def create_mobile_page_html_content(page, page_component, project=None):
    if settings.DEBUG:
        __load_templates()
    else:
        if len(type2template) == 0:
            __load_templates()

    htmls = []
    htmls.append(__render_component(page, page_component, project))

    return '\n'.join(htmls)


#################################################################################
# __load_templates: 加载components的template
#################################################################################
def __load_templates():
    type2template.clear()
    components_home_dir = settings.COMPONENTS_DIR
    print 'components_home_dir: ', components_home_dir
    for components_dir in os.listdir(components_home_dir):
        component_category = components_dir
        components_dir = os.path.join(components_home_dir, components_dir)
        if not os.path.isdir(components_dir):
            continue
        for file_name in os.listdir(components_dir):
            component_dir = os.path.join(components_dir, file_name)
            if not os.path.isdir(component_dir):
                continue

            __load_template(component_dir, component_category)

    type2template['unknown'] = get_template('component/common/common.html')

#################################################################################
# __load_template: 加载component dir下的template
#################################################################################
def __load_template(component_dir, component_category):
    component_name = os.path.basename(component_dir)
    template_path = os.path.join(component_dir, '%s.html' % component_name)
    if os.path.isfile(template_path):
        template_path = template_path.split('/app/')[-1]
        if settings.DEBUG:
            #print 'load... ', template_path
            pass
        template = get_template(template_path)
    else:
        print '[WARN]: no template file - ', os.path.join(component_dir, '%s.html' % component_name)
        template = None

    for file_name in os.listdir(component_dir):
        if file_name.endswith('.js'):
            file_path = os.path.join(component_dir, file_name)
            component_type = __extract_component_type(file_path)
            if component_type:
                type = '%s.%s' % (component_category, component_type)
                type2template[type] = template


#################################################################################
# __extract_component_type: 从f中抽取component type
#################################################################################
def __extract_component_type(file_path):
    #print 'extract component type from ', file_path
    component_type = None
    src_file = open(file_path, 'rb')
    should_capture_type = False
    for line in src_file:
        line = line.strip()
        if 'W.component.Component.extend' in line:
            should_capture_type = True
        if should_capture_type and line.startswith('type:'):
            beg = line.find("'")
            if beg != -1:
                end = line.find("'", beg+1)
            else:
                beg = line.find('"')
                if beg == -1:
                    print '[ERROR]: no W.component.register in ', file_path
                else:
                    end = line.find('"', beg+1)

            component_type = line[beg+1:end]
            #only process first type line
            break
    src_file.close()

    return component_type


# ===============================================================================
# create_mobile_page : 创建移动页面
# ===============================================================================
def __render_component(page, component, project):
    # 获取所有sub component的html片段
    sub_components = component.get('components', [])
    component['sub_component_count'] = len(sub_components)
    sub_components.sort(lambda x, y: cmp(x['model']['index'], y['model']['index']))
    for sub_component in sub_components:
        if not sub_component.get('__is_valid', True):
            sub_component['html'] = ''
            continue

        sub_component['parent_component'] = component
        sub_component['html'] = __render_component(page, sub_component, project)
        # 将sub_component的信息放入component中
        sub_component_type = sub_component['type'].replace('.', '')

        # 替换 链接地址
        sub_component['html'] = sub_component['html'].replace('./?', '/workbench/jqm/preview/?')
        if not sub_component_type in component:
            component[sub_component_type] = sub_component

    # 渲染component自身
    context = Context({
        'page': page,
        'component': component,
        'project': project,
        'project_id': project.id,
        'in_design_mode': True,
        'in_preview_mode': False,
        'in_production_mode': False,
    })

    component_category = project.type
    template = __get_template(component_category, component)
    content = strip_lines(template.render(context))

    return content

#################################################################################
# __get_template: 获得component对应的template
#################################################################################
def __get_template(component_category, component):
    component_type = '%s.%s' % (component_category, component['type'])
    template = type2template.get(component_type, None)
    if not template:
        template = type2template['unknown']

    #if 'common.html' in template.name:
    #	print 'use template(%s) for component(%s) [!]' % (template.name, component_type)
    #else:
    #	print 'use template(%s) for component(%s)' % (template.name, component_type)
    return template

'''
strip lines
'''
def strip_lines(content):
    if not STRIPPER_ENABLED:
        return content

    # Checks if the content type is allowed
    allowed = True

    # If the content type is not allowed, untag and return
    if not allowed:
        content = content.replace(STRIPPER_TAG, DELETE_TAG)
        return content

    # Suppress a blank line at the beginning of the document
    content = re.sub(FIND_START_BLANK_LINE, DELETE_START_BLANK_LINE, content)
    # Suppress blank lines
    content = re.sub(FIND_BLANK_LINE, DELETE_BLANK_LINE, content)
    # Delete STRIPPER_TAG
    # response.content = re.sub(FIND_TAG, DELETE_TAG, response.content)
    content = content.replace(STRIPPER_TAG, DELETE_TAG)
    return content