from django.conf.urls import patterns, include, url
from django.contrib import admin
from order.order_admin.admin import order_admin_site
import order.urls
from orderproject.views import home

urlpatterns = patterns('',

    url(r'^$', home, name='home'),

    url(r'^order/', include(order.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^edit/', include(order_admin_site.urls)),
    
    #All Auth URLS
    url(r'^accounts/', include('allauth.urls')),

)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
