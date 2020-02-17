from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from tkinter import*
import pyttsx3 as pp
import speech_recognition as s
import threading

engine = pp.init()

voices = engine.getProperty('voices')
print(voices)

engine.setProperty('voice', voices[0].id)


def speak(word):
    engine.say(word)
    engine.runAndWait()

# pyttsx3
bot = ChatBot("My Bot")
#==========================Database=========================
import mysql.connector
con= mysql.connector.connect(host="localhost", user="root", passwd="ag584",database="bot")
cur = con.cursor()
cur.execute("select txt from chatbot")
result = cur.fetchall()
convo = [",".join(x) for x in result]

trainer = ListTrainer(bot)

# now training the bot with the help of trainer

trainer.train(convo)

# answer = bot.get_response("what is your name?")
# print(answer)

# print("Talk to bot ")
# while True:
#     query = input()
#     if query == 'exit':
#         break
#     answer = bot.get_response(query)
#     print("bot : ", answer)

main = Tk()

main.geometry("550x620")
main.title("The Chatbot")
main.config(bg="cyan")
Label(main,text="Welcome To Chatbot",font = "comicsansms 20 bold",bg="cyan",fg="red").pack()
img = PhotoImage(file="logo.png")

photoL = Label(main, image=img,relief=SUNKEN)

photoL.pack(pady=5)



# take query : it takes audio as input from user and convert it to string..

def takeQuery():
     sr = s.Recognizer()
     sr.pause_threshold = 1
     print("your bot is listening try to speak")
     with s.Microphone() as m:
        try:
             audio = sr.listen(m)
             query = sr.recognize_google(audio, language='eng-in')
             print(query)
             textF.delete(0, END)
             textF.insert(0, query)
             ask_from_bot()
        except Exception as e:
             print(e)
             print("not recognized")

s = ""
for x in convo:
    s += x
s = s.lower()
def ask_from_bot():
    query = textF.get()
    if len(query) <= 1 :
        msgs.insert(END, 'you:' + query)
        msgs.insert(END, "bot: Please complete the input")
        textF.delete(0, END)
        speak("Please complete the input")
        msgs.yview(END)
    elif query.lower() in s:
        answer_from_bot = bot.get_response(query)
        msgs.insert(END, "you : " + query)
        print(type(answer_from_bot))
        msgs.insert(END, "bot : " + str(answer_from_bot))
        speak(answer_from_bot)
        textF.delete(0, END)
        msgs.yview(END)

    else:
        msgs.insert(END, 'you:' + query)
        msgs.insert(END, "bot: Invalid Input")
        textF.delete(0, END)
        speak("Please enter valid input")
        msgs.yview(END)

frame = Frame(main)
sc = Scrollbar(frame)
msgs = Listbox(frame,bg="white",fg="black",font = "comicsansms 10 bold",width=120, height=12, yscrollcommand=sc.set)
sc.pack(side=RIGHT, fill=Y)
msgs.pack(side=RIGHT, fill=BOTH,pady=10)
frame.pack(padx=10)
sc.config(command=msgs.yview)

textF = Entry(main,bg="white",font = "comicsansms 20 bold",fg="black")
textF.pack(fill=X, pady=10,padx=10)
btn = Button(main, fg="white",bg="red",relief=SUNKEN, text="Ask from bot",font = "comicsansms 15 bold", command=ask_from_bot)
btn.pack()


# Creating a function
def enter_function(event):
    btn.invoke()


# Going to bind main window with enter key...

main.bind('<Return>', enter_function)


def repeatL():
    while True:
        takeQuery()
t = threading.Thread(target=takeQuery)
t.start()

main.mainloop()