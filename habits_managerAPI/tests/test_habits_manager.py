from os import name
from django.urls import reverse
from habits_managerAPI.models import HabitFulfillment, Habit, FulfillmentLevel
from habits_managerAPI.serializers import HabitSerializer, FulfillmentSerializer, FulfillmentLevelSerializer
from rest_framework.test import APITestCase
from rest_framework import status
import pytest

class HabitTests(APITestCase):
    fixtures = ["habits_managerAPI/fixtures/fixtures.json"]

    @pytest.mark.django_db
    def test_getting_habits(self):
        url = reverse('habits')
        response = self.client.get(url, format="json")
        assert len(response.data) == 2
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_retreving_habit(self):
        url = reverse('habit', kwargs={'pk':1})
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Czysty kod'

    @pytest.mark.django_db
    def test_creating_habit(self):
        url = reverse('habits')
        level = FulfillmentLevel.objects.get(pk=1)
        fulfillments = HabitFulfillment.objects.filter(pk__in=[1,2,3])

        habit = Habit.objects.create(name="Test", description="test test")
        habit.fulfillemnts.set(fulfillments)
        data = HabitSerializer(habit)
        response = self.client.post(url, data.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED


