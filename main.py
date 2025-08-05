import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import time
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

recognizer = sr.Recognizer()


def speak(text):
    print(f"Jarvis: {text}")    
    engine = pyttsx3.init()
    engine.setProperty("volume", 1.0)
    engine.say(text) # reinitialize every time
    engine.runAndWait()
    # no e.stop() needed; runAndWait blocks until done
    del engine
    time.sleep(0.05)  # tiny pause to settle audio
    
def aiprocess(command):
    client = OpenAI(
    
    api_key= os.getenv("OPENAI_API_KEY")
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a virtual assistant named  Jarvis skilled in general task like google cloud and alexa !"},
        {"role":"user","content":command}
        ]
    )
    return response.choices[0].message.content 
    
    
def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")
    elif "open news" in c:
        webbrowser.open("https://timesofindia.indiatimes.com/india")        
        
    elif c.lower().startswith("play"):
        song = " ".join(c.lower().split(" ")[1:])
        link = musiclibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find {song} in the music library.")
    elif "exit" in c or "stop" in c:
        exit()
        
    else:
        output = aiprocess(c)
        speak(output)

     
if __name__== "__main__": 
    speak(" Initializing Jarvis... ")

    while True:
        #listen for the wake up word "Jarvis"
        #obtain audio from the microphone
        
        print("Listening for wake word...")
        
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
            word = recognizer.recognize_google(audio)
            print("Heard: ",word)
            
            if(word.lower() == "jarvis"):
                speak("Yes! I am jarvis, How can I help you?")
                
                with sr.Microphone() as source:
                    print(" Jarvis active and waiting for command")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio) 
                    print("Command : ",command)
                    processCommand(command)
                    
        except sr.WaitTimeoutError:
            print("Timeout: no speech detected.")
        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.RequestError as e:
            print("Google error:", e)
        except Exception as e:
            print("Error:", e)
            
