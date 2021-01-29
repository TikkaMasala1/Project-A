import tkinter as tk
import moderation
import user
import spectator


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
                      text='Selection',
                      font=('Calibri', 30, 'bold'),
                      fg='white',
                      bg='#212B5C')
    header.place(relwidth=1)

    # window, text to display, x pos, y pos, function to button
    ButtonMaker(window, 'Moderatie', 240, 300, moderation.start)
    ButtonMaker(window, 'Gebruiker', 540, 300, user.start)
    ButtonMaker(window, 'Station', 840, 300, spectator.start)


if __name__ == '__main__':
    mainForm()
    window.mainloop()
