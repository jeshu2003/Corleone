import pyttsx3
import os
import webbrowser
import speech_recognition as sr
import datetime
import wikipedia
import requests
from cryptography.fernet import Fernet
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

conversation_context = None
user_data = []

# Generate secret key for encryption and decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetUser(name="Jeshu"):
    speak(f"Hello, {name}! How can I assist you today?")

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
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


def updateContext(query):
    global conversation_context
    if "weather" in query:
        conversation_context = "weather"
    elif "news" in query:
        conversation_context = "news"

def collectUserData(query):
    global user_data
    user_data.append({'query': query, 'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

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

def news_updates():
    api_key = "c6e981dbaac94efd9ca041c335f40a18"
    url = f"http://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    news_data = response.json()
    articles = news_data["articles"]
    for article in articles[:5]:
        speak(article["title"])

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

def wireframe_modeling():
    speak("What type of structure would you like to see a wireframe model of?")
    speak("Options: Cube, Sphere, Pyramid, City Layout")
    
    query = takeCommand().lower()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if "cube" in query:
        speak("Creating a wireframe model of a cube.")
        # Wireframe model of a cube
        r = [-1, 1]
        X, Y = np.meshgrid(r, r)
        ax.plot_wireframe(X, Y, np.array([[1, 1], [-1, -1]]), color="r")
        ax.plot_wireframe(X, Y, np.array([[-1, -1], [1, 1]]), color="r")
        ax.plot_wireframe(X, np.array([[1, 1], [-1, -1]]), Y, color="r")
        ax.plot_wireframe(X, np.array([[-1, -1], [1, 1]]), Y, color="r")
        ax.plot_wireframe(np.array([[1, 1], [-1, -1]]), X, Y, color="r")
        ax.plot_wireframe(np.array([[-1, -1], [1, 1]]), X, Y, color="r")

    elif "sphere" in query:
        speak("Creating a wireframe model of a sphere.")
        # Wireframe model of a sphere
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = 5 * np.outer(np.cos(u), np.sin(v))
        y = 5 * np.outer(np.sin(u), np.sin(v))
        z = 5 * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_wireframe(x, y, z)

    elif "pyramid" in query:
        speak("Creating a wireframe model of a pyramid.")
        # Wireframe model of a pyramid
        x = np.array([0, 1, 0, -1, 0])
        y = np.array([0, 0, 1, 0, -1])
        z = np.array([1, -1, -1, -1, -1])
        vertices = [list(zip(x, y, z))]
        ax.plot_trisurf(x, y, z, linewidth=0.2, antialiased=True)

    elif "city layout" in query:
        speak("Creating a wireframe model of a simple city layout.")
    # Simple city layout with buildings
    for _ in range(10):
        x = np.random.rand(4) * 10 - 5
        y = np.random.rand(4) * 10 - 5
        z = np.zeros((2, 2))  # Ensure z is 2-dimensional
        ax.plot_wireframe(x, y, z)
        ax.plot_wireframe(x, y, np.ones((2, 2)) * 5)  # Ground level

    else:
        speak("I did not understand the structure name. Please try again.")

    plt.show()
    speak("Wireframe model created successfully.")

# Encryption function
def encrypt_message(message):
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

# Decryption function
def decrypt_message(encrypted_message):
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
    return decrypted_message

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

        elif "weather update" in query:
            speak("Sure, please tell me the city name.")
            city_name = takeCommand()
            print("Recognized city name:", city_name)
            weather_update = get_weather(city_name)
            speak(weather_update)

        elif "news update" in query:
            news_updates()

        elif "tell me a joke" in query:
            joke()

        elif "wireframe model" in query:
            wireframe_modeling()

        elif "encrypt" in query:
            speak("What message would you like to encrypt?")
            message = takeCommand()
            encrypted_message = encrypt_message(message)
            speak(f"Your encrypted message is: {encrypted_message}")

        elif "decrypt" in query:
            speak("Please provide the message to decrypt.")
            encrypted_message = takeCommand()
            decrypted_message = decrypt_message(encrypted_message)
            speak(f"Your decrypted message is: {decrypted_message}")
        
        elif "analyse sentiment" in query:
            response = generateResponse(query)
            speak(response)
