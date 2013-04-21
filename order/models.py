from base.models import BaseEntity, BaseModel
from decimal import Decimal
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse


class Company(BaseEntity):
    address = models.TextField()
    id_number = models.CharField(max_length=20)


class Tax(BaseEntity):
    rate = models.DecimalField(max_digits=5, decimal_places=2)


class Product(BaseEntity):
    print_name = models.CharField(max_length=50)
    company = models.ForeignKey(Company)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.ForeignKey(Tax)


class Client(BaseEntity):
    company = models.ForeignKey(Company)
    address = models.TextField()
    id_number = models.CharField(max_length=20)


class Invoice(BaseModel):
    company = models.ForeignKey(Company)
    code = models.CharField(max_length=50)
    date = models.DateField()
    client = models.ForeignKey(Client)
    date_paid = models.DateField(blank=True, null=True)

    base = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)

    def get_absolute_url(self):
        return reverse('invoice_edit', args=[self.id])

    def calculate(self):
        sum_base = 0
        sum_taxes = 0
        sum_total = 0
        for invoice_item in self.invoiceitem_set.all():
            sum_base += invoice_item.base
            sum_taxes += invoice_item.taxes
            sum_total += invoice_item.total
            
        self.base = sum_base
        self.taxes = sum_taxes
        self.total = sum_total
    
    def save(self, force_insert=False, force_update=False, using=None,
        update_fields=None):
        self.calculate()
        return BaseModel.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __unicode__(self):
        return "[" + str(self.id) + "][" + str(self.date) + "] " + self.client.name


class InvoiceItem(BaseModel):
    invoice = models.ForeignKey(Invoice)
    product = models.ForeignKey(Product)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=0)

    base = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    tax_name = models.CharField(max_length=500)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)

    def get_absolute_url(self):
        return None

    def calculate(self):
        # Change to multiple taxes
        if self.tax_rate is None or self.tax_rate == 0:
            self.tax_name = self.product.tax.name
            self.tax_rate = self.product.tax.rate
            
        self.base = (self.price * self.quantity)
        self.taxes = (self.base * self.tax_rate / Decimal(100.0))
        self.total = self.base + self.taxes

    def save(self, force_insert=False, force_update=False, using=None,
        update_fields=None):
        self.calculate()
        return BaseModel.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

class UserProfile(models.Model):
    # This field is required.
    # user = models.OneToOneField(User)
    # user = models.ForeignKey(User, unique=True)
    user = models.OneToOneField(User, unique=True, primary_key=True, related_name="user")

    # Other fields here
    company = models.ForeignKey(Company, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Default group with default perms
        try:
            default_group = Group.objects.get(name='Usuario')
            self.user.groups.add(default_group)
        except:
            pass
        
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # UserProfile.objects.get_or_create(user=instance)
        profile = UserProfile(user=instance)
        profile.save()
    
post_save.connect(create_user_profile, sender=User)
