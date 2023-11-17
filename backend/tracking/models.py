from django.db import models
from user.models import User



#user's macro goals
class Goal(models.Model):
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    date = models.DateField()
    calories = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    carbs = models.IntegerField()
    
    def __str__(self):
        return self.user_id.username + " " + str(self.date)
    
#user's log for a given day
class Log(models.Model):
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    date = models.DateField()
    total_calories = models.IntegerField(default=0)
    total_protein = models.IntegerField(default=0)
    total_fat = models.IntegerField(default=0)
    total_carbs = models.IntegerField(default=0)
    
    #calculate totals for the log entry
    def calculate_totals(self):
        food = FoodEntry.objects.filter(log_id=self)
        self.total_calories = sum(food.values_list('food_id__calories', flat=True))
        self.total_protein = sum(food.values_list('food_id__protein', flat=True))
        self.total_fat = sum(food.values_list('food_id__fat', flat=True))
        self.total_carbs = sum(food.values_list('food_id__carbs', flat=True))
        self.save()
        
    def __str__(self):
        return self.user_id.username + " " + str(self.date)
    
class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=50)
    calories = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    serving_size = models.IntegerField(default=0)
    
    #update macros based on serving size
    def update_macros(self):
        self.calories *= self.serving_size
        self.protein *= self.serving_size
        self.fat *= self.serving_size
        self.carbs *= self.serving_size
        self.save()
        
        
    def __str__(self):
        return self.food_name + str(self.food_id)

#food entry for a given log
class FoodEntry(models.Model):
    food_id = models.ForeignKey('Food', on_delete=models.CASCADE)
    log_id = models.ForeignKey('Log', on_delete=models.CASCADE)
    time = models.TimeField()
    
    def __str__(self):
            return self.food_id.food_name + " " + str(self.log_id.date)