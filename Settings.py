import os
import time 
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import picamera
import subprocess
import RPi.GPIO as gp
from serial import Serial
import pyraspii as pii
import paths as p

PATHTEST = p.PATHTEST
PATHPROJET =  p.PATHPROJET
PATHTMP = p.PATHTMP
PATHRESSOURCES = p.PATHRESSOURCES
PATHPHOTOG = p.PATHPHOTOG
icons_path = p.icons_path

global resolution_item
global numberOfLEDs

back_ground_color = 175, 222, 255
def _from_rgb(rgb):
	return "#%02x%02x%02x" % rgb

class settings:
    
	def __init__(self, master):
        
		self.master = master
		self.window = Toplevel(self.master)
		self.window.attributes('-fullscreen', True)
		self.w = self.window.winfo_screenwidth()
# 		self.window.geometry('+400+80')
		self.window.title('Dome')
		self.window.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.window, background=_from_rgb(back_ground_color))
		self.frameRet = Frame(self.window, background=_from_rgb(back_ground_color))
		
		self.prop = self.w / 1024 
		
		#icons
		self.photoResolution = ImageTk.PhotoImage(Image.open(icons_path+"resolutions.png").resize((int(self.prop*120), int(self.prop*100)),Image.BILINEAR)) 
		self.photoTile= ImageTk.PhotoImage(Image.open(icons_path+"dome_leds.png").resize((int(self.prop*120), int(self.prop*100)),Image.BILINEAR)) 
		self.photoCamTest = ImageTk.PhotoImage(Image.open(icons_path+"camera_test.png").resize((int(self.prop*120), int(self.prop*100)),Image.BILINEAR))
		self.photoDomeTest = ImageTk.PhotoImage(Image.open(icons_path+"dome_test.png").resize((int(self.prop*120), int(self.prop*100)),Image.BILINEAR))
		self.photoSettings = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeSettings.png").resize((int(self.prop*75), int(self.prop*75)),Image.BILINEAR))
		self.photoRetour = ImageTk.PhotoImage(Image.open(icons_path+"back.png").resize((int(self.prop*75), int(self.prop*75)),Image.BILINEAR))
		
		
		#Boutons
		self.boutonResolution = Button(self.frame, text="Résolution des images",foreground=_from_rgb((176,175,179)),relief="flat",
                                    background=_from_rgb(back_ground_color),image=self.photoResolution,compound=TOP,cursor="tcross",command=self.resolutionSet)
		
		self.boutonTile = Button(self.frame, text="Nombre de LEDs à Allumer",foreground=_from_rgb((176,175,179)),relief="flat",
                                         background=_from_rgb(back_ground_color),image=self.photoTile,compound=TOP,cursor="tcross",command=self.tileSet)
		
		self.boutonCamTest = Button(self.frame, text="Tester la caméra",foreground=_from_rgb((176,175,179)),bd=0,relief="flat",
                                       image=self.photoCamTest,compound=TOP,background=_from_rgb(back_ground_color),command=self.CamTest)
		
		self.boutonDomeTest = Button(self.frame, text="Tester le Dome",relief="flat",foreground=_from_rgb((176,175,179)),
                                   image=self.photoDomeTest,compound=TOP,background=_from_rgb(back_ground_color),command=self.DomeTest)
		
		
		self.boutonFermer = Button(self.frameRet,text="",image=self.photoRetour,foreground=_from_rgb((176,175,179)),compound=TOP,
                                     highlightcolor=_from_rgb((176,175,179)),relief="flat",background=_from_rgb(back_ground_color),command=self.bureau)
		
		
		self.afficher()

	def afficher(self):
		Grid.rowconfigure(self.window, 0, weight=1)
		Grid.columnconfigure(self.window, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.boutonTile.grid(row=2,column=2, padx=10, pady=10, sticky='news')
		# self.boutonCapturePhoto.grid(row=2,column=1,sticky='news')
		self.boutonResolution.grid(row=2,column=3, padx=10, pady=10, sticky='news') #columnspan=2,
		self.boutonCamTest.grid(row=3,column=2, padx=10, pady=10, sticky='news')
		self.boutonDomeTest.grid(row=3,column=3, padx=10, pady=10, sticky='news')
		self.boutonFermer.grid(row=1,column=5,padx=0,pady=0,sticky='news')
		self.frame.grid(row=0,column=0)
		self.frameRet.grid(row=0,column=0, sticky='ne')
		
	def select_item(self):
		
		self.label.config(text=str(self.listbox.get(ANCHOR))+" Selected!")
		print(self.listbox.get(ANCHOR))
		resolution_item = self.listbox.get(ANCHOR)
		if resolution_item == "Full Screen":
			w = self.window.winfo_screenwidth()
			h = self.window.winfo_screenheight()
			resolution_item = w, h
			
		return resolution_item
        
	def resolutionSet(self):
		
		self.win= tk.Toplevel()
		self.win.attributes('-fullscreen', True)
# 		self.win.geometry('+400+80')
		self.win.title('Dome')
		self.win.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.win, background=_from_rgb(back_ground_color))
		
		self.listbox = Listbox(self.frame, background=_from_rgb(back_ground_color), width=40, height=10, selectmode=SINGLE)
		
		## List of resolutions 
		self.listbox.insert(1, "Full Screen")
		self.listbox.insert(2, (1024, 720))
		self.listbox.insert(3, (720, 480))
		self.listbox.insert(4, (480, 360))
		self.listbox.insert(5, (360, 240))
		
		
		self.btn_valid = Button(self.frame, text="Retour", command=self.win.destroy)
		self.label = Label(self.frame, text='')
		
		self.btnretour = Button(self.frame, text="Select", command=self.select_item)
		
        
		Grid.rowconfigure(self.win, 0, weight=1)
		Grid.columnconfigure(self.win, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.btn_valid.grid(row=4,column=5,sticky='news')
		self.listbox.grid(sticky='news')
		self.label.grid(sticky='news')
		self.btnretour.grid(row=5, column=5, sticky='news')
		self.frame.grid(row=0,column=0)
		
	
	def select_led(self):
		self.label.config(text=self.listbox.get(ANCHOR)+" LED Selected!")
		print(self.listbox.get(ANCHOR))
		
		numberOfLEDs = self.listbox.get(ANCHOR)
		return numberOfLEDs
		
		
	def tileSet(self):
		
		self.win = Tk()
		self.win.attributes('-fullscreen', True)
# 		self.win.geometry('+400+80')        
		self.win.title('Dome')
		self.win.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.win, background=_from_rgb(back_ground_color))
		
		self.listbox = Listbox(self.frame, background=_from_rgb(back_ground_color), bd=5, width=40, height=5, font=('Helvetica', 20, 'bold'),
                               selectmode=SINGLE)
		
		## List of LEDs 
		self.listbox.insert(1, "1")
		self.listbox.insert(2, "2")
		self.listbox.insert(3, "3")
		
		self.btn_valid = Button(self.frame, text="Retour", command=self.win.destroy)
		
		self.label = Label(self.frame, text='LEDs Will be ON')
		
		self.btnretour = Button(self.frame, text="Select", command=self.select_led)
		
        
		Grid.rowconfigure(self.win, 0, weight=1)
		Grid.columnconfigure(self.win, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.btn_valid.grid(row=4,column=5,sticky='news')
		self.listbox.grid(sticky='news')
		self.label.grid(sticky='news')
		self.btnretour.grid(row=5, column=5, sticky='news')
		self.frame.grid(row=0,column=0)
		
		
	def CamTest(self):
		
		self.win = Tk()
		self.win.attributes('-fullscreen', True)
# 		self.win.geometry('+400+80')
		self.win.title('Dome')
		self.win.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.win, background=_from_rgb(back_ground_color))
		
		self.frameRet = Frame(self.win, background=_from_rgb(back_ground_color))
		
		### Add Buttons
		self.btn1 = Button(self.frame, text= "CAM ON", height=5, width=10, command=self.take_photo)
		self.btn2 = Button(self.frame, text= "CAM TEST", height=5, width=10, command=self.allumer_cam)
		self.btnRetour = Button(self.frameRet, text="Retour", fg='red', height=5, width=10, command=self.win.destroy)
		Grid.rowconfigure(self.win, 0, weight=1)
		Grid.columnconfigure(self.win, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.btn1.grid(row=2,column=2, padx=5, pady=5, sticky='news')
		self.btn2.grid(row=2,column=3, padx=5, pady=5, sticky='news')
		self.btnRetour.grid(row=3,column=3, sticky='news')
		self.frame.grid(row=0,column=0)
		self.frameRet.grid(row=0, column=0, sticky='ne')
		
		
	def DomeTest(self):
		
		self.win = Tk()
		self.win.attributes('-fullscreen', True)
# 		self.win.geometry('+400+80')
		self.win.title('Dome')
		self.win.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.win, background=_from_rgb(back_ground_color))
		
		self.frameRet = Frame(self.win, background=_from_rgb(back_ground_color))
		
		
		
		### Add Buttons
		self.btn1 = Button(self.frame, text= "ALL ON", height=5, width=10, command=self.allumer)
		self.btn2 = Button(self.frame, text= "ALL OFF", height=5, width=10, command=self.Eteindre)
		self.btn3 = Button(self.frame, text= "ONE LED", height=5, width=10, command=self.OneLed)
		self.btn4 = Button(self.frame, text= "CHENILL", height=5, width=10, command=self.chenillard)
		self.btnRetour = Button(self.frameRet, text="Retour", fg='red', height=5, width=10, command=self.win.destroy)
		
		
		Grid.rowconfigure(self.win, 0, weight=1)
		Grid.columnconfigure(self.win, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.btn1.grid(row=2,column=2, padx=5, pady=5, sticky='news')
		# self.boutonCapturePhoto.grid(row=2,column=1,sticky='news')
		self.btn2.grid(row=2,column=3, padx=5, pady=5, sticky='news') #columnspan=2,
		self.btn3.grid(row=3,column=2, padx=5, pady=5, sticky='news')
		self.btn4.grid(row=3,column=3, padx=5, pady=5, sticky='news')
		self.btnRetour.grid(row=0,column=0, sticky='ne')

		self.frame.grid(row=0,column=0)
		self.frameRet.grid(row=0, column=0, sticky='ne')
		
		
		
	
	#To send  
    #External events
	def allumer(self):
		pii.send_data(1, 0x44)
		return pii.getData_from(0x44)
           
	def Eteindre(self):
		pii.send_data(2, 0x44)
		return pii.getData_from(0x44)
        
	def OneLed(self):
		pii.send_data(3, 0x44)
		return pii.getData_from(0x44)
    
	def chenillard(self):
		pii.send_data(4, 0x44)
		return pii.getData_from(0x44)
		
	def bureau(self):
		self.window.destroy()
		
	## Cam
	def take_photo(self):
		subprocess.run(['raspistill', '-o', 'image.jpg'])
		im = Image.open('image.jpg')
		im.show()
		try:
			os.remove("image.jpg")
		except:
			pass
		if os.path.exists("image.jpg"):
			os.remove("image.jpg")
    
	def allumer_cam(self): ### To edit Later ----- ----- -----  
		pass
	