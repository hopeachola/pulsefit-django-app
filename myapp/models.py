from django.db import models
from django.contrib.auth.models import User

class CalorieLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    food_item = models.CharField(max_length=200)
    calories = models.IntegerField()
    date_logged = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anon'} - {self.food_item}"

class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    routine_id = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    duration = models.IntegerField()  
    calories_burned = models.IntegerField()
    date_completed = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anon'} - {self.title}"
