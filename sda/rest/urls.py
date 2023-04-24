from django.urls import path
from . import views


urlpatterns = [
    path('v1/calendar/init/', views.GoogleCalendarInitView.as_view(), name='google_calendar_init'),
    path('v1/calendar/redirect/', views.GoogleCalendarRedirectView.as_view())
]