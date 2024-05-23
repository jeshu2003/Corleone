# Corleone :  Computational.Organization.and.Real-time.Language.Engineering.and.Operational.Navigation.Environment  

Corleone AI is a versatile assistant designed to perform a wide range of tasks, from fetching weather updates to playing music. Below is a comprehensive overview of its functions.

## Initialization

### `pyttsx3`
The text-to-speech (TTS) engine used to convert text to speech. It uses the SAPI5 voice synthesizer.

### `conversation_context`
Global variable to keep track of the current context of the conversation.

### `user_data`
List to store user queries and timestamps for logging purposes.

### `Fernet`
Library from `cryptography` used to encrypt and decrypt messages.

## Utility Functions

### `remove_words(query, words)`
Removes specific words from the query to clean or preprocess the input.

### `speak(audio)`
Converts text to speech using the TTS engine.

### `greetUser(name="Jeshu")`
Greets the user with a personalized message.

### `wishMe()`
Wishes the user based on the current time of the day.

### `takeCommand()`
Listens to the user’s voice input and converts it to text using the Google Speech Recognition API.

### `updateContext(query)`
Updates the global context based on keywords in the query.

### `collectUserData(query)`
Collects user data, such as queries and timestamps, for logging and analysis.

## Weather and News Functions

### `get_weather(city_name)`
Fetches the weather update for a given city using the OpenWeatherMap API.

### `news_updates()`
Provides news updates in different categories using the NewsAPI.

## Sentiment Analysis and Response

### `analyzeSentiment(query)`
Analyzes the sentiment of the user’s query to determine if it is positive, negative, or neutral.

### `generateResponse(query)`
Generates an appropriate response based on the sentiment analysis of the user’s query.

## Entertainment and Utility Functions

### `extract_yt_term(command)`
Extracts the search term from a query to play a video on YouTube.

### `PlayYoutube(query)`
Plays a YouTube video based on the search term extracted from the query.

### `joke()`
Tells a random joke.

### `cricket_updates()`
Fetches live cricket updates from the Cricbuzz API.

### `open_desktop_app(app_name)`
Opens a specified desktop application.

### `open_android_app(package_name)`
Opens a specified Android application using ADB.

## Encryption and Decryption Functions

### `encrypt_message(message)`
Encrypts a given message using the Fernet encryption.

### `decrypt_message(encrypted_message)`
Decrypts a given encrypted message.

## Main Functionality Loop

The main loop listens for user commands and executes the corresponding functions based on the input. It handles various commands such as:
- Searching Wikipedia
- Opening websites like YouTube and Google
- Playing music from a local directory
- Telling the current time
- Providing weather updates
- Fetching news updates
- Telling jokes
- Encrypting and decrypting messages
- Analyzing sentiment
- Playing YouTube videos
- Fetching cricket updates
- Opening desktop and Android applications
- Exiting or going to sleep

## How to Use Corleone AI

1. **Start the Assistant:**
   - Initialize the TTS engine.
   - Call `wishMe()` and `greetUser()` to welcome the user.

2. **Give Commands:**
   - Use voice commands to interact with the assistant.
   - The assistant listens, processes the command, and executes the corresponding function.

3. **Utility Functions:**
   - Use commands like "What's the weather in [city]?" or "Give me the news update in [category]" to get specific information.

4. **Entertainment:**
   - Ask the assistant to play music or tell jokes.

5. **Encryption and Decryption:**
   - Encrypt and decrypt messages using voice commands.

6. **Application Control:**
   - Open desktop or Android applications using specific commands.

7. **Sentiment Analysis:**
   - The assistant can analyze the sentiment of your queries and respond accordingly.

8. **Exit:**
   - Use commands like "Go to sleep" or "Exit" to close the assistant.

Running the Assistant
The script contains a main loop that listens for user commands and triggers the appropriate functions based on the input.

Contributions
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

License
This project is licensed under the MIT License. See the LICENSE file for details.                                                                                  

Project Link:
     The Complete Project is in this drive link.
     Gdrive Link: https://drive.google.com/drive/folders/1hbN8Uu8hwMSCDHUmiMTR_4QaLtdbEtTK?usp=drive_link

Conclusion :  
     Enjoy this AI and be happy
