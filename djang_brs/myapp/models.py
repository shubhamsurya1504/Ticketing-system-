# Create your models here.
from django.db import models
from datetime import datetime, timedelta

# Create your models here.

class Bus(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    
    class Meta:
        verbose_name_plural = "List of Busses"

    def __str__(self):
        return self.bus_name


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural = "List of Users"

    def __str__(self):
        return self.email
    



class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    userid =models.DecimalField(decimal_places=0, max_digits=2)
    busid=models.DecimalField(decimal_places=0, max_digits=2)
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=2)

    class Meta:
        verbose_name_plural = "List of Books"
    def __str__(self):
        return self.email

class Registration(models.Model):
    name = models.CharField(max_length = 70)
    email = models.CharField(max_length=70)
    age = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    amount = models.CharField(max_length=100)
    # regno = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100,blank=True)
    # razorpay_payment_id = models.CharField(max_length=100,blank=True)
    paid = models.BooleanField(default=False)

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    message = models.CharField(max_length=500)

class Refund(models.Model):

    REFUNDED = 'R'
    NOT_REFUNDED = 'NR'

    TICKET_STATUSES = ((REFUNDED, 'Refunded'),
                       (NOT_REFUNDED, 'Not Refunded'),)

    username = models.CharField(max_length=50)
    busname = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    nofseats = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    refundprice = models.PositiveIntegerField(max_length=50)
    status = models.CharField(choices=TICKET_STATUSES, default=NOT_REFUNDED, max_length=2)
