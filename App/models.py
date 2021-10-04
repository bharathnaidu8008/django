from django.db import models

# Create your models here.
class Indias(models.Model):
    Active = models.IntegerField(default=0)
    Confirmed = models.IntegerField(default=0)
    Deaths = models.IntegerField(default=0)
    Date = models.DateField()
    Recovered = models.IntegerField(default=0)

class States(models.Model):
    Active = models.IntegerField(default=0)
    Confirmed = models.IntegerField(default=0)
    Deaths = models.IntegerField(default=0)
    State = models.TextField(default=0)
    Recovered = models.IntegerField(default=0)
