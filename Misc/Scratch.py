

root = Tk()
root.geometry('480x480')


def printYo(event):
    print('Yo')


button_1 = Button(root, text="Yo")
button_1.bind("<Button-1>", printYo)
button_1.pack()

root.mainloop()
