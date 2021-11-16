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
import time
import json
from datetime import datetime
# from Settings.settings import select_led, select_item

#Pin connected to ST_CP of 74HC595
latchPin = 31
#Pin connected to SH_CP of 74HC595
clockPin = 29
#Pin connected to DS of 74HC595
dataPin = 33
nbbras=8
tabled=[2**i for i in range(8)]
ledposition=[i for i in range(65)]

PATHTEST = p.PATHTEST
PATHPROJET =  p.PATHPROJET
PATHTMP = p.PATHTMP
PATHRESSOURCES = p.PATHRESSOURCES
PATHPHOTOG = p.PATHPHOTOG
icons_path = p.icons_path

global nomprojet
global nbimg
global nbimgphotog
global NbImage

nbimgphotog = 50

DIGITS_FONT_STYLE = ("Arial", 24, "bold")
back_ground_color = 175, 222, 255

def _from_rgb(rgb):
	return "#%02x%02x%02x" % rgb

class FenetreCapture:

	def __init__(self, master):
		#Parametres globaux
		global nomprojet
		global CAMERASPEED
		global nbimg
		
		
		self.varprogress = IntVar()
		self.txtboutonFrameCamera = StringVar()
		self.varprogress.set(int(0))
		self.txtboutonFrameCamera.set("Lancer la prévisualisation")
		
		# management fenetre
		self.master = master
		self.window = Toplevel(self.master)
