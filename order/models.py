from base.models import BaseEntity, BaseModel
from decimal import Decimal
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    BaseUserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class OrderUserManager(BaseUserManager):
    def create_user(self, email, company, password=None):
        """
        Creates and saves a User with the given email, company name, and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        if not company:
            raise ValueError("Users must have a company name")

        user = self.model(
            email=OrderUserManager.normalize_email(email),
            company=company,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, company, password):
        """
        Creates and saves a superuser
        with the given email, company name and password.
        """
        user = self.create_user(email,
            password=password,
            company=company
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

USERNAME_FIELD = "email"
REQUIRED_FIELDS = ["company", ]


class OrderUser(AbstractBaseUser, PermissionsMixin):
    objects = OrderUserManager()

    USERNAME_FIELD = USERNAME_FIELD
    REQUIRED_FIELDS = REQUIRED_FIELDS

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        db_index=True,
    )
    company = models.CharField(max_length=50, verbose_name=_('Company Name'))
    address = models.TextField(verbose_name=_('Address'))
    id_number = models.CharField(max_length=20, verbose_name=_('ID Number'))

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def get_full_name(self):
        # The user is identified by their email and company
        return "%s from %s" % (self.email, self.company)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email


class Tax(BaseEntity):
    user = models.ForeignKey(OrderUser)
    rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Rate'))

    def get_absolute_url(self):
        return reverse('tax_edit', args=[self.id])

    class Meta:
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')


class Product(BaseEntity):
    user = models.ForeignKey(OrderUser)
    print_name = models.CharField(max_length=50, verbose_name=_('Print name'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    tax = models.ForeignKey(Tax, verbose_name=_('Tax'))

    def get_absolute_url(self):
        return reverse('product_edit', args=[self.id])

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Client(BaseEntity):
    user = models.ForeignKey(OrderUser)
    address = models.TextField(verbose_name=_('Address'))
    id_number = models.CharField(max_length=20, verbose_name=_('ID Number'))

    def get_absolute_url(self):
        return reverse('client_edit', args=[self.id])

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')


class Invoice(BaseModel):
    user = models.ForeignKey(OrderUser)
    code = models.CharField(max_length=50, editable=False)
    date = models.DateField()
    client = models.ForeignKey(Client, verbose_name=_('Client'))
    date_paid = models.DateField(blank=True, null=True, verbose_name=("Date paid"))

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

    def get_next_code(self):
        # Autocalculate next Invoice code
        if not self.code and self.id:
            num = 1
            try:
                lastcode = Invoice.objects.filter(user=self.user).exclude(pk=self.id).order_by('-id')[0].code
                parts = lastcode.split('-')
                num = int(parts[1]) + 1
            except:
                pass

            return '%d-%03d' % (self.date.year, num)
        else:
            return self.code

    def save(self, force_insert=False, force_update=False, using=None,
        update_fields=None):
        self.calculate()
        self.code = self.get_next_code()
        return BaseModel.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __unicode__(self):
        return "[" + str(self.id) + "][" + str(self.date) + "] " + self.client.name

    def tax_map(self):
        taxmap = {}
        for invoice_item in self.invoiceitem_set.all():
            group = invoice_item.tax_group()
            if group in taxmap:
                taxmap[group] += invoice_item.taxes
            else:
                taxmap[group] = invoice_item.taxes
        return taxmap

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')


class InvoiceItem(BaseModel):
    invoice = models.ForeignKey(Invoice)
    product = models.ForeignKey(Product, verbose_name=_('Product'))

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    quantity = models.DecimalField(max_digits=10, decimal_places=0, verbose_name=_('Quantity'))

    base = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    tax_name = models.CharField(max_length=500, editable=False)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)

    def get_absolute_url(self):
        return None

    def __unicode__(self):
        return self.tax_name + ": " + str(self.tax_rate) + "%"

    def tax_group(self):
        return self.__unicode__()

    def calculate(self):
        # Change to multiple taxes
        if not self.tax_rate or not self.tax_rate:
            self.tax_name = self.product.tax.name
            self.tax_rate = self.product.tax.rate

        if not self.price:
            self.price = self.product.price

        self.base = self.price * self.quantity
        self.taxes = self.base * self.tax_rate / Decimal("100")
        self.total = self.base + self.taxes

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.calculate()
        return BaseModel.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta:
        verbose_name = _('Invoice item')
        verbose_name_plural = _('Invoice items')
