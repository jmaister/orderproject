import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from extra_views.advanced import InlineFormSet
from order.models import Invoice, InvoiceItem, Product, Client, Tax


class InvoiceForm(forms.ModelForm):

    date = forms.DateField(initial=datetime.date.today, label=_('Date'))
    #date_paid = forms.DateField(label=_('Date paid'), required=False)

    class Meta:
        model = Invoice
        fields = ('date', 'client', 'date_paid')


class InvoiceItemForm(forms.ModelForm):

    price = forms.DecimalField(localize=True, decimal_places=2)
    quantity = forms.IntegerField(localize=True)

    class Meta:
        model = InvoiceItem


class InvoiceItemInline(InlineFormSet):
    model = InvoiceItem
    extra = 1
    form_class = InvoiceItemForm


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'print_name', 'price', 'tax')


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name', 'address', 'id_number')


class TaxForm(forms.ModelForm):

    class Meta:
        model = Tax
        fields = ('name', 'rate')
