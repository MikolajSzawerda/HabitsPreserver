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
from django.core.exceptions import ObjectDoesNotExist

'''
Fulfillment Action:
    Add new action, by choosing fulfillment from available habits
    When edit, create just new object
    Remove action
'''

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
        actions = HabitAction.user_objects.created_by(self.user)
        response = self.client.get(url)
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
    def test_updating_action(self):
        url = reverse('action', kwargs={'pk':1})
        action_data = self.client.get(url)
        action_data.data['fulfillment'] = 4
        response = self.client.put(url, action_data.data)
        assert response.status_code == status.HTTP_200_OK
        action = HabitAction.objects.get(pk=1)
        assert action.fulfillment.id == 4

    @pytest.mark.django_db
    def test_updating_action_forbidden(self):
        action = HabitAction.objects.get(pk=1)
        url = reverse('action', kwargs={'pk':1})
        action_data = self.client.get(url)
        action_data.data['fulfillment'] = 9
        response = self.client.put(url, action_data.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        up_action = HabitAction.objects.get(pk=1)
        assert action.fulfillment.id == up_action.fulfillment.id

    @pytest.mark.django_db
    def test_deleting_action(self):
        url = reverse('action', kwargs={'pk':1})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(ObjectDoesNotExist):
            action = HabitAction.objects.get(pk=1)


    @pytest.mark.django_db
    def test_retriving_forbidden_action(self):
        url = reverse('action', kwargs={'pk':7})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

class HabitTestsDislogged(APITestCase):
    fixtures = ["habits_managerAPI/fixtures/fixtures.json"]

    def setUp(self) -> None:
        self.json_action = json_action_obj()

    @pytest.mark.django_db
    def test_retriving_actions(self):
        url = reverse('actions')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_retriving_action(self):
        url = reverse('action', kwargs={'pk':1})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_creating_action(self):
        url = reverse('actions')
        data = self.json_action
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_deleting_action(self):
        url = reverse('action', kwargs={'pk':1})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


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

    @pytest.mark.django_db
    def test_creating_action(self):
        actions_num = len(HabitAction.objects.all())
        url = reverse('actions')
        data = self.json_action
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(HabitAction.objects.all()) == actions_num +1

    @pytest.mark.django_db
    def test_updating_action(self):
        url = reverse('action', kwargs={'pk':1})
        action_data = self.client.get(url)
        action_data.data['fulfillment'] = 4
        response = self.client.put(url, action_data.data)
        assert response.status_code == status.HTTP_200_OK
        action = HabitAction.objects.get(pk=1)
        assert action.fulfillment.id == 4

    @pytest.mark.django_db
    def test_deleting_action(self):
        url = reverse('action', kwargs={'pk':1})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(ObjectDoesNotExist):
            action = HabitAction.objects.get(pk=1)

