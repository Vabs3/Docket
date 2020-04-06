from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserEvent(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EventSlot(models.Model):
    event_id = models.ForeignKey(UserEvent, related_name='slot', on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)

    def __str__(self):
        return "{start_time = " + self.start_time + ", end_time" + self.end_time


class UserBooking(models.Model):
    user_id = models.ForeignKey(User, related_name='user_booking', on_delete=models.CASCADE)
    event_id = models.ForeignKey(UserEvent, related_name='event_booking', on_delete=models.CASCADE)
    slot_time = models.DateTimeField(blank=False)

    def __str__(self):
        return "{used_id = " + self.user_id + ", event_id" + self.event_id + ", slot_time" + self.slot_time

