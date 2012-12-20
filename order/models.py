from base.models import BaseEntity, BaseModel
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Empresa(BaseEntity):
    direccion = models.TextField()
    nif = models.CharField(max_length=20)

class Iva(BaseEntity):
    tipo = models.DecimalField(max_digits=5, decimal_places=2)

class Producto(BaseEntity):
    empresa = models.ForeignKey(Empresa)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.ForeignKey(Iva)

class Cliente(BaseEntity):
    empresa = models.ForeignKey(Empresa)
    direccion = models.TextField()
    nif = models.CharField(max_length=20)

class Factura(BaseModel):
    empresa = models.ForeignKey(Empresa)
    codigo = models.CharField(max_length=50)
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self):
        sum_total_iva = 0
        sum_base = 0
        sum_total = 0
        for factura_item in self.facturaitem_set.all():
            factura_item.save()
            sum_total_iva += factura_item.total_iva
            sum_base += factura_item.base
            sum_total += factura_item.total
            
        self.total_iva = sum_total_iva
        self.base = sum_base
        self.total = sum_total
        super(Factura, self).save()

    def __unicode__(self):
        return "[" + str(self.id) + "][" + str(self.fecha) + "] " + self.cliente.name

class FacturaItem(BaseModel):
    factura = models.ForeignKey(Factura)
    producto = models.ForeignKey(Producto)

    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.DecimalField(max_digits=10, decimal_places=0)

    tipo_iva = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self):
        if self.tipo_iva is None:
            self.tipo_iva = self.producto.iva.tipo
            
        self.base = (self.precio * self.cantidad)
        self.total_iva = (self.base * self.tipo_iva / Decimal(100.0))
        self.total = self.base + self.total_iva
        super(FacturaItem, self).save()

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    empresa = models.ForeignKey(Empresa, null=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    
post_save.connect(create_user_profile, sender=User)
