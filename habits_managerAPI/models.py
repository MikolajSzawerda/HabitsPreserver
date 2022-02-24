from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ActivityItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name



class Habit(ActivityItem):
   pass


class FulfillmentLevel(ActivityItem):
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])


class HabitFulfillment(ActivityItem):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    fulfillment_level = models.ForeignKey(FulfillmentLevel, on_delete=models.CASCADE)