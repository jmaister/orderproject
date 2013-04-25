from django import forms
from extra_views.advanced import InlineFormSet
from order.models import Invoice, InvoiceItem, Product, Client, Tax


class InvoiceForm(forms.ModelForm):
    
    class Meta:
        model = Invoice
        exclude = ('company',)


class InvoiceItemInline(InlineFormSet):
    model = InvoiceItem
    extra = 1


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        exclude = ('company',)


class ClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        exclude = ('company',)


class TaxForm(forms.ModelForm):
    
    class Meta:
        model = Tax
        exclude = ('company',)
