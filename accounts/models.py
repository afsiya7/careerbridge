from django.db import models
class UserProfile(models.Model):
    profile_completed = models.BooleanField(default=False)