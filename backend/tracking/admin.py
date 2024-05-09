from django.contrib import admin
from .models import Log, Goal, Food, Meal



#register the models with the admin site
admin.site.register(Log)
admin.site.register(Goal)
admin.site.register(Food)
admin.site.register(Meal)

