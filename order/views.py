# Create your views here.
from django.core import serializers
from django.http import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from order.models import Product, Order, OrderItem, Iva


def json_product(request):
    search = request.GET.get('product_id')
    if search:
        result = Product.objects.filter(id=search)
        return HttpResponse(serializers.serialize('json', result), mimetype='application/json')
    return HttpResponse()

def json_iva(request, iva_id):
    result = Iva.objects.filter(id=iva_id)
    return HttpResponse(serializers.serialize('json', result), mimetype='application/json')

def print_order(request, order_id):
    #order = Order.objects.select_related().get(id=order_id)
    order = Order.objects.get(id=order_id)
    orderitems = OrderItem.objects.select_related().filter(order_id=order_id).all()
    
    t = get_template('order_print.html')
    html = t.render(Context(
        {'order': order,
         'orderitems': orderitems,
         'blank_lines': range(8 - orderitems.count())
         }
        ))
    return HttpResponse(html)    

