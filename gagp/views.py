from django.shortcuts import render, redirect, HttpResponse
from .forms import (
    RegistrationForm,
    EditProfileForm,
    EventForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash
from .models import *
import json
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime



# Create your views here.
def index(request):
    selected = 'home'
    args = {'selected':selected}
    return render(request, 'index.html', args)

def locations(request):
    events = Event.objects.all()
    if request.method == 'POST':
        form = EventForm(request.POST, instance=request.user)
        if(form.is_valid()):
            mod_entry = Event(
                name = form.cleaned_data['name'],
                location = form.cleaned_data['location'],
                date_of_event = form.cleaned_data['date_of_event'],
                activity = form.cleaned_data['activity'],
                time_of_event = form.cleaned_data['time_of_event'],
                created_by = request.user
            )
            mod_entry.save()
            args = {'events':events, 'form':form}
            return render(request, 'locations.html', args)
        else:
            return redirect('/locations')
    else:
        form = EventForm()
        args = {'events':events,'form':form}
        return render(request, 'locations.html', args)

def view_event(request, event_id):
    # event_id = request.GET.get('id')
    if request.method == 'GET':
        event = Event.objects.get(id=event_id)
        users = event.attendees.all().values()
        args = {'event':event,'users':users}
        return render(request, 'event_info.html', args)

def join_event(request, event_id):
    # user = request.user.username
    event = Event.objects.get(id=event_id)
    event.attendees.add(request.user)
    print(event)
    print(event.attendees.all())
    return redirect('/profile')

def add_to_calendar(request, event_id):
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    #
    # event = Event.objects.get(id=event_id)
    # dict = event.asDict()
    # dict['location'] = dict['location'].asDict()
    # dict['date_of_event'] = str(dict['date_of_event'])
    #
    # event = {
    #     'summary': 'Test Summary',
    #     'location': 'Test Location',
    #     'start': {
    #     'dateTime': '2018-10-31T09:00:00-07:00',
    #     'timeZone': 'America/Los_Angeles',
    #       },
    #       'end': {
    #         'dateTime': '2018-11-01T17:00:00-07:00',
    #         'timeZone': 'America/Los_Angeles',
    #     }
    # }
    # event = service.events().insert(calendarId='primary', body=event).execute()
    # print('Event created: %s' % (event.get('htmlLink')))

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    return redirect('/events/view/' + event_id)

def get_data(request):
    if(request.method == 'POST'):
        locations = Location.objects.all()
        events = Event.objects.all()
        location_and_events = []
        location_results = []
        event_results = []
        dict = {}

        for row in locations:
            dict = row.asDict()
            location_results.append(dict)

        location_and_events.append(location_results)
        dict = {}

        for row in events:
            dict = row.asDict()
            dict['location'] = dict['location'].asDict()
            event_results.append(dict)
        location_and_events.append(event_results)

        response = json.dumps(location_and_events, default = str)
        return HttpResponse(response, content_type = 'application/json')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = True)
            if(user is not None):
                login(request,user)
            return redirect('/')
    else:
        form = RegistrationForm()
        args = {'form':form}
        return render(request, 'register.html', args)

@login_required
def view_profile(request):
    selected = 'profile'
    args = {'user': request.user, 'selected':selected}
    return render(request, 'profile.html', args)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'edit_profile.html', args)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile')
        else:
            return redirect('/change-password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'change_password.html', args)
