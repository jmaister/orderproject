from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from order import views
from order.forms import InvoiceCreateView, InvoiceUpdateView
from order.models import Invoice, Product, Client, Tax


admin.autodiscover()

urlpatterns = patterns('',

    # Invoice
    url(r'^invoice/$', login_required(ListView.as_view(model=Invoice,)), name="invoice_list"),
    url(r'^invoice/new/$', login_required(InvoiceCreateView.as_view()), name="invoice_create"),
    url(r'^invoice/(?P<pk>\d+)/$', login_required(InvoiceUpdateView.as_view()), name="invoice_edit"),

    # Product
    url(r'^product/$', login_required(ListView.as_view(model=Product,)), name="product_list"),
    url(r'^product/new/$', login_required(CreateView.as_view(model=Product)), name="product_create"),
    url(r'^product/(?P<pk>\d+)/$', login_required(UpdateView.as_view(model=Product)), name="product_edit"),

    # Client
    url(r'^client/$', login_required(ListView.as_view(model=Client,)), name="client_list"),
    url(r'^client/new/$', login_required(CreateView.as_view(model=Client)), name="client_create"),
    url(r'^client/(?P<pk>\d+)/$', login_required(UpdateView.as_view(model=Client)), name="client_edit"),
    
    # Tax
    url(r'^tax/$', login_required(ListView.as_view(model=Tax,)), name="tax_list"),
    url(r'^tax/new/$', login_required(CreateView.as_view(model=Tax)), name="tax_create"),
    url(r'^tax/(?P<pk>\d+)/$', login_required(UpdateView.as_view(model=Tax)), name="tax_edit"),

    # JSON
    url(r'^json/product/(\d+)/$', views.json_product),
    url(r'^json/tax/(\d+)/$', views.json_tax),

)
