from rest_framework import serializers

from .models import UserEvent, EventSlot, UserBooking


class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = '__all__'


class EventSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventSlot
        fields = '__all__'


class UserBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBooking
        fields = '__all__'
