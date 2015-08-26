# -*- coding: utf-8 -*-
__STRIPPER_TAG__
{% for resource in resources %}
{% if resource.is_mobile_resource %}
import m_{{resource.lower_name}}
{% else %}
import {{resource.lower_name}}
{% endif %}
{% endfor %}