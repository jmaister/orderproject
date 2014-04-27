from order.models import Product, Tax, Client, Invoice, InvoiceItem
from tastypie import fields
from tastypie.resources import ModelResource


class FilterByUserMixin(object):
    def get_object_list(self, request):
        return super(FilterByUserMixin, self).get_object_list(request).filter(user=request.user)


class TaxResource(FilterByUserMixin, ModelResource):
    class Meta:
        queryset = Tax.objects.all()
        resource_name = 'tax'


class ProductResource(FilterByUserMixin, ModelResource):
    tax = fields.ToOneField(TaxResource, 'tax', full=True)

    class Meta:
        queryset = Product.objects.all()
        resource_name = 'product'


class ClientResource(FilterByUserMixin, ModelResource):
    class Meta:
        queryset = Client.objects.all()
        resource_name = 'client'


class InvoiceItemResource(ModelResource):
    class Meta:
        queryset = InvoiceItem.objects.all()
        resource_name = 'invoiceitem'


class InvoiceResource(FilterByUserMixin, ModelResource):
    invoice_items = fields.ToManyField(InvoiceItemResource, 'invoiceitem_set', full=True)

    class Meta:
        queryset = Invoice.objects.all()
        resource_name = 'invoice'
