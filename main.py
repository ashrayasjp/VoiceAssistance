import speech_recognition as sr 
import pyttsx3              # library for text to speech  
from utils.time_utils import get_current_time
from utils.wiki_utils import search_wikipedia
from utils.media_utils import play_youtube
import os
import random

# Initialize engine and listener
engine = pyttsx3.init()
listener = sr.Recognizer()  

# Talk function
def talk(text):
    print("🤖:", text)     
    engine.say(text)
    engine.runAndWait()      

# Log function
def log_command(command):
    os.makedirs("logs", exist_ok=True)
    with open("logs/log.txt", "a") as f:
        f.write(command + "\n")

# Listen function
def listen_command():
        with sr.Microphone() as source:
            print("🎤 Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice).lower()
            print("👉 You said:", command)
            log_command(command)
            return command

# Main assistant loop
def run_assistant():
    print("🤖 Assistant is running. Say 'stop' to exit.")
    while True:
        command = listen_command().lower()  

        if not command:
            continue

        if "stop" in command:
            talk("Goodbye!")
            break

        elif "time" in command:
            current_time = get_current_time()
            talk("The time is " + current_time)

        elif "play" in command:
            song = command.replace("play", "")  
            try:
                response = play_youtube(song)
                talk(response)
            except Exception as e:
                talk("Sorry, I couldn't play that song.")
                print("Error:", e)

        elif any(kw in command for kw in ["who is", "what is", "where is", "tell me about", "define"]):
            # Extract query
            keywords = ["who is", "what is", "where is", "tell me about", "define"]
            query = command
            for kw in keywords:
                if kw in command:
                    query = command.replace(kw, "")  
                    break
            # Search Wikipedia
            try:
                info = search_wikipedia(query)
                talk(info)
            except Exception as e:
                talk("Sorry, I couldn't find information.")
                print("Error:", e)

        elif "joke" in command:
            os.makedirs("data", exist_ok=True)
            try:
                with open("data/jokes.txt") as f:
                    jokes = f.readlines()
                    joke = random.choice(jokes)  
                    talk(joke)
            except Exception as e:
                talk("I don't have any jokes right now.")
                print("Error:", e)

        else:
            talk("Sorry, I didn’t understand that.")

# Run the assistant
if __name__ == "__main__":
    run_assistant()
