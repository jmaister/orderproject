from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from order.views import json_product, print_order, json_iva

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OrderProject.views.home', name='home'),
    # url(r'^OrderProject/', include('OrderProject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),

    # json
    url(r'^json/product/$', json_product),
    url(r'^json/iva/(\d+)/$', json_iva),
    
    url(r'^print_order/(\d+)/$', print_order),
    
)
