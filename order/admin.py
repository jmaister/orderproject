from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from order.models import UserProfile, Factura, Producto, Cliente, Iva, Empresa, \
    FacturaItem

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

classes = (Factura, FacturaItem, Producto, Cliente, Iva, Empresa )
for cl in classes:
    admin.site.register(cl)
