from typing import Iterable
from django.db import models
from user.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
    
#user's macro goals
class Goal(models.Model):
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    
    # Need logic to compare these macros against daily logs
    
    calories = models.IntegerField(default=0) 
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    
    @property 
    def __str__(self):
        return self.user_id.username + " " + str(self.date)
    
    """
    provides a URL for the given model
    """
    def get_absolute_url(self):
        
        return reverse('Goal', args=[str(self.user_id)])
    
# user's log for a given day
class Log(models.Model):
    # model fields
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=True)
    total_calories = models.IntegerField(default=0)
    total_protein = models.IntegerField(default=0)F
    total_fat = models.IntegerField(default=0)
    total_carbs = models.IntegerField(default=0)
    
    class Meta:
        """
        configures default ordering of queryset by date
        """
        ordering = ["date"]
        
    #calculate totals for the log entry
    def calculate_totals(self):
        food = FoodEntry.objects.filter(log_id=self)
        self.total_calories = sum(food.values_list('food_id__calories', flat=True))
        self.total_protein = sum(food.values_list('food_id__protein', flat=True))
        self.total_fat = sum(food.values_list('food_id__fat', flat=True))
        self.total_carbs = sum(food.values_list('food_id__carbs', flat=True))
        self.save()
     
    
    @property   
    def __str__(self):
        return self.user_id.username + " " + str(self.date)
    
    """
    provides a URL for the given model
    """
    def get_absolute_url(self):
        
        return reverse('Log', args=[str(self.user_id)])

#food item relation
class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=50)
    calories = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    serving_size = models.IntegerField(default=0)
    
    
    class Meta():
        """
        configures default queryset by food name
        """
        ordering = ['food_name']
        

    @property 
    def __str__(self):
        return self.food_name + str(self.food_id)
    
    """
    provides URL for the given model
    """
    def get_absolute_url(self):
    
        return reverse('Food-Item', args=[str(self.food_id)]) 
    

#food entry for a given log
class FoodEntry(models.Model):
    food_id = models.ForeignKey('Food', on_delete=models.CASCADE)
    log_id = models.ForeignKey('Log', on_delete=models.CASCADE)
    time = models.TimeField(auto_now=False, auto_now_add=True)
    
    class Meta:
        """
        configures default ordering of queryset by time
        """
        ordering = ['time']
        
    """
    provides URL for the given model
    """
    def get_absolute_url(self):
    
        return reverse('Food-Entry', args=[str(self.food_id)])    
    
    
    @property
    def __str__(self):
            return self.food_id.food_name + " " + str(self.log_id.date)
        
        
      
    """
    Use post_save receiver to update and modify 
    the macro nutrient data based on serving size
    after the "Food" instance is saved
    
    Args:
        sender(Food): The model class
        instance(Food): The instance of the model being saved
        **kwargs: Additional keyword agruments
    
    Returns:
        
    """
    @receiver(post_save, sender=Food)
    def post_save_serving_size(sender,instance,true,**kwargs):
        
        # grab and set all of the macro data fields from "Food" instance
        serving_size = instance.serving_size
        calories = instance.calories
        protein = instance.protein
        fats = instance.fats
        carbs = instance.carbs
        
        # compute the update macro nutrient data based on the serving size field
        calories *= serving_size
        protein *= serving_size
        fats *= serving_size
        carbs *= serving_size

        