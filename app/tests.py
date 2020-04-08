from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient
from rest_framework.utils import json

from app.serializers import UserEventSerializer, EventSlotSerializer

# Create your tests here.


def setup_user():
    User = get_user_model()
    User.objects.create_user(
        'test',
        email='testuser@test.com',
        password='test'
    )
    User.objects.create_user(
        'test2',
        email='testuser2@test.com',
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
        self.event_uri = '/event/'
        self.event_detail_uri = '/event/1/'

    def test_create_event(self):
        self.client.login(username="test", password="test")
        params = {"name": "postman"}
        response = self.client.post(self.event_uri, params)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_event_list(self):
        self.client.login(username="test", password="test")
        response = self.client.get(self.event_uri)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_event_detail(self):
        self.client.login(username="test", password="test")
        response = self.client.get(self.event_detail_uri)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_event_detail_unauthorize(self):
        self.client.login(username="test2", password="test")
        response = self.client.get(self.event_detail_uri)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_event_update(self):
        self.client.login(username="test", password="test")
        params = {"name": "postman update"}
        response = self.client.put(self.event_detail_uri, params)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_event_update_unauthorize(self):
        self.client.login(username="test2", password="test")
        params = {"name": "postman update"}
        response = self.client.put(self.event_detail_uri, params)
        self.assertEqual(response.status_code, 403,
                         'Expected Response Code 403, received {0} instead.'
                         .format(response.status_code))

    def test_event_delete(self):
        self.client.login(username="test", password="test")
        response = self.client.delete(self.event_detail_uri)
        self.assertEqual(response.status_code, 204,
                         'Expected Response Code 204, received {0} instead.'
                         .format(response.status_code))

    def test_event_unauthorize(self):
        self.client.login(username="test2", password="test")
        response = self.client.delete(self.event_detail_uri)
        self.assertEqual(response.status_code, 403,
                         'Expected Response Code 403, received {0} instead.'
                         .format(response.status_code))


class TestEventSlots(APITestCase):
    def setUp(self):
        setup_user()
        create_event()
        self.client = APIClient()
        self.slot_uri = '/slot/'
        self.slot_delete_uri = '/slot/1/'

    def test_create_slot(self):
        self.client.login(username="test", password="test")
        params = [{
            "event_id": "1",
            "date": "2020-06-01",
            "start_time": "2020-06-01T12:00",
            "end_time": "2020-06-01T15:00"
        }]
        response = self.client.post(self.slot_uri, json.dumps(params), content_type='application/json')
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_create_slot_unauthorize(self):
        self.client.login(username="test2", password="test")
        params = [{
            "event_id": "1",
            "date": "2020-06-01",
            "start_time": "2020-06-01T12:00",
            "end_time": "2020-06-01T15:00"
        }]
        response = self.client.post(self.slot_uri, json.dumps(params), content_type='application/json')
        self.assertEqual(response.status_code, 403,
                         'Expected Response Code 403, received {0} instead.'
                         .format(response.status_code))

    def test_delete_slot(self):
        self.client.login(username="test", password="test")
        params = [{
            "event_id": "1",
            "date": "2020-06-01",
            "start_time": "2020-06-01T12:00",
            "end_time": "2020-06-01T16:00"
        }]
        self.client.post(self.slot_uri, json.dumps(params), content_type='application/json')
        response = self.client.delete(self.slot_delete_uri, json.dumps(params), content_type='application/json')
        self.assertEqual(response.status_code, 204,
                         'Expected Response Code 204, received {0} instead.'
                         .format(response.status_code))


class TestEventBooking(APITestCase):
    def setUp(self):
        setup_user()
        create_event()
        self.client = APIClient()
        self.book_uri = '/book/'
        self.book_update_uri = '/book/1/'
        self.book_delete_uri = '/book/1/'
        self.slot_uri = '/slot/'

    def test_book_event_invalid_time(self):
        self.client.login(username="test", password="test")
        params = {
            "event_id": "1",
            "slot_time": "2020-04-06T13:00"
        }
        response = self.client.post(self.book_uri, params)
        self.assertEqual(response.status_code, 400,
                         'Expected Response Code 400, received {0} instead.'
                         .format(response.status_code))

    def test_book_event(self):
        self.client.login(username="test", password="test")
        slot_params = [{
            "event_id": "1",
            "date": "2020-06-01",
            "start_time": "2020-06-01T12:00",
            "end_time": "2020-06-01T16:00"
        }]
        book_event_params = {
            "event_id": "1",
            "slot_time": "2020-06-01T13:00"
        }
        self.client.post(self.slot_uri, json.dumps(slot_params), content_type='application/json')
        response = self.client.post(self.book_uri, book_event_params)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_update_booking(self):
        self.client.login(username="test", password="test")
        slot_params = [{
            "event_id": "1",
            "date": "2020-06-01",
            "start_time": "2020-06-01T12:00",
            "end_time": "2020-06-01T16:00"
        }]
        book_event_params = {
            "event_id": "1",
            "slot_time": "2020-06-01T13:00"
        }
        updated_book_event_params = {
            "event_id": "1",
            "slot_time": "2020-06-01T15:00"
        }
        self.client.post(self.slot_uri, json.dumps(slot_params), content_type='application/json')
        # self.client.post(self.book_uri, book_event_params)
        response = self.client.put(self.book_update_uri, updated_book_event_params)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_update_booking_invalid_time(self):
        self.client.login(username="test", password="test")
        slot_params = [{
            "event_id": "1",
            "date": "2020-06-01",
            "start_time": "2020-06-01T12:00",
            "end_time": "2020-06-01T16:00"
        }]
        book_event_params = {
            "event_id": "1",
            "slot_time": "2020-06-01T13:00"
        }
        updated_book_event_params = {
            "event_id": "1",
            "slot_time": "2020-06-01T16:00"
        }
        self.client.post(self.slot_uri, json.dumps(slot_params), content_type='application/json')
        self.client.post(self.book_uri, book_event_params)
        response = self.client.put(self.book_update_uri, updated_book_event_params)
        self.assertEqual(response.status_code, 400,
                         'Expected Response Code 400, received {0} instead.'
                         .format(response.status_code))

    def test_delete_booking(self):
        self.client.login(username="test", password="test")
        slot_params = [{
            "event_id": "1",
            "date": "2020-06-01",
            "start_time": "2020-06-01T12:00",
            "end_time": "2020-06-01T16:00"
        }]
        book_event_params = {
            "event_id": "1",
            "slot_time": "2020-06-01T13:00"
        }
        updated_book_event_params = {
            "event_id": "1",
            "slot_time": "2020-06-01T15:00"
        }
        self.client.post(self.slot_uri, json.dumps(slot_params), content_type='application/json')
        self.client.post(self.book_uri, book_event_params)
        response = self.client.put(self.book_delete_uri, updated_book_event_params)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_booking_list(self):
        self.client.login(username="test", password="test")
        response = self.client.get(self.book_uri)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
