# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group, User
__STRIPPER_TAG__
__STRIPPER_TAG__


RESOUCE2MODEL = {}
__STRIPPER_TAG__

{% for model_class in model_classes %}
{{model_class}}
__STRIPPER_TAG__
__STRIPPER_TAG__
{% endfor %}