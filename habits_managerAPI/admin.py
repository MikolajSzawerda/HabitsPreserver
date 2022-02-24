from django.contrib import admin
from .models import Habit, HabitFulfillment, FulfillmentLevel

# Register your models here.
admin.site.register(Habit)
admin.site.register(FulfillmentLevel)