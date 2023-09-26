# Voice Assistant Program

import pyttsx3 
import speech_recognition as sr 
import wikipedia
import webbrowser
import os
import smtplib
from datetime import datetime

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.now().hour)
    if hour>=0 and hour<12:
        print("\n Voice Assistant : Good Morning!")
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        print("\n V Good Afternoon!")   
        speak("Good Afternoon!")   

    else:
        print("\n V Good Evening!")  
        speak("Good Evening!")  

    print("\n I am your Voice Assistant Sir. Please tell me how may I help you \n")       
    speak("I am your Voice Assistant Sir. Please tell me how may I help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n\n Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("\n Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"\n User Command : {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('pavanpatil3546@gmail.com', 'password')
    server.sendmail('pavanpatil3546@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            print('Searching Wikipedia...')
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            print("According to Wikipedia :- ")
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")   


        elif 'play music' in query:
            music_dir = 'D:\Music\English'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'tell me the time' in query:
            strTime = datetime.now().strftime("%H:%M:%S")    
            print(" Time : ", strTime)
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "D:\PAVAN\Folder_3\INTERNSHIP\Projects\CodeClause(Python)\P\main.py"
            os.startfile(codePath)

        elif 'email to xyz' in query:
            try:
                print("What should I say?")
                speak("What should I say?")
                content = takeCommand()
                to = "xyz@gmail.com"    
                sendEmail(to, content)
                print("Email has been sent!")
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                print("Sorry my friend pavan. I am not able to send this email")    
                speak("Sorry my friend pavan. I am not able to send this email")    
