from rest_framework.serializers import ModelSerializer, IntegerField, ListSerializer, PrimaryKeyRelatedField
from .models import FulfillmentLevel, Habit, HabitFulfillment, HabitAction

class FulfillmentLevelSerializer(ModelSerializer):
    id = IntegerField(required=False)

    class Meta:
        model = FulfillmentLevel
        fields = '__all__'


class FulfillmentListSerializer(ListSerializer):
    def update(self, instance, validated_data):
        fulfillment_mapping = {fulfillment.id: fulfillment for fulfillment in instance.all()}
        data_mapping = {}
        for i, item in enumerate(validated_data, 1):
            try:
                data_mapping[item['id']] = item
            except KeyError:
                data_mapping[-i] = item
        ret = []
        for book_id, data in data_mapping.items():
            book = fulfillment_mapping.get(book_id, None)
            id = data['fulfillment_level']['id']
            level = FulfillmentLevel.objects.get(pk=id)
            data['fulfillment_level']=level
            if book is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(book, data))

        for book_id, book in fulfillment_mapping.items():
            if book_id not in data_mapping:
                book.delete()

        return ret


class FulfillmentSerializer(ModelSerializer):
    id = IntegerField(required=False)
    fulfillment_level = PrimaryKeyRelatedField(queryset=FulfillmentLevel.objects.all())

    class Meta:
        model = HabitFulfillment
        fields = ['id', 'name', 'description', 'fulfillment_level']
        list_serializer_class = FulfillmentListSerializer
        # depth = 1


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


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        fulfillments = validated_data.get('fulfillments')
        updated_fulfillments = FulfillmentSerializer(instance.fulfillments, data=fulfillments, many=True)
        updated_fulfillments.is_valid()
        updated_fulfillments.save(habit=instance)
        instance.save()
        return instance


class SUDOHabitSerializer(HabitSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'user', 'description', 'fulfillments']


class HabitActionSerializer(ModelSerializer):
    class Meta:
        model = HabitAction
        fields = '__all__'
