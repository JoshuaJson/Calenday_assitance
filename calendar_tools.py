import json
from google_calendy_api import create_service
from datetime import datetime, timedelta
client_secret ='client_secret.json'

def construct_google_calendar_client(client_secret):
    """
    Constructs a Google Calendar API Client
    
    Parameters:
    - client_secret (str): The path to the client secret JSON file
        
    Returns:
    - service: The Google Calendar API service instance 
    """
    API_NAME='calendar'
    API_VERSION='v3'
    SCOPE=['https://www.googleapis.com/auth/calendar']
    service = create_service(client_secret, API_NAME, API_VERSION, SCOPE)
    return service

calendar_service= construct_google_calendar_client(client_secret)

def create_calendar(calendar_name):
    """
    Create a new calendar list. 
    
    Parameters:
    - calendar_name (str): The name of the new calendar list.
    
    Returns:
    - dict: A dictionary containing the ID of the new calendar list.
    """
    calendar_list={
        'summary':calendar_name
    }
    create_calendar_list= calendar_service.calendars().insert(body=calendar_list).execute()
    return create_calendar_list

def list_calendar_list(max_capacity=200):
    """
    List calendar lists until the total numbers of items reaches max_capacity
    
    Parameters:
    - max_capacity (int or str, optional): The maximum number of calendar list to retrieve. Defaults to 200
        If a string is provided, it will be converted to a integer.
    
    Returns:
    - List: A list of dictionaries containing cleaned calenders list information with 'id', 'name', and 'description'.
    """
    if isinstance(max_capacity,str):
        max_capacity= int(max_capacity)
        
    all_calendars=[]
    all_calendars_cleaned=[]
    next_page_token= None
    capacity_tracker= 0
    
    while True:
        calendar_list = calendar_service.calendarList().list(
            maxResults=min(200, max_capacity - capacity_tracker),
            pageToken=next_page_token
        ).execute()
        calendars= calendar_list.get('items', [])
        all_calendars.extend(calendars)
        capacity_tracker += len(calendars)
        if capacity_tracker >= max_capacity:
            break
        next_page_token=calendar_list.get('nextPageToken')
        if not next_page_token:
            break
        
    
    for calendar in all_calendars:
        all_calendars_cleaned.append(
            {
                'id':calendar['id'],
                'name':calendar['id'],
                'description':calendar.get('description', '')
            })
    return all_calendars_cleaned

def list_calendar_events(calendar_id, max_capacity=20):
    """
    List events from specified calendar until the total number of events reaches max_capacity.
    
    Parameters:
    - calendar_id (str): The ID of the calendar from which to list events.
    - max_capacity (int or str, optional): The maximum number of events to retrieve. Defaults to 20.
        If a string provided, it will be converted to a integer.

    Returns:
    - list: A list of events from specified calendar.
    """
    
    if isinstance(max_capacity, str):
        max_capacity= int(max_capacity)
        
    all_events=[]
    next_page_token= None
    capacity_tracker=0
    
    while True:
        events_list=calendar_service.events().list(
            calendarId=calendar_id,
            maxResults=min(250, max_capacity - capacity_tracker),
            pageToken=next_page_token
        ).execute()
        events=events_list.get('items', [])
        all_events.extend(events)
        capacity_tracker += len(events)
        if capacity_tracker >= max_capacity:
            break
        next_page_token= events_list.get('nextPageToken')
        if not next_page_token:
            break
    return all_events

def insert_calendar_event(calendar_id, **kwargs):
    """
    Inserts an event into the specified calendar.

    Parameters:
    - calendar_id: The ID of the calendar where the event will be inserted.
    - **kwargs: Additional keyword arguments representing the event details.

    Returns:
    - The created event or an error message.
    """
    try:
        # Parse the event details from kwargs
        request_body = json.loads(kwargs['kwargs'])

        # Validate that start and end times are present
        if 'start' not in request_body or 'end' not in request_body:
            raise ValueError("Event must include both 'start' and 'end' times.")

        if not request_body['end']:
            raise ValueError("Event 'end' time is missing or invalid.")

        # Insert the event
        event = calendar_service.events().insert(
            calendarId=calendar_id,
            body=request_body
        ).execute()
        return event

    except ValueError as ve:
        return {"error": str(ve)}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
