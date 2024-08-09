# utils.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

def create_google_calendar_event(appointment):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': f'Appointment with {appointment.patient.first_name} {appointment.patient.last_name}',
        'start': {
            'dateTime': f'{appointment.date}T{appointment.start_time.isoformat()}',
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': f'{appointment.date}T{appointment.end_time.isoformat()}',
            'timeZone': 'America/New_York',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
