import pyttsx3
import pyaudio
import os
import webbrowser
import speech_recognition as sr
import datetime
import wikipedia
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Corleone. Always at Your Service")

def takeCommand():
    # It takes microphone input from user and returns string output

    r = sr.Recognizer()
    mic_list = sr.Microphone.list_microphone_names()
    print("Available microphones:")
    for i, microphone_name in enumerate(mic_list):
        print(f"{i}: {microphone_name}")

    # Select the desired microphone
    mic_index = None
    for index, name in enumerate(mic_list):
        if "Boult Audio Airbass" in name:
            mic_index = index
            break

    if mic_index is None:
        print("Earbuds microphone not found!")
        return "None"

    with sr.Microphone(device_index=mic_index) as source:
        print("Listening...")
        r.pause_threshold = 1  # Reduced pause_threshold for better performance
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query


# to get weather 
def get_weather(city_name):
    api_key = "db1608fd00a61d98a7f390e3edac41ae"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"

    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] == 200:
        weather_data = data["main"]
        temperature = weather_data["temp"]
        humidity = weather_data["humidity"]
        weather_description = data["weather"][0]["description"]
        return f"{city_name}: {weather_description}, Temperature: {temperature}°C, Humidity: {humidity}%"
    else:
        return f"Failed to fetch weather data for {city_name}"

#to get news 
def news_updates():
    api_key = "c6e981dbaac94efd9ca041c335f40a18"
    url = f"http://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    news_data = response.json()
    articles = news_data["articles"]
    for article in articles[:5]:
        speak(article["title"])

#to get calendar
def calendar_updates():
    today = datetime.date.today()
    speak(f"Today is {today.strftime('%A')}, {today.strftime('%B')} {today.day}, {today.year}.")

#to remind the tasks
def task_reminder():
    speak("You have a meeting at 3 PM today.")

#to solve calculations
def mathematical_calculations(query):
    if "calculate" in query:
        query = query.replace("calculate", "")
        result = eval(query)
        speak(f"The result is {result}")

#to tell jokes
def joke():
    speak("Why don't scientists trust atoms? Because they make up everything!")
    speak("What do you call a fish wearing a crown? King fish")
    speak("I told my wife she should embrace her mistakes. How? She gave me a hug")
    speak("What did the janitor say when he jumped out of the closet? Supplies")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif "open youtube" in query:
            webbrowser.open("youtube.com")

        elif "open google" in query:
            webbrowser.open("google.com")

        elif "play music" in query:
            music_dir = "D:\\Music\\Favorites"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif "open code" in query:
            codePath = "C:\\Users\\jeshu\\AppData\\Local\\Programs\\Microsoft VS\\Code.exe"
            os.startfile(codePath)

        elif "weather update" in query:
            speak("Sure, please tell me the city name.")
            city_name = takeCommand()
            print("Recognized city name:", city_name)  # Add this line for debugging
            weather_update = get_weather(city_name)
            speak(weather_update)

        elif "news update" in query:
            news_updates()

        elif "calendar update" in query:
            calendar_updates()

        elif "task reminder" in query:
            task_reminder()

        elif "calculate" in query:
            mathematical_calculations(query)

        elif "tell me a joke" in query:
            joke()