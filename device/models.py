from django.db import models
from account.models import User
# Create your models here.


class FishPond(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    location = models.CharField(max_length=100)


class Device(models.Model):
    createdAt = models.DateField(auto_now_add=True)
    fishPond = models.ForeignKey(FishPond, on_delete=models.DO_NOTHING)


class Record(models.Model):
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    create_date = models.DateField(auto_now_add=True)
    dissolved_oxygen = models.CharField(max_length=10)
    humidity = models.CharField(max_length=10)
    temperature = models.CharField(max_length=10)
    ph = models.CharField(max_length=10)
    evaluation = models.CharField(max_length=30)
