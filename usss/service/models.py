from django.db import models

class Products(models.Model):
    category = models.CharField(max_length=15)
    name = models.TextField(unique=True)
    product_code = models.IntegerField(null=False, blank=False, unique=True)
    is_coffee = models.BooleanField(null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'Products'



