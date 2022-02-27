from django.contrib import admin
from .models import Habit, HabitFulfillment, FulfillmentLevel, HabitAction

# Register your models here.
admin.site.register(Habit)
admin.site.register(FulfillmentLevel)
admin.site.register(HabitFulfillment)
admin.site.register(HabitAction)