from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

class Food(models.Model):
    name = models.CharField(max_length=200, null=False)
    quantity = models.PositiveIntegerField(null=False, default=0)
    calorie = models.FloatField(null=False, default=0)
    personOf = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Profile(models.Model):
    personOf = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    calorieCount = models.FloatField(default=0,null=True,blank=True)
    