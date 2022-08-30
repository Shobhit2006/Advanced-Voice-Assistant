import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time
import requests
import os
import smtplib
import pywhatkit
from email.message import EmailMessage
import pyjokes
import random






engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate', 150)


def remove(string):
    return string.replace(" ", "")

def voice_change(v):
    x = int(v)
    engine.setProperty('voice', voices[x].id)
    speak("voice changed")

def jokes():
    j = pyjokes.get_joke()
    print(j)
    speak(j)

def sendEmail(msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("sbaijal55@gmail.com", "gckqxyohsacbrynf")
    server.send_message(msg)
    server.close()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Good Morning")
        print("Good Morning")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
        print("Good Afternoon")
    else:
        speak("Good Evening")
        print("Good Evening")

def takeCommand():
    r=sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio)
            print(f"user said:{statement}\n")

        except Exception as e:
            
            speak("I can't hear you clearly, please speak again")
            return "None"
        return statement

print('Hello! I am a Personal Assistant made by Shobhit. My name is Shobot.')
speak("Hello! I am a Personal Assistant made by Shobhit. My name is Showbawt.")
wishMe()

speak("How can I help you")


if __name__=='__main__':

    while True:
        
        statement = takeCommand().lower()
        if statement==0:
            continue

        if "bye" in statement or "stop" in statement or "see you soon" in statement:
           
            speak("bye, I hope we meet again")
            print("Bye, I hope we meet again")
            break

        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement =statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'tell a joke' in statement or 'tell me a joke' in statement:
            jokes()

        
        elif 'open google' in statement:
            
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")
            time.sleep(5)

        elif 'open youtube' in statement:
            
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Youtube is open now")
            time.sleep(5)

        elif 'open gmail' in statement:
            
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            time.sleep(5)
                
        elif "do i have any reminders" in statement or "current reminders" in statement or "show reminders" in statement or "all reminders" in statement:
            reminder_file = open("data.txt", 'r')
            if os.stat("data.txt").st_size == 0:
                speak("You have no reminders")                
                print('You have no reminders')
            else:                
                speak("The reminders include: " + reminder_file.read())

        elif "clear reminders" in statement or "delete reminders" in statement or "remove reminders" in statement:
            reminder_file = open("data.txt", 'w')
            speak("All the reminders have been cleared")
        
        elif "new reminder" in statement or "create reminder" in statement or "add reminder" in statement:
            
            speak("What is the reminder?")
            data = takeCommand()
            speak("The following has been added as a reminder" + data)
            reminder_file = open("data.txt", 'a')
            reminder_file.write('\n')
            reminder_file.write(data)
            reminder_file.close()

        elif "movie" in statement or "series" in statement or "tv show" in statement or "film" in statement:
            speak("what is the name of the movie or series")
            name=takeCommand()            
            base_url="https://api.popcat.xyz/imdb?q="
            complete_url=base_url+name
            response = requests.get(complete_url)
            n=response.json()
            title=n['title']
            director=n['director']
            plot=n['plot']
            print(f"{title} is directed by {director}")
            speak(f"{title} is directed by {director}")
            print(f"It is about {plot}")
            speak(f"It is about {plot}")                
        
        elif "voice" in statement:
            print("for female voice say `female` and, for male voice say `male`")
            speak("for female voice say `female` and, for male voice say `masculine`")
            
            q = takeCommand()
            if ("female" in q):

                voice_change(1)
            elif ("masculine" in q):

                voice_change(0)
        
 
        elif "weather" in statement or "temperature" in statement:
            
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name=takeCommand()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(f" Temperature is {str(int(current_temperature - 273.15))} degree celsius " +
                       
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in celsius unit = " +
                      str(int(current_temperature - 273.15)) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

            else:
                speak(" City Not Found ")

        elif 'currency converter' in statement or "currency exchange" in statement or "currency" in statement:
            print("What is the currency CODE from which you what to convert: ")
            speak("What is the currency CODE from which you what to convert: ")
            c1=takeCommand()
            print("Enter the currency CODE to which you what to convert: ")
            speak("Enter the currency CODE to which you what to convert: ")
            c2=takeCommand()
            print("Enter the amount: ")
            speak("Enter the amount: ")
            amt=float(takeCommand())
            url = "https://currency-exchange.p.rapidapi.com/exchange"
            querystring = {"from": c1,"to": c2}
            headers={                
                "X-RapidAPI-Key": "4a7bf47ff1mshc831d0864665364p1c6871jsnbae885015071",
	            "X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.text=="0" and amt!=0:
                print("Invalid currency code entered")
            result=float(response.text)*amt
            speak(f"{amt} {c1} is equal to {result} {c2}")
            print(f"{amt:.2f}" ,c1,"is equal to",f"{result:.2f}",c2)

        elif "message" in statement or "text" in statement:  #Your whatsapp web must be logged in 
            print("Which number would you like to send the message to(speak the number without the country code)")                 
            speak("Which number would you like to send the message to")
            number=takeCommand()
            speak("What is the content of your message")
            wmsg=takeCommand()            
            speak("sending message, kindly be patient")
            pywhatkit.sendwhatmsg_instantly(f"+91{remove(number)}", wmsg, 15)
            speak("message sent")
            

        elif 'what is the time' in statement or 'tell me the time' in statement or 'what time is it' in statement:
            
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am Showbawt! your persoanl assistant. I am programmed to perform minor tasks like'
                  'opening youtube, google, and gmail, tell you the weather forecast, I can also send emails, play a song, convert currencies and get top headline news from times of india!')


        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("Shobhit has made me!")
            print("Shobhit has made me!")

        elif 'news' in statement:
            inx=random.randint(0,4)
            inx=random.randint(0,4)
            response = requests.get("https://newsapi.org/v2/top-headlines?sources=reuters&pageSize=5&apiKey=9d51c0ea809f4d3d96c9d9915b17ea5d")
            news=response.json()
            at=news['articles']
            print(at[inx]['title'])
            speak(at[inx]['title'])
            print(at[inx]['description'])
            speak(at[inx]['description'])
            print(at[inx]['content'])
            speak(at[inx]['content'])
            time.sleep(6)

        elif 'search'  in statement:
            
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'song'  in statement or 'music' in statement or 'play' in statement:
            
            speak('Which song do you want me to play')
            song = takeCommand()
            speak(f"playing {song}")
            pywhatkit.playonyt(song)
            #playsound.playsound('Files/Responses/song.wav', True)
            time.sleep(6)
                
        
        
        
        elif "email" in statement or "mail" in statement:
            try:
                speak("What is your email subject")
                subject = takeCommand()
                speak("What is the message for the email")
                content = takeCommand()
                speak("Enter the email address would you like to send it to?")
                to=input("Enter your email address: ")
                msg = EmailMessage()
                
                msg.set_content(content)
                msg['Subject'] = subject
                msg['From'] = "sbaijal55@gmail.com"
                msg['To'] = to

                sendEmail(msg)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak(
                    "Unable to send email check the address of the recipient")

        else:
            base_url="http://api.brainshop.ai/get?bid=162341&key=XEQ17ETA0siJTQkT&uid=[uid]&msg="
            complete_url=base_url+statement
            response = requests.get(complete_url)
            x=response.json()
            
            print(x['cnt'])
            speak(x['cnt'])

