# Create your views here.
from django.core import serializers
from django.forms.models import inlineformset_factory, ModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.template.context import Context
from django.template.loader import get_template
from order.models import Producto, Factura, FacturaItem, Iva

def _json_view(request, clazz, pk):
    result = clazz.objects.filter(pk=pk)
    return HttpResponse(serializers.serialize('json', result), mimetype='application/json')

def json_producto(request, pk):
    return _json_view(request, Producto, pk)

def json_iva(request, pk):
    return _json_view(request, Iva, pk)

def print_order(request, factura_id):
    factura = Factura.objects.get(id=factura_id)
    facturaitems = FacturaItem.objects.select_related().filter(factura_id=factura_id).all()
    
    t = get_template('order_print_bs.html')
    html = t.render(Context(
        {'factura': factura,
         'facturaitems': facturaitems,
         'blank_lines': range(8 - facturaitems.count())
         }
        ))
    return HttpResponse(html)    

class FacturaForm(ModelForm):
    class Meta:
        model = Factura
    def __init__(self, *args, **kwargs):
        super(FacturaForm, self).__init__(*args, **kwargs)

def factura_update(request, pk):

    FacturaInlineFormSet = inlineformset_factory(Factura, FacturaItem)
    
    factura = Factura.objects.get(pk=pk)
    form = FacturaForm(request.POST or None, request.FILES or None, instance=factura)
    formset = FacturaInlineFormSet(request.POST or None, request.FILES or None, instance=factura)
    
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        form.save()
        formset.save()

    return render(request, "order/factura_form.html", {
        "form": form,
        "formset": formset,
    })    

