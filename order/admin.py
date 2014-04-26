from django.contrib import admin
from order.models import Invoice, InvoiceItem, Product, Client, Tax

classes = (Invoice, InvoiceItem, Product, Client, Tax)
for cl in classes:
    admin.site.register(cl)
