from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import FulfillmentLevel, Habit
from .serializers import FulfillmentLevelSerializer, HabitSerializer


class Index(APIView):
    def get(self, request):
        endpoints = {
            'levels': '/levels',
            'habits': '/habits/<int:pk>',
        }
        return Response(endpoints)


class FulfillmentLevels(ListAPIView):
    queryset = FulfillmentLevel.objects.all()
    serializer_class = FulfillmentLevelSerializer


class Habits(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer