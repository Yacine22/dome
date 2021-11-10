# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 14:20:50 2021

@author: yme
"""
from tkinter import * 
from PIL import Image, ImageTk
import subprocess 

## Set Colors 
def _from_rgb():
    return "#%02x%02x%02x" %rgb 

class Settings:
    global resolutionVal
    global led_number
    
    def __init__(self, master): 
        
        self.master = master 
        self.window = Toplevel(self.master)
        self.window.geometry('400+80')
        # self.window.attributes("-fullscreen", True)
        self.window.title('Dome')
        self.window.iconbitmap('./icons/icon_f.png')
        self.window.configure(background=_from_rgb((175, 222, 255)))
        self.frame = Frame(self.window, bg=_from_rgb((175, 222, 255)))
        
        
        ## icons
        self.photoResolution = ImageTk.PhotoImage(Image.open('./icons/resolutions.png').resize((120, 100), Image.BILINEAR))
        self.photoTile = ImageTk.PhotoImage(Image.open('./icons/dome_led.png').resize((120, 100), Image.BILINEAR))
        self.photoCamTest = ImageTk.PhotoImage(Image.open('./icons/camera_test.png').resize((120, 100), Image.BILINEAR))
        self.photoDomeTest = ImageTk.PhotoImage(Image.open('./icons/dome_test.png').resize((120, 100), Image.BILINEAR))
        self.photoBack = ImageTk.PhotoImage(Image.open('./icons/back.png').resize((75, 75), Image.BILINEAR))
        
        ## Buttons
        self.btn_resolution = Button(self.frame, text="Image Resolutions", fg=_from_rgb((176, 175, 179)), relief="flat", 
                                     bg=_from_rgb((175, 222, 255)), image=self.photoResolution, compound=TOP, 
                                     cursor="tcross", command=self.setResolution)
        self.btn_tile = Button(self.frame, text="LED Numbers by Tile", fg=_from_rgb((176, 175, 179)), relief="flat", 
                                     bg=_from_rgb((175, 222, 255)), image=self.photoResolution, compound=TOP, 
                                     cursor="tcross", command=self.setTile)
        self.btn_camTest = Button(self.frame, text="Camera Test", fg=_from_rgb((176, 175, 179)), relief="flat", 
                                     bg=_from_rgb((175, 222, 255)), image=self.photoResolution, compound=TOP, 
                                     cursor="tcross", command=self.camTest)
        self.btn_domTest = Button(self.frame, text="Dome Test", fg=_from_rgb((176, 175, 179)), relief="flat", 
                                     bg=_from_rgb((175, 222, 255)), image=self.photoResolution, compound=TOP, 
                                     cursor="tcross", command=self.domeTest)
        self.btn_back = Button(self.frame, text="Retour", fg=_from_rgb((176, 175, 179)), relief="flat", 
                                     bg=_from_rgb((175, 222, 255)), image=self.photoResolution, compound=TOP, 
                                     cursor="tcross", command=self.back)
        
        self.display() ### display Sub menu 
        
        def display(self):
            Grid.rowconfigure(self.window, 0, weight=1)
            Grid.columnconfigure(self.window, 0, weight=1)
            Grid.rowconfigure(self.frame, 0, weight=1)
            Grid.columnconfigure(self.frame, 0, weight=1)
            
            self.btn_resolution.grid(row=2, column=2, sticky='news')
            self.btn_tile.grid(row=2, column=3, sticky='news')
            self.btn_camTest.grid(row=3, column=2, sticky='news')
            self.btn_domTest.grid(row=3, column=3, sticky='news')
            self.btn_back.grid(row=1, column=5, sticky='news')
            self.frame.grid(row=0, column=0)
            
            
        def setResolution(self): 
            self.win = tk.Toplevel()
            self.win.geometry('+400+80')
            # self.win.attributes('-fullscreen', True)
            self.win.title("Dome")
            self.win.configure(background=_from_rgb((175, 222, 255)))
            self.frame = Frame(self.win, background=_from_rgb((175, 222, 255)))
            
            
            # Create a listbox  ## Buttons
            self.listbox = Listbox(self.frame, background=_from_rgb((175, 222, 255)), width=40, height=10, selectmode=SINGLE)
            self.btn_validation = Button(self.frame, text="valid", bg='green')
            self.btn_exit = Button(self.frame, text="valider", fg=_from_rgb((176, 175, 179)), relief="flat", 
                                     bg=_from_rgb((175, 222, 255)), compound=TOP, 
                                     cursor="tcross", command=self.win.destroy)
            
            # Inserting the listbox items
            self.listbox.insert(1, "Full Screen")
            self.listbox.insert(2, [1024, 900])
            self.listbox.insert(3, [800, 720])
            self.listbox.insert(4, [600, 480])
            self.listbox.insert(5, [480, 360])
            
            for i in self.listbox.curselection():
                resolutionVal = self.listbox.get(i)
                print(resolutionVal)
                
            Grid.rowconfigure(self.win, 0, weight=1)
            Grid.columnconfigure(self.win, 0, weight=1)
            Grid.rowconfigure(self.frame, 0, weight=1)
            Grid.columnconfigure(self.frame, 0, weight=1)
            
            self.btn_validation.grid(row=1, column=5, sticky='news')
            self.btn_exit.grid(row=4, column=5, sticky='news')
            self.listbox.grid(row=2, column=3, width=40, height=10, selectmode=MULTIPLE, sticky='news')
            self.frame.grid(row=0, column=0)
                
            

            
            
            
        
            
        

