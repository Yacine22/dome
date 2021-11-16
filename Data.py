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
import os 

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

nbimgphotog = 50

DIGITS_FONT_STYLE = ("Arial", 24, "bold")
back_ground_color = 175, 222, 255
def _from_rgb(rgb):
	return "#%02x%02x%02x" % rgb



class FenetreCapturePhoto:

	def __init__(self, master):
		#Parametres globaux
		global nomprojet
		global CAMERASPEED
		global nbimgphotog
		nomprojet = str(defaultprojet+str(ConfigNumProjet(PATHPROJET)))
		self.varprogress = IntVar()
		self.txtboutonFrameCamera = StringVar()
		self.varprogress.set(int(0))
		self.txtboutonFrameCamera.set("Lancer la prévisualisation")
		# management fenetre
		self.master = master
		self.window = tk.Toplevel(self.master)
		self.window.geometry('+400+80')
		# self.window.attributes("-fullscreen",True)
		self.window.configure(background=_from_rgb((41,40,46)))
		Grid.rowconfigure(self.window, 0, weight=1)
		Grid.columnconfigure(self.window, 0, weight=1)
		#Images
		self.iconeretour = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeRetour.png").resize((75,75),Image.BILINEAR))
		self.imageOk = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeOk.png").resize((75,75),Image.BILINEAR))
		#Frame
		self.frame = Frame(self.window,background=_from_rgb((41,40,46))) #,height=50,width=10
		#Label 
		self.labelExpo = Label(self.frame, text="Exposition",foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((41,40,46)), compound=TOP)
		self.labelLed = Label(self.frame, text="Nombre de photos",foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((41,40,46)), compound=TOP)
		
		#Boutons
		self.labelProjet = Button(self.frame, text=nomprojet,foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((41,40,46)), command=self.OuvreTextEntry)
		self.boutonOk = Button(self.frame, text="Capture", image=self.imageOk,foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((41,40,46)), compound=TOP, command=self.startCapture)
		self.boutonRetour = Button(self.frame, text="Retour", image=self.iconeretour,foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((41,40,46)),compound=TOP, command=self.fermerFenetreCapture)
		self.boutonFrameCamera = Button(self.frame,textvariable=self.txtboutonFrameCamera, foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((41,40,46)),command=self.startPreview) 
		#Slides
		self.sliderExpo = Scale(self.frame, orient='vertical', from_=-25, to=25, resolution=1, tickinterval=5,relief = "flat",foreground=_from_rgb((176,175,179)),background=_from_rgb((41,40,46)), command=self.updateExposure)
		self.sliderNbPhoto = Scale(self.frame, orient='vertical', from_=1, to=120, resolution=1,relief = "flat",foreground=_from_rgb((176,175,179)),background=_from_rgb((41,40,46)),command=self.updateNbPhoto)
		self.progressbar = ttk.Progressbar(self.window,maximum=nbimgphotog,variable=self.varprogress,orient ="horizontal",mode ="determinate")
		self.sliderNbPhoto.set(int(nbimgphotog))
		#Camera
		#On récupère la taille de la fenêtre
		self.camerapreviewX = 400
		self.camerapreviewY = int(self.camerapreviewX * 3 / 4)
		self.cameraposX= int((self.window.winfo_screenwidth() / 2) - (self.camerapreviewX / 2))
		self.cameraposY= int((self.window.winfo_screenheight() / 2) - (self.camerapreviewY / 2))
		#print("cameraposX = "+ str(self.cameraposX))
		#On crée une frame pour décaler les boutons autour
		#self.frameCamera = Frame(self.frame,background=_from_rgb((100,100,100)),width=self.camerapreviewX+20, height=self.camerapreviewY+50)
		
		self.startPreview()
		self.afficher()

	def afficher(self):
		Grid.rowconfigure(self.window, 0, weight=1)
		Grid.columnconfigure(self.window, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=2)
		Grid.rowconfigure(self.frame, 1, weight=20)
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
		self.sliderNbPhoto.grid(row=1,column=2,sticky='nsew')
		#self.frameCamera.grid(row=1,column=1,sticky='news')
		self.boutonFrameCamera.grid(row=1,column=1,sticky='nsew') #dans le frame camera
		self.labelExpo.grid(row=2,column=0,pady=50,sticky='nsew')
		self.labelLed.grid(row=2,column=2,pady=50,sticky='nsew')
		self.progressbar.grid(row=3,column=0,sticky="ew")
		self.boutonFrameCamera.configure(state='disabled')

	def startPreview(self):
		#Lancement Camera
		self.labelProjet.configure(text=nomprojet)
		self.window.update()
		self.window.update_idletasks()
		self.camera = picamera.PiCamera()
		self.camera.resolution = (self.camerapreviewX,self.camerapreviewY)
		self.camera.exposure_compensation = 0
		self.camera.iso=100
		self.camera.rotation = 180
		self.camera.awb_mode= 'auto'
		self.camera.still_stats = 'true' #MODIFICATION190621
		time.sleep(0.5)
		self.camera._check_camera_open()
		self.camera.preview_fullscreen = False
		self.camera.preview_window = (self.cameraposX,self.cameraposY,self.camerapreviewX,self.camerapreviewY)
		self.camera.start_preview()
		self.boutonFrameCamera.configure(state='disabled')
		zero()
		AllumeLedPhotog()

	def fermerFenetreCapture(self):
		zero()
		self.camera.stop_preview()
		self.camera.close()
		self.window.destroy()

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

	def startCapture(self):
		global nbimgphotog
		global CAMERASPEED
		global EXPOSURECOMPENSATION
		self.progressbar['maximum'] = int(nbimgphotog)
		EXPOSURECOMPENSATION = self.sliderExpo.get()
		CAMERASPEED = self.camera.exposure_speed
		self.camera.shutter_speed= CAMERASPEED
		print("shutter_speed = "+ str(CAMERASPEED))
		print("exposure_compensation = "+ str(EXPOSURECOMPENSATION))
		self.camera.awb_mode = 'off'
		self.camera.awb_mode = 'off'
		AWB_GAINS = self.camera.awb_gains
		self.camera.stop_preview()
		self.camera.close()
		time.sleep(0.1)
		#self.window.destroy()
		self.sliderExpo.configure(state='disabled')
		#self.sliderLed.configure(state='disabled')
		self.boutonOk.configure(state='disabled')
		self.boutonRetour.configure(state='disabled')
		self.labelProjet.configure(state='disabled')

		#Camera
		self.camera = picamera.PiCamera()
		self.camera.resolution = (3280, 2464) #3280 × 2464 #1640, 1232
		self.camera.iso=100
		self.camera.rotation = 180
		self.camera.preview_fullscreen = False
		self.camera.still_stats = 'true' #MODIFICATION190621
		self.camera.preview_window = (self.cameraposX,self.cameraposY,self.camerapreviewX,self.camerapreviewY)
		time.sleep(0.2)
		self.camera._check_camera_open()
		zero2()
		AllumeLedPhotog()
		self.camera.start_preview()
		time.sleep(1)
		self.camera.exposure_mode = 'off'
		self.camera.shutter_speed= CAMERASPEED
		self.camera.exposure_compensation = EXPOSURECOMPENSATION
		self.camera.awb_mode = 'off'
		self.camera.awb_gains = AWB_GAINS
		##############
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		##############
		"""
		"""
		step=int(3200/nbimgphotog)
		print("On va prendre :"+str(nbimgphotog)+" images.")
		with Serial(port="/dev/ttyUSB0", baudrate=9600, timeout=1, writeTimeout=1) as port_serie:
			if port_serie.isOpen():
				time.sleep(5)
				for i in range(0,nbimgphotog):	
					data = port_serie.readline()[:-2] #the last bit gets rid of the new-line chars
					if data:
						print("Données reçues:"+str(data))
					#print("On envoie "+str(step)+" pas a l'Arduino")
					port_serie.write(str(step).encode())
					time.sleep(2)
					self.camera.capture(PATHTMP +'{0:02d}'.format(i)+".jpg",format='jpeg',quality=95,use_video_port=False)
					self.varprogress.set(int(i))
					self.window.update()
					self.window.update_idletasks()
				port_serie.write('1'.encode())
		self.camera.stop_preview()
		##############
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		#	 PDV PHOTOGRAMMETRY.   #
		##############
		zero()
		self.boutonOk.configure(command=self.Continuer,text="Continuer")
		self.txtboutonFrameCamera.set("Fin de la prise de vue")
		self.boutonOk.configure(state='active')
		self.boutonRetour.configure(state='active')
		self.camera.close()


	def Continuer(self):
		zero()
		self.movefiles()
		self.window.destroy()

	def updateNbPhoto(self,abc):
		global nbimgphotog
		nbimgphotog = int(self.sliderNbPhoto.get())
		#print (nbimgphotog)

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
		
