from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import UserEvent, EventSlot, UserBooking
from django.contrib.auth.models import User


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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

