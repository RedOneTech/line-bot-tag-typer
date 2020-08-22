from django.db import models

import secrets

class LINEUser(models.Model):
    userid = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        # Generate Token For New User
        if not self.pk:
            self.token = secrets.token_hex(16)
        super(LINEUser, self).save(*args, **kwargs)