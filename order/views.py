# Create your views here.
from advanced import InlineFormSet, CreateWithInlinesView, UpdateWithInlinesView
from django.core import serializers
from django.forms.forms import Form
from django.forms.models import inlineformset_factory, modelform_factory, \
    ModelForm, modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
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


class FacturaItemInline(InlineFormSet):
    model = FacturaItem
    readonly_fields = ('base', 'total_iva', 'total')


class FacturaCreateView(CreateWithInlinesView):
    model = Factura
    inlines = [FacturaItemInline]


"""
class FacturaUpdateView(UpdateWithInlinesView):
    model = Factura
    inlines = [FacturaItemInline]
"""

"""
class FacturaItemForm(ModelForm):
    class Meta:
        model = FacturaItem

class FacturaForm(ModelForm):
    
    FacturaItemFormSet = inlineformset_factory(Factura, FacturaItem, form=FacturaItemForm)
    
    class Meta:
        model = Factura
        
    class Forms:
        inlines = {
            'lineas': FacturaItemFormSet,           
        } 
"""

class FacturaForm(ModelForm):
    class Meta:
        model = Factura

def factura_update(request, pk):
    factura = Factura.objects.get(pk=pk)

    FacturaInlineFormSet = inlineformset_factory(Factura, FacturaItem)
    if request.method == "POST":
        form = FacturaForm(request.POST, request.FILES, instance=factura)
        formset = FacturaInlineFormSet(request.POST, request.FILES, instance=factura)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            # Do something.
    else:
        form = FacturaForm(instance=factura)
        formset = FacturaInlineFormSet(instance=factura)

    return render(request, "order/factura_form.html", {
        "form": form,
        "formset": formset,
    })    

