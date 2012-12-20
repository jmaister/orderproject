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
