# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from weapp import views as weizoom
from account import views as account_view
from account import accounts_landing_views
from mall import home_views as mall_views
#from weixin import views as weixin_view
from termite.workbench import jqm_views as termite_jqm_views

from pay.weixin.simulator import views as pay_simulator_views

from django.contrib import admin
admin.autodiscover()

from core.restful_url import restful_url, restful_url2

# from admin.sites import site
# site = admin_sites.AdminSite()

#import admin as loc_admin
#from weixin import sinulator_views as sinulator_views

urlpatterns = patterns('',

	(r'^$', account_view.index),
	(r'^captcha/', include('captcha.urls')),

	(r'^login/', accounts_landing_views.login),
	(r'^logout/', account_view.logout),
	(r'^loading/', account_view.show_loading_page),

	(r'^touch/', account_view.show_touch_page),

	(r'^m/weizoom/about/(\d+)/$', weizoom.about_us),
	url(r'^m/tools/', include('tools.mobile_urls')),

	url(r'^weixin/dev/', include('weixin.urls')),
	url(r'^weixin/', include('weixin.urls')),
	
	url(r'^new_weixin/', restful_url2('new_weixin')),
	url(r'^termite2/', restful_url2('termite2')),

	#url(r'^new_mall/', restful_url2('new_mall')), # for exercises

	url(r'^account/', include('account.urls')),
	url(r'^simulator/', include('simulator.urls')),
	url(r'^watchdog/', include('watchdog.urls')),
	url(r'^operation/', include('operation.urls')),
	url(r'^market_tools/', include('market_tools.urls')),
	url(r'^prize/', include('market_tools.prize.urls')),
	url(r'^tools/', include('tools.urls')),
	url(r'^modules/', include('modules.urls')),

	url(r'^webapp/', include('webapp.urls')),
	url(r'^product/', include('product.urls')),
	url(r'^termite/', include('termite.urls')),
	#url(r'^shop/', include('webapp.modules.shop.urls')),

	url(r'^mall/', mall_views.get_outline),
	url(r'^mall2/', restful_url2('mall2')),
	url(r'^mall_promotion/', restful_url('mall_promotion')),
	url(r'^auth/', restful_url('auth')),
	url(r'^cms/', include('webapp.modules.cms.urls')),
	url(r'^user_center/', include('webapp.modules.user_center.urls')),
	url(r'^help/', include('help_system.urls')),

	(r'^alipay/([^/]+)/([^/]+)/([^/]+)/(\d+)/(\d+)/$', termite_jqm_views.show_alipay_callback_page),
	(r'^tenpay/([^/]+)/([^/]+)/([^/]+)/(\d+)/(\d+)/$', termite_jqm_views.show_tenpay_callback_page),
	(r'^wxpay/([^/]+)/([^/]+)/([^/]+)/(\d+)/(\d+)/$', termite_jqm_views.show_wxpay_callback_page),

	#url(r'^webapp/wxpay/', include('wxpay.urls')),
	url(r'^webapp/wxpay/', include('pay.weixin.urls')),
	url(r'^webapp/alipay/', include('pay.ali.urls')),

	url(r'^notice/', include('notice.urls')),

	url(r'^mockapi/', include('mockapi.urls')),
	url(r'^example/', include('example.urls')),
	url(r'^apps/', include('apps.urls')),

	url(r'^ft/', include('order.urls')),

	#定制化app，之后会清除
	url(r'^apps/shengjing/', include('apps.customerized_apps.shengjing.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mobile_app/', include('mobile_app.urls')),
    url(r'^erp/', include('erp.urls')),
    url(r'^pay/', include('pay.urls')),

    url(r'^member/', restful_url('member')),
    url(r'^messages/', restful_url('message')),

    #微信支付模拟api
    url(r'^sns/oauth2/access_token', pay_simulator_views.access_token),
    url(r'^pay/unifiedorder', pay_simulator_views.pay_unifiedorder),
    url(r'^card/', restful_url('card')),

    url(r'^stats/', restful_url2('stats')),
    # WGlass用的接口
    url(r'^wapi/', restful_url2('wapi')),
    
	url(r'^cloud_housekeeper/', restful_url2('cloud_housekeeper')),
)

urlpatterns += staticfiles_urlpatterns()

handler404 = 'account.views.show_error_page'
handler500 = 'account.views.show_error_page'
