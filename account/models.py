from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Expense(models.Model):

    amount = models.IntegerField(max_length=25)
    description = models.TextField(max_length=500)
    date = models.DateField(max_length=300)
    time = models.TimeField(max_length=300)
    comment = models.TextField(max_length=500)
    user = models.ForeignKey(User, unique=True)