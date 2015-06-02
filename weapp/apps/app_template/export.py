# -*- coding: utf-8 -*-

from apps.module_api import get_app_link_url
from apps import viper_util
import pagestore as pagestore_manager
from core.jsonresponse import create_response, JsonResponse
__STRIPPER_TAG__
__STRIPPER_TAG__

{% for page in pages %}
{% with page.component as resource %}

	{% if resource.model.type == 'edit_page' %}
def __get_{{resource.model.title}}_targets(request, ret_link_targets):
	pagestore = pagestore_manager.get_pagestore('mongo')
	project_id = 'apps:{{app_name}}:0'
	workspace_id = 'apps:{{app_name}}' #用于ProjectMiddleware进行project识别
	page_id = 'apps:{{app_name}}:{{resource.model.module}}:{{resource.model.title}}'
	_, records = pagestore.get_records(request.user.id, project_id, page_id)
__STRIPPER_TAG__
	pages = []
__STRIPPER_TAG__
	for record in records:
		pages.append(
			{
				'text': record['model'].get('name', 'id:'+record['id']),
				'value': get_app_link_url(request, '{{app_name}}', '{{resource.model.module}}', '{{resource.model.title}}', 'get', 'workspace_id='+workspace_id+'&record_id='+record['id'])
			}
		)
__STRIPPER_TAG__
	return ret_link_targets.append({
		'name': u'{{page.component.model.entityName}}',
		'data': pages
	})
__STRIPPER_TAG__
__STRIPPER_TAG__
	{% endif %}

{% endwith %}
{% endfor %}

########################################################################
# get_link_targets: 获取可链接的目标
########################################################################
def get_link_targets(request):
	ret_link_targets = []
{% for page in pages %}
{% with page.component as resource %}
	{% if resource.model.type == 'edit_page' %}
	__get_{{resource.model.title}}_targets(request, ret_link_targets)
	{% endif %}
{% endwith %}
{% endfor %}
__STRIPPER_TAG__
	response = create_response(200)
	response.data = ret_link_targets
__STRIPPER_TAG__
	return response.get_response()
