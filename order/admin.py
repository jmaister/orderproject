from django.contrib import admin
from order.models import Invoice, InvoiceItem, Product, Client, Tax, Company


classes = (Invoice, InvoiceItem, Product, Client, Tax, Company)
for cl in classes:
    admin.site.register(cl)
