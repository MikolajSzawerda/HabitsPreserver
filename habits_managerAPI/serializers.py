from rest_framework.serializers import ModelSerializer
from .models import FulfillmentLevel, Habit, HabitFulfillment, HabitAction


class FulfillmentLevelSerializer(ModelSerializer):
    class Meta:
        model = FulfillmentLevel
        fields = '__all__'


class FulfillmentSerializer(ModelSerializer):
    class Meta:
        model = HabitFulfillment
        fields = ['id', 'name', 'fulfillment_level']


class HabitSerializer(ModelSerializer):
    fulfillments = FulfillmentSerializer(many=True)

    class Meta:
        model = Habit
        fields = ['id', 'name', 'description', 'fulfillments']

    def create(self, validated_data):
        user=self.context['request'].user
        fulfillemnts_data = validated_data.pop('fulfillments')
        habit = Habit.objects.create(user=user, **validated_data)
        for fulfillment in fulfillemnts_data:
            HabitFulfillment.objects.create(habit=habit, **fulfillment)
        return habit


class SUDOHabitSerializer(HabitSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'user', 'description', 'fulfillments']


class HabitActionSerializer(ModelSerializer):
    class Meta:
        model = HabitAction
        fields = '__all__'
