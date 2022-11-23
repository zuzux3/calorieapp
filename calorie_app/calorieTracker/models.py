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
    foodSelected = models.ForeignKey(Food, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.FloatField(default=0)
    totalCalorie = models.FloatField(default=0,null=True)
    date = models.DateField(auto_now_add=True)
    calorieGoal = models.PositiveBigIntegerField(default=0)
    allFoodSelectedToday = models.ManyToManyField(Food,through='PostFood',related_name='inventory')

    def save(self, *args, **kwargs):
        if self.foodSelected != None:
            self.amount = (self.foodSelected.calorie/self.foodSelected.quantity)
            self.calorieCount = self.amount*self.quantity
            calories = Profile.objects.filter(personOf = self.personOf).last()
            PostFood.objects.create(profile=calories,food=self.foodSelected,calorieAmount=self.calorieCount, amount=self.quantity)
            self.foodSelected = None
            super(Profile, self).save(*args, **kwargs)

        else:
            super(Profile, self).save(*args, **kwargs)


class PostFood(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    calorieAmount = models.FloatField(default=0,null=True,blank=True)
    amount = models.FloatField(default=0)