import inspect
from django.db.models import Model as _django_db_models_Model
from django.contrib import admin as _django_contrib_admin

_app_models = None
try:
    from . import models as _app_models
    for c in [ getattr(_app_models, k) for k in dir(_app_models) ]:
        if inspect.isclass(c) and issubclass(c, _django_db_models_Model):
            _django_contrib_admin.site.register(c)
except:
    pass
