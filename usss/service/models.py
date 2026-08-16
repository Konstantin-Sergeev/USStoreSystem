from django.db import models

class Products(models.Model):
    category = models.CharField(max_length=15)
    name = models.TextField(unique=True)
    product_code = models.IntegerField(null=False, blank=False, unique=True)
    is_coffee = models.BooleanField(null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'Products'

class Stores(models.Model):
    state = models.CharField(max_length=15)
    market = models.CharField(max_length=4)
    market_size = models.CharField(max_length=15)
    store_code = models.CharField(max_length=30, null = False, blank = False, unique=True)

    class Meta:
        managed = False
        db_table = 'Stores'

class Accounting(models.Model):
    date = models.DateTimeField(null = False, blank = False)
    product_id = models.ForeignKey(Products, on_delete = models.PROTECT, null = False, blank = False)
    store_id = models.ForeignKey(Stores, on_delete=models.PROTECT, null=False, blank=False)
    sales = models.FloatField()
    COGS = models.FloatField()
    marketing_expenses = models.FloatField()
    other_expenses = models.FloatField()

    class Meta:
        managed = False
        db_table = 'Accounting'