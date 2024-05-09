from django.db import models
from user.models import User
from django.urls import reverse
    
#user's macro goals
class Goal(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=True)
    calories = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    class Meta:
        """
        configures default ordering of queryset by date
        """
        ordering = ['date']
        app_label = 'tracking'
     
    
    @property 
    def __str__(self):
        return self.user.username + " " + str(self.date)
    """
    provides a URL for the given model
    """
    def get_absolute_url(self):
        
        return reverse('Goal', args=[str(self.user_id)])
    
"""
Model that holds a user's log for a given day 
Many-To-One relation: "User"
"""
class Log(models.Model):
    #total macros for the day has to be accumlated from the food entries
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=True)
    total_calories = models.IntegerField(default=0)
    total_protein = models.IntegerField(default=0)
    total_fat = models.IntegerField(default=0)
    total_carbs = models.IntegerField(default=0)
    
    class Meta:
        """
        configures default ordering of queryset by date
        """
        ordering = ["date"]
           
    # save method to calculate totals
    def save(self, *args, **kwargs):
        food = Meal.objects.filter(log_id=self)
        self.total_calories = sum(food.values_list('food_id__calories', flat=True))
        self.total_protein = sum(food.values_list('food_id__protein', flat=True))
        self.total_fat = sum(food.values_list('food_id__fat', flat=True))
        self.total_carbs = sum(food.values_list('food_id__carbs', flat=True))
        super().save(*args, **kwargs)
    
    @property   
    def __str__(self):
        return self.user.username + " " + str(self.date)
    
    """
    provides a URL for the given model
    """
    def get_absolute_url(self):
        
        return reverse('Log', args=[str(self.user_id)])

"""
Model that holds a meal for a given log
Many-To-One relation: "Food"
"""
class Meal(models.Model):
    log = models.ForeignKey('Log', on_delete=models.CASCADE)
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
        
# model that holds data for a food item
class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    meal = models.ForeignKey('Meal',on_delete=models.CASCADE, null=True) # set null to true to defined a food relation without connection
    food_name = models.CharField(max_length=50)
    serving_size = models.IntegerField(default=0)    
    calories = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        self.calories = self.calories * self.serving_size
        self.protein = self.protein * self.serving_size
        self.fat = self.fat * self.serving_size
        self.carbs = self.carbs * self.serving_size
        super().save(*args, **kwargs)
    
    
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
