from django.conf.urls import patterns, url
from django.contrib import admin
from django.views.generic.list import ListView

from order.forms import InvoiceCreateView, InvoiceUpdateView
from order import views
from order.models import Invoice

admin.autodiscover()

urlpatterns = patterns('',

    # Invoice
    url(r'^invoice/$', ListView.as_view(model=Invoice,), name="invoice_list"),
    url(r'^invoice/new/$', InvoiceCreateView.as_view(), name="invoice_create"),
    url(r'^invoice/(?P<pk>\d+)/$', InvoiceUpdateView.as_view(), name="invoice_edit"),

    # JSON
    url(r'^json/product/(\d+)/$', views.json_product),
    url(r'^json/tax/(\d+)/$', views.json_tax),

)
