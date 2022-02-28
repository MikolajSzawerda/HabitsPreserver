from curses.panel import update_panels
from functools import partial
from rest_framework.serializers import ModelSerializer, IntegerField, ListSerializer
from .models import FulfillmentLevel, Habit, HabitFulfillment, HabitAction
from .utils import get_pks_to_delete

class FulfillmentLevelSerializer(ModelSerializer):
    class Meta:
        model = FulfillmentLevel
        fields = '__all__'


# class FulfillmentsListSerializer(ListSerializer):

#     def update(self, instance, validated_data):
#         fulfillments = instance.all()
#         fulfillments_mapping = {fulfill.id : fulfill for fulfill in fulfillments}
#         updated_data = []
#         ids = set()
#         for fulfill in validated_data:
#             if 'id' in fulfill.keys():
#                 id = fulfill.get('id')
#                 ids.add(id)
#                 updated_obj = self.child.update(fulfillments_mapping[id], fulfill)
#                 updated_data.append(updated_obj)
#             else:
#                 updated_data.append(self.child.create(fulfill))
#         for id, fulfill in fulfillments_mapping.items():
#             if id not in ids:
#                 fulfill.delete()
#         return updated_data


class FulfillmentSerializer(ModelSerializer):
    # id = IntegerField(required=False)
    # fulfillment_level = FulfillmentLevelSerializer()
    class Meta:
        model = HabitFulfillment
        fields = '__all__'
        # list_serializer_class = FulfillmentsListSerializer
        # depth = 1

    # def create(self, validated_data):
    #     name = validated_data.get('fulfillment_level')['name']
    #     # validated_data.pop('fulfillment_level')
    #     fulfillment_level = FulfillmentLevel.objects.get(name=name)
    #     return super().create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     name = validated_data.get('fulfillment_level')['name']
    #     instance.fulfillment_level = FulfillmentLevel.objects.get(name=name)
    #     instance.save()
    #     return instance


class HabitSerializer(ModelSerializer):
    fulfillments = FulfillmentSerializer(many=True)
    class Meta:
        model = Habit
        fields = ['id', 'name', 'description', 'fulfillments']

    # def create(self, validated_data):
    #     user=self.context['request'].user
    #     fulfillemnts_data = validated_data.pop('fulfillemnts')
    #     habit = Habit.objects.create(user=user, **validated_data)
    #     for fulfillemnt in fulfillemnts_data:
    #         HabitFulfillment.objects.create(habit=habit, **fulfillemnt)
    #     return habit


    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data.get('description', instance.description)
    #     fulfillments_to_update = validated_data.get('fulfillemnts')
    #     fulfillments = instance.fulfillemnts
    #     serialized_fulfillments = FulfillmentSerializer(fulfillments, data=fulfillments_to_update, many=True, partial=True)
    #     serialized_fulfillments.is_valid()
    #     new_fulfillments = serialized_fulfillments.save()
    #     instance.fulfillemnts.set(new_fulfillments)
    #     # up_fulfillemnts = validated_data.get('fulfillemnts')
    #     # serialized_insance_fulfill = FulfillmentSerializer(instance.fulfillemnts, many=True).data
    #     # for fulfillement in up_fulfillemnts:
    #     #     id = fulfillement.get('id', None)
    #     #     if id:
    #     #         instance_fulfill = HabitFulfillment.objects.get(pk=id)
    #     #         instance_fulfill.name = fulfillement.get('name', instance_fulfill.name)
    #     #         instance_fulfill.description = fulfillement.get('description', instance_fulfill.description)
    #     #         instance_fulfill.fulfillment_level = fulfillement.get('fulfillment_level', instance_fulfill.fulfillment_level)
    #     #         instance_fulfill.save()
    #     #         continue
    #     #     HabitFulfillment.objects.create(habit=instance, **fulfillement)
    #     # pks_to_delete = get_pks_to_delete(serialized_fulfillments.data, fulfillments)
    #     # for pk in pks_to_delete:
    #     #     fulfil = HabitFulfillment.objects.get(pk=pk)
    #     #     fulfil.delete()
    #     instance.save()
    #     return instance


class SUDOHabitSerializer(HabitSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'user', 'description', 'fulfillments']

    # def create(self, validated_data):
    #     pass


class HabitActionSerializer(ModelSerializer):
    class Meta:
        model = HabitAction
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     instance.fulfillment = validated_data.get('fulfillment', instance.fulfillment)
    #     instance.date = validated_data.get('date', instance.date)
    #     instance.save()
    #     return instance
