from django.conf import settings
from django.http import HttpResponseRedirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from rest_framework.views import APIView
from rest_framework.response import Response

# Google Calendar Init View
class GoogleCalendarInitView(APIView):
    def get(self, request, *args, **kwargs):
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
                    "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                    "redirect_uris": ["http://127.0.0.1:8000/rest/v1/calendar/redirect/"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=["https://www.googleapis.com/auth/calendar.readonly"],
            redirect_uri="http://127.0.0.1:8000/rest/v1/calendar/redirect/",
        )
        authorization_url, state = flow.authorization_url()
        return HttpResponseRedirect(authorization_url)

# Google Calendar Redirect View
class GoogleCalendarRedirectView(APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
                    "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                    "redirect_uris": ["http://127.0.0.1:8000/rest/v1/calendar/redirect/"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=["https://www.googleapis.com/auth/calendar.readonly"],
            redirect_uri="http://127.0.0.1:8000/rest/v1/calendar/redirect/",
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', timeMin='2023-04-24T00:00:00Z', maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        return Response(events)