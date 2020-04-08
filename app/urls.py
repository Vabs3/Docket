from django.urls import path
from rest_framework.routers import DefaultRouter

from app.views import UserEventController, BookEventController, UserCreate, LoginView, EventSlotController

router = DefaultRouter()
router.register('event', UserEventController, basename='event')
router.register('book', BookEventController, basename='book')

urlpatterns = [
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    path("slot/<int:event_id>/<str:date>/", EventSlotController.as_view(), name="get_event_slots_on_date"),
    path("slot/<int:event_id>/", EventSlotController.as_view(), name="get_event_slots"),
    path("slot/", EventSlotController.as_view(), name="slot"),
]

urlpatterns += router.urls

