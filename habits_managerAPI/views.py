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

    def retrieve(self, request, *args, **kwargs):
        obj = Habit.objects.get(pk=kwargs['pk'])
        self.check_object_permissions(request, obj)
        return Response(HabitSerializer(obj).data)


class HabitActions(ModelViewSet):
    serializer_class = HabitActionSerializer
    permission_classes = [IsAuthenticated, IsHabitActionOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return HabitAction.objects.all()
        return HabitAction.objects.filter(
            fulfillment__habit__user = user
        ).prefetch_related(
            Prefetch('fulfillment', queryset=HabitFulfillment.objects.filter(
                habit__user=user
            ).prefetch_related(
                Prefetch('habit', queryset=Habit.objects.filter(user=user)
                )))
        )

    def retrieve(self, request, *args, **kwargs):
        obj = HabitAction.objects.get(pk=kwargs['pk'])
        self.check_object_permissions(request, obj)
        return Response(HabitActionSerializer(obj).data)

    def create(self, request, *args, **kwargs):
        pk = request.data['fulfillment']
        fulfil = HabitFulfillment.objects.get(pk=pk)
        self.check_object_permissions(request, fulfil)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pk = request.data['fulfillment']
        fulfil = HabitFulfillment.objects.get(pk=pk)
        self.check_object_permissions(request, fulfil)
        return super().update(request, *args, **kwargs)