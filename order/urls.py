from django.conf.urls import patterns, url
from django.contrib import admin
from order.forms import InvoiceCreateView, InvoiceUpdateView

admin.autodiscover()

urlpatterns = patterns('',

    # Invoice
    url(r'^invoice/$', InvoiceCreateView.as_view(), name="invoice_create"),
    url(r'^invoice/(?P<pk>\d+)/$', InvoiceUpdateView.as_view(), name="invoice_edit"),

)
