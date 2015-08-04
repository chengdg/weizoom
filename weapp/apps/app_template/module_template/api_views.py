# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.contrib.auth.decorators import login_required
__STRIPPER_TAG__
from core.jsonresponse import JsonResponse, create_response
from core.exceptionutil import unicode_full_stack
__STRIPPER_TAG__
from apps.register import api
from apps import viper_util
from {{app_name}}.models import *
from {{app_name}}.mysql_models import *
from {{app_name}} import settings as app_settings
__STRIPPER_TAG__
__STRIPPER_TAG__


{% for page in pages %}
{% if page.component.model.type == 'edit_page' %}
{{page.component.model.title|upper}}_TARGET_RESOURCE = "{{page.component.model.title}}"
__STRIPPER_TAG__
__STRIPPER_TAG__
{% endif %}
{% endfor %}


{% for page in pages %}

{% with page.component as resource %}


	{% if resource.model.type == 'edit_page' or resource.model.type == 'dialog_page' %}
	{% with resource.model.title as resource_name %}
	{% with resource.model.storeEngine as store_engine %}
@login_required
@api(resource='records', action='get')
def get_records(request):
	request.target_resource = {{page.component.model.title|upper}}_TARGET_RESOURCE
	{% if store_engine == 'mysql' %}
	request.model_class = {{resource.model.className}}
	{% endif %}
	return viper_util.get_records_by_query(request, settings)
	{% endwith %}
	{% endwith %}
	{% endif %}



{% endwith %}

{% endfor %}