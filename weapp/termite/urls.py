from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'termite.views.home', name='home'),
    # url(r'^termite/', include('termite.foo.urls')),
    (r'^workbench/', include('workbench.urls')),
)