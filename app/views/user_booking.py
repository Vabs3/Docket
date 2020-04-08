from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from app.models import EventSlot, UserBooking
from app.serializers import UserBookingSerializer
from app.utility import parse_error


class BookEventController(viewsets.ModelViewSet):
    queryset = UserBooking.objects.all()
    serializer_class = UserBookingSerializer

    def validate_slot_time(self, data):
        valid_slot_duration = 3600
        slot_time = datetime.fromisoformat(data.get('slot_time'))
        available_slots = EventSlot.objects.filter(event_id=data['event_id'], date=str(slot_time.date()))
        is_valid_slot = False
        for slot in available_slots:
            start_time = slot.start_time.replace(tzinfo=None)
            end_time = slot.end_time.replace(tzinfo=None)
            time_duration = end_time - slot_time
            if start_time <= slot_time <= end_time and \
                    time_duration.seconds >= valid_slot_duration and time_duration.days >= 0:
                is_valid_slot = True
                break
        if not is_valid_slot:
            raise ValidationError("Please select a valid slot from event's slots.")

    def create(self, request, *args, **kwargs):
        try:
            if hasattr(request.data, '_mutable'):
                request.data._mutable = True
            request.data['user_id'] = request.user.id
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.validate_slot_time(request.data)
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(parse_error(str(e)), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(parse_error(str(e)))

    def update(self, request, *args, **kwargs):
        try:
            if hasattr(request.data, '_mutable'):
                request.data._mutable = True
            request.data['event_id'] = kwargs.get('pk')
            request.data['user_id'] = request.user.id
            booking = UserBooking.objects.get(user_id=request.user.id, event_id=request.data.get('event_id'))
            serializer = self.get_serializer(booking, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.validate_slot_time(request.data)
            self.perform_update(serializer)
            return Response(serializer.data)
        except ValidationError as e:
            return Response(parse_error(str(e)), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(parse_error(str(e)))

    def list(self, request, *args, **kwargs):
        self.queryset = UserBooking.objects.filter(user_id=self.request.user)
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            booking = UserBooking.objects.get(user_id=request.user.id, event_id=kwargs.get('pk'))
            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(parse_error(str(e)))
