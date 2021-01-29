import psycopg2
import tkinter as tk
from datetime import datetime


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
                      text='User',
                      font=('Calibri', 30, 'bold'),
                      fg='white',
                      bg='#212B5C')
    header.place(relwidth=1)

    # window, text to display, x pos, y pos, function to button
    ButtonMaker(window, 'Submit', 550, 500, lambda: messageMake(nameEntry.get(), retrieve_input()))

    global textbox
    textbox = tk.Text(window, width=135, height=10, state='normal')
    textbox.place(x=101, y=260)

    nameLabel = tk.Label(window, text="Naam", bg='#FCC63F')
    nameLabel.config(font=('Calibri', 20))
    nameLabel.place(x=100, y=130)

    berichtLabel = tk.Label(window, text="Bericht", bg='#FCC63F')
    berichtLabel.config(font=('Calibri', 20))
    berichtLabel.place(x=100, y=220)

    global nameEntry
    nameEntry = tk.Entry(window)
    nameEntry.place(x=101, y=170)


def retrieve_input():
    message = textbox.get("1.0", "end-1c")
    return message


def actionLabel(action):
    if action == 'success':
        successLabel = tk.Label(window, text="Bericht is opgestuurd!", bg='#FCC63F')
        successLabel.place(x=540, y=625)
        successLabel.config(font=('Calibri', 20))
        successLabel.after(111000, lambda: successLabel.destroy())

    elif action == 'missing':
        missingLabel = tk.Label(window, text="Bericht is verplicht!", bg='#FCC63F')
        missingLabel.place(x=540, y=625)
        missingLabel.config(font=('Calibri', 20))
        missingLabel.after(111000, lambda: missingLabel.destroy())

    elif action == 'limit':
        limitLabel = tk.Label(window, text="Bericht is te lang", bg='#FCC63F')
        limitLabel.place(x=540, y=625)
        limitLabel.config(font=('Calibri', 20))
        limitLabel.after(111000, lambda: limitLabel.destroy())


def messageMake(name, bericht):
    """User creates message"""
    con = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="root"
    )
    cur = con.cursor()

    if name == '':
        name = 'Anoniem'

    if bericht == '':
        con.commit()
        cur.close()
        con.close()
        actionLabel('missing')
        return

    if len(bericht) > 140:
        con.commit()
        cur.close()
        con.close()
        actionLabel('limit')
        return

    else:
        cur.execute("insert into berichten (naam, bericht, datum) values (%s, %s, %s)", (name, bericht, datetime.now()))
        con.commit()
        cur.close()
        con.close()

        actionLabel('success')

        textbox.delete('1.0', "end")
        nameEntry.delete('0', "end")


def start():
    mainForm()
