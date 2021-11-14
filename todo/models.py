from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager


# Create your models here.
# Name, memo, important, date and time
class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = UserManager()

    def __str__(self):
        return self.title