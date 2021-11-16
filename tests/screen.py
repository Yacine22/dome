from tkinter import *


def set_text(word):
	text.set(word)
	return

screen = Tk()
screen.title("Screen")
# screen.geometry('380x240')
text = StringVar()
display = Entry(screen, justify='right', textvariable=text).grid(columnspan=5)

btn1 = Button(screen, text="1", command=lambda:set_text(1)).grid(row=1, column=0)
btn2 = Button(screen, text="2", command=lambda:set_text(2)).grid(row=1, column=1)
btn3 = Button(screen, text="3", command=lambda:set_text(3)).grid(row=1, column=2)

btn4 = Button(screen, text="4", command=lambda:set_text(4)).grid(row=2, column=0)
btn5 = Button(screen, text="5", command=lambda:set_text(5)).grid(row=2, column=1)
btn6 = Button(screen, text="6", command=lambda:set_text(6)).grid(row=2, column=2)

btn7 = Button(screen, text="7", command=lambda:set_text(7)).grid(row=3, column=0)
btn8 = Button(screen, text="8", command=lambda:set_text(8)).grid(row=3, column=1)
btn9 = Button(screen, text="9", command=lambda:set_text(9)).grid(row=3, column=2)

btn0 = Button(screen, text="0", command=lambda:set_text(0)).grid(row=4, column=1)

btnOK = Button(screen, text="OK").grid(row=4, column=3)
btnCancel = Button(screen, text="Cancel", command=screen.destroy).grid(row=5, column=3)
btnDel = Button(screen, text="Del").grid(row=5, column=2)

screen.mainloop()