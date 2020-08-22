from django.db import models

from user.models import LINEUser

class MentionData(models.Model):
    requester = models.ForeignKey(LINEUser, on_delete=models.CASCADE)
    member_name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)