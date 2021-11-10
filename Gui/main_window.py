# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 12:09:27 2021

@author: mercurio  
"""
from tkinter import *
import os 
from PIL import Image, ImageTk
import subprocess 

import settings
import repertoire
import capture 

## Set Colors 
def _from_rgb():
    return "#%02x%02x%02x" %rgb 

### This class contains main widgets in the main window 
class MainWindow: 
    
    def __init__(self):
        """
        constructor
        -------
        """
        ## main Window 
        self.main_window = Tk()
        self.main_window.geometry("+400+80")
        # self.main_window.attributes("-fullscreen", True)
        self.main_window.tile("Dome")
        self.main_window.iconbitmap('./icons/icon_f.png')
        self.main_window.configure(background=_from_rgb((175, 222, 255)))
        
        ## Adding icons and buttons 
        self.photoCamera = ImageTk.PhotoImage(Image.open(
            './icons/cam_projet.png').resize((186, 154), Image.BILINEAR))
        self.photoRepertoire = ImageTk.PhotoImage(Image.open('./icons/prev_projets.png').resize((200, 154), 
            Image.BILINEAR))
        self.photoBack = ImageTk.PhotoImage(Image.open(
            './icons/back.png').resize((75, 75), Image.BILINEAR))
        self.photoShutDown = ImageTk.PhotoImage(Image.open(
            './icons/IconeEteindre.png').resize((75, 75), Image.BILINEAR))
        self.photoExit = ImageTk.PhotoImage(Image.open(
            './icons/IconeAnnuler.png').resize((75, 75), Image.BILINEAR))
        self.photoSettings = ImageTk.PhotoImage(Image.open(
            './icons/IconeSettings.png').resize((75, 75), Image.BILINEAR))
        
        #Frame 
        self.frame = Frame(self.main_window, bg=_from_rgb((175, 222, 255)))
        
        #Buttons 
        self.btn_capture = Button(self.frame, text="New Project", fg=_from_rgb((176, 175, 179)), 
                                        bg=_from_rgb((175, 222, 255)), relief="flat", 
                                            image=self.photoCamera, compound=TOP,
                                                cursor="tcross", command=self.openCapture)
        self.btn_Repertoire = Button(self.frame, text="View Projects", fg=_from_rgb((176, 175, 179)), 
                                        bg=_from_rgb((175, 222, 255)), relief="flat", 
                                            image=self.photoCamera, compound=TOP,
                                                cursor="tcross", command=self.openRepertoire)
        self.btn_back = Button(self.frame, text="Retour", fg=_from_rgb((176, 175, 179)), 
                                        bg=_from_rgb((175, 222, 255)), relief="flat", 
                                            image=self.photoCamera, compound=TOP,
                                                cursor="tcross", command=self.back)
        self.btn_shutDown = Button(self.frame, text="Eteindre", fg=_from_rgb((176, 175, 179)), 
                                        bg=_from_rgb((175, 222, 255)), relief="flat", 
                                            image=self.photoCamera, compound=TOP,
                                                cursor="tcross", command=self.shudown)
        self.btn_exit = Button(self.frame, text="Sortir", fg=_from_rgb((176, 175, 179)), 
                                        bg=_from_rgb((175, 222, 255)), relief="flat", 
                                            image=self.photoCamera, compound=TOP,
                                                cursor="tcross", command=self.exit_)
        self.btn_settings = Button(self.frame, text="Réglages", fg=_from_rgb((176, 175, 179)), 
                                        bg=_from_rgb((175, 222, 255)), relief="flat", 
                                            image=self.photoCamera, compound=TOP,
                                                cursor="tcross", command=self.settings)
        
        
        def display(self): 
            
            Grid.rowconfigure(self.main_window, 0, weight=1)
            Grid.columnconfigure(self.main_window, 0, weight=1)
            Grid.rowconfigure(self.frame,0, weight=1)
            Grid.columnconfigure(self.frame, 0, weight=1)
            
            self.btn_capture.grid(row=2, column=2, sticky='news')
            self.btn_Repertoire.grid(row=2, column=3, sticky='news')
            self.btn_settings.grid(row=1, column=1, sticky='news')
            self.btn_exit.grid(row=1, column=5, sticky='news') 
            self.btn_shutDown.grid(row=3, column=5, sticky='news')
            
        def openCapture(self): 
            print("Ouvrir la fenetre Capture")
            capt = capture.Capture(self.main_window)
        
        def openRepertoire(self): 
            print("Ouvrir la fenetre Repertoire")
            repert = repertoire.Repertoire(self.main_window)
            
        # def back(self):
        
        def shudown(self): 
            subprocess.run(['sudo', 'shutdown', '-h', '0'])
        
        def exit_(self): 
            self.main_window.destroy()
            
        def settings(self): 
            regalges = settings.Settings(self.main_window)
            
        def mainloop(self): 
            self.main_window.mainloop()
            

if __name__ == '__main__': 
    main_window = MainWindow()
    main_window.display()
    main_window.mainloop()            
        
        
            
        
            
        
        
        
        
                
        
    