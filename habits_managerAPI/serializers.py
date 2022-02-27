from rest_framework.serializers import ModelSerializer, IntegerField
from .models import FulfillmentLevel, Habit, HabitFulfillment, HabitAction
from .utils import get_pks_to_delete

class FulfillmentLevelSerializer(ModelSerializer):
    class Meta:
        model = FulfillmentLevel
        fields = '__all__'


class FulfillmentSerializer(ModelSerializer):
    id = IntegerField(required=False)
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
        up_fulfillemnts = validated_data.get('fulfillemnts')
        serialized_insance_fulfill = FulfillmentSerializer(instance.fulfillemnts, many=True).data
        pks_to_delete = get_pks_to_delete(serialized_insance_fulfill,
                                          up_fulfillemnts)
        for fulfillement in up_fulfillemnts:
            id = fulfillement.get('id', None)
            if id:
                instance_fulfill = HabitFulfillment.objects.get(pk=id)
                instance_fulfill.name = fulfillement.get('name', instance_fulfill.name)
                instance_fulfill.description = fulfillement.get('description', instance_fulfill.description)
                instance_fulfill.fulfillment_level = fulfillement.get('fulfillment_level', instance_fulfill.fulfillment_level)
                instance_fulfill.save()
                continue
            HabitFulfillment.objects.create(habit=instance, **fulfillement)
        for pk in pks_to_delete:
            fulfil = HabitFulfillment.objects.get(pk=pk)
            fulfil.delete()
        instance.save()
        return instance


class SUDOHabitSerializer(HabitSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'user', 'description', 'fulfillemnts']

    def create(self, validated_data):
        pass


class HabitActionSerializer(ModelSerializer):
    class Meta:
        model = HabitAction
        fields = '__all__'
