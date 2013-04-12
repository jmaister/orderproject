from base.admin import EntityAdmin
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from order.models import Producto, Factura, FacturaItem, Cliente, Empresa
from order.order_admin.forms import UserAdminAuthenticationForm

class OrderAdminSite(AdminSite):
    
    login_form = UserAdminAuthenticationForm
    
    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active

order_admin_site = OrderAdminSite(name="ordersite")


class EmpresaEntity(EntityAdmin):
    exclude = ('empresa',)

    def get_empresa(self, request):
        return request.user.get_profile().empresa

    def save_form(self, request, form, change):
        form.instance.empresa = request.user.get_profile().empresa
        return EntityAdmin.save_form(self, request, form, change)
    
    def queryset(self, request):
        return EntityAdmin.queryset(self, request).filter(empresa__id=request.user.id)

class EmpresaAdmin(EntityAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def queryset(self, request):
        return EntityAdmin.queryset(self, request).filter(id=request.user.id)


class FacturaItemInline(admin.TabularInline):
    model = FacturaItem
    readonly_fields = ('tipo_iva', 'base', 'total_iva', 'total')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "producto":
            kwargs["queryset"] = Producto.objects.filter(empresa=request.user.get_profile().empresa)
        return admin.TabularInline.formfield_for_foreignkey(self, db_field, request=request, **kwargs)

class FacturaAdmin(EmpresaEntity):
    # FORM
    exclude = ('empresa',)
    readonly_fields = ('codigo', 'base', 'total_iva', 'total')
    inlines = [
        FacturaItemInline,
    ]

    def response_add(self, request, obj, post_url_continue='../%s/'):
        obj = self.recalculate(obj)
        return EmpresaEntity.response_add(self, request, obj, post_url_continue=post_url_continue)
    
    def response_change(self, request, obj):
        obj = self.recalculate(obj)
        return EmpresaEntity.response_change(self, request, obj)
    
    def recalculate(self, obj):
        obj.calculate()
        if obj.codigo is None or obj.codigo == '':
            num = 1
            try:
                codigo = Factura.objects.filter(empresa=obj.empresa).exclude(pk=obj.pk).order_by('-id')[0].codigo
                partes = codigo.split('-')
                num = int(partes[1]) + 1
            except:
                pass
                
            obj.codigo = '%d-%03d' % (obj.fecha.year, num)
        obj.save()
        return obj

    # LIST
    list_filter = ('fecha', )
    list_display = ('codigo', 'fecha', 'cliente', 'total', 'pagado', 'print_link',)
    
    def print_link(self, obj):
        return '<a target="top" href="%s/%d">Imprimir</a>' % ('/order/print_order', obj.id,)
    print_link.allow_tags = True
    print_link.short_description = 'Imprimir'
    
    def pagado(self, obj):
        if obj.fecha_pagado is not None:
            return '<i class="icon-ok"></i>'
        return '<i class="icon-remove"></i>'
    pagado.allow_tags = True
    pagado.short_description = 'Pagado'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cliente":
            kwargs["queryset"] = Cliente.objects.filter(empresa=self.get_empresa(request))
        return super(EmpresaEntity, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # Javascript form
    class Media:
        js = ('http://code.jquery.com/jquery-1.9.1.min.js', '/static/order/js/order.js', '/static/order/js/jshashtable-2.1.js','/static/order/js/jquery.numberformatter-1.2.3.js',)
        css = {
               all: ('/static/order/css/order.css',)
        }


class ClienteAdmin(EmpresaEntity):
    pass

class ProductoAdmin(EmpresaEntity):
    pass

order_admin_site.register(Empresa, EmpresaAdmin)
order_admin_site.register(Cliente, ClienteAdmin)
order_admin_site.register(Producto, ProductoAdmin)
order_admin_site.register(Factura, FacturaAdmin)
