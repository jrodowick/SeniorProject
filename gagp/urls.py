from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from . import views


urlpatterns = [
    re_path(r'^$', views.index),
    path('login/', auth_views.LoginView.as_view(template_name='login.html')),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('locations/', views.locations, name='locations'),
    path('send_alert/<event_id>/', views.send_alert, name='send_alert'),
    path('events/view/<event_id>/', views.view_event, name='view_event'),
    path('events/join/<event_id>/', views.join_event, name='join_event'),
    path('events/add_to_calendar/<event_id>/', views.add_to_calendar, name='add_to_calendar'),
    path('get_data/', views.get_data, name = 'get_data'),
    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
    path('reset-password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>[0-9A-Za-z]+-<token>.+/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

]
