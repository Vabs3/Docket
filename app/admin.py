from django.contrib import admin

# Register your models here.

from .models import UserEvent, EventSlot, UserBooking

admin.site.register(UserEvent)
admin.site.register(EventSlot)
admin.site.register(UserBooking)
