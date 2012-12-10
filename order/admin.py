from base.admin import EntityAdmin
from decimal import Decimal
from django.contrib import admin
from order.models import Product, Order, OrderItem, Client, Iva

class IvaAdmin(EntityAdmin):
    pass

class ClientAdmin(EntityAdmin):
    pass

class ProductAdmin(EntityAdmin):
    pass

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('base', 'total_iva', 'total')
    
class OrderAdmin(EntityAdmin):
    # FORM
    readonly_fields = ('base', 'total_iva', 'total')
    inlines = [
        OrderItemInline,
    ]

    # LIST
    list_filter = ('date',)
    list_display = ('id', 'date', 'client', 'total', 'print_link',)
    def print_link(self, obj):
        return '<a target="top" href="%s/%d">Print</a>' % ('/print_order', obj.id,)
    print_link.allow_tags = True
    print_link.short_description = 'Print'
    
    # SAVE
    def save_formset(self, request, form, formset, change):
        sum_total_iva = 0
        sum_base = 0
        sum_total = 0

        print "save start"
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, OrderItem):
                print "instance"
                if instance.iva is None:
                    instance.iva = instance.product.iva.percent
                
                instance.base = (instance.price * instance.quantity)
                instance.total_iva = (instance.base * instance.iva / Decimal(100.0))
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
        
        super(OrderAdmin, self).save_formset(request, form, formset, change)

    # Javascript form
    class Media:
        js = ('admin/js/jquery.js', '/static/order/js/order.js', '/static/order/js/jshashtable-2.1.js','/static/order/js/jquery.numberformatter-1.2.3.js',)


admin.site.register(Iva, IvaAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
