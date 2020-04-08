from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import UserEvent, EventSlot
from app.serializers import EventSlotSerializer
from app.utility import parse_error


class EventSlotController(APIView):
    serializer_class = EventSlotSerializer

    def validate_slot_duration(self, slots):
        valid_duration_in_seconds = 3600
        for slot in slots:
            start_time = datetime.fromisoformat(slot.get('start_time'))
            end_time = datetime.fromisoformat(slot.get('end_time'))
            date = datetime.fromisoformat(slot.get('date'))
            time_diff = end_time - start_time
            if time_diff.seconds < valid_duration_in_seconds or time_diff.days < 0 or \
                    start_time.date() != end_time.date() or start_time.date() != date.date():
                raise ValidationError("Time duration should be between 1 - 24 hours,"
                                      " and date should be equal to start_time and end_time date")

    def validate_user_permissions(self, request):
        for slot in request.data:
            event = UserEvent.objects.get(pk=slot.get('event_id'))
            if request.user != event.created_by:
                raise PermissionDenied(
                    'You do not have rights to update/delete this event\'s slots. Event name - {}'.format(event))

    def delete_slots_util(self, slots):
        for slot in slots:
            self.delete_slots(slot.get('date'), slot.get('event_id'))

    def delete_slots(self, date, event_id):
        for slot in EventSlot.objects.filter(date=date, event_id=event_id):
            slot.delete()

    def validate_and_create_slots(self, request):
        data = request.data
        self.validate_slot_duration(data)
        serializer = EventSlotSerializer(data=data, many=True)
        if serializer.is_valid():
            self.validate_user_permissions(request)
            self.delete_slots_util(data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_event_slot_list(self, event_id):
        queryset = EventSlot.objects.filter(event_id=event_id)
        serializer = EventSlotSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_event_slot_list_for_date(self, event_id, date):
        queryset = EventSlot.objects.filter(event_id=event_id, date=date)
        serializer = EventSlotSerializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        try:
            event_id = self.kwargs.get("event_id")
            date = self.kwargs.get("date")
            if event_id and date:
                return self.get_event_slot_list_for_date(event_id, date)
            elif event_id:
                return self.get_event_slot_list(event_id)
            else:
                return Response(parse_error("Missing event_id in request", status=status.HTTP_400_BAD_REQUEST))
        except Exception as e:
            return Response(parse_error(str(e)))

    def post(self, request):
        try:
            return self.validate_and_create_slots(request)
        except PermissionDenied as e:
            return Response(parse_error(str(e)), status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response(parse_error(str(e)), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(parse_error(str(e)))

    def delete(self, request, *args, **kwargs):
        try:
            event_id = self.kwargs.get("event_id")
            for row in request.data:
                row['event_id'] = event_id
            self.validate_user_permissions(request)
            self.delete_slots_util(request.data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied as e:
            return Response(parse_error(str(e)), status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(parse_error(str(e)))
