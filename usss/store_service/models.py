from django.db import models

class Stores(models.Model):
    state = models.CharField(max_length=15)
    market = models.CharField(max_length=4)
    market_size = models.CharField(max_length=15)
    store_code = models.CharField(max_length=30, null = False, blank = False, unique=True)

    class Meta:
        managed = False
        db_table = 'Stores'
