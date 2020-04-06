from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

# Create your tests here.
from app.serializers import UserEventSerializer, EventSlotSerializer


def setup_user():
    User = get_user_model()
    return User.objects.create_user(
        'test',
        email='testuser@test.com',
        password='test'
    )


def create_event():
    data = {
        "name": "interview",
        "created_by": "1",
    }
    event_serializer = UserEventSerializer(data=data)
    event_serializer.is_valid()
    event_serializer.save()


class TestUserEvent(APITestCase):
    def setUp(self):
        setup_user()
        create_event()
        self.client = APIClient()
        self.event_list_uri = '/events/'
        self.create_event_uri = '/create-event/'
        self.event_detail_uri = '/events/1'

    def test_create_event(self):
        self.client.login(username="test", password="test")
        params = {
            "name": "postman",
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

    def test_event_detail(self):
        self.client.login(username="test", password="test")
        response = self.client.get(self.event_detail_uri)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))


class TestEventSlots(APITestCase):
    def setUp(self):
        setup_user()
        self.client = APIClient()
        self.add_slot_uri = '/add-slot/'

    def test_create_slot(self):
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


class TestEventBooking(APITestCase):
    def setUp(self):
        setup_user()
        create_event()
        self.client = APIClient()
        self.booking_list_uri = '/bookings/'
        self.book_event_uri = '/book-event/'

    def test_book_event(self):
        self.client.login(username="test", password="test")
        params = {
            "user_id": "1",
            "event_id": "1",
            "slot_time": "2020-04-06T13:00"
        }
        response = self.client.post(self.book_event_uri, params)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_booking_list(self):
        self.client.login(username="test", password="test")
        response = self.client.get(self.booking_list_uri)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

