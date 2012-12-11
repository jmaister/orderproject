from base.admin import EntityAdmin
from decimal import Decimal
from django.contrib import admin
from django.contrib.auth.models import User
from order.models import Producto, Factura, FacturaItem, Cliente, Iva, Empresa, \
    UserProfile
from django.contrib.auth.admin import UserAdmin

class FacturaItemInline(admin.TabularInline):
    model = FacturaItem
    readonly_fields = ('base', 'total_iva', 'total')
    
class FacturaAdmin(EntityAdmin):
    # FORM
    readonly_fields = ('base', 'total_iva', 'total')
    inlines = [
        FacturaItemInline,
    ]

    # LIST
    list_filter = ('fecha',)
    list_display = ('id', 'codigo', 'fecha', 'cliente', 'total', 'print_link',)
    def print_link(self, obj):
        return '<a target="top" href="%s/%d">Imprimir</a>' % ('/order/print_order', obj.id,)
    print_link.allow_tags = True
    print_link.short_description = 'Imprimir'
    
    # SAVE
    def save_formset(self, request, form, formset, change):
        sum_total_iva = 0
        sum_base = 0
        sum_total = 0

        print "save start"
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, FacturaItem):
                print "instance"
                if instance.tipo_iva is None:
                    instance.tipo_iva = instance.producto.iva.tipo
                
                instance.base = (instance.precio * instance.cantidad)
                instance.total_iva = (instance.base * instance.tipo_iva / Decimal(100.0))
                instance.total = instance.base + instance.total_iva
                sum_total_iva += instance.total_iva
                sum_base += instance.base
                sum_total += instance.total
                print "instance end %d %d %d" % (sum_total_iva, sum_base, sum_total)

        order = form.save(commit=False)
        order.total_iva = sum_total_iva
        order.base = sum_base
        order.total = sum_total
        order.save()
        
        super(FacturaAdmin, self).save_formset(request, form, formset, change)

    # Javascript form
    class Media:
        js = ('admin/js/jquery.js', '/static/order/js/order.js', '/static/order/js/jshashtable-2.1.js','/static/order/js/jquery.numberformatter-1.2.3.js',)


admin.site.register(Empresa)
admin.site.register(Iva)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Factura, FacturaAdmin)




# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
