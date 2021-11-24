import os
import time 
import tkinter as tk
from tkinter import *
from tkinter import simpledialog
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import picamera
from picamera import PiCamera
import time
import subprocess
import RPi.GPIO as gp
from serial import Serial
import pyraspii as pii
import paths as p
import json
from tinydb import TinyDB, Query ### For Data Store --- the best !! 

PATHTEST = p.PATHTEST
PATHPROJET =  p.PATHPROJET
PATHTMP = p.PATHTMP
PATHRESSOURCES = p.PATHRESSOURCES
PATHPHOTOG = p.PATHPHOTOG
icons_path = p.icons_path

global resolution_item
global numberOfLEDs

back_ground_color = 175, 222, 255
DIGITS_FONT_STYLE = ("Arial", 24, "bold")

def _from_rgb(rgb):
	return "#%02x%02x%02x" % rgb

take_pic_img = Image.open(icons_path+"take_pic.png")
global all_data
all_data = {} ### Creating a dict for Json file saving
db = TinyDB('test.json') ### Json File  

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
		self.photoMeta = ImageTk.PhotoImage(Image.open(icons_path+"meta.png").resize((int(self.prop*120), int(self.prop*100)),Image.BILINEAR))
		self.photoRetour = ImageTk.PhotoImage(Image.open(icons_path+"back.png").resize((int(self.prop*75), int(self.prop*75)),Image.BILINEAR))
		
		
		#Boutons
