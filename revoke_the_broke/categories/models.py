from django.db import models
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    incognito_user_token = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default='#FFFFFF')

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = "Categories"

        def __unicode__(self):
            return self.title
        
    def __str__(self, *args, **kwargs):
        return self.title + " | " + (self.author.username if self.author else 'Incognito')