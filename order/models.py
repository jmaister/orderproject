from base.models import BaseEntity, BaseModel
from django.db import models


class Iva(BaseEntity):
    percent = models.DecimalField(max_digits=5, decimal_places=2)

class Product(BaseEntity):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.ForeignKey(Iva)

class Client(BaseEntity):
    address = models.TextField()
    nif = models.CharField(max_length=20)

class Order(BaseModel):
    date = models.DateField()
    client = models.ForeignKey(Client)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __unicode__(self):
        return "[" + str(self.id) + "][" + str(self.date) + "] " + self.client.name

class OrderItem(BaseModel):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=0)

    iva = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
