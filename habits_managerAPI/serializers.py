from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import FulfillmentLevel, Habit, HabitFulfillment


class FulfillmentLevelSerializer(ModelSerializer):
    class Meta:
        model = FulfillmentLevel
        fields = '__all__'


class FulfillmentSerializer(ModelSerializer):
    class Meta:
        model = HabitFulfillment
        fields = ['id', 'name', 'fulfillment_level']


class HabitSerializer(ModelSerializer):
    fulfillemnts = FulfillmentSerializer(many=True)
    class Meta:
        model = Habit
        fields = ['id', 'name', 'description', 'fulfillemnts']

    def create(self, validated_data):
        user=self.context['request'].user
        fulfillemnts_data = validated_data.pop('fulfillemnts')
        habit = Habit.objects.create(user=user, **validated_data)
        for fulfillemnt in fulfillemnts_data:
            HabitFulfillment.objects.create(habit=habit, **fulfillemnt)
        return habit


class SUDOHabitSerializer(ModelSerializer):
    fulfillemnts = FulfillmentSerializer(many=True)
    class Meta:
        model = Habit
        fields = ['id', 'name', 'user', 'description', 'fulfillemnts']

    def create(self, validated_data):
        user=self.context['request'].user
        fulfillemnts_data = validated_data.pop('fulfillemnts')
        habit = Habit.objects.create(user=user, **validated_data)
        for fulfillemnt in fulfillemnts_data:
            HabitFulfillment.objects.create(habit=habit, **fulfillemnt)
        return habit
