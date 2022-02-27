from os import stat
from django.http import response
from django.urls import reverse
from habits_managerAPI.models import HabitAction, HabitFulfillment, Habit
from habits_managerAPI.serializers import HabitActionSerializer, HabitSerializer, FulfillmentSerializer
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
import pytest
from django.db.models import Prefetch, FilteredRelation, Q


def json_action_obj():
    obj = HabitActionSerializer(data={
        "date": "2022-01-27",
        "fulfillment": 6
    })
    obj.is_valid()
    return obj.data


def json_forbidden_action_obj():
    obj = HabitActionSerializer(data={
        "date": "2022-01-27",
        "fulfillment": 8
    })
    obj.is_valid()
    return obj.data


class HabitTestsLogged(APITestCase):
    fixtures = ["habits_managerAPI/fixtures/fixtures.json"]

    def setUp(self) -> None:
        username = "Polskipolak"
        password = "chustka1234"
        self.user = User.objects.get(username=username)
        self.client.login(username=username, password=password)
        self.json_action = json_action_obj()
        self.json_forbidden_action = json_forbidden_action_obj()

    @pytest.mark.django_db
    def test_retriving_actions(self):
        url = reverse('actions')
        response = self.client.get(url)
        actions = HabitAction.objects.filter(
            fulfillment__habit__user = self.user
        ).prefetch_related(
            Prefetch('fulfillment', queryset=HabitFulfillment.objects.filter(
                habit__user=self.user
            ).prefetch_related(
                Prefetch('habit', queryset=Habit.objects.filter(user=self.user)
                )))
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(actions)

    @pytest.mark.django_db
    def test_retriving_action(self):
        url = reverse('action', kwargs={'pk':1})
        response = self.client.get(url)
        action = HabitAction.objects.get(pk=1)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['fulfillment'] == action.fulfillment.id

    @pytest.mark.django_db
    def test_creating_forbidden_action(self):
        actions_num = len(HabitAction.objects.all())
        url = reverse('actions')
        data = self.json_forbidden_action
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert len(HabitAction.objects.all()) == actions_num

    @pytest.mark.django_db
    def test_creating_action(self):
        actions_num = len(HabitAction.objects.all())
        url = reverse('actions')
        data = self.json_action
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(HabitAction.objects.all()) == actions_num +1

    @pytest.mark.django_db
    def test_retriving_forbidden_action(self):
        url = reverse('action', kwargs={'pk':7})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

class HabitTestsDislogged(APITestCase):
    fixtures = ["habits_managerAPI/fixtures/fixtures.json"]

    def setUp(self) -> None:
        self.json_action = json_action_obj()


class HabitTestsAdmin(APITestCase):
    fixtures = ["habits_managerAPI/fixtures/fixtures.json"]

    def setUp(self) -> None:
        username = "admin"
        password = "admin"
        self.user = User.objects.get(username=username)
        self.client.login(username=username, password=password)
        self.json_action = json_action_obj()

    @pytest.mark.django_db
    def test_retriving_actions(self):
        url = reverse('actions')
        response = self.client.get(url)
        actions = HabitAction.objects.all()
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(actions)

