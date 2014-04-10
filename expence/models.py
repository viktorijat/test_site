from django.db import models


class Expence(models.Model):

    note = models.CharField(max_length=300)
    value = models.IntegerField(max_length=25)


