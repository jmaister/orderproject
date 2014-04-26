# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder

from braces.views import LoginRequiredMixin

from extra_views.advanced import NamedFormsetsMixin, CreateWithInlinesView, \
    UpdateWithInlinesView

from order.forms import InvoiceForm, InvoiceItemInline
from order.models import Product, Invoice, InvoiceItem, Tax, Client


@login_required
def _json_view(request, clazz, pk):
    result = clazz.objects.filter(pk=pk)
    return HttpResponse(serializers.serialize('json', result), mimetype='application/json')


@login_required
def json_product(request, pk):
    obj = Product.objects.get(pk=pk)
    # Only serialize the needed data
    result = {'price': obj.price, 'tax': {'name': obj.tax.name, 'rate': obj.tax.rate}}
    return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder), mimetype='application/json')


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


class AddModelNameMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AddModelNameMixin, self).get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name
        context['verbose_name_plural'] = self.model._meta.verbose_name_plural
        return context


class AddUserMixin(LoginRequiredMixin):

    def get_queryset(self):
        """
        Just show the user entities.
        """
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """
        Add the current user to the "user" field of the entity.
        """
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        messages.success(self.request, str(self.object) + " saved.")
        return super(AddUserMixin, self).form_valid(form)


class InvoiceCreateView(LoginRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Invoice
    form_class = InvoiceForm

    context_object_name = 'invoice'
    inlines = [InvoiceItemInline]
    inlines_names = ['InvoiceItemInline']

    def get_form(self, form_class):
        # Filter cilents on main form, by user
        form = CreateWithInlinesView.get_form(self, form_class)
        form.fields['client'].queryset = Client.objects.filter(user=self.request.user)
        return form

    def construct_inlines(self):
        # Filter products inlines, by user
        inlines = CreateWithInlinesView.construct_inlines(self)
        invoiceItemInline = inlines[0]
        invoiceItemInline.form.base_fields['product'].queryset = Product.objects.filter(user=self.request.user)
        return inlines

    def forms_valid(self, form, inlines):
        # Default user
        self.object.user = self.request.user

        # Save object to recalculate totals
        out = CreateWithInlinesView.forms_valid(self, form, inlines)
        self.object.save()
        messages.success(self.request, "Invoice %s saved." % (self.object.code,))
        return out


class InvoiceUpdateView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Invoice
    form_class = InvoiceForm

    context_object_name = 'invoice'
    inlines = [InvoiceItemInline]
    inlines_names = ['InvoiceItemInline']

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def construct_inlines(self):
        # Only select the products on the user
        qs = Product.objects.filter(user=self.request.user)
        inline_formsets = super(InvoiceUpdateView, self).construct_inlines()
        for form in inline_formsets[0].forms:
            form.fields['product'].queryset = qs
        return inline_formsets

    def forms_valid(self, form, inlines):
        # Default user
        if not self.object.user:
            self.object.user = self.request.user

        out = UpdateWithInlinesView.forms_valid(self, form, inlines)

        # Save object to recalculate totals
        self.object.save()
        messages.success(self.request, "Invoice %s saved." % (self.object.code,))
        return out


class CreateUserEntityView(AddModelNameMixin, AddUserMixin, CreateView):
    template_name = "order/entity_form.html"


class UpdateUserEntityView(AddModelNameMixin, AddUserMixin, UpdateView):
    template_name = "order/entity_form.html"


class ListViewByUser(AddModelNameMixin, AddUserMixin, ListView):
    pass
