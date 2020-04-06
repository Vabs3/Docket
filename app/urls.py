from django.urls import path

from app.views import CreateEvent, AddEventAvailableSlot, UserEventDetail, UserEventList, EventSlotDays, \
    EventSlotHours, UserCreate, LoginView, BookEvent, UserBookingList

urlpatterns = [
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    path("create-event/", CreateEvent.as_view(), name="create_event"),
    path("add-slot/", AddEventAvailableSlot.as_view(), name="add_slot"),
    path("events/<int:pk>", UserEventDetail.as_view(), name="get_event_detail"),
    path("events/", UserEventList.as_view(), name="get_event_list"),
    path("slots/<int:event_id>/<str:date>/", EventSlotHours.as_view(), name="get_hour_slots"),
    path("slots/<int:event_id>/", EventSlotDays.as_view(), name="get_day_slots"),
    path("book-event/", BookEvent.as_view(), name="book_event"),
    path("bookings/", UserBookingList.as_view(), name="user_bookings"),
]
