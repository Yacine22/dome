from tkinter import *


class MainWindow:
    def __init__(self):
        self.window = Tk()
        self.window.geometry('+400+80')
        self.window.title('SSC')
        
        self.frame = Frame(self.window, bg='white')
        self.label_text = Label(self.frame, text='Write', bg='white')
        self.E = Entry(self.frame)
        self.btn = Button(self.frame, text='PUSH', bg='blue', command=self.write_)
        self.quitBtn = Button(self.frame, text='quit', bg='red', command=self.window.destroy)
        
        Grid.rowconfigure(self.window,0, weight=0)
        Grid.columnconfigure(self.window,0, weight=0)
        Grid.rowconfigure(self.frame,0, weight=0)
        Grid.columnconfigure(self.frame,0, weight=0)
        
        self.label_text.grid(row=1, column=1, sticky='news')
        self.E.grid(row=1, column=2, sticky='news')
        self.btn.grid(row=3, column=3, sticky='news')
        self.quitBtn.grid(row=4, column=3, sticky='news')
        self.frame.grid(row=0, column=0)
        
    def write_(self):
        # self.E = Entry(self.frame)
        self.E.delete(0, END)
        self.E.insert(0, 't')
        
        
        
if __name__ == '__main__':
    b = MainWindow()
