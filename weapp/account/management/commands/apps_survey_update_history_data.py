# -*- coding: utf-8 -*-
import json
import os
import re
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template
from django.template import Context, RequestContext

# from termite.core import stripper
from termite import pagestore as pagestore_manager
from apps.customerized_apps.survey import models as app_models
from apps.models import PageHtml
from webapp import models as webapp_models
from account.models import UserProfile
from cache import webapp_cache

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
        surveies = app_models.survey.objects()
        record_id2related_page_id = {str(survey.id): str(survey.related_page_id) for survey in surveies}
        record_ids = [str(survey.id) for survey in surveies]
        survey_participances = app_models.surveyParticipance.objects(belong_to__in=record_ids)
        pagestore = pagestore_manager.get_pagestore('mongo')
        try:
            for survey in surveies:
                related_page_id = survey.related_page_id
                page = pagestore.get_page(related_page_id, 1)
                page_details = page['component']['components'][0]['model']
                survey.subtitle = page_details['subtitle']
                survey.description = page_details['description']
                survey.prize = page_details['prize']
                survey.permission = page_details['permission']
                survey.save()

                #
                project_id = 'new_app:survey:%s' % related_page_id
                html = create_page(project_id)
                PageHtml.objects.create(
                    related_page_id = related_page_id,
                    html = html
                )
            for par in survey_participances:
                par.related_page_id = record_id2related_page_id[str(par.belong_to)]
                par.save()
        except Exception,e:
            print 'update survey history data error!!!!!!!!'
            print e
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


def process_item_group_data(request, component):
    if hasattr(request, 'manager'):
        woid = request.manager.id
        user_profile = request.manager.get_profile()
    else:
        woid = request.user.id
        user_profile = request.user_profile

    if user_profile.manager_id != woid and user_profile.manager_id > 2:
        user_profile = UserProfile.objects.filter(user_id=user_profile.manager_id).first()

    # woid = request.user_profile.user_id
    if len(component['components']) == 0 and request.in_design_mode:
        # 空商品，需要显示占位结果
        component['_has_data'] = True
        return

    model_product_ids = []
    product_ids = set()
    for sub_component in component['components']:
        sub_component['runtime_data'] = {}
        target = sub_component['model']['target']
        if target:
            try:
                data = json.loads(target)
                product_id = int(data['meta']['id'])
                product_ids.add(product_id)
                sub_component['__is_valid'] = True
                sub_component['runtime_data']['product_id'] = product_id
                model_product_ids.append(product_id)
            except:
                # TODO: 记录watchdog
                sub_component['__is_valid'] = False
        else:
            sub_component['__is_valid'] = False

    if request.in_design_mode == False:
        # 非编辑模式，显示空的div占位符
        component['_has_data'] = False
        component_model = component['model']
        component_model['items'] = model_product_ids
        component[
            'empty_placeholder'] = "<div data-ui-role='async-component' data-type='{}' data-model='{}'></div>".format(
            component['type'], json.dumps(component_model))
        return

    # products = [product for product in mall_models.Product.objects.filter(id__in=product_ids) if product.shelve_type == mall_models.PRODUCT_SHELVE_TYPE_ON]
    valid_product_count = 0
    if len(product_ids) == 0:
        component['_has_data'] = False
    else:
        component['_has_data'] = True
        products = []
        category, cached_products = webapp_cache.get_webapp_products_new(user_profile, False, 0)

        for product in cached_products:
            if product.id in product_ids:
                products.append(product)
        id2product = dict([(product.id, product) for product in products])

        for sub_component in component['components']:
            if not sub_component['__is_valid']:
                continue

            runtime_data = sub_component['runtime_data']
            product_id = runtime_data['product_id']
            product = id2product.get(product_id, None)
            if not product:
                sub_component['__is_valid'] = False
                continue

            valid_product_count = valid_product_count + 1
            runtime_data['product'] = {
                "id": product.id,
                "name": product.name,
                "thumbnails_url": product.thumbnails_url,
                "display_price": product.display_price,
                "is_member_product": product.is_member_product,
                "promotion_js": json.dumps(product.promotion) if product.promotion else ""
            }

    if valid_product_count == 0 and request.in_design_mode:
        valid_product_count = -1
    component['valid_product_count'] = valid_product_count

def _set_empty_product_list(request, component):
    if request.in_design_mode:
        # 分类信息为空，构造占位数据
        count = 4
        product_datas = []
        for i in range(count):
            product_datas.append({
                "id": -1,
                "name": "",
            })
        component['runtime_data'] = {
            "products": product_datas
        }
    else:
        component['_has_data'] = False


def process_item_list_data(request, component):
    if hasattr(request, 'manager'):
        print 2222222
        woid = request.manager.id
        user_profile = request.manager.get_profile()
    else:
        woid = request.user.id
        user_profile = request.user_profile

    component['_has_data'] = True
    count = int(component['model']['count'])

    category = component["model"].get("category", '')
    if len(category) == 0:
        _set_empty_product_list(request, component)
        return

    category = json.loads(category)
    if len(category) == 0:
        _set_empty_product_list(request, component)
        return

    category_id = category[0]["id"]
    categories = mall_models.ProductCategory.objects.filter(id=category_id)
    if categories.count() == 0:
        # 分类已被删除，直接返回
        _set_empty_product_list(request, component)
        return

    if user_profile.manager_id != woid and user_profile.manager_id > 2:
        user_profile = UserProfile.objects.filter(user_id=user_profile.manager_id).first()

    category, products = webapp_cache.get_webapp_products_new(user_profile, False, int(category_id))
    # product_ids = set([r.product_id for r in mall_models.CategoryHasProduct.objects.filter(category_id=category_id)])
    # product_ids.sort()
    # products = [product for product in mall_models.Product.objects.filter(id__in=product_ids) if product.shelve_type == mall_models.PRODUCT_SHELVE_TYPE_ON]

    # 当count == -1时显示全部，大于-1时，取相应的product
    if count > -1:
        products = products[:count]

    if len(products) == 0:
        _set_empty_product_list(request, component)

    else:
        # webapp_owner_id = products[0].owner_id
        # mall_models.Product.fill_details(webapp_owner_id, products, {'with_product_model':True})
        # products = _update_product_display_count_by_type(request, products, component)
        product_datas = []
        for product in products:
            product_datas.append({
                "id": product.id,
                "name": product.name,
                "thumbnails_url": product.thumbnails_url,
                "display_price": product.display_price,
                "url": './?module=mall&model=product&action=get&rid=%d&webapp_owner_id=%d&workspace_id=mall' % (
                product.id, user_profile.user_id),
                "is_member_product": product.is_member_product,
                "promotion_js": json.dumps(product.promotion) if product.promotion else ""
            })

        component['runtime_data'] = {
            "products": product_datas
        }

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
