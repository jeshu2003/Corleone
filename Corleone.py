#imported libraries
import pyttsx3
import os
import webbrowser
import speech_recognition as sr
import datetime
import wikipedia
import wikipedia as googleScrap
import requests
import pywhatkit
import re
import pyautogui
import time
import random
import string
import subprocess
import json
from googletrans import Translator
from googletrans import LANGUAGES
from pynput.keyboard import Key,Controller
from time import sleep
from cryptography.fernet import Fernet
from urllib.parse import quote
from bs4 import BeautifulSoup

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

conversation_context = None
user_data = []

# Generate secret key for encryption and decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

#remove unnecessay word from the query of the user
def remove_words(query, words):
    query_words = query.split()
    updated_query_words = [word for word in query_words if word.lower() not in words]
    updated_query = ' '.join(updated_query_words)
    return updated_query

#audio function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#greeting the user
def greetUser(name="Jeshu"):
    try:
        speak(f"Hello, {name}! How can I assist you today?")
    except Exception as e:
        print(f"An error occurred while greeting the user: {e}")

#wish function
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Corleone. Always at Your Service")

#taking command from user
def takeCommand():
    # It takes microphone input from user and returns string output

    r = sr.Recognizer()

    # Adjusting pause_threshold and energy_threshold for better performance
    r.pause_threshold = 0.5  # Short pause threshold for faster response
    r.energy_threshold = 4000  # Adjust according to ambient noise level

    with sr.Microphone() as source:
        print("Listening...")
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

#youtube control
keyboard=Controller()

def volumeup():
    for i in range(5):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(0.1)

def volumedown():
    for i in range(5):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(0.1)

def controlYoutube(action):
    time.sleep(1)
    if action=="next video":
        pyautogui.hotkey("shift","n")
    
    elif action=="pause" or action=="play":
        pyautogui.press("k")

#google and youtube automation
def searchGoogle(query):
    query=query.replace("google","")
    query=query.replace("google search","")
    query=query.replace("Corleone","")

    try:
        pywhatkit.search(query)
        result=googleScrap.summary(query,1)
        speak(result)

    except:
        speak("No speakable output available")

def searchYoutube(query):
    query=query.replace("youtube","")
    query=query.replace("youtube search","")
    query=query.replace("Corleone","")
    web="https://www.youtube.com/results?search_query="+query
    webbrowser.open(web)
    pywhatkit.playonyt(query)
    speak("Done sir")

#update and collect functions
def updateContext(query):
    global conversation_context
    if "weather" in query:
        conversation_context = "weather"
    elif "news" in query:
        conversation_context = "news"

