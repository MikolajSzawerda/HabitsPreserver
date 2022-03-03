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
        'fulfillments': [
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


class CRUDOperations:
    '''
    Defintion of CRUD operation on Habit object
    '''
    def __init__(self, testObj):
        self.testingUnit = testObj

    def read(self, url):
        return self.testingUnit.client.get(url, format="json")

    def create(self, url):
        habit = self.testingUnit.json_habit
        return (self.testingUnit.client.post(url, habit, format="json"), habit)


class BaseTestUnit(APITestCase):
    '''
    Class defining data used in across all testing unit(admin, user, anon)
    '''
    fixtures = ["habits_managerAPI/fixtures/fixtures.json"]

    def setUp(self, testingUnit, user_data=None) -> None:
        self.json_habit = json_habit_obj()
        self.urls = urls()
        self.crud = CRUDOperations(testingUnit)
        if user_data:
            username = user_data.get('username', None)
            password = user_data.get('password', None)
            self.user = User.objects.get(username=username)
            self.client.login(username=username, password=password)


class HabitTestsLogged(BaseTestUnit):
    '''
    Login to db as normal user
    '''
    def setUp(self) -> None:
        user_data = {
            'username': "Polskipolak",
            'password': "chustka1234"
        }
        super().setUp(self, user_data)

    '''
    Retrieve from db all habits available to the user
    '''
    @pytest.mark.django_db
    def test_retrieving_habits(self):
        user_habits_number = len(Habit.objects.filter(user=self.user))
        response = self.crud.read(self.urls['habits'])
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == user_habits_number
    '''
    User cannot see what is his id
    '''
    @pytest.mark.django_db
    def test_not_getting_user_id_in_habit_view(self):
        response = self.crud.read(self.urls['habits'])
        with pytest.raises(KeyError):
            response.data[0]['user']

    '''
    Retrieve from db single habit obj, checking if it is available to the user
    '''
    @pytest.mark.django_db
    def test_retrieving_habit(self):
        url = reverse('habit', kwargs={'pk': 1})
        response = self.crud.read(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Czysty kod'

    @pytest.mark.django_db
    def test_retrieving_forbidden_habit_to_user(self):
        url = reverse('habit', kwargs={'pk': 3})
        response = self.crud.read(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_creating_habit(self):
        url = reverse('habits')
        habits_num = len(Habit.objects.all())
        response, habit = self.crud.create(url)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(Habit.objects.all()) == habits_num + 1
        assert len(response.data['fulfillments']) == len(habit['fulfillments'])

    @pytest.mark.django_db
    def test_updating_habit(self):
        url = reverse('habit', kwargs={'pk':1})
        fulfillments_num = len(HabitFulfillment.objects.all())
        habit = Habit.objects.get(pk=1)
        habit_serialized = HabitSerializer(habit).data
        habit_serialized['name']='Test test'
        response = self.client.put(url, habit_serialized, format="json")
        assert response.status_code == status.HTTP_200_OK
        habit = Habit.objects.get(pk=1)
        assert habit.name == 'Test test'
        assert fulfillments_num == len(HabitFulfillment.objects.all())

    @pytest.mark.django_db
    def test_updating_habit_fulfillemnt(self):
        url = reverse('habit', kwargs={'pk':1})
        habit = Habit.objects.get(pk=1)
        habit_serialized = HabitSerializer(habit).data
        habit_serialized['fulfillments'][0]['name']='test34'
        habit_serialized['fulfillments'].pop(1)
        response = self.client.put(url, habit_serialized, format="json")
        assert response.status_code == status.HTTP_200_OK
        habit = Habit.objects.get(pk=1)
        assert len(habit.fulfillments.all()) == 2
        assert habit.fulfillments.get(name='test34') is not None

    @pytest.mark.django_db
    def test_updating_habit__by_adding_fulfillemnt(self):
        url = reverse('habit', kwargs={'pk':1})
        habit = Habit.objects.get(pk=1)
        habit_serialized = HabitSerializer(habit).data
        fulfil = habit_serialized['fulfillments'].pop(1)
        fulfil.pop('id')
        fulfil['name'] = '2 rodziały'
        habit_serialized['fulfillments'].append(fulfil)
        response = self.client.put(url, habit_serialized, format="json")
        assert response.status_code == status.HTTP_200_OK
        habit = Habit.objects.get(pk=1)
        assert len(habit.fulfillments.all()) == 3

    @pytest.mark.django_db
    def test_updating_habit_fulfillemnt_id_preserve(self):
        url = reverse('habit', kwargs={'pk':1})
        habit = Habit.objects.get(pk=1)
        fulfillment_id = habit.fulfillments.first()
        habit_serialized = HabitSerializer(habit).data
        habit_serialized['fulfillments'].pop(1)
        response = self.client.put(url, habit_serialized, format="json")
        assert response.status_code == status.HTTP_200_OK
        habit = Habit.objects.get(pk=1)
        updated_fulfillment_id = habit.fulfillments.first()
        assert fulfillment_id == updated_fulfillment_id


    @pytest.mark.django_db
    def test_deleting_habit(self):
        url = reverse('habit', kwargs={'pk':1})
        habit_num = len(Habit.objects.all())
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(Habit.objects.all()) == habit_num - 1


class HabitTestsDislogged(BaseTestUnit):
    '''
    Trying to access db as anon
    '''
    def setUp(self) -> None:
        super().setUp(self)

    @pytest.mark.django_db
    def test_retrieving_habits(self):
        response = self.crud.read(self.urls['habits'])
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_retrieving_habit(self):
        url = reverse('habit', kwargs={'pk': 1})
        response = self.crud.read(url)
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


class HabitTestsAdmin(BaseTestUnit):
    '''
    Accessing db as admin
    '''
    def setUp(self) -> None:
        user_data = {
        'username' : "admin",
        'password' : "admin"
        }
        super().setUp(self, user_data)

    '''
    Retrieve from db all habits
    '''
    @pytest.mark.django_db
    def test_retrieving_habits(self):
        habits_number = len(Habit.objects.all())
        response = self.crud.read(self.urls['habits'])
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == habits_number


    @pytest.mark.django_db
    def test_admin_can_see_habit_owner(self):
        response = self.crud.read(self.urls['habits'])
        assert all('user' in x.keys() for x in response.data)

    @pytest.mark.django_db
    def test_retrieving_habit(self):
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