from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
    PasswordResetForm
    )
from .models import Event, EVENT_CHOICES, UserProfile
import datetime

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget = forms.TextInput(attrs={
        'class':'form-control',
        'type':'username',
        'placeholder':'Username',
        })
    )
    email = forms.EmailField(
        label = 'Email',
        required = True,
        widget = forms.TextInput(attrs={
        'class':'form-control',
        'type':'email',
        'placeholder':'Email address',
        })
    )
    password1 = forms.CharField(
        widget = forms.TextInput(attrs={
        'class':'form-control',
        'type':'password',
        'placeholder':'Password',
        })
    )
    password2 = forms.CharField(
        widget = forms.TextInput(attrs={
        'class':'form-control',
        'type':'password',
        'placeholder':'Confirm Password',
        })
    )

    def save(self, commit = True):
        return User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )
    email = forms.EmailField(
        label = 'Email',
        required = True,
        widget = forms.TextInput(attrs={
        'class':'form-control',
        'type':'email',
        'placeholder':'Email address',
        })
    )
    first_name = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'First Name',
        })
    )
    last_name = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Last Name',
        })
    )


class EditDetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preferences'].widget.attrs.update({'class':'form-control'})
    class Meta:
        model = UserProfile
        fields = (
            'preferences',
            'phone'
        )

    preferences = forms.MultipleChoiceField(
        choices=EVENT_CHOICES,
        required=False,
    )
    phone = forms.IntegerField(
        required=False,
        widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Phone Number'
        })
    )

class ChangePassForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password1',
            'new_password2'
        )
    old_password = forms.CharField(
        widget = forms.TextInput(attrs={
        'class':'form-control',
        'type':'password',
        'placeholder':'Old Password',
        })
    )
    new_password1 = forms.CharField(
        widget = forms.TextInput(attrs={
        'class':'form-control',
        'type':'password',
        'placeholder':'New Password',
        })
    )
    new_password2 = forms.CharField(
        widget = forms.TextInput(attrs={
        'class':'form-control',
        'type':'password',
        'placeholder':'Confirm New Password',
        })
    )


## Used for date format on event form
class DateInput(forms.DateInput):
    input_type = 'date'

## Used for time input on event form
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
