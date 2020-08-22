from django.db import models

class LINEToken(models.Model):
    token = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

