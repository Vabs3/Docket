from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import UserEvent, EventSlot
from app.serializers import UserEventSerializer, EventSlotSerializer, UserSerializer

from django.contrib.auth import authenticate


# Create your views here.

class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class CreateEvent(generics.CreateAPIView):
    serializer_class = UserEventSerializer


# also add functionality of update. in that case only user who created that event can update slot.
class AddEventAvailableSlot(APIView):
    serializer_class = EventSlotSerializer

    def post(self, request):
        data = request.data
        serializer = EventSlotSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEventList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = UserEvent.objects.filter(created_by=self.request.user)
        return queryset

    serializer_class = UserEventSerializer


class UserEventDetail(generics.RetrieveDestroyAPIView):
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer


class EventSlotDays(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = EventSlot.objects.filter(event_id=self.kwargs["event_id"])
        return queryset

    serializer_class = EventSlotSerializer


class EventSlotHours(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = EventSlot.objects.filter(event_id=self.kwargs["event_id"], date=self.kwargs["date"])
        return queryset

    serializer_class = EventSlotSerializer

