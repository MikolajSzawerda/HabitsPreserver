import rest_framework.serializers
from rest_framework.serializers import ModelSerializer
from .models import FulfillmentLevel


class FulfillmentLevelSerializer(ModelSerializer):
    class Meta:
        model = FulfillmentLevel
        fields = '__all__'

