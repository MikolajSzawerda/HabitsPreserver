from os import stat
from django.http import response
from django.urls import reverse
from habits_managerAPI.models import HabitFulfillment, Habit
from habits_managerAPI.serializers import HabitSerializer, FulfillmentSerializer
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
import pytest

'''
Habit:
    Create new habit:
        name
        description
        Create Fulfillments
    View habit:
        {User protection}
        name
        description
        Fulfillments
    Edit existing habit:
        {User protection}
        name
        description
        Edit Fulfillments
    Delete existing habit:
        {User protection}

Fulfillment:
    {Obj depend on Habit obj, therefore no need to check for permisson}
    Add new fulfillment to habit
    Edit existing fulfillment
    Remove existing fulfillment from habit

Fulfillment level:
    Const
'''


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


def urls():
    return {
        'habits': reverse('habits'),
    }


class HabitTestsLogged(APITestCase):
    fixtures = ["habits_managerAPI/fixtures/fixtures.json"]
    '''
    Login to db as normal user
    '''
    def setUp(self) -> None:
        username = "Polskipolak"
        password = "chustka1234"
        self.user = User.objects.get(username=username)
        self.client.login(username=username, password=password)
        self.json_habit = json_habit_obj()
        self.urls = urls()

    '''
    Retrieve from db all habits available to the user
    '''
    @pytest.mark.django_db
    def test_retrieving_habits(self):
        user_habits_number = len(Habit.objects.filter(user=self.user))
        response = self.client.get(self.urls['habits'], format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == user_habits_number

    @pytest.mark.django_db
    def test_not_getting_user_id_in_habit_view(self):
        response = self.client.get(self.urls['habits'], format="json")
        with pytest.raises(KeyError):
            habit = response.data[0]['user']

    '''
    Retrieve from db single habit obj, checking if it is available to the user
    '''
    @pytest.mark.django_db
    def test_retrieving_habit(self):
        url = reverse('habit', kwargs={'pk': 1})
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Czysty kod'

    @pytest.mark.django_db
    def test_retrieving_forbidden_habit_to_user(self):
        url = reverse('habit', kwargs={'pk': 3})
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
    def test_updating_habit(self):
        url = reverse('habit', kwargs={'pk':1})
        habit = Habit.objects.get(pk=1)
        habit_serialized = HabitSerializer(habit).data
        habit_serialized['name']='Test test'
        response = self.client.put(url, habit_serialized, format="json")
        assert response.status_code == status.HTTP_200_OK
        habit = Habit.objects.get(pk=1)
        assert habit.name == 'Test test'

    @pytest.mark.django_db
    def test_updating_habit_fulfillemnt(self):
        url = reverse('habit', kwargs={'pk':1})
        habit = Habit.objects.get(pk=1)
        habit_serialized = HabitSerializer(habit).data
        habit_serialized['fulfillemnts'][0]['name']='test34'
        habit_serialized['fulfillemnts'].pop(1)
        response = self.client.put(url, habit_serialized, format="json")
        assert response.status_code == status.HTTP_200_OK
        habit = Habit.objects.get(pk=1)
        assert len(habit.fulfillemnts.all()) == 2
        assert habit.fulfillemnts.get(name='test34') is not None

    @pytest.mark.django_db
    def test_updating_habit__by_adding_fulfillemnt(self):
        url = reverse('habit', kwargs={'pk':1})
        habit = Habit.objects.get(pk=1)
        habit_serialized = HabitSerializer(habit).data
        fulfil = habit_serialized['fulfillemnts'].pop(1)
        fulfil.pop('id')
        fulfil['name'] = '2 rodziały'
        habit_serialized['fulfillemnts'].append(fulfil)
        response = self.client.put(url, habit_serialized, format="json")
        assert response.status_code == status.HTTP_200_OK
        habit = Habit.objects.get(pk=1)
        assert len(habit.fulfillemnts.all()) == 3

    @pytest.mark.django_db
    def test_updating_habit_fulfillemnt_id_preserve(self):
        url = reverse('habit', kwargs={'pk':1})
        habit = Habit.objects.get(pk=1)
        fulfillment_id = habit.fulfillemnts.first()
        habit_serialized = HabitSerializer(habit).data
        habit_serialized['fulfillemnts'].pop(1)
        response = self.client.put(url, habit_serialized, format="json")
        assert response.status_code == status.HTTP_200_OK
        habit = Habit.objects.get(pk=1)
        updated_fulfillment_id = habit.fulfillemnts.first()
        assert fulfillment_id == updated_fulfillment_id


    @pytest.mark.django_db
    def test_deleting_habit(self):
        url = reverse('habit', kwargs={'pk':1})
        habit_num = len(Habit.objects.all())
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(Habit.objects.all()) == habit_num - 1


class HabitTestsDislogged(APITestCase):
    fixtures = ["habits_managerAPI/fixtures/fixtures.json"]

    def setUp(self) -> None:
        self.json_habit = json_habit_obj()

    @pytest.mark.django_db
    def test_getting_habits(self):
        url = reverse('habits')
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_retreving_habit(self):
        url = reverse('habit', kwargs={'pk': 1})
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_creating_habit(self):
        url = reverse('habits')
        habit = self.json_habit
        response = self.client.post(url, habit, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_deleting_habit(self):
        url = reverse('habit', kwargs={'pk':1})
        habit_num = len(Habit.objects.all())
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert len(Habit.objects.all()) == habit_num


class HabitTestsAdmin(APITestCase):
    fixtures = ["habits_managerAPI/fixtures/fixtures.json"]

    def setUp(self) -> None:
        username = "admin"
        password = "admin"
        self.user = User.objects.get(username=username)
        self.client.login(username=username, password=password)
        self.json_habit = json_habit_obj()

    @pytest.mark.django_db
    def test_getting_habits(self):
        habits_num = len(Habit.objects.all())
        url = reverse('habits')
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == habits_num

    @pytest.mark.django_db
    def test_habits_content(self):
        url = reverse('habits')
        response = self.client.get(url, format="json")
        assert all('user' in x.keys() for x in response.data)

    @pytest.mark.django_db
    def test_retreving_habit(self):
        url = reverse('habit', kwargs={'pk': 1})
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Czysty kod'

    @pytest.mark.django_db
    def test_updating_habit(self):
        url = reverse('habit', kwargs={'pk':1})
        habit = Habit.objects.get(pk=1)
        user = habit.user
        habit_serialized = HabitSerializer(habit).data
        habit_serialized['name']='Test test'
        response = self.client.put(url, habit_serialized, format="json")
        assert response.status_code == status.HTTP_200_OK
        habit = Habit.objects.get(pk=1)
        assert habit.user.username == user.username
        assert habit.name == 'Test test'

    @pytest.mark.django_db
    def test_updating_habit_fulfillemnt(self):
        url = reverse('habit', kwargs={'pk':1})
        habit = Habit.objects.get(pk=1)
        habit_serialized = HabitSerializer(habit).data
        habit_serialized['fulfillemnts'][0]['name']='test34'
        habit_serialized['fulfillemnts'].pop(1)
        response = self.client.put(url, habit_serialized, format="json")
        assert response.status_code == status.HTTP_200_OK
        habit = Habit.objects.get(pk=1)
        assert len(habit.fulfillemnts.all()) == 2
        assert habit.fulfillemnts.get(name='test34') is not None

    @pytest.mark.django_db
    def test_deleting_habit(self):
        url = reverse('habit', kwargs={'pk':1})
        habit_num = len(Habit.objects.all())
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(Habit.objects.all()) == habit_num - 1