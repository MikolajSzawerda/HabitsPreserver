from django.urls import reverse
from habits_managerAPI.models import HabitFulfillment, Habit
from habits_managerAPI.serializers import HabitSerializer, FulfillmentSerializer
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
import pytest


def json_habit_obj():
    obj = HabitSerializer(data={
        'name': 'Test',
        'description': 'test',
        'fulfillemnts': [
            {
                'name': 'Test1',
                'description': 'test1',
                'fulfillment_level': 1,
            },
            {
                'name': 'Test2',
                'description': 'test2',
                'fulfillment_level': 2,
            },
            {
                'name': 'Test3',
                'description': 'test3',
                'fulfillment_level': 3,
            },
        ]
    })
    obj.is_valid()
    return obj.data


class HabitTests(APITestCase):
    fixtures = ["habits_managerAPI/fixtures/fixtures.json"]

    def setUp(self) -> None:
        username = "Polskipolak"
        password = "chustka1234"
        self.user = User.objects.get(username=username)
        self.client.login(username=username, password=password)
        self.json_habit = json_habit_obj()

    @pytest.mark.django_db
    def test_getting_habits_logged(self):
        habits_num = len(Habit.objects.filter(user=self.user))
        url = reverse('habits')
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == habits_num

    @pytest.mark.django_db
    def test_getting_habits_not_logged(self):
        self.client.logout()
        url = reverse('habits')
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_retreving_habit(self):
        url = reverse('habit', kwargs={'pk': 1})
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Czysty kod'

    @pytest.mark.django_db
    def test_retreving_forbidden_habit_to_user(self):
        url = reverse('habit', kwargs={'pk': 3})
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_retreving_habit_not_logged(self):
        self.client.logout()
        url = reverse('habit', kwargs={'pk': 1})
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_creating_habit(self):
        url = reverse('habits')
        habits_num = len(Habit.objects.all())
        habit = self.json_habit
        response = self.client.post(url, habit, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert len(Habit.objects.all()) == habits_num + 1
        created_habit = Habit.objects.get(name="Test")
        assert len(created_habit.fulfillemnts.all()) == len(habit['fulfillemnts'])
        assert created_habit.description == habit['description']

    @pytest.mark.django_db
    def test_creating_habit_not_logged(self):
        self.client.logout()
        url = reverse('habits')
        habit = self.json_habit
        response = self.client.post(url, habit, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
