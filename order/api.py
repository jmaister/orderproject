from order.models import Product, Tax
from tastypie.resources import ModelResource


class ProductResource(ModelResource):
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'product'


class TaxResource(ModelResource):
    class Meta:
        queryset = Tax.objects.all()
        resource_name = 'tax'
