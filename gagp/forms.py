from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordResetForm
    )
from .models import Event, EVENT_CHOICES
import datetime

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.eamil = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    preferences = forms.MultipleChoiceField(choices=EVENT_CHOICES, required=False)
    phone = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'preferences',
            'phone'
        )
    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        user.userprofile.preferences = self.cleaned_data['preferences']
        user.userprofile.phone = self.cleaned_data['phone']

        if commit:
            user.save()
        return user

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_event'].widget.attrs.update({'class':'form-control'})
        self.fields['time_of_event'].widget.attrs.update({'class':'form-control'})
        self.fields['name'].widget.attrs.update({'class':'form-control'})
        self.fields['location'].widget.attrs.update({'class':'form-control'})
        self.fields['activity'].widget.attrs.update({'class':'form-control'})

    class Meta:
        model = Event
        fields = ('name',
                  'location',
                  'activity',
                  'date_of_event',
                  'time_of_event')
        widgets = {
            'date_of_event': DateInput(),
            'time_of_event': TimeInput(),
        }
    # def save(self, commit=True):
    #     event = super(EventForm, self).save(commit=False)
    #     event.name = self.cleaned_data['name']
    #     event.location = self.cleaned_data['location']
    #     event.activity = self.cleaned_data['activity']
    #     event.date_of_event = self.cleaned_data['date_of_event']
    #     event.time_of_event = self.cleaned_data['time_of_event']
    #
    #     if commit:
    #         event.save()
    #     return event

    def clean(self):
        date = self.cleaned_data['date_of_event']
        if date < datetime.date.today():
            raise forms.ValidationError("Date of event cannot be in the past!")
