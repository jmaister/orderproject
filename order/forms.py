import datetime
from django import forms
from extra_views.advanced import InlineFormSet
from order.models import Invoice, InvoiceItem, Product, Client, Tax


class InvoiceForm(forms.ModelForm):

    date = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = Invoice
        exclude = ('company',)

class InvoiceItemForm(forms.ModelForm):
    
    price = forms.CharField(max_length=10, min_length=1)
    quantity = forms.CharField(max_length=10, min_length=1)
    
    class Meta:
        model = InvoiceItem


class InvoiceItemInline(InlineFormSet):
    model = InvoiceItem
    extra = 1
    form_class = InvoiceItemForm


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
