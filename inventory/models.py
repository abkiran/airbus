from django.db import models

# Create your models here.
from inventory.vo import PRODUCT_CATEGORIES

CATEGORY_CHOICES = sorted([(item, item) for item in PRODUCT_CATEGORIES])


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(unique=True, max_length=10, blank=False)
    product_category = models.CharField(choices=CATEGORY_CHOICES, max_length=100, blank=False)
    product_name = models.CharField(max_length=100, blank=False)
    product_description = models.TextField(blank=True, default=None)
    units = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
