from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from app.models import UserEvent
from app.serializers import UserEventSerializer
from app.utility import parse_error


class UserEventController(viewsets.ModelViewSet):
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer

    def create(self, request, *args, **kwargs):
        try:
            if hasattr(request.data, '_mutable'):
                request.data._mutable = True
            request.data['created_by'] = request.user.id
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(parse_error(str(e)))

    def update(self, request, *args, **kwargs):
        try:
            event = self.get_object()
            if request.user != event.created_by:
                raise PermissionDenied("You do not have rights to update this event. Event - {}".format(event))
            if hasattr(request.data, '_mutable'):
                request.data._mutable = True
            request.data['created_by'] = request.user.id
            return super().update(request, *args, **kwargs)
        except PermissionDenied as e:
            return Response(parse_error(str(e)), status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(parse_error(str(e)))

    def destroy(self, request, *args, **kwargs):
        try:
            event = self.get_object()
            if request.user != event.created_by:
                raise PermissionDenied("You do not have rights to delete this event. Event  - {}".format(event))
            return super().destroy(request, *args, **kwargs)
        except PermissionDenied as e:
            return Response(parse_error(str(e)), status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(parse_error(str(e)))

    def list(self, request, *args, **kwargs):
        self.queryset = UserEvent.objects.filter(created_by=self.request.user)
        return super().list(request, *args, **kwargs)
