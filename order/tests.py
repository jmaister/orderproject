from decimal import Decimal
from django.core.urlresolvers import reverse
from django.test import TestCase
from order.models import Invoice, InvoiceItem
import datetime


class ViewsTestCase(TestCase):

    def test_index(self):
        resp = self.client.get('/', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_invoice_list(self):
        resp = self.client.get(reverse('invoice_list'), follow=True)
        self.assertEqual(resp.status_code, 200)


class InvoiceTestCase(TestCase):
    fixtures = ['invoice_test.json']

    def setUp(self):
        super(InvoiceTestCase, self).setUp()
        self.invoice = Invoice.objects.create(company_id=1, date=datetime.datetime.now(), client_id=1)

    def test_new_invoiceitem(self):
        self.assertTrue(self.invoice.total == 0)

        item = InvoiceItem(invoice_id=self.invoice.id, product_id=1, quantity=2, price=Decimal("100.27"))
        item.save()
        self.invoice.save()

        # Checks
        item = InvoiceItem.objects.get(id=item.id)
        self.assertEqual(str(item.price), "100.27")
        self.assertEqual(str(item.base), "200.54")
        self.assertEqual(item.tax_name, item.product.tax.name)
        self.assertEqual(item.tax_rate, item.product.tax.rate)
        self.assertEqual(str(item.taxes), "42.11")
        self.assertEqual(str(item.total), "242.65")

        self.assertEqual(str(self.invoice.base), "200.54")
        self.assertEqual(str(self.invoice.taxes), "42.11")
        self.assertEqual(str(self.invoice.total), "242.65")
