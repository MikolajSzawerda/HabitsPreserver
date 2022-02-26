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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        up_fulfillemnts = validated_data.get('fulfillemnts', instance.fulfillemnts)
        for ful in instance.fulfillemnts.all():
            ful.delete()
        for fulfillement in up_fulfillemnts:
            HabitFulfillment.objects.create(habit=instance, **fulfillement)
        instance.save()
        return instance


class SUDOHabitSerializer(HabitSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'user', 'description', 'fulfillemnts']

    def create(self, validated_data):
        pass

