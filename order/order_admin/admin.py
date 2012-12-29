from base.admin import EntityAdmin
from django.contrib import admin
from django.contrib.admin.forms import ERROR_MESSAGE
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.fields import BooleanField
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy
from order.models import Producto, Factura, FacturaItem, Cliente, Iva, Empresa

## http://tryolabs.com/Blog/2012/06/18/django-administration-interface-non-staff-users/

class UserAdminAuthenticationForm(AuthenticationForm):
    """
    Same as Django's AdminAuthenticationForm but allows to login
    any user who is not staff.
    """
    this_is_the_login_form = BooleanField(widget=HiddenInput,
                                initial=1,
                                error_messages={'required': ugettext_lazy(
                                "Please log in again, because your session has"
                                " expired.")})
 
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE
         
        if username and password:
            self.user_cache = authenticate(username=username,
            password=password)
            if self.user_cache is None:
                if u'@' in username:
                    # Mistakenly entered e-mail address instead of username?
                    # Look it up.
                    try:
                        user = User.objects.get(email=username)
                    except (User.DoesNotExist, User.MultipleObjectsReturned):
                        # Nothing to do here, moving along.
                        pass
                    else:
                        if user.check_password(password):
                            message = _("Your e-mail address is not your "
                                        "username."
                                        " Try '%s' instead.") % user.username
                raise ValidationError(message)
            # Removed check for is_staff here!
            elif not self.user_cache.is_active:
                raise ValidationError(message)
        self.check_for_test_cookie()
        return self.cleaned_data

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
        return EntityAdmin.queryset(self, request).filter(empresa=self.get_empresa(request))


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
            codigo = '' 
            try:
                codigo = Factura.objects.filter(empresa=obj.empresa).exclude(pk=obj.pk).order_by('-id')[0].codigo
                partes = codigo.split('-')
                codigo = '%d-%03d' % (obj.fecha.year, int(partes[1]) + 1)
            except:
                codigo = '%d-%03d' % (obj.fecha.year, 1)
                
            obj.codigo = codigo
        obj.save()
        return obj

    # LIST
    list_filter = ('fecha', 'cliente',)
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
        js = ('admin/js/jquery.js', '/static/order/js/order.js', '/static/order/js/jshashtable-2.1.js','/static/order/js/jquery.numberformatter-1.2.3.js',)
        css = {
               all: ('/static/order/css/order.css',)
        }


class ClienteAdmin(EmpresaEntity):
    pass

class ProductoAdmin(EmpresaEntity):
    pass

order_admin_site.register(Empresa)
order_admin_site.register(Iva)
order_admin_site.register(Cliente, ClienteAdmin)
order_admin_site.register(Producto, ProductoAdmin)
order_admin_site.register(Factura, FacturaAdmin)


