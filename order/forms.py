from django import forms
from extra_views.advanced import InlineFormSet
from order.models import Invoice, InvoiceItem


class InvoiceForm(forms.ModelForm):
    
    class Meta:
        model = Invoice
        exclude = ('company',)


class InvoiceItemInline(InlineFormSet):
    model = InvoiceItem
    extra = 1

