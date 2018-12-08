from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Location)
admin.site.register(Event)
admin.site.register(Event_Post)
