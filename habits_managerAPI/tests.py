from django.http import response
from django.urls import reverse
from .models import HabitFulfillment, Habit, FulfillmentLevel
from rest_framework.test import APITestCase
from rest_framework import status
import pytest


def test_exmp():
    assert 1 == 1

# class HabitTests(APITestCase):
#     def test_create_habit(self):
#         url = reverse('habits')
#         data = {}
#         response = self.client.post(url, data, format="json")
#         assert response.status_code == status.HTTP_400_BAD_REQUEST