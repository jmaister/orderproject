# Create your views here.
from django.core import serializers
from django.http import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from order.models import Product, Invoice, InvoiceItem, Tax


def _json_view(request, clazz, pk):
    result = clazz.objects.filter(pk=pk)
    return HttpResponse(serializers.serialize('json', result), mimetype='application/json')

def json_product(request, pk):
    return _json_view(request, Product, pk)

def json_tax(request, pk):
    return _json_view(request, Tax, pk)

def print_order(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    invoiceitems = InvoiceItem.objects.select_related().filter(invoice_id=invoice_id)
    
    t = get_template('order_print_bs.html')
    html = t.render(Context(
        {'invoice': invoice,
         'invoiceitems': invoiceitems,
         'blank_lines': range(8 - invoiceitems.count())
         }
        ))
    return HttpResponse(html)    