# 		self.boutonResolution = Button(self.frame, text="Résolution des images",foreground=_from_rgb((176,175,179)),relief="flat",
#                                     background=_from_rgb(back_ground_color),image=self.photoResolution,compound=TOP,cursor="tcross",
#                                        command=self.resolutionSet)
		
		self.boutonTile = Button(self.frame, text="Nombre de LEDs à Allumer",foreground=_from_rgb((176,175,179)),relief="flat",
                                         background=_from_rgb(back_ground_color),image=self.photoTile,compound=TOP,cursor="tcross",
                                 command=self.tileSet)
		
		self.boutonCamTest = Button(self.frame, text="Tester la caméra",foreground=_from_rgb((176,175,179)),bd=0,relief="flat",
                                       image=self.photoCamTest,compound=TOP,background=_from_rgb(back_ground_color),
                                    command=self.CamTest)
		
		self.boutonDomeTest = Button(self.frame, text="Tester le Dome",relief="flat",foreground=_from_rgb((176,175,179)),
                                   image=self.photoDomeTest,compound=TOP,background=_from_rgb(back_ground_color),
                                     command=self.DomeTest)
		
		
		self.boutonFermer = Button(self.frameRet,text="",image=self.photoRetour,foreground=_from_rgb((176,175,179)),compound=TOP,
                                     highlightcolor=_from_rgb((176,175,179)),relief="flat",background=_from_rgb(back_ground_color),
                                   command=self.bureau)
		
		self.boutonMeta = Button(self.frame, text="Meta Data d'acquisition", image=self.photoMeta, foreground=_from_rgb((176,175,179)),compound=TOP,
                                     highlightcolor=_from_rgb((176,175,179)),relief="flat",background=_from_rgb(back_ground_color),
                                 command=self.metadata)
		
		self.afficher()

	def afficher(self):
		Grid.rowconfigure(self.window, 0, weight=1)
		Grid.columnconfigure(self.window, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.boutonTile.grid(row=2,column=2, padx=10, pady=10, sticky='news')
		# self.boutonCapturePhoto.grid(row=2,column=1,sticky='news')
		self.boutonMeta.grid(row=2,column=3, padx=10, pady=10, sticky='news') #columnspan=2,
		self.boutonCamTest.grid(row=3,column=2, padx=10, pady=10, sticky='news')
		self.boutonDomeTest.grid(row=3,column=3, padx=10, pady=10, sticky='news')
		self.boutonFermer.grid(row=1,column=5,padx=0,pady=0,sticky='news')
		self.frame.grid(row=0,column=0)
		self.frameRet.grid(row=0,column=0, sticky='ne')
		
#### --------------------- Functions ----------------------------- ############################### 
################################################################################################## 
	
	def select_led(self, event):       
		
		self.selection = event.widget.curselection()
		self.index = self.selection[0]
		self.value = event.widget.get(self.index)
		self.label.config(text="You selected "+" : " + str(self.value))
		print("LEDs Selected : ")
		print(self.index,' -> ', self.value)
		
		all_data['LEDs_Selected'] = self.value
		db.insert(all_data)
		
		return self.value 
		
		
	def tileSet(self):
		
		self.win = Tk()
		self.win.attributes('-fullscreen', True)
# 		self.win.geometry('+400+80')        
		self.win.title('Dome')
		self.win.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.win, background=_from_rgb(back_ground_color))
		self.frameRet = Frame(self.win, background=_from_rgb(back_ground_color)) 
		
		
		self.listbox = Listbox(self.frame, background=_from_rgb(back_ground_color), bd=5, width=50, height=5,
                               font=('Helvetica', 20, 'bold')
                            )
		self.led_list = (0, 1, 2, 3)
		for i in self.led_list:
			self.listbox.insert(END, i)
		
		## List of LEDs
		
		self.btn_valid = Button(self.frameRet, text="Valider",fg='green', font=('Helvetica', 15, 'bold'), width=8, height=3, command=self.win.destroy)
		
		self.label = Label(self.frame, text="...", height=3, font=('Helvetica', 22, 'bold'))
		
		self.listbox.bind('<<ListboxSelect>>', self.select_led)
		
		
        
		Grid.rowconfigure(self.win, 0, weight=1)
		Grid.columnconfigure(self.win, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.btn_valid.grid(row=4,column=5,sticky='news')
		self.listbox.grid(sticky='news')
		self.label.grid(sticky='news')
		self.frame.grid(row=0,column=0)
		self.frameRet.grid(row=0, column=0, sticky='ne') 
		
		### Save Selection 
		all_data['LEDs_Selected'] = self.select_led
		db.insert(all_data)
		
######################################################################################
	def CamTest(self):
		
		self.win = Tk()
		self.win.attributes('-fullscreen', True)
# 		self.win.geometry('+400+80')
		self.win.title('Dome')
		self.win.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.win, background=_from_rgb(back_ground_color))
		
		self.w = self.win.winfo_screenwidth()
		self.prop = self.w / 1024 
		
		self.frameRet = Frame(self.win, background=_from_rgb(back_ground_color))
		
		### Add Photos for Buttons
		# self.photoTakePic = ImageTk.PhotoImage(take_pic_img.resize((int(self.prop*75), int(self.prop*75)),Image.BILINEAR))
		# self.photoTakePic = ImageTk.PhotoImage(Image.open(icons_path+"back.png").resize((int(self.prop*75), int(self.prop*75)),Image.BILINEAR)) 
		
		### Add Buttons
		self.btn_takePic = Button(self.frame, text="Take Picture", height=5, width=10, font=('helvetica', 16), command=self.take_photo)
		self.btn_camTest = Button(self.frame, text= "CAM TEST", height=5, width=10, font=('helvetica', 16), command=self.allumer_cam)
		self.btnRetour = Button(self.frameRet, text="Retour", fg='red', height=5, width=10, font=('helvetica', 12), command=self.win.destroy)
		
		Grid.rowconfigure(self.win, 0, weight=1)
		Grid.columnconfigure(self.win, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.btn_takePic.grid(row=2,column=2, padx=5, pady=5, sticky='news')
		self.btn_camTest.grid(row=2,column=3, padx=5, pady=5, sticky='news')
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
		self.btn_allON = Button(self.frame, text= "ALL ON", height=5, width=15, font=('helevtica', 16), command=self.allumer)
		self.btn_allOFF = Button(self.frame, text= "ALL OFF", height=5, width=15, font=('helevtica', 16), command=self.Eteindre)
		self.btn_OneLED = Button(self.frame, text= "ONE LED", height=5, width=15, font=('helevtica', 16), command=self.OneLed)
		self.btn_Cheni = Button(self.frame, text= "CHENILL", height=5, width=15, font=('helevtica', 16), command=self.chenillard)
		self.btnRetour = Button(self.frameRet, text="Retour", fg='red', height=5, width=10, font=('helevtica', 12), command=self.win.destroy)
		
		
		Grid.rowconfigure(self.win, 0, weight=1)
		Grid.columnconfigure(self.win, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.btn_allON.grid(row=2,column=2, padx=5, pady=5, sticky='news')
		# self.boutonCapturePhoto.grid(row=2,column=1,sticky='news')
		self.btn_allOFF.grid(row=2,column=3, padx=5, pady=5, sticky='news') #columnspan=2,
		self.btn_OneLED.grid(row=3,column=2, padx=5, pady=5, sticky='news')
		self.btn_Cheni.grid(row=3,column=3, padx=5, pady=5, sticky='news')
		self.btnRetour.grid(row=0,column=0, sticky='ne')

		self.frame.grid(row=0,column=0)
		self.frameRet.grid(row=0, column=0, sticky='ne')

#######################################################################-------------
	def metadata(self):
		
		met = metaData()

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
		
	def bureau(self): ###Just to Quit 
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
		camera = PiCamera()
		camera.start_preview()
		time.sleep(10)
		camera.stop_preview()

class metaData(settings):
	def __init__(self):
		self.wind = Tk()
		self.wind.attributes('-fullscreen', True)
		self.wind.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.wind, background=_from_rgb(back_ground_color))
		self.frameRet = Frame(self.wind, background=_from_rgb(back_ground_color))
		self.screenwidth = self.wind.winfo_screenwidth()
		
		self.prop = self.screenwidth / 1024 ### Proportion __ _To have pretty and responsive icons
		
		### Upload Icons  From icons Folder 
		self.photoResolution = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeSettings.png").resize((int(self.prop*75), int(self.prop*75))
                                                                                                  ,Image.BILINEAR))
		self.photoDate = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeSettings.png").resize((int(self.prop*75), int(self.prop*75)),
                                                                             Image.BILINEAR))
		self.photoActor = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeSettings.png").resize((int(self.prop*75), int(self.prop*75)),
                                                                              Image.BILINEAR))
		self.photoPlace = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeSettings.png").resize((int(self.prop*75), int(self.prop*75)),
                                                                              Image.BILINEAR))
		self.photoRetour = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeSettings.png").resize((int(self.prop*75), int(self.prop*75)),
                                                                               Image.BILINEAR))
        
		### Create Buttons with last icons
		self.btnResolutions = Button(self.frame, text="Resolution", font=DIGITS_FONT_STYLE, width=15, height=4, 
            command=self.resolutionSet)
        
		self.btnDate = Button(self.frame, text="Env data", font=DIGITS_FONT_STYLE, width=15, height=4, command=environ_data
            )
        
		self.btnPhotographer = Button(self.frame, text="Photographer", font=DIGITS_FONT_STYLE, width=10, height=4, 
                                      command=photograph_data
            )
        
		self.btnAbout = Button(self.frame, text="About", font=DIGITS_FONT_STYLE, width=15, height=4, command=about
            )
        
		self.btnRet = Button(self.frameRet, text="Retour", fg='red', font=DIGITS_FONT_STYLE, width=8, height=4,
                             command=self.wind.destroy) 
        
		### Display
		Grid.rowconfigure(self.wind, 0, weight=1)
		Grid.columnconfigure(self.wind, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
        
		self.btnResolutions.grid(row=2, column=1, padx=15, pady=15, sticky='news')
		self.btnDate.grid(row=2, column=2, padx=15, pady=15, sticky='news')
		self.btnPhotographer.grid(row=3, column=1, padx=15, pady=15, sticky='news')
		self.btnAbout.grid(row=3, column=2, padx=15, pady=15, sticky='news')
		self.btnRet.grid(row=0, column=0, sticky='news')
        
		self.frame.grid(row=0, column=0)
		self.frameRet.grid(row=0, column=0, sticky='ne')
		
#####################################################################################################
######## FCT RESOLUTION ---- OPT

	def select_item(self, event):
		global resolution_item
		global all_data
		self.selection = event.widget.curselection()
		self.index = self.selection[0]
		self.value = event.widget.get(self.index)
		if self.value == "Full Screen":
			w = self.window.winfo_screenwidth()
			h = self.window.winfo_screenheight()
			resolution_item = w, h
		self.label.config(text="You selected "+" : " + str(self.value))
		resolution_item = str(self.value)
		print("Resolutions :" )
		print(self.index,' -> ', resolution_item)
		
		all_data['Resolution_Selected'] = resolution_item
		
		return resolution_item

        
	def resolutionSet(self):
		
		self.win= tk.Toplevel()
		self.win.attributes('-fullscreen', True)
		self.win.title('Dome')
		self.win.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.win, background=_from_rgb(back_ground_color))
		self.frameRet = Frame(self.win, background=_from_rgb(back_ground_color)) 
		
		self.listbox = Listbox(self.frame, background=_from_rgb(back_ground_color), width=50, height=8, bd=2,
                               font=('Helvetica', 16, 'bold'))
		
		## List of resolutions 
		self.listbox.insert(1, "Full Screen")
		self.listbox.insert(2, (1024, 900))
		self.listbox.insert(3, (900, 720))
		self.listbox.insert(4, (720, 600))
		self.listbox.insert(5, (600, 480))
		self.listbox.insert(6, (480, 360))
		
		self.btn_valid = Button(self.frameRet, text="Valider",fg='green', font=('Helvetica', 15, 'bold'), width=8, height=3, command=self.win.destroy)
		
		self.label = Label(self.frame, text="...", height=3, font=('Helvetica', 22, 'bold'))
		
		self.listbox.bind('<<ListboxSelect>>', self.select_item)
		
		
		Grid.rowconfigure(self.win, 0, weight=1)
		Grid.columnconfigure(self.win, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.btn_valid.grid(row=4,column=5,sticky='news')
		self.listbox.grid(sticky='news')
		self.label.grid(sticky='news')
		self.frame.grid(row=0,column=0)
		self.frameRet.grid(row=0, column=0, sticky='ne')
		
		all_data['Resolution_Selected'] = self.select_item
		

#############################################################################################
####################################  DATA  #######################################################
#######################################DATA#############################################################################
################################################################################################

class photograph_data(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-fullscreen', True) 
        self.data = ["First Name", "Last Name", "Age", "Company"]
        for i,d in enumerate(self.data):
            self.label = tk.Label(self, text=" "+d+" ", height=5, bd=2, relief="ridge", background=_from_rgb(back_ground_color), font=('helvetica', 16),
                                  ).grid(row=i+1, column=1, padx=15, pady=5, sticky='news')
        
        self.entries = [tk.Entry(self, width=60, bd=3, font=('helvetica', 15)) for i in range(len(self.data))]
        self.entry_list = []
        for i,e in enumerate(self.entries):
            e.grid(row=i+1, column=2, padx=15, pady=5)
            self.entry_list.append(e)

        keypad_frame = tk.Frame(self, background=_from_rgb(back_ground_color))
        keypad_frame.grid(row=8, column=4, sticky="s")
        
        btn_quit = tk.Button(keypad_frame, text='quit', bd=2, bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=self.destroy).grid(row=1, column=11, padx=20, pady=10, sticky='ne')
        btn_delete = tk.Button(keypad_frame, text='del', bd=2, bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=self.delete_text).grid(row=1, column=12, padx=20, pady=10, sticky='ne')
        btn_save = tk.Button(keypad_frame, text='save', bd=2, bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=self.save_data).grid(row=1, column=13, padx=20, pady=10, sticky='ne') 
        
        cara = {1: (4, 1), 2: (4, 2), 3: (4, 3),
                        4: (4, 4), 5: (4, 5), 6: (4, 6),
                        7: (4, 7), 8: (4, 8), 9: (4, 9),
                       0: (4, 10), 'a':(5, 1), 'z':(5, 2), 'e':(5, 3), 'r':(5, 4), 't': (5, 5), 'y':(5, 6), 'u':(5, 7), 'i':(5, 8),
                      'o':(5, 9), 'p':(5, 10), 'q':(6, 1), 's':(6, 2), 'd':(6, 3), 'f':(6, 4), 'g':(6, 5), 'h':(6, 6),
                      'j':(6, 7), 'k':(6, 8), 'l':(6, 9), 'm':(6, 10), 'w':(7, 1), 'x':(7, 2), 'c':(7, 3), 'v':(7, 4),
                      'b':(7, 5), 'n':(7, 6), ' ':(7, 7), '_':(7, 8), '-':(7, 9)}
        
            
        for car, grid_value in cara.items():
            if grid_value[0] == 4:
                button = tk.Button(keypad_frame, text=str(car), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=car: self.set_text(x)).grid(row=grid_value[0], column=grid_value[1], padx=5, pady=10, sticky='s')
                
            if grid_value[0] == 5:
                button = tk.Button(keypad_frame, text=str(car), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=car: self.set_text(x)).grid(row=grid_value[0], column=grid_value[1], pady=2, sticky='s')
                
            if grid_value[0] == 6:
                button = tk.Button(keypad_frame, text=str(car), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=car: self.set_text(x)).grid(row=grid_value[0], column=grid_value[1], pady=2, sticky='s')
                
            if grid_value[0] == 7:
                button = tk.Button(keypad_frame, text=str(car), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=car: self.set_text(x)).grid(row=grid_value[0], column=grid_value[1], pady=2, sticky='s')

        self.mainloop()

    def set_text(self, text):
        widget = self.focus_get()
        if widget in self.entries:
            widget.insert("insert", text)
            
    def delete_text(self):
        widget = self.focus_get()
        widget.delete(0, tk.END)
    
    
    def save_data(self):
        global  data_dict
        global data
        data_dict = {}
        for s, i in enumerate(self.entry_list):
            widget = i
            data = widget.get()
            data_dict[s] = data
            data_dict[self.data[s]] = data_dict.pop(s)
        new_wind = Toplevel(self)
        new_wind.title("info")
        new_lab = Label(new_wind, text="data Saved!").grid(row=0, column=0)
        btn_quit_ = Button(new_wind, text="OK", command=new_wind.destroy).grid(row=1, column=0)
        print(data_dict)
        all_data['Photographe'] = data_dict
        db.insert(all_data)
        
################################# Environment  dATa ############################################        
        
class environ_data(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-fullscreen', True)
        
        self.data = ["Today Date", "Where",
                     "Camera Name", "Project Name"
            ]
        
        for i,d in enumerate(self.data):
            self.label = tk.Label(self, text=" "+d+" ", height=5, bd=2, relief="ridge", background=_from_rgb(back_ground_color), font=('helvetica', 16),
                                  ).grid(row=i+1, column=1, padx=15, pady=5, sticky='news')
        
        self.entries = [tk.Entry(self, width=60, bd=3, font=('helvetica', 15)) for i in range(len(self.data))]
        self.entry_list = []
        for i,e in enumerate(self.entries):
            e.grid(row=i+1, column=2, padx=15, pady=5)
            self.entry_list.append(e)

        keypad_frame = tk.Frame(self, background=_from_rgb(back_ground_color))
        keypad_frame.grid(row=8, column=4, sticky="s")
        
        btn_quit = tk.Button(keypad_frame, text='quit', bd=2, bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=self.destroy).grid(row=1, column=11, padx=20, pady=10, sticky='ne')
        btn_delete = tk.Button(keypad_frame, text='del', bd=2, bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=self.delete_text).grid(row=1, column=12, padx=20, pady=10, sticky='ne')
        btn_save = tk.Button(keypad_frame, text='save', bd=2, bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=self.save_data).grid(row=1, column=13, padx=20, pady=10, sticky='ne') 
        
        cara = {1: (4, 1), 2: (4, 2), 3: (4, 3),
                        4: (4, 4), 5: (4, 5), 6: (4, 6),
                        7: (4, 7), 8: (4, 8), 9: (4, 9),
                       0: (4, 10), 'a':(5, 1), 'z':(5, 2), 'e':(5, 3), 'r':(5, 4), 't': (5, 5), 'y':(5, 6), 'u':(5, 7), 'i':(5, 8),
                      'o':(5, 9), 'p':(5, 10), 'q':(6, 1), 's':(6, 2), 'd':(6, 3), 'f':(6, 4), 'g':(6, 5), 'h':(6, 6),
                      'j':(6, 7), 'k':(6, 8), 'l':(6, 9), 'm':(6, 10), 'w':(7, 1), 'x':(7, 2), 'c':(7, 3), 'v':(7, 4),
                      'b':(7, 5), 'n':(7, 6), ' ':(7, 7), '_':(7, 8), '-':(7, 9)}
        
            
        for car, grid_value in cara.items():
            if grid_value[0] == 4:
                button = tk.Button(keypad_frame, text=str(car), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=car: self.set_text(x)).grid(row=grid_value[0], column=grid_value[1], padx=5, pady=10, sticky='s')
                
            if grid_value[0] == 5:
                button = tk.Button(keypad_frame, text=str(car), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=car: self.set_text(x)).grid(row=grid_value[0], column=grid_value[1], pady=2, sticky='s')
                
            if grid_value[0] == 6:
                button = tk.Button(keypad_frame, text=str(car), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=car: self.set_text(x)).grid(row=grid_value[0], column=grid_value[1], pady=2, sticky='s')
                
            if grid_value[0] == 7:
                button = tk.Button(keypad_frame, text=str(car), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=car: self.set_text(x)).grid(row=grid_value[0], column=grid_value[1], pady=2, sticky='s')

        self.mainloop()

    def set_text(self, text):
        widget = self.focus_get()
        if widget in self.entries:
            widget.insert("insert", text)
            
    def delete_text(self):
        widget = self.focus_get()
        widget.delete(0, tk.END)
    
    
    def save_data(self):
        global  data_dict
        global data
        data_dict = {}
        for s, i in enumerate(self.entry_list):
            widget = i
            data = widget.get()
            data_dict[s] = data
            data_dict[self.data[s]] = data_dict.pop(s)
        new_wind = Toplevel(self)
        new_wind.title("info")
        new_lab = Label(new_wind, text="data Saved!").grid(row=0, column=0)
        btn_quit_ = Button(new_wind, text="OK", command=new_wind.destroy).grid(row=1, column=0)
        print(data_dict)
        all_data['environmentData'] = data_dict
        db.insert(all_data)
        
#################################################### ABOUT ####################################### Other Data ##
        
class about(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-fullscreen', True)
        
        self.data = ["Technique", "Automation",
                     "AcquisitionType", "Measurement", "Others"
            ]
        
        for i,d in enumerate(self.data):
            self.label = tk.Label(self, text=" "+d+" ", height=5, bd=2, relief="ridge", background=_from_rgb(back_ground_color), font=('helvetica', 12),
                                  ).grid(row=i+1, column=1, padx=15, pady=5, sticky='news')
        
        self.entries = [tk.Entry(self, width=60, bd=3, font=('helvetica', 15)) for i in range(len(self.data))]
        self.entry_list = []
        for i,e in enumerate(self.entries):
            e.grid(row=i+1, column=2, padx=15, pady=5)
            self.entry_list.append(e)

        keypad_frame = tk.Frame(self, background=_from_rgb(back_ground_color))
        keypad_frame.grid(row=8, column=4, sticky="s")
        
        btn_quit = tk.Button(keypad_frame, text='quit', bd=2, bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=self.destroy).grid(row=1, column=11, padx=20, pady=10, sticky='ne')
        btn_delete = tk.Button(keypad_frame, text='del', bd=2, bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=self.delete_text).grid(row=1, column=12, padx=20, pady=10, sticky='ne')
        btn_save = tk.Button(keypad_frame, text='save', bd=2, bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=self.save_data).grid(row=1, column=13, padx=20, pady=10, sticky='ne') 
        
        cara = {1: (4, 1), 2: (4, 2), 3: (4, 3),
                        4: (4, 4), 5: (4, 5), 6: (4, 6),
                        7: (4, 7), 8: (4, 8), 9: (4, 9),
                       0: (4, 10), 'a':(5, 1), 'z':(5, 2), 'e':(5, 3), 'r':(5, 4), 't': (5, 5), 'y':(5, 6), 'u':(5, 7), 'i':(5, 8),
                      'o':(5, 9), 'p':(5, 10), 'q':(6, 1), 's':(6, 2), 'd':(6, 3), 'f':(6, 4), 'g':(6, 5), 'h':(6, 6),
                      'j':(6, 7), 'k':(6, 8), 'l':(6, 9), 'm':(6, 10), 'w':(7, 1), 'x':(7, 2), 'c':(7, 3), 'v':(7, 4),
                      'b':(7, 5), 'n':(7, 6), ' ':(7, 7), '_':(7, 8), '-':(7, 9)}
        
            
        for car, grid_value in cara.items():
            if grid_value[0] == 4:
                button = tk.Button(keypad_frame, text=str(car), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=car: self.set_text(x)).grid(row=grid_value[0], column=grid_value[1], padx=5, pady=10, sticky='s')
                
            if grid_value[0] == 5:
                button = tk.Button(keypad_frame, text=str(car), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=car: self.set_text(x)).grid(row=grid_value[0], column=grid_value[1], pady=2, sticky='s')
                
            if grid_value[0] == 6:
                button = tk.Button(keypad_frame, text=str(car), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=car: self.set_text(x)).grid(row=grid_value[0], column=grid_value[1], pady=2, sticky='s')
                
            if grid_value[0] == 7:
                button = tk.Button(keypad_frame, text=str(car), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=car: self.set_text(x)).grid(row=grid_value[0], column=grid_value[1], pady=2, sticky='s')

        self.mainloop()

    def set_text(self, text):
        widget = self.focus_get()
        if widget in self.entries:
            widget.insert("insert", text)
            
    def delete_text(self):
        widget = self.focus_get()
        widget.delete(0, tk.END)
    
    
    def save_data(self):
        global  data_dict
        global data
        data_dict = {}
        for s, i in enumerate(self.entry_list):
            widget = i
            data = widget.get()
            data_dict[s] = data
            data_dict[self.data[s]] = data_dict.pop(s)
        new_wind = Toplevel(self)
        new_wind.title("info")
        new_lab = Label(new_wind, text="data Saved!").grid(row=0, column=0)
        btn_quit_ = Button(new_wind, text="OK", command=new_wind.destroy).grid(row=1, column=0)
        print(data_dict)
        all_data['otherData'] = data_dict
        db.insert(all_data)

print(all_data)
json.dumps(all_data, indent=4)
with open('data.txt', 'w') as outfile:
    json.dump(all_data, outfile)