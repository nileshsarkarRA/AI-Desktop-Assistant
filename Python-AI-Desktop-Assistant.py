# General Examples of Introductory Prompts for the Assistant
# """
# Hi, Nilesh! Your Desktop Chat Assistant here, How, may i help you today?
# Hi, This is your Desktop Assistant, Chryselle! How, may i help you today?
# text_to_speech("Hello, This is Hp Omen Laptop !")
# """

# Plays Introductory Speech once Executed

# 


# Prompt user for input in text to convert it to Speech TTS

# user_text = input("\nEnter the text you want the Assistant to respond to: ")
# text_to_speech(user_text)

# Getting Audio from the user and then Converting it to Text

# audio_from_user_to_text = get_audio_from_user()

# Checking for familiar pharases and then responding accordingly!

# if "hello" in audio_from_user_to_text:
#     text_to_speech("Hi! How are you?    ")
# elif "what is your name" in audio_from_user_to_text:
#     text_to_speech("My name is Chryselle!  ")


# google_service = authenticate_google_calendar_API()
# user_input = int(input("Enter the Number of Events you wish to Retrieve: "))
# get_events_from_calender_API(user_input, google_service)





#def get_events_from_calender_API(n, service):
    # Retrieves upcoming events from the user's primary calendar.
    # now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    # print(f"\nGetting Your upcoming {n} events")
    # events_result = (
    #     service.events()
    #     .list(
    #         calendarId="primary",
    #         timeMin=now,
    #         maxResults=n,
    #         singleEvents=True,
    #         orderBy="startTime",
    #     )
    #     .execute()
    # )
    # events = events_result.get("items", [])

    # if not events:
    #     print("No upcoming events found.")
    # for event in events:
    #     start = event["start"].get("dateTime", event["start"].get("date"))
    #     print(start, event["summary"])



from __future__ import print_function
import datetime
import os.path
import pytz
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from pytz import timezone
from gtts import gTTS
import os
import time
import pyttsx3
import speech_recognition as sr
import playsound


SCOPES = ['https://www.googleapis.com/auth/calendar']
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october","november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]
CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]



# Using pyttsx3 module for Offline Usage of voice recognition !
def speak_using_gTTS_module(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Voice Recognition using gTTS requires Internet Connectivity
# def speak_using_gTTS_module(text):
#     # tts = gTTS(text=text, lang="en",slow=False,tld="us")
#     text_to_speech = gTTS(text = text , lang="en", slow=False,tld="us")
#     filename = "voice.mp4"
#     text_to_speech.save(filename)
#     playsound.playsound(filename)

# Using the microphone to get audio from user and converting it into text and store it !
def get_audio_and_convert_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said

# Authenticate user with their google calendar API !
def authenticate_google_calendar_API():
    """Authenticates with the Google Calendar API and returns the service."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service

# Fetch events from the google calendar using the pyttsx3 module voice out the output and display it 
def get_events(day, service):
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak_using_gTTS_module('No upcoming events found.')
    else:
        speak_using_gTTS_module(f"You have {len(events)}  events  on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12)
                start_time = start_time + "pm"

            speak_using_gTTS_module(event["summary"] + " at " + start_time)

# Analyze the audio text of the user to understand context of day, weekdays and month as well as any other future date!
def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:  
        year = year+1

    
    if month == -1 and day != -1:  
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:  
        return datetime.date(month=month, day=day, year=year)

playsound.playsound("AI-Intro-Speech-Chryselle.mp4")

SERVICE = authenticate_google_calendar_API()
print("Start")
text = get_audio_and_convert_to_text()

for phrase in CALENDAR_STRS:
    if phrase in text.lower():
        date = get_date(text)
        if date:
            get_events(date, SERVICE)
        else:
            speak_using_gTTS_module("Please Try Again")


