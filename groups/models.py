from django.db import models

# Create your models here.
class LINEGroup(models.Model):
    groupid = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=32)

class LINEGroupMember(models.Model):
    group = models.ForeignKey(LINEGroup, on_delete=models.CASCADE)
    userid = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
