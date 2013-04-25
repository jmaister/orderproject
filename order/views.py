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
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages


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
def print_invoice(request, pk):
    invoice = Invoice.objects.get(id=pk)
    invoiceitems = InvoiceItem.objects.select_related().filter(invoice_id=pk)
    
    t = get_template('order/invoice_print_bs.html')
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


class AddUserCompanyMixin(CompanyFilterMixin):
    def _get_company(self):
        return self.request.user.get_profile().company

    @transaction.commit_on_success
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self._get_company()
        messages.success(self.request, str(self.object) +" saved.")
        return super(AddUserCompanyMixin, self).form_valid(form)


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
        messages.success(self.request, "Invoice %s saved." % (self.object.code, ))
        return out


class InvoiceUpdateView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Invoice
    form_class = InvoiceForm

    context_object_name = 'invoice'
    inlines = [InvoiceItemInline]
    inlines_names = ['InvoiceItemInline']

    def _get_company(self):
        return self.request.user.get_profile().company

    def get_queryset(self):
        company = self._get_company()
        return self.model.objects.filter(company=company)

    def construct_inlines(self):
        # Only select the products on the company
        qs = Product.objects.filter(company=self._get_company())
        inline_formsets = super(InvoiceUpdateView, self).construct_inlines()
        for form in inline_formsets[0].forms:
            form.fields['product'].queryset = qs 
        return inline_formsets

    @transaction.commit_on_success
    def forms_valid(self, form, inlines):
        # Default company
        if not self.object.company:
            self.object.company = self._get_company()

        out = UpdateWithInlinesView.forms_valid(self, form, inlines)

        # Save object to recalculate totals
        self.object.save()
        messages.success(self.request, "Invoice %s saved." % (self.object.code, ))
        return out


class CreateViewByCompany(AddUserCompanyMixin, CreateView):
    pass


class UpdateViewByCompany(AddUserCompanyMixin, UpdateView):
    pass
