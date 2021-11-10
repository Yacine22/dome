# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 14:20:50 2021

@author: yme
"""
from tkinter import * 

## Set Colors 
def _from_rgb():
    return "#%02x%02x%02x" %rgb 

class Settings:
    def __init__(self, master): 
        
        self.master = master 
        self.window = Toplevel(self.master)
        self.window.geometry('400+80')
        # self.window.attributes("-fullscreen", True)
        self.window.title('Dome')
        self.window.iconbitmap('./icons/icon_f.png')
        self.window.configure(background=_from_rgb((175, 222, 255)))
        
        
        ## icons
        

