from django import forms
from django.db import transaction
from extra_views.advanced import CreateWithInlinesView, InlineFormSet, \
    NamedFormsetsMixin, UpdateWithInlinesView
from order.models import Invoice, InvoiceItem, Tax


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ('company',)


class InvoiceItemInline(InlineFormSet):
    model = InvoiceItem
    extra = 1


class InvoiceCreateView(NamedFormsetsMixin, CreateWithInlinesView):
    model = Invoice
    form_class = InvoiceForm

    context_object_name = 'invoice'
    inlines = [InvoiceItemInline]
    inlines_names = ['InvoiceItemInline']
    template_name = 'order.html'

    def get_context_data(self, **kwargs):
        ctx = NamedFormsetsMixin.get_context_data(self, **kwargs)
        ctx['taxes'] = Tax.objects.all()
        return ctx

    @transaction.commit_on_success
    def forms_valid(self, form, inlines):
        # Default company
        self.object.company = self.request.user.get_profile().company

        # Save object to recalculate totals
        out = CreateWithInlinesView.forms_valid(self, form, inlines)
        self.object.save()
        return out


class InvoiceUpdateView(NamedFormsetsMixin, UpdateWithInlinesView):
    model = Invoice
    form_class = InvoiceForm

    context_object_name = 'invoice'
    inlines = [InvoiceItemInline]
    inlines_names = ['InvoiceItemInline']
    template_name = 'order.html'

    @transaction.commit_on_success
    def forms_valid(self, form, inlines):
        # Default company
        if not self.object.company:
            self.object.company = self.request.user.get_profile().company

        # Save object to recalculate totals
        out = UpdateWithInlinesView.forms_valid(self, form, inlines)
        self.object.save()
        return out

