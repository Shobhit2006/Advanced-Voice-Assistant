import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time
import requests
import os
import smtplib
from email.message import EmailMessage
import pyjokes
import random
from googletrans import Translator
import ast
import fileinput
import sys
import cv2 as cv


engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate', 150)

def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)
def remove(string):
    return string.replace(" ", "")

def voice_change(v):
    x = int(v)
    engine.setProperty('voice', voices[x].id)
    speak("voice changed")



def sendEmail(msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("sbaijal55@gmail.com", "gckqxyohsacbrynf")
    server.send_message(msg)
    server.close()

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def jokes():
    j = pyjokes.get_joke()
    
    speak(j)

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Good Morning")
        
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
        
    else:
        speak("Good Evening")
        

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

try:    
    response = requests.get("https://www.google.com")
    
except:    
    speak("Internet is not connected. Try again later")
    exit()
import pywhatkit


speak('Hello! I am ShoBot, your personal voice assistant.')

wishMe()

speak("How can I help you")




while True:    
        
    statement = takeCommand().lower()        
    if statement==0:
        continue

    if "bye" in statement or "stop" in statement or "see you soon" in statement:
           
        speak("bye, I hope we meet again")
            
        break

    if 'wikipedia' in statement:
        speak('Searching Wikipedia...')
        statement =statement.replace("wikipedia", "")
        results = wikipedia.summary(statement, sentences=3)
        speak("According to Wikipedia")
            
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
                
        else:                
            speak("The reminders include: " + reminder_file.read())

    elif "clear reminders" in statement or "delete reminders" in statement or "remove reminders" in statement:
        reminder_file = open("data.txt", 'w')
        speak("All the reminders have been cleared")
        
    elif "new reminder" in statement or "create reminder" in statement or "add reminder" in statement or "create a reminder" in statement or "add a reminder" in statement:
            
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
        try:                
            title=n['title']
            director=n['director']
            plot=n['plot']                
            speak(f"{title} is directed by {director}")                
            speak(f"It is about {plot}")
        except Exception as e:
            print(e)
            speak("unable to get the movie/series details, try again")                
        
    elif "voice" in statement:           
        speak("for female voice say `female` and, for male voice say `masculine`")
            
        q = takeCommand()
        if ("female" in q):

            voice_change(1)
        elif ("masculine" in q):

            voice_change(0)
        else:
            speak("Voice not changed, invalid input given")
        
 
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

        else:
            speak(" City Not Found ")

    elif 'currency converter' in statement or "currency exchange" in statement or "currency" in statement:            
        speak("What is the currency CODE from which you what to convert: ")
        c1=takeCommand()            
        speak("What is the currency CODE to which you what to convert: ")
        c2=takeCommand()            
        speak("What is the the amount: ")
        amt=float(takeCommand())
        url = "https://currency-exchange.p.rapidapi.com/exchange"
        querystring = {"from": c1,"to": c2}
        headers={                
            "X-RapidAPI-Key": "4a7bf47ff1mshc831d0864665364p1c6871jsnbae885015071",
	        "X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.text=="0" and amt!=0:
            speak("Invalid currency code entered")                
        result=float(response.text)*amt
        speak(f"{amt:.2f} {c1} is equal to {result:.2f} {c2}")
            

    elif "message" in statement:  #Your whatsapp web must be logged in 
                        
        speak("Which number would you like to send the message to")
        number=takeCommand()
        speak("What is the content of your message")
        wmsg=takeCommand()
        try:
                            
            speak("sending message, kindly be patient")
            pywhatkit.sendwhatmsg_instantly(f"+91{remove(number)}", wmsg, 15)
            speak("message sent")
        except Exception as e:
            print(e)
            speak("Invalid number mentioned. Try again with a valid 10 digit number")                
            

    elif 'what is the time' in statement or 'tell me the time' in statement or 'what time is it' in statement:
            
        strTime=datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"the time is {strTime}")

    elif 'who are you' in statement or 'what can you do' in statement:
            
        speak("I am ShoBot! your persoanl assistant. I was programmed by Shobhit to perform minor tasks like opening youtube, google, and gmail, tell you the weather forecast, I can also send emails, play a song, convert currencies, translate texts, give you information about movies, narrate the news and a lot more")

    elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("Shobhit has made me!")
            

    elif "stock" in statement:
            
        speak("what is the symbol of the stock")
        symbol=takeCommand()
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={remove(symbol)}&apikey=5YIZ9GTZQDZ475XJ'
        r = requests.get(url)
        data = r.json()
        try:
                    
            num=data["Global Quote"]
                
            speak(f"current stock price of {num['01. symbol']} is {num['05. price']}")
        except Exception as e:                
            speak("Error. Invalid stock name")        
            
    elif 'news' in statement:
        inx=random.randint(0,4)
        inx=random.randint(0,4)
        response = requests.get("https://newsapi.org/v2/top-headlines?sources=reuters&pageSize=5&apiKey=9d51c0ea809f4d3d96c9d9915b17ea5d")
        news=response.json()
        at=news['articles']            
        speak(at[inx]['title'])            
        speak(at[inx]['description'])            
        speak(at[inx]['content'])
        time.sleep(6)

    elif 'search'  in statement:
            
        statement = statement.replace("search", "")
        webbrowser.open_new_tab(statement)
        time.sleep(5)

    elif 'song'  in statement or 'music' in statement:
            
        speak('Which song do you want me to play')
        song = takeCommand()
        speak(f"playing {song}")
        pywhatkit.playonyt(song)        
        time.sleep(6)
                
        
        
    elif "translate" in statement or "translator" in statement:
        translator = Translator()
            
        speak("speak the text that you want to translate")
        text=takeCommand()
            
        speak("which language do you want to translate it to")
        lang=takeCommand()
        try:                                         
            translated_text = translator.translate(text,dest=lang)
                
            speak(f"The translated text is: `{translated_text.text}`")
        except Exception as e:
            print(e)
            speak("Unable to translate the text. Try again")
    elif "email" in statement or "mail" in statement:
        try:
            speak("To whom shall I send it?")
            to = takeCommand()
            file=open('email.txt','r')
            d=file.read()
            r=ast.literal_eval(d)                
            file.close()
            if to in r.keys():
                                    
                To=r[to]
            else:
                speak("This contact doesn't exist, you can add contacts by saying `create contact`")
                break  
            speak("What is your email subject")
            subject = takeCommand()
            speak("What is the message for the email")
            content = takeCommand()
                                
            msg = EmailMessage()
                              
            msg.set_content(content)
            msg['Subject'] = subject
            msg['From'] = "sbaijal55@gmail.com"
            msg['To'] = To

            sendEmail(msg)
            speak("Email has been sent")
        except Exception as e:
            print(e)
            speak("Unable to send email")
    elif "create contact" in statement or "new contact" in statement or "add contact" in statement or "create a contact" in statement or "add a contact" in statement:

        speak("What name would you like to save it with")
        cname=takeCommand()
        speak("Enter the email id of the contact")
        mail=input("Email: ")
        try:               
                
            file=open('email.txt','r+')
            d=file.read()
            r=ast.literal_eval(d)
                
            if cname in r.keys():
                print("contact with name already exists") 
                break                                                

            dict2={cname:mail}
            r.update(dict2)
            file.truncate(0)
            file.close()
            file=open('email.txt','w')
            w=file.write(str(r))
            file.close()
            speak("contact has been saved")
        except:
            file=open('email.txt','w')
            pp=str({cname:mail})
            file.write(pp)                
            file.close()
            speak("contact has been saved")
    elif "delete contact" in statement or "remove contact" in statement or "delete a contact" in statement or "remove a contact" in statement:
        file=open('email.txt','r')
        d=file.read()
        dr=ast.literal_eval(d)                
        file.close()
        speak("Whom do you want to remove")
        email=takeCommand()
        if email in dr.keys():                
            replaceAll("email.txt",email,"")
            replaceAll("email.txt",dr[email],"")
            speak(f"{email} has been removed from your contracts")
        else:
            speak("The name doesn't exist in your contracts")

    elif "camera" in statement or "photo" in statement or "picture" in statement:
        try:
            speak("Say Cheeeese")    
            cam = cv.VideoCapture(0)
               
            s, img = cam.read()
            if s:
                cv.namedWindow("ShoBot")
                cv.imshow("ShoBot",img)
                speak("Press any key to save the file")
                cv.waitKey(0)
                cv.destroyWindow("ShoBot")
                speak("What is the name you wish to save this file with")
                imgn=takeCommand()
                cv.imwrite(f"{imgn}.jpg",img)
        except:
            speak("Error occured")




    else:
        base_url="http://api.brainshop.ai/get?bid=162341&key=XEQ17ETA0siJTQkT&uid=[uid]&msg="
        complete_url=base_url+statement
        response = requests.get(complete_url)
        x=response.json()          
           
        speak(x['cnt'])
