from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient


# Create your tests here.


class TestUserEvent(APITestCase):
    def setUp(self):
        TestUserEvent.setup_user()
        self.client = APIClient()
        self.event_list_uri = '/events/'
        self.create_event_uri = '/create-event/'

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_create_event(self):
        self.client.login(username="test", password="test")
        params = {
            "name": "interview",
            "created_by": "1"
        }
        response = self.client.post(self.create_event_uri, params)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_event_list(self):
        self.client.login(username="test", password="test")
        response = self.client.get(self.event_list_uri)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))


class TestEventSlots(APITestCase):
    def setUp(self):
        TestUserEvent.setup_user()
        self.client = APIClient()
        self.add_slot_uri = '/add-slot/'

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_create_event(self):
        self.client.login(username="test", password="test")
        params = {
                "event_id": "1",
                "date": "2020-06-01",
                "start_time": "2020-06-01T12:00",
                "end_time": "2020-06-01T15:00"
            }
        response = self.client.post(self.add_slot_uri, params)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