# 		self.window.geometry('+400+80') 
		self.window.attributes("-fullscreen",True)
		self.w = self.window.winfo_screenwidth()
		self.window.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.window, background=_from_rgb(back_ground_color))
		
		self.prop = self.w / 1024
		
		self.frame_digits = Frame(self.window, background=_from_rgb(back_ground_color))
		self.frame_alphas1 = Frame(self.window, background=_from_rgb(back_ground_color))
		self.frame_alphas2 = Frame(self.window, background=_from_rgb(back_ground_color))
		self.frame_alphas3 = Frame(self.window, background=_from_rgb(back_ground_color))
		
		self.frameRet = Frame(self.window, background=_from_rgb(back_ground_color))
		self.frameDef = Frame(self.window, background=_from_rgb(back_ground_color))
		self.photoRetour = ImageTk.PhotoImage(Image.open(icons_path+"back.png").resize((int(self.prop*75), int(self.prop*75)),Image.BILINEAR))
		
		self.projectName = Entry(self.frame, width=40)
		self.NbImage = Entry(self.frame, width=40)
		
		self.current_expression = ""
		self.total_expression = ""
		self.keypad = self.keyboard_()
		
		self.btn_back = Button(self.frameRet, text="Retour",foreground=_from_rgb((176,175,179)),relief="flat",
                                    background=_from_rgb(back_ground_color),image=self.photoRetour,compound=TOP,cursor="tcross",command=self.window.destroy)
		
		self.label_proName = Label(self.frame, text='Enter Project Name', background=_from_rgb(back_ground_color))
		self.label_imgNb = Label(self.frame, text='Enter Image Number', background=_from_rgb(back_ground_color))
		self.btn_save = Button(self.frame, text='Save', bg='green',command=self.save_projectParam)
		
		self.btn_default = Button(self.frameDef, text='Start with Default Param', bg='yellow', command=self.default_param)
		self.btn_clear = Button(self.frame, text='Clear', bg='white', command=self.clear)
		
		Grid.rowconfigure(self.window, 0, weight=1)
		Grid.columnconfigure(self.window, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		
		self.label_proName.grid(row=1, column=1, sticky='news')
		self.projectName.grid(row=1,column=2, padx=5, pady=15, sticky='news')
		self.label_imgNb.grid(row=2, column=1, sticky='news')
		self.NbImage.grid(row=2, column=2, padx=5, pady=15, sticky='news')
		self.btn_save.grid(row=3, column=6, sticky='news')
		self.btn_back.grid(row=0, column=6, sticky='n')
		self.btn_default.grid(row=0, column=7, padx=5, pady=5, sticky='nw')
		self.btn_clear.grid(row=6 ,column=6)
		
		self.frameRet.grid(row=0, column=0, sticky='ne')
		self.frameDef.grid(row=0, column=0, sticky='nw')
		self.frame.grid(row=0,column=0)
		self.frame_digits.grid(row=3,column=0, pady=5)
		self.frame_alphas1.grid(row=4,column=0, sticky='n')
		self.frame_alphas2.grid(row=5,column=0, sticky='n')
		self.frame_alphas3.grid(row=6,column=0, sticky='n')
		
		
	def default_param(self):
		print('default Project')
		nomprojet = str(defaultprojet+str(ConfigNumProjet(PATHPROJET)))
		nbimg = 64 
		
		
	def keyboard_(self):
        
		self.digits = {9: (3, 1), 8: (3, 2), 7: (3, 3),
                        6: (3, 4), 5: (3, 5), 4: (3, 6),
                        3: (3, 7), 2: (3, 8), 1: (3, 9),
                       0: (3, 10)
		}
		self.alpha = {'a':(4, 1), 'z':(4, 2), 'e':(4, 3), 'r':(4, 4), 't': (4, 5), 'y':(4, 6), 'u':(4, 7), 'i':(4, 8),
                      'o':(4, 9), 'p':(4, 10), 'q':(5, 1), 's':(5, 2), 'd':(5, 3), 'f':(5, 4), 'g':(5, 5), 'h':(5, 6),
                      'j':(5, 7), 'k':(5, 8), 'l':(5, 9), 'm':(5, 10), 'w':(6, 1), 'x':(6, 2), 'c':(6, 3), 'v':(6, 4),
                      'b':(6, 5), 'n':(6, 6), '_':(6, 8)}
		
		self.frame.rowconfigure(0, weight=1)
		
		for x in range(1, 10):
			self.frame.rowconfigure(x, weight=1)
			self.frame.columnconfigure(x, weight=1)
			
		for digit, grid_value in self.digits.items():
			button = Button(self.frame_digits, text=str(digit), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=digit: self.add_to_expression_digit(x))
			button.grid(row=grid_value[0], column=grid_value[1], sticky='news')
		
		for alpha, grid_value in self.alpha.items():
			if grid_value[0] == 4:
				button = Button(self.frame_alphas1, text=str(alpha), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=alpha: self.add_to_expression_alpha(x))
				button.grid(row=grid_value[0], column=grid_value[1], sticky='news')
			if grid_value[0] == 5:
				button = Button(self.frame_alphas2, text=str(alpha), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=alpha: self.add_to_expression_alpha(x))
				button.grid(row=grid_value[0], column=grid_value[1], sticky='news')
			elif grid_value[0] == 6: 
				button = Button(self.frame_alphas3, text=str(alpha), bg='white', fg='blue', font=DIGITS_FONT_STYLE,
                            borderwidth=0, command=lambda x=alpha: self.add_to_expression_alpha(x))
				button.grid(row=grid_value[0], column=grid_value[1], sticky='news')
		
		self.bind_keys()
        
	def add_to_expression_digit(self, value):
		self.current_expression += str(value)
		self.NbImage.insert(END, value)
	
	def add_to_expression_alpha(self, value):       
		self.current_expression += str(value)
		self.projectName.insert(END, value)
		
		
	def bind_keys(self):
		self.window.bind("<Return>", lambda event: self.evaluate())
		for key in self.digits:
			self.window.bind(str(key), lambda event, digit=key: self.add_to_expression_digit(digit))
		
		
	def clear(self):
		self.current_expression = ""
		self.total_expression = ""
		self.NbImage.delete(0, END)
		self.projectName.delete(0, END)
		
	##### PROGRESS BAR
# 	def update_progress_label(self):
# 		return f"Current Progress: {pb['value']}%"
# 	
# 	def progress(self):
# 		if self.pb['value'] &lt; 100:
# 			self.pb['value'] += 20
# 			self.value_label['text'] = self.update_progress_label()
# 		else:
# 			showinfo(message='Complet!')
# 			
# 	def stop(self):
# 		self.pb.stop()
# 		self.value_label['text'] = self.update_progress_label()
# 		
# 		
# 	def pb(self, wind):
# 		self.pb = ttk.Progressbar(self.wind, orient='horizontal', mode='determinate', length=280)
# 		self.value_label = ttk.Label(self.wind, text=self.update_progress_label())
# 		self.value_label.grid(row=2, column=2, columnspan=2, sticky='news')
		

        
	def save_projectParam(self):
		global projectName
		projectName = self.projectName.get()
		if projectName.isspace() == True or len(projectName)<3:
			# self.wind = Toplevel(self.master)
			messagebox.showwarning("warning","Enter a Valid data")
		
		nomprojet = projectName
		print(nomprojet)
        
		global NbImage
		NbImage = self.NbImage.get()
		if NbImage.isspace() == True or str(NbImage).isnumeric() == False: 
			messagebox.showwarning("warning","Enter a Valid data")            
		nbimg = NbImage
		print(nbimg)
		
		self.afficher(self.master)

	def afficher(self, master):
		
		self.wind = Toplevel(self.master)
		self.wind.attributes('-fullscreen', True)
		self.wind.title('Dome')
		
		#Images
		self.iconeretour = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeRetour.png").resize((int(self.prop*75), int(self.prop*75)), Image.BILINEAR))
		self.imageOk = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeOk.png").resize((int(self.prop*75), int(self.prop*75)),Image.BILINEAR))
		#Frame
		self.frame = Frame(self.wind, background=_from_rgb(back_ground_color)) #,height=50,width=10
		# self.frame_data = Frame(self.wind, background=_from_rgb(back_ground_color))
		#Label 
		self.labelExpo = Label(self.frame, text="Exposition",foreground=_from_rgb((5,5,5)),relief="flat",background=_from_rgb((200, 200, 200)), compound=TOP)
		self.labelLed = Label(self.frame, text="LED",foreground=_from_rgb((5,5,5)),relief="flat",background=_from_rgb((200, 200, 200)), compound=TOP)
		
		#Boutons
		self.labelProjet = Button(self.frame, text=projectName,foreground=_from_rgb((5,5,5)),relief="flat",background=_from_rgb(back_ground_color), command=self.OuvreTextEntry)
		self.boutonOk = Button(self.frame, text="Capture", image=self.imageOk,foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((41,40,46)), compound=TOP, command=self.startCapture)
		self.boutonRetour = Button(self.frame, text="Retour", image=self.iconeretour,foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((41,40,46)),compound=TOP, command=self.wind.destroy)
		self.boutonFrameCamera = Button(self.frame,textvariable=self.txtboutonFrameCamera, foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((41,40,46)),command=self.startPreview) 
		#Slides
		self.sliderExpo = Scale(self.frame, orient='vertical', from_=-25, to=25, resolution=1, tickinterval=5,relief = "flat",foreground=_from_rgb((176,175,179)),background=_from_rgb((41,40,46)), command=self.updateExposure)
		self.sliderLed = Scale(self.frame, orient='vertical', from_=0, to=64, resolution=1, relief = "flat",foreground=_from_rgb((176,175,179)),background=_from_rgb((41,40,46)),command=self.updateLed)
		self.progressbar = ttk.Progressbar(self.wind, maximum=nbimgphotog,variable=self.varprogress,orient ="horizontal",mode ="determinate")
		#Camera
		#On récupère la taille de la fenêtre
		self.camerapreviewX = 400
		self.camerapreviewY = int(self.camerapreviewX * 3 / 4)
		self.cameraposX= int((self.wind.winfo_screenwidth() / 2) - (self.camerapreviewX / 2))
		self.cameraposY= int((self.wind.winfo_screenheight() / 2) - (self.camerapreviewY / 2))
		#print("cameraposX = "+ str(self.cameraposX))
		#On crée une frame pour décaler les boutons autour
		#self.frameCamera = Frame(self.frame,background=_from_rgb((100,100,100)),width=self.camerapreviewX+20, height=self.camerapreviewY+50)
		#self.afficher(self.master)
		self.data = {}
		self.data['Date'] = str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
		self.data['Project Name'] = str(projectName)
		self.data['Number of Images'] = str(NbImage)
		print(self.data) 
		
# 		with open('data.json', 'wb') as fp:
# 			json.dump(dict, fp)
		self.startPreview()
		
		#Grid.rowconfigure(self.window, 0, weight=1)
		#Grid.columnconfigure(self.window, 0, weight=1)
		
		Grid.rowconfigure(self.wind, 0, weight=1)
		Grid.columnconfigure(self.wind, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.rowconfigure(self.frame, 1, weight=5)
		Grid.rowconfigure(self.frame, 2, weight=1)
		Grid.rowconfigure(self.frame, 3, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 1, weight=5)
		Grid.columnconfigure(self.frame, 2, weight=1)
		#Grid.rowconfigure(self.frameCamera, 0, weight=1)
		#Grid.columnconfigure(self.frameCamera, 0, weight=1)
		self.frame.grid(row=0,column=0,sticky='nsew')
		self.boutonRetour.grid(row=0, column=0,sticky='nsew')
		self.labelProjet.grid(row=0,column=1,sticky="nsew")
		self.boutonOk.grid(row=0, column=2,sticky='nsew')
		self.sliderExpo.grid(row=1,column=0,sticky='nsew')
		#self.frameCamera.grid(row=1,column=1,sticky='news')
		self.boutonFrameCamera.grid(row=1,column=1,sticky='nsew') #dans le frame camera
		self.sliderLed.grid(row=1,column=2,sticky='nsew')
		self.labelExpo.grid(row=2,column=0,pady=50,sticky='nsew')
		self.labelLed.grid(row=2,column=2,pady=50,sticky='nsew')
		self.progressbar.grid(row=3,column=0,sticky="ew")
		self.boutonFrameCamera.configure(state='disabled')

	def startPreview(self):
		#Lancement Camera
		nomprojet = projectName
		self.labelProjet.configure(text=nomprojet)
		self.wind.update()
		self.wind.update_idletasks()
		self.camera = picamera.PiCamera()
		self.camera.resolution = (self.camerapreviewX,self.camerapreviewY)
		self.camera.still_stats = 'true' #MODIFICATION190621
		self.camera.exposure_compensation = 0
		self.camera.iso=100
		self.camera.rotation = 180
		self.camera.awb_mode= 'auto'
		time.sleep(0.5)
		self.camera._check_camera_open()
		self.camera.preview_fullscreen = False
		self.camera.preview_window = (self.cameraposX,self.cameraposY,self.camerapreviewX,self.camerapreviewY)
		self.camera.start_preview()
		self.boutonFrameCamera.configure(state='disabled')
		zero()
		LED(1)

	def fermerFenetreCapture(self):
		zero()
		self.camera.stop_preview()
		self.camera.close()
		self.wind.destroy()

	def OuvreTextEntry(self):
		self.camera.stop_preview()
		self.camera.close()
		#self.window.destroy()
		fenetreTextEntry = TextEntry(self.master)
		self.boutonFrameCamera.configure(state='active')
		print("on ouvre la fenetre de saisieTexte")

	def updateExposure(self,abc):
		self.camera.exposure_compensation = self.sliderExpo.get()
		#print(str(self.camera.exposure_compensation))

	def updateLed(self,abc):
		start = time.time()
		zero2()
		LED(ledposition[int(self.sliderLed.get())])
		end = time.time()
		print(end - start)

	def startCapture(self):
		global nbimg
		global CAMERASPEED
		global EXPOSURECOMPENSATION
		EXPOSURECOMPENSATION = self.sliderExpo.get()
		CAMERASPEED = self.camera.exposure_speed
		self.camera.shutter_speed= CAMERASPEED
		print("shutter_speed = "+ str(CAMERASPEED))
		print("exposure_compensation = "+ str(EXPOSURECOMPENSATION))
		
		self.data["shutter speed"] = str(CAMERASPEED)
		self.data["exposure compensation"] = str(EXPOSURECOMPENSATION)
		
		self.camera.awb_mode = 'off'
		AWB_GAINS = self.camera.awb_gains
		self.camera.stop_preview()
		self.camera.close()
		time.sleep(0.1)
		#self.window.destroy()
		self.sliderExpo.configure(state='disabled')
		self.sliderLed.configure(state='disabled')
		self.boutonOk.configure(state='disabled')
		self.boutonRetour.configure(state='disabled')
		self.labelProjet.configure(state='disabled')
		self.wind.update()
		#Camera
		self.camera = picamera.PiCamera()
		self.camera.resolution = 480, 360 #3280 × 2464 #2460,1848
		self.data["Resolution"] = self.camera.resolution
		self.camera.iso=100
		self.camera.rotation = 180
		self.camera.preview_fullscreen = False
		self.camera.still_stats = 'true' #MODIFICATION190621
		self.camera.preview_window = (self.cameraposX,self.cameraposY,self.camerapreviewX,self.camerapreviewY)
		time.sleep(0.2)
		self.camera._check_camera_open()
		zero()
		LED(int(ledposition[int(0)]))
		self.camera.start_preview()
		time.sleep(1)
		self.camera.exposure_mode = 'off'
		self.camera.shutter_speed= CAMERASPEED
		self.camera.exposure_compensation = EXPOSURECOMPENSATION
		self.camera.awb_mode = 'off'
		self.camera.awb_gains = AWB_GAINS
		##############
		#	 PDV.   #
		#	 PDV.   #
		#	 PDV.   #
		#	 PDV.   #
		#	 PDV.   #
		#	 PDV.   #
		#	 PDV.   #
		##############
		
		nbimg = int(NbImage) 
		for i in range(0, nbimg):
			zero2()
			LED(ledposition[i])
			time.sleep(0.75)
			self.camera.capture(PATHTMP +'{0:02d}'.format(i)+".jpg",format='jpeg',quality=95,use_video_port=False)
			time.sleep(0.25)
			self.varprogress.set(int(i))
			self.wind.update()
			self.wind.update_idletasks()
		self.camera.stop_preview()


		##############
		#	 PDV.   #
		#	 PDV.   #
		#	 PDV.   #
		#	 PDV.   #
		#	 PDV.   #
		#	 PDV.   #
		#	 PDV.   #
		##############
		zero()
		self.boutonOk.configure(command=self.Continuer,text="Continuer")
		self.txtboutonFrameCamera.set("Fin de la prise de vue")
		self.boutonOk.configure(state='active')
		self.boutonRetour.configure(state='active')
		self.camera.close()

	def pdv(self,img):
		imagepath = PATHTMP +'{0:02d}'.format(img)+".jpg"
		print("On prend la photo numéro : "+str(imagepath))
		self.camera.capture(imagepath,format='jpeg',quality=100,use_video_port=True)

	def Continuer(self):
		zero()
		self.movefiles()
		self.wind.destroy()

	def movefiles(self):
		global nomprojet
		dossierprojet = PATHPROJET + nomprojet
		os.system("mkdir "+dossierprojet)#Cree un nouveau repertoire pour un projet
		#os.system("mkdir "+PATHPROJET+str(num)+"/miniature") 
		cmd1 = "cp "+PATHTMP+"01.jpg "+PATHTMP+"miniature.jpg"
		cmd2 = "convert "+PATHTMP+"miniature.jpg -thumbnail 320x240 "+PATHTMP+"miniature.jpg"
		#find src_image_dir/ -type f -name '*.jpg' -print0 | xargs -0r mv -t dst_image_dir/
		#cmd3 = "mv "+PATHTMP+"*.jpg "+dossierprojet
		cmd3 = "find "+PATHTMP+" -type f -name '*.jpg' -print0 | xargs -0r mv -t "+dossierprojet
		os.system(cmd1)
		os.system(cmd2)
		os.system(cmd3) #deplace les photos dans ce repertoire
	
	def print_data(self):
		print(self.data)
		
		
def ConfigNumImage(Path): #num de l'image
	numero = 0
	while True :
		file = '{0:02d}'.format(numero) + "pic.jpg"
		if os.path.isfile(Path+file) :
			numero+=1
			continue
		else :
			return numero

def ConfigNumProjet(Path):
	numero = 0
	while True:
		projet = str(numero)
		if os.path.exists(Path +"Projet"+ projet):
			numero += 1
			continue
		else:
			return numero

def _from_rgb(rgb):
	"""translates an rgb tuple of int to a tkinter friendly color code
	"""
	return "#%02x%02x%02x" % rgb 

def configGPIO(): #configue des pins gpio
	gp.setwarnings(False)
	gp.setmode(gp.BOARD)
	gp.setup(latchPin, gp.OUT)
	gp.output(latchPin, False)
	gp.setup(clockPin, gp.OUT)
	gp.output(clockPin, False)
	gp.setup(dataPin, gp.OUT)
	gp.output(dataPin, False)

def ShiftOut2(val):
	if type(val) is bytes:
		val=val[0]
	gp.output(latchPin, 0)
	for x in range(8):
		gp.output(dataPin, (val >> x) & 1)
		gp.output(clockPin, 1)
		gp.output(clockPin, 0)
		gp.output(latchPin, 1)

def shiftOut (dataPin, cPin, order, val):
	#print(val)
	if type(val) is bytes:
		val=val[0]
		#print(val)
	if (order == "MSBFIRST"):
		for i in range(7,-1,-1):
			#print("La valeur du bit n°"+str(i)+" est "+str((val >> i) & 0b00000001))
			if (val >> i) & 1 == True:
				gp.output(dataPin, True) 
				#print("1")
			else:
				gp.output(dataPin, False)
			time.sleep(0.0001)
			gp.output(cPin, True)
			time.sleep(0.0001)
			gp.output(cPin, False)
			gp.output(dataPin, False)
			time.sleep(0.0001)
	else:
		print("LSB")
		for i in range(0,7,1):
			if (val >> i) & 1 == True:
				gp.output(dataPin, False) 
			else:
				gp.output(dataPin, True)
			gp.output(cPin, True) 
			gp.output(cPin, False) 

def zero():
	#gp.output(latchPin, False)
	print('...')
	time.sleep(0.001)
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	time.sleep(0.001)
	print('...')
	#gp.output(latchPin, True)

def zero2():
	#BitBang flush 0 on all Leds
	gp.output(latchPin, False)
	time.sleep(0.001)
	gp.output(dataPin, False)
	time.sleep(0.0001)
	for i in range(0,64):
		gp.output(clockPin, True)
		time.sleep(0.0001)
		gp.output(clockPin, False)
		time.sleep(0.0001)
	time.sleep(0.0001)
	gp.output(latchPin, True)
# Créer une class LedController

def LED(ledindex):
	gp.output(latchPin, False)
	time.sleep(0.001)
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	bras=int(ledindex/8)
	for k in range(bras+1,nbbras,1):
		shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00')  
	#On verifie quel Led dans quel ordre on allume	
	led = tabled[int(ledindex %8)]
	#print("On allume la led "+str(int(ledindex % 8)+1)+" de valeur "+str(led)+" du bras "+str(bras+1))
	shiftOut(dataPin, clockPin, "MSBFIRST", int(led))  
	for j in range(0,bras,1):
		shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00') 
		#print("00000000-apres")
	time.sleep(0.001)
	gp.output(latchPin, True)
	#print("Led allumée")

def LED2(ledindex):
	bras=int(ledindex/8)
	led = tabled[int(ledindex %8)]
	for k in range(bras+1,nbbras,1):
		ShiftOut2(b'\x00')  
	ShiftOut2(led)  
	for j in range(0,bras,1):
		ShiftOut2(b'\x00') 

def AllumeLedPhotog():
	#00000000001AF6DD
	gp.output(latchPin, False)
	time.sleep(0.001)
	#print("On allume les leds de")
	#print(str(bin(0x0000000000BB57D6)))
	shiftOut(dataPin, clockPin, "MSBFIRST", int(187));
	shiftOut(dataPin, clockPin, "MSBFIRST", int(87));
	shiftOut(dataPin, clockPin, "MSBFIRST", int(214));
	#shiftOut(dataPin, clockPin, "MSBFIRST", int(255));
	#shiftOut(dataPin, clockPin, "MSBFIRST", int(255));
	#shiftOut(dataPin, clockPin, "MSBFIRST", int(255));
	#shiftOut(dataPin, clockPin, "MSBFIRST", int(255));
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	shiftOut(dataPin, clockPin, "MSBFIRST", b'\x00');
	time.sleep(0.001)
	gp.output(latchPin, True)
	print("Led allumée")