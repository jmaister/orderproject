# Create your views here.
from django.core import serializers
from django.http import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from order.models import Producto, Factura, FacturaItem, Iva


def json_producto(request, prod_id):
    result = Producto.objects.filter(id=prod_id)
    return HttpResponse(serializers.serialize('json', result), mimetype='application/json')

def json_iva(request, iva_id):
    result = Iva.objects.filter(id=iva_id)
    return HttpResponse(serializers.serialize('json', result), mimetype='application/json')

def print_order(request, factura_id):
    factura = Factura.objects.get(id=factura_id)
    facturaitems = FacturaItem.objects.select_related().filter(factura_id=factura_id).all()
    
    t = get_template('order_print.html')
    html = t.render(Context(
        {'factura': factura,
         'facturaitems': facturaitems,
         'blank_lines': range(8 - facturaitems.count())
         }
        ))
    return HttpResponse(html)    

