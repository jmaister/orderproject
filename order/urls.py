from django.conf.urls.defaults import patterns, url
from order import views


urlpatterns = patterns('',
    # json
    url(r'^json/producto/(\d+)/$', views.json_producto),
    url(r'^json/iva/(\d+)/$', views.json_iva),
    
    url(r'^print_order/(\d+)/$', views.print_order),

    
    #url(r'factura/$', FacturaCreate.as_view(), name='factura_add'),
    #url(r'factura/add/$', views.FacturaCreateView.as_view(), name='factura_add'),
    #url(r'factura/(?P<pk>\d+)/$', FacturaUpdateView.as_view(), name='factura_update'),
    #url(r'factura/(?P<pk>\d+)/$', login_required(views.factura_update), name='factura_update'),

)
