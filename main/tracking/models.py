from typing import Iterable
from django.db import models
from user.models import User
from django.urls import reverse
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
    
"""
    Model that represents a user's target for macronutrient intake  
"""
class Target(models.Model):
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
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
        
        return reverse('Target', args=[str(self.user_id)])
    
"""
    Model that represents a user's macronutrient data log for a given day
"""
class Log(models.Model):
    
    # model fields
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=True)
    total_calories = models.IntegerField(default=0)
    total_protein = models.IntegerField(default=0)
    total_fat = models.IntegerField(default=0)
    total_carbs = models.IntegerField(default=0)
    
    """
        Internal class that changes the behavior of model fields
    """
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
    
    """
        Internal class that changes the behavior of model fields
    """
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
    
    """
        Internal class that changes the behavior of model fields
    """
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
    def post_save_serving_size(sender, instance, true, **kwargs):
        
        serving_size = 0
        calories = 0
        protein = 0
        fats = 0
        carbs = 0
        
        # check if the instance "Food" was created and set
        if true:
            serving_size = instance.serving_size
            calories = instance.calories
            protein = instance.protein
            fats = instance.fats
            carbs = instance.carbs
        else:
            raise Exception("The Food model instance was not created")
        
        # compute the update macro nutrient data based on the serving size field
        calories *= serving_size
        protein *= serving_size
        fats *= serving_size
        carbs *= serving_size
        
        
    """
        Use the pre save method to compute the macronutrient totals
        from all related Food Entries and store in the "Log" relation
    """

    @receiver(pre_save,sender=Log)    
    def pre_save_total_macros(sender, instance, true, **kwargs):
        
        # declare variables to hold the instance model's variables
        total_calories = 0
        total_protein = 0
        total_fats = 0
        total_carbs = 0
        
         
        