from django.db import models

from datetime import datetime

from django.db.models import *


class Product(Model):
    name = CharField(max_length=255)
    price = FloatField(default=0.0)


class Staff(Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик')
    ]
    
    full_name = CharField(max_length=255)
    position = CharField(max_length=2, choices=POSITIONS)
    labor_contract = IntegerField()

    def get_last_name(self):
        return self.full_name.split()[0]


class Order(Model):
    time_in = DateTimeField(auto_now_add=True)
    time_out = DateTimeField(null=True)
    cost = FloatField(default=0.0)
    take_away = BooleanField(default=False)
    complete = BooleanField(default=False)
    staff = ForeignKey(Staff, on_delete=CASCADE)
    products = ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds() // 60
        else:
            return (datetime.now() - self.time_in).total_seconds() // 60


class ProductOrder(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    order = ForeignKey(Order, on_delete=CASCADE)
    _amount = IntegerField(default=1)

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()

    def product_sum(self):
        return self.amount * self.product.price
