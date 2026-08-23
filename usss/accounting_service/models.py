from django.db import models
from service.models import Products
from store_service.models import Stores

class Accounting(models.Model):
    date = models.DateTimeField(null = False, blank = False)
    product = models.ForeignKey(Products, on_delete = models.PROTECT, null = False, blank = False, related_name='accounting_product', db_column='product_id')
    store = models.ForeignKey(Stores, on_delete=models.PROTECT, null=False, blank=False, related_name='accounting_store', db_column='store_id')
    sales = models.FloatField()
    COGS = models.FloatField()
    marketing_expenses = models.FloatField()
    other_expenses = models.FloatField()

    class Meta:
        managed = False
        db_table = 'Accounting'
