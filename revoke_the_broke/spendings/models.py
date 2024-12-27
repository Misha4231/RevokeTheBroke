from django.db import models
from django.conf import settings
from categories.models import Category


class Expenditure(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']

        def __unicode__(self):
            return self.title