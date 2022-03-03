from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import FulfillmentLevel, Habit, HabitAction, HabitFulfillment
from .serializers import FulfillmentLevelSerializer, HabitSerializer, SUDOHabitSerializer, HabitActionSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsHabitCreator, IsHabitActionOwner
from django.db.models import Prefetch


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
    # serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsHabitCreator]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_superuser:
            return SUDOHabitSerializer
        return HabitSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Habit.objects.all()
        return Habit.objects.filter(user=user)

    def get_object(self):
        pk = self.kwargs['pk']
        obj = Habit.objects.get(pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj


class HabitActions(ModelViewSet):
    serializer_class = HabitActionSerializer
    permission_classes = [IsAuthenticated, IsHabitActionOwner]