class RevueProjet:
	
	def __init__(self,master):
		#management fenetre
		self.master = master
		self.window = tk.Toplevel(self.master)
		self.window.attributes("-fullscreen",True)
		self.window.configure(background=_from_rgb((41,40,46)))
		self.frame = Frame(self.window,background=_from_rgb((41,40,46))) 
		#images
		self.iconeretour = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeRetour.png").resize((75,75),Image.BILINEAR))
		self.imageOk = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeOk.png").resize((75,75),Image.BILINEAR))
		self.boutonRetour = Button(self.frame, text="Retour", image=self.iconeretour,foreground=_from_rgb((176,175,179)),relief="flat",width = 75, height = 75,background=_from_rgb((41,40,46)),compound=TOP, command=self.window.destroy)
		#self.boutonOk = Button(self.window,text = "Ok",image=self.imageOk,cursor="tcross",command=self.visionage3D)
		#preview
		self.previewPhoto = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"fondProjet.png"))
		self.label = Label(self.frame,text="Preview",image=self.previewPhoto)
		#scrollbar
		self.scrollbar = Scrollbar(self.frame)
		#listbox
		liste = os.listdir(PATHPROJET)
		liste.sort()
		#print (liste)
		NomProjet = StringVar(value = liste)
		self.listeProjet = Listbox(self.frame,yscrollcommand = self.scrollbar.set,font=('TkDefaultFont',15,'bold'))
		for projet in liste:
			self.listeProjet.insert(END,projet)	
		self.listeProjet.bind("<<ListboxSelect>>", self.selection)

		#affiche le tout
		self.afficher()
		
	def selection(self,event):
		projetSelectionner = self.listeProjet.get(self.listeProjet.curselection())
		print("Projet : "+projetSelectionner)
		previewPilPhoto = Image.open(PATHPROJET+projetSelectionner+"/miniature.jpg")
		self.previewPhoto = ImageTk.PhotoImage(previewPilPhoto)
		self.label.configure(image = self.previewPhoto)
		self.label.image = self.previewPhoto
		#self.master.update()
	
	def afficher(self):
		Grid.rowconfigure(self.window, 0, weight=1)
		Grid.columnconfigure(self.window, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=4)
		Grid.rowconfigure(self.frame, 1, weight=40)
		Grid.columnconfigure(self.frame, 1, weight=1)
		Grid.rowconfigure(self.frame, 2, weight=10)
		Grid.columnconfigure(self.frame, 2, weight=10)				
		self.scrollbar.grid(row=1,column=1,sticky='nesw')
		self.listeProjet.grid(row=1,column=0,sticky='nesw')
		self.frame.grid(row=0,column=0,sticky='nesw')
		self.label.grid(row=1,column=2,sticky='nesw')
		self.boutonRetour.grid(row=0,column=0,sticky='nesw')
		#self.boutonOk.grid(row=3,column=4)

	def visionage3D(self):
		projetSelectionner = self.listeProjet.get(self.listeProjet.curselection())
		#os.system("meshlab "+PATHPROJET+projetSelectionner+"/C3DC_QuickMac.ply")
		print("Vous avez séléctionné ce projet!")