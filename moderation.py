import psycopg2
import tkinter as tk
from datetime import datetime
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


class ButtonMaker:
    def __init__(self, master, text, posx, posy, cmd):
        self.button1 = tk.Button(master, text=text, font=(
            'Calibri', 30), wraplength=180, bg="white", command=cmd)
        self.button1.place(height=80, width=200, x=posx, y=posy)


def mainForm():
    """Makes main window form"""
    global window
    window = tk.Tk()
    window.title('NS Twitter Zuil')
    window.geometry('1280x720')
    window.configure(bg='#FCC63F')

    """Builds all widgets"""
    header = tk.Label(window,
                      text='Moderator',
                      font=('Calibri', 30, 'bold'),
                      fg='white',
                      bg='#212B5C')
    header.place(relwidth=1)

    # window, text to display, x pos, y pos, function to button
    ButtonMaker(window, 'Accept', 240, 500, lambda: moderateOldestMessage('accept', nameEntry.get()))
    ButtonMaker(window, 'Reject', 820, 500, lambda: moderateOldestMessage('reject', nameEntry.get()))
    # ButtonMaker(window, 'Overzicht non moderated berichten', 840, 300)

    global textbox
    textbox = tk.Text(window, width=105, height=8, state='disabled')
    textbox.config(font=('Calibri', 15))
    textbox.place(x=101, y=260)

    nameLabel1 = tk.Label(window, text="Naam: ", bg='#FCC63F')
    nameLabel1.config(font=('Calibri', 20))
    nameLabel1.place(x=100, y=130)

    nameLabel2 = tk.Label(window, text="Verplicht!", bg='#FCC63F')
    nameLabel2.config(font=('Calibri', 20))
    nameLabel2.place(x=100, y=160)

    nameEntry = tk.Entry(window, width=50, )
    nameEntry.place(x=101, y=200)


def convert(x):
    """Converts set variable into a list"""
    return list(x)


def actionLabel(action, moderation):
    if action == 'success':
        successLabel = tk.Label(window, text=f"Bericht {moderation}ed", bg='#FCC63F')
        successLabel.place(x=550, y=525)
        successLabel.config(font=('Calibri', 20))
        successLabel.after(2000, lambda: successLabel.destroy())

    elif action == 'warning':
        warningLabel = tk.Label(window, text="Naam is verplicht!", bg='#FCC63F')
        warningLabel.place(x=550, y=525)
        warningLabel.config(font=('Calibri', 20))
        warningLabel.after(2000, lambda: warningLabel.destroy())


def showOldestNonModerated():
    """Shows the oldest NON moderated message in the database"""
    con = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="root"
    )

    cur = con.cursor()
    cur.execute("select berichten.berichten_id, naam, bericht, datum from berichten "
                "WHERE NOT EXISTS (select 1 from moderaties where berichten.berichten_id = "
                "moderaties.berichten_id) "
                "ORDER BY datum ASC LIMIT 1 ")

    rows = cur.fetchall()

    if rows:
        for x in rows:
            message = f'Naam: {x[1]}\nDatum: {x[3]}\n\nBericht:\n{x[2]}'
    elif not rows:
        message = 'Er zijn berichten meer om te moderaten'

    textbox.config(state='normal')
    textbox.delete('1.0', "end")
    textbox.insert('1.0', message)
    textbox.config(state='disabled')

    cur.close()
    con.close()


def moderateOldestMessage(moderation, modName):
    """Moderates the oldest message in the database"""
    con = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="root"
    )

    cur = con.cursor()

    if not modName:
        actionLabel('warning', 'nothing')

        con.commit()
        cur.close()
        con.close()
        return

    cur.execute("select berichten.berichten_id, naam, bericht, datum from berichten "
                "WHERE NOT EXISTS (select 1 from moderaties where berichten.berichten_id = moderaties.berichten_id)"
                "ORDER BY datum ASC LIMIT 1 ")

    rows = cur.fetchall()

    for x in rows:
        message = f'Naam: {x[1]}\n\nBericht:\n{x[2]}'
        messageId = {x[0]}

    convertedId = convert(messageId)[0]

    if moderation == 'accept' or moderation == 'reject':
        cur.execute("insert into moderaties (moderatie, naam, datum, berichten_id) values(%s, %s, %s, %s)",
                    (moderation, modName, datetime.now(), convertedId))
        con.commit()
        cur.close()
        con.close()

        actionLabel('success', moderation)

        twitter.update_status(status=message)

        showOldestNonModerated()
        return


def start():
    mainForm()
    showOldestNonModerated()
