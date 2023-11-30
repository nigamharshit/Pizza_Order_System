from django.db import models

# Create your models here.
class Pizza(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class PizzaBase(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Cheese(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Topping(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('Placed', 'Placed'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('Dispatched', 'Dispatched'),
        ('Delivered', 'Delivered'),
    )

    order_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Placed')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Order {self.order_id} - Status: {self.status}"