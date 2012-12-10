from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from order.views import json_producto, print_order, json_iva

urlpatterns = patterns('',
    # json
    url(r'^json/producto/(\d+)/$', json_producto),
    url(r'^json/iva/(\d+)/$', json_iva),
    
    url(r'^print_order/(\d+)/$', print_order),

)
