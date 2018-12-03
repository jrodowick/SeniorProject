from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

EVENT_CHOICES = (
    ('Soccer', "Soccer"),
    ('Football', "Football"),
    ('Baseball', "Baseball"),
    ('Wiffleball', "Wiffleball"),
    ('Ultimate Frisbee', "Ultimate Frisbee"),
    ('Basketball', "Basketball"),
    ('Disc Golf', "Disc Golf"),
    ('Kickball', "Kickball"),
)

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    phone = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return str(self.user)

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


class Location(models.Model):
    name = models.CharField(max_length = 80)
    address = models.CharField(max_length = 50)
    city = models.CharField(max_length = 25)

    def __str__(self):
        return self.name

    def asDict(self):
        return {
            'name': self.name,
            'address': self.address,
            'city': self.city,
        }

class Event(models.Model):
    name = models.CharField(max_length = 50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add = True)
    date_of_event = models.DateField(blank = False)
    time_of_event = models.TimeField(blank = False)
    activity = models.CharField(choices = EVENT_CHOICES, max_length = 50)
    created_by = models.ForeignKey(User,  related_name='creator', on_delete = models.CASCADE)
    attendees = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def asDict(self):
        return {
            'name': self.name,
            'location': self.location,
            'date_created': self.date_created,
            'date_of_event': self.date_of_event,
            'time_of_event': self.time_of_event,
            'activity': self.activity,
            'created_by': self.created_by,
            'attendees': self.attendees,
            'id': self.id
        }

# class Event_Post(models.Models):
