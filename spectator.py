import tkinter as tk
import json
from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

tweets = twitter.get_user_timeline(tweet_mode='extended')

with open('twitter.json', 'w+') as data_file:
    json.dump(tweets, data_file)

with open('twitter.json') as data_file:
    data = json.load(data_file)


def mainForm():
    """Makes main window form"""
    global window
    window = tk.Tk()
    window.title('NS Twitter Zuil')
    window.geometry('1280x720')
    window.configure(bg='#FCC63F')

    """Builds all widgets"""
    header = tk.Label(window,
                      text='Station',
                      font=('Calibri', 30, 'bold'),
                      fg='white',
                      bg='#212B5C')
    header.place(relwidth=1)

    i = 0
    posistions = [0.10, 0.33, 0.56, 0.79]
    for tweet in data:
        i += 1
        if i > 4:
            break
        else:
            for k, v in tweet.items():
                if k == 'full_text':
                    textbox1 = tk.Text(window, width=52, height=6, state='disabled')
                    textbox1.config(font=('Calibri', 14))
                    textbox1.place(relx=0.3, rely=posistions[i-1])
                    textbox1.config(state='normal')
                    textbox1.delete('1.0', "end")
                    textbox1.insert('1.0', v)
                    textbox1.config(state='disabled')


def start():
    mainForm()