def collectUserData(query):
    global user_data
    user_data.append({'query': query, 'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

#weather updates with temperature,humidity of a city
def get_weather(city_name):
    search = f"weather in {city_name}"
    url = f"https://www.google.com/search?q={search}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    try:
        temp = soup.find("span", attrs={"id": "wob_tm"}).text
        weather_desc = soup.find("span", attrs={"id": "wob_dc"}).text
        humidity = soup.find("span", attrs={"id": "wob_hm"}).text
        return f"{city_name}: {weather_desc}, Temperature: {temp}°C, Humidity: {humidity}"
    except AttributeError:
        return "Failed to fetch weather data. Please check the city name or try again later."

#news updates on the particular category
def news_updates(query):
    apidict={"business":"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=c6e981dbaac94efd9ca041c335f40a18",
             "entertainment":"https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=c6e981dbaac94efd9ca041c335f40a18",
             "health":"https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=c6e981dbaac94efd9ca041c335f40a18",
             "science":"https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=c6e981dbaac94efd9ca041c335f40a18",
             "sports":"https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=c6e981dbaac94efd9ca041c335f40a18",
             "technology":"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=c6e981dbaac94efd9ca041c335f40a18"
}
  
    speak("Which category of news are you interested in? Options are: business, entertainment, health, science, sports, or technology.")
    field = takeCommand().lower()

    url = apidict.get(field)
    if url is None:
        speak("Sorry, I don't have updates for that category..")
        return

    response = requests.get(url).text
    news = json.loads(response)
    speak("Here is the first news.")

    arts = news["articles"]
    for articles in arts:
        article = articles["title"]
        speak(article)
        news_url = articles["url"]
        print(f"For more info visit: {news_url}")

        speak("Press 1 to continue, or press 2 to stop.")
        a = takeCommand().lower()
        if "1" in a:
            pass
        elif "2" in a:
            break
        speak("thats all")

#analysis of the user's sentiment 
def analyzeSentiment(query):
    positive_keywords = ["happy", "good", "great", "fantastic", "wonderful", "love"]
    negative_keywords = ["sad", "bad", "terrible", "horrible", "hate", "angry"]

    sentiment_score = 0
    for word in positive_keywords:
        if word in query:
            sentiment_score += 1
    for word in negative_keywords:
        if word in query:
            sentiment_score -= 1

    return sentiment_score

def generateResponse(query):
    sentiment_score = analyzeSentiment(query)
    if sentiment_score < -0.2:
        return "I'm sorry to hear that. Is there anything I can do to help?"
    elif sentiment_score > 0.2:
        return "That's great to hear!"
    else:
        return "Thank you for letting me know."

# Encryption function
def encrypt_message(message):
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

# Decryption function
def decrypt_message(encrypted_message):
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
    return decrypted_message

# File encryption and decryption functions
def encrypt_file(file_path, key):
    cipher_suite = Fernet(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    with open(file_path + '.encrypted', 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(file_path, key):
    cipher_suite = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    with open(file_path.replace('.encrypted', ''), 'wb') as file:
        file.write(decrypted_data)

#telling jokes
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "What do you call a fish wearing a crown? A kingfish!",
    "I told my wife she should embrace her mistakes. How? She gave me a hug.",
    "What did the janitor say when he jumped out of the closet? Supplies!"
]

current_joke_index = 0

def joke():
    global current_joke_index
    speak(jokes[current_joke_index])
    current_joke_index = (current_joke_index + 1) % len(jokes)

#cricket updates
def cricket_updates():
    search = "live cricket score"
    url=f"https://www.google.com/search?q={search}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    try:
        updates = []
        for item in soup.find_all("div", class_="BNeawe deIvCb AP7Wnd"):
            updates.append(item.text)
        return updates if updates else ["No live matches at the moment."]
    except Exception as e:
        return [f"An error occurred: {str(e)}"]

#phishing mail check
def is_phishing_email(email_content):
    phishing_phrases = [
        "urgent action required",
        "your account has been suspended",
        "verify your account",
        "click here to update your information",
        "you have won a prize"
    ]
    is_phishing = any(phrase in email_content.lower() for phrase in phishing_phrases)
    return is_phishing, phishing_phrases

def check_url_legitimacy(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, url) is not None:
        return "URL looks legitimate."
    else:
        return "URL seems suspicious. Please be cautious."

#checking the strength of a password
def check_password_strength(password):
    length_criteria = len(password) >= 8
    digit_criteria = any(char.isdigit() for char in password)
    uppercase_criteria = any(char.isupper() for char in password)
    lowercase_criteria = any(char.islower() for char in password)
    special_char_criteria = any(char in string.punctuation for char in password)

    strength = "Weak"
    if all([length_criteria, digit_criteria, uppercase_criteria, lowercase_criteria, special_char_criteria]):
        strength = "Strong"
    elif length_criteria and (digit_criteria or uppercase_criteria or lowercase_criteria or special_char_criteria):
        strength = "Moderate"

    return strength

#password generator
def generate_password(length=12):
    all_chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_chars) for _ in range(length))
    return password

#ip address checking for malicious activities
def scan_open_ports(ip):
    result = subprocess.run(['nmap', '-sT', ip], capture_output=True, text=True)
    return result.stdout

#cybersecurity tips for better protection
def wifi_security_advice():
    tips = [
        "Change the default SSID and password of your WiFi router.",
        "Use WPA3 encryption if available, otherwise use WPA2.",
        "Disable WPS (WiFi Protected Setup) to prevent unauthorized access.",
        "Regularly update your router firmware to patch security vulnerabilities.",
        "Consider setting up a guest network for visitors."
    ]
    return tips

def daily_cybersecurity_tip():
    tips = [
        "Never share your passwords with anyone.",
        "Use two-factor authentication wherever possible.",
        "Regularly update your software and operating system.",
        "Be cautious of email attachments from unknown senders.",
        "Use a VPN when connected to public WiFi."
    ]
    tip = random.choice(tips)
    speak(f"Here is your daily cybersecurity tip: {tip}")

def provide_training_module(module_name):
    modules = {
        "phishing": "Phishing attacks are attempts to trick you into giving away personal information. Always verify the sender's email address and avoid clicking on suspicious links.",
        "passwords": "A strong password is at least 12 characters long and includes a mix of letters, numbers, and special characters. Avoid using common words or phrases.",
        "malware": "Malware is software designed to harm your computer. Keep your antivirus software up to date and avoid downloading files from untrusted sources."
    }
    speak(modules.get(module_name, "Sorry, I don't have information on that topic."))

#google translate process
translator = Translator()

def translateHandler(query):
    speak("What text would you like to translate?")
    text = takeCommand().lower()
    speak("To which language would you like to translate it?")
    target_lang = takeCommand().lower()
    translated_text = translateText(text, target_lang)
    speak(f"Translated text: {translated_text}")  # Speak the translated text
    print(f"Translated text: {translated_text}")  # Print the translated text

def translateText(text, target_lang):
    translation = translator.translate(text, dest=target_lang)
    return translation.text

#event scheduler 
def scheduleEventHandler(query):
    speak("What event would you like to schedule?")
    event = takeCommand().lower()
    speak("At what time would you like to schedule it?")
    event_time = takeCommand().lower()
    scheduleEvent(event, event_time)

def scheduleEvent(event, event_time):
    scheduled_time = datetime.datetime.strptime(event_time, "%H:%M")
    current_time = datetime.datetime.now()

    while current_time < scheduled_time:
        current_time = datetime.datetime.now()
        time.sleep(1)

    speak(f"Reminder: {event} is scheduled at {event_time}")

#alarm setter
def setAlarmHandler(query):
    speak("What time would you like to set the alarm for?")
    alarm_time = takeCommand().lower()
    setAlarm(alarm_time)

def setAlarm(alarm_time):
    current_time = datetime.datetime.now().strftime("%H:%M")
    while current_time != alarm_time:
        current_time = datetime.datetime.now().strftime("%H:%M")
        time.sleep(1)

    speak(f"It's {alarm_time}. Wake up!")

#sleep or exit or closing AI
def sleepAndExit():
    speak("Sure, I will go to sleep now. Feel free to wake me up anytime. Goodbye!")
    exit()

#main function block
if __name__ == "__main__":
    wishMe()
    greetUser()
    while True:
        query = takeCommand().lower()
        updateContext(query)
        collectUserData(query)

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        
        elif 'tell me a joke' in query:
            joke()
        
        elif 'weather' in query:
            speak("Which city's weather would you like to know?")
            city_name = takeCommand().lower()
            weather_data = get_weather(city_name)
            speak(weather_data)
            
        elif 'cricket' in query:
            cricket_data=cricket_updates()
            for update in cricket_data:
                speak(update)

        elif 'email phishing' in query:
            speak("Please provide the content of the email.")
            email_content = takeCommand().lower()
            is_phishing, suspicious_phrases = is_phishing_email(email_content)
            if is_phishing:
                speak(f"The email may be a phishing attempt. Suspicious phrases detected: {', '.join(suspicious_phrases)}.")
            else:
                speak("The email seems safe.")

        elif 'url check' in query:
            speak("Please provide the URL.")
            url =input("Enter the url:")
            legitimacy = check_url_legitimacy(url)
            speak(legitimacy)

        elif 'password strength' in query:
            speak("Please provide the password to check its strength.")
            password = takeCommand().lower()
            strength = check_password_strength(password)
            speak(f"The password strength is: {strength}")

        elif 'generate password' in query:
            password = generate_password()
            speak(f"Generated password: {password}")

        elif 'encrypt' in query:
            speak("What message would you like to encrypt:")
            message=takeCommand().lower()
            encrypt_message(message)
            speak(f"Your encrypted message:{message}")
        
        elif 'decrypt' in query:
            speak("What message would you like to decrypt:")
            message=input("Enter the encrypted message:")
            decrypt_message(message)
            speak(f"Your decrypted message:{message}")

        elif 'encrypt file' in query:
            speak("Please provide the file path.")
            file_path = takeCommand().lower()
            encrypt_file(file_path, key)
            speak(f"The file {file_path} has been encrypted.")

        elif 'decrypt file' in query:
            speak("Please provide the file path.")
            file_path = takeCommand().lower()
            decrypt_file(file_path, key)
            speak(f"The file {file_path} has been decrypted.")

        elif 'scan network' in query:
            speak("Please provide the IP address.")
            ip = takeCommand().lower()
            scan_results = scan_open_ports(ip)
            speak(f"Network scan results: {scan_results}")

        elif 'wifi security advice' in query:
            tips = wifi_security_advice()
            for tip in tips:
                speak(tip)

        elif 'daily cybersecurity tip' in query:
            daily_cybersecurity_tip()

        elif 'training module' in query:
            speak("Which training module would you like? Options are: phishing, passwords, malware.")
            module_name = takeCommand().lower()
            provide_training_module(module_name)
       
        elif 'translate' in query:
            translateHandler(query)
        
        elif 'schedule event' in query:
            scheduleEventHandler(query)

        elif 'set the alarm' in query:
            setAlarmHandler(query)
        
        elif "go to sleep" in query or "exit" in query:
            sleepAndExit() 

        elif "youtube" in query:
            speak("This is what i found for your search")
            searchYoutube(query)
        
        elif "google" in query:
            searchGoogle(query)
            speak("This is what I found on Google")
        
        elif 'pause' in query:
            speak("Pausing the video")
            controlYoutube("pause")
        
        elif 'play' in query:
            speak("Resuming the video")
            controlYoutube("play")
        
        elif 'next video' in query:
            speak("Playing next video")
            controlYoutube("next video")
        
        elif 'volume up' in query:
            speak("Turning volume up")
            volumeup()
        
        elif 'volume down' in query:
            speak("Turning volume down")
            volumedown()
        
        elif 'news' in query:
             news_updates()
