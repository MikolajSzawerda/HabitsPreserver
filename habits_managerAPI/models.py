from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class ActivityItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Habit(ActivityItem):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)


class FulfillmentLevel(ActivityItem):
    value = models.IntegerField(validators=[MinValueValidator(0),
                                            MaxValueValidator(3)])


class HabitFulfillment(ActivityItem):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE,
                              related_name='fulfillments')
    fulfillment_level = models.ForeignKey(FulfillmentLevel,
                                          on_delete=models.CASCADE)


class HabitAction(models.Model):
    fulfillment = models.ForeignKey(HabitFulfillment, on_delete=models.CASCADE)
    date = models.DateField()
