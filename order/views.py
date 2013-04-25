# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.http import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from django.views.generic.list import ListView

from braces.views import LoginRequiredMixin

from extra_views.advanced import NamedFormsetsMixin, CreateWithInlinesView, \
    UpdateWithInlinesView

from order.forms import InvoiceForm, InvoiceItemInline
from order.models import Product, Invoice, InvoiceItem, Tax


@login_required
def _json_view(request, clazz, pk):
    result = clazz.objects.filter(pk=pk)
    return HttpResponse(serializers.serialize('json', result), mimetype='application/json')

@login_required
def json_product(request, pk):
    return _json_view(request, Product, pk)

@login_required
def json_tax(request, pk):
    return _json_view(request, Tax, pk)

@login_required
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


class CompanyFilterMixin(LoginRequiredMixin):

    def get_queryset(self):
        # Filter the company items only
        profile = self.request.user.get_profile()
        return self.model.objects.filter(company=profile.company)


class ListViewByCompany(CompanyFilterMixin, ListView):
    pass


class InvoiceCreateView(LoginRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Invoice
    form_class = InvoiceForm

    context_object_name = 'invoice'
    inlines = [InvoiceItemInline]
    inlines_names = ['InvoiceItemInline']

    @transaction.commit_on_success
    def forms_valid(self, form, inlines):
        # Default company
        self.object.company = self.request.user.get_profile().company

        # Save object to recalculate totals
        out = CreateWithInlinesView.forms_valid(self, form, inlines)
        self.object.save()
        return out


class InvoiceUpdateView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Invoice
    form_class = InvoiceForm

    context_object_name = 'invoice'
    inlines = [InvoiceItemInline]
    inlines_names = ['InvoiceItemInline']

    def get_queryset(self):
        company = self.request.user.get_profile().company
        return self.model.objects.filter(company=company)

    def construct_inlines(self):
        # Only select the products on the company
        qs = Product.objects.filter(company=self.request.user.get_profile().company)
        inline_formsets = super(InvoiceUpdateView, self).construct_inlines()
        for form in inline_formsets[0].forms:
            form.fields['product'].queryset = qs 
        return inline_formsets

    @transaction.commit_on_success
    def forms_valid(self, form, inlines):
        # Default company
        if not self.object.company:
            self.object.company = self.request.user.get_profile().company

        # Save object to recalculate totals
        out = UpdateWithInlinesView.forms_valid(self, form, inlines)
        self.object.save()
        return out

