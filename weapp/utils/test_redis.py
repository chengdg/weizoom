__author__ = 'Administrator'
from mall import module_api as mall_api
from mall import models as mall_models
from utils import cache_util

products = mall_api.get_products_in_webapp(webapp_id, is_access_weizoom_mall, webapp_owner_id, 0)

categories = mall_models.ProductCategory.objects.filter(owner_id=webapp_owner_id)