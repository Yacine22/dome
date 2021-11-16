import os
import io
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

#Pin connected to ST_CP of 74HC595
latchPin = 31
#Pin connected to SH_CP of 74HC595
clockPin = 29
#Pin connected to DS of 74HC595
dataPin = 33
nbbras=8
tabled=[2**i for i in range(8)]
ledposition=[i for i in range(65)]

CAMERASPEED = None
EXPOSURECOMPENSATION = None
nomprojet = None
defaultprojet = None
defaultprojet = str("Projet")
nbimg = 64
nbimgphotog = 50

PATHTEST = os.getcwd()+"/"
PATHPROJET =  PATHTEST+"Projet/"
PATHTMP = PATHTEST+"tmp/"
PATHRESSOURCES = PATHTEST+"Ressources/"
PATHPHOTOG = PATHTEST+"ProjetPhoto"
icons_path = './icons/'

back_ground_color = 175, 222, 255
global resolution_
#################
#   Fenetres	#
#################
class FenetrePrincipale:

	def __init__(self):
		#fenetre
		self.fenetre = tk.Tk()
		self.fenetre.geometry("+400+80")
		self.fenetre.title("Dome")
		# self.fenetre.attributes("-fullscreen",True)
		self.fenetre.configure(background=_from_rgb(back_ground_color))
		global nomprojet

		#icons
		self.photoCamera = ImageTk.PhotoImage(Image.open(icons_path+"cam_projet.png").resize((186,154),Image.BILINEAR)) #945 × 780
		self.photoTurntable = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeTurntable.png").resize((75,75),Image.BILINEAR)) #945 × 780
		self.photoRepertoire = ImageTk.PhotoImage(Image.open(icons_path+"prev_projets.png").resize((200,154),Image.BILINEAR))
		self.photoFermer = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeAnnuler.png").resize((75,75),Image.BILINEAR))
		self.photoSettings = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeSettings.png").resize((75,75),Image.BILINEAR))
		self.photoEteindre = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeEteindre.png").resize((75,75),Image.BILINEAR))

		#Frame
		self.frame = Frame(self.fenetre,background=_from_rgb(back_ground_color))
		#Boutons
		self.boutonCapture = Button(self.frame, text="Nouveau projet",foreground=_from_rgb((176,175,179)),relief="flat",
                                    background=_from_rgb(back_ground_color),image=self.photoCamera,compound=TOP,cursor="tcross",command=self.ouvrirCapture)
		
		# self.boutonCapturePhoto = Button(self.frame, text="Turntable",foreground=_from_rgb((176,175,179)),relief="flat",
                                         # background=_from_rgb(back_ground_color),image=self.photoTurntable,compound=TOP,cursor="tcross",command=self.ouvrirCapturePhoto)
		
# 		self.boutonRepertoire = Button(self.frame, text="Projets passés",foreground=_from_rgb((176,175,179)),bd=0,relief="flat",
#                                        image=self.photoRepertoire,compound=TOP,background=_from_rgb(back_ground_color),command=self.ouvrirRepertoire)
		
		self.boutonFermer = Button(self.frame, text="Fermer",relief="flat",foreground=_from_rgb((176,175,179)),
                                   image=self.photoFermer,compound=TOP,background=_from_rgb(back_ground_color),command=self.bureau)
		
		self.boutonSettings = Button(self.frame,text="Réglages",image=self.photoSettings,foreground=_from_rgb((176,175,179)),relief="flat",
                                     compound=TOP,background=_from_rgb(back_ground_color),command=self.settings)
		
		self.boutonEteindre = Button(self.frame,text="Eteindre",image=self.photoEteindre,foreground=_from_rgb((176,175,179)),compound=TOP,
                                     highlightcolor=_from_rgb((176,175,179)),relief="flat",background=_from_rgb(back_ground_color),command=self.eteindre)
		#label
		#self.labelMap = Label(self.fenetre,image=self.photoMAP)

	def afficher(self):
		Grid.rowconfigure(self.fenetre, 0, weight=1)
		Grid.columnconfigure(self.fenetre, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.boutonCapture.grid(row=2,column=2,sticky='news')
		# self.boutonCapturePhoto.grid(row=2,column=1,sticky='news')
		# self.boutonRepertoire.grid(row=2,column=3,sticky='news') #columnspan=2,
		self.boutonFermer.grid(row=1,column=5,sticky='news')
		self.boutonSettings.grid(row=1,column=1,padx =0,pady=0,sticky='news')
		self.boutonEteindre.grid(row=3,column=5,padx=0,pady=0,sticky='news')
		self.frame.grid(row=0,column=0)
		#self.frame.pack(fill=X, expand=YES)
		#self.labelMap.grid(row=2,column=1,padx=5,pady=5)

	def ouvrirCapture(self):
		fenetreCapture = FenetreCapture(self.fenetre)
		print("on ouvre la fenetre de capture0")
		
# 	def ouvrirRepertoire(self): #ouvre un repertoire
# 		print("on ouvre le repertoire")
# 		fenetreprojet = RevueProjet(self.fenetre)
# 		#fenetreProjet = FenetreProjet(self.fenetre)
# 		#fenetreProjet.attributes("-fullscreen",True)

# 	def ouvrirCapturePhoto(self):
# 		fenetreCapturePhoto = FenetreCapturePhoto(self.fenetre)
# 		print("on ouvre la fenetre de capture")

	def mainloop(self):
		self.fenetre.mainloop()

	def bureau(self):
	#os.system('xdotool key ctrl+super+d')
		self.fenetre.destroy()
		
	def settings(self):
		fenetreReglages = settings(self.fenetre)

	def eteindre(self):
		#os.system('sudo shutdown -h 0')
		print("on ouvre le repertoire")
		
		
		
		
class settings:
    
	def __init__(self, master):
        
		self.master = master
		self.window = tk.Toplevel(self.master)
		self.window.geometry('+400+80')
		self.window.title('Dome')
		self.window.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.window, background=_from_rgb(back_ground_color)) 
		
		#icons
		self.photoResolution = ImageTk.PhotoImage(Image.open(icons_path+"resolutions.png").resize((120,100),Image.BILINEAR)) 
		self.photoTile= ImageTk.PhotoImage(Image.open(icons_path+"dome_leds.png").resize((120,100),Image.BILINEAR)) 
		self.photoCamTest = ImageTk.PhotoImage(Image.open(icons_path+"camera_test.png").resize((120,100),Image.BILINEAR))
		self.photoDomeTest = ImageTk.PhotoImage(Image.open(icons_path+"dome_test.png").resize((120,100),Image.BILINEAR))
		self.photoSettings = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeSettings.png").resize((75,75),Image.BILINEAR))
		self.photoRetour = ImageTk.PhotoImage(Image.open(icons_path+"back.png").resize((75,75),Image.BILINEAR))
		
		
		#Boutons
		self.boutonResolution = Button(self.frame, text="Résolution des images",foreground=_from_rgb((176,175,179)),relief="flat",
                                    background=_from_rgb(back_ground_color),image=self.photoResolution,compound=TOP,cursor="tcross",command=self.resolutionSet)
		
		self.boutonTile = Button(self.frame, text="Nombre de LEDs à Allumer",foreground=_from_rgb((176,175,179)),relief="flat",
                                         background=_from_rgb(back_ground_color),image=self.photoTile,compound=TOP,cursor="tcross",command=self.tileSet)
		
		self.boutonCamTest = Button(self.frame, text="Tester la caméra",foreground=_from_rgb((176,175,179)),bd=0,relief="flat",
                                       image=self.photoCamTest,compound=TOP,background=_from_rgb(back_ground_color),command=self.CamTest)
		
		self.boutonDomeTest = Button(self.frame, text="Tester le Dome",relief="flat",foreground=_from_rgb((176,175,179)),
                                   image=self.photoDomeTest,compound=TOP,background=_from_rgb(back_ground_color),command=self.DomeTest)
		
		self.boutonSettings = Button(self.frame,text="",image=self.photoSettings,foreground=_from_rgb((176,175,179)),relief="flat",
                                     compound=TOP,background=_from_rgb(back_ground_color),command=self.bureau)
		
		self.boutonFermer = Button(self.frame,text="",image=self.photoRetour,foreground=_from_rgb((176,175,179)),compound=TOP,
                                     highlightcolor=_from_rgb((176,175,179)),relief="flat",background=_from_rgb(back_ground_color),command=self.bureau)
		
		
		self.afficher()

	def afficher(self):
		Grid.rowconfigure(self.window, 0, weight=1)
		Grid.columnconfigure(self.window, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.boutonTile.grid(row=2,column=2,sticky='news')
		# self.boutonCapturePhoto.grid(row=2,column=1,sticky='news')
		self.boutonResolution.grid(row=2,column=3,sticky='news') #columnspan=2,
		self.boutonCamTest.grid(row=3,column=2, sticky='news')
		self.boutonDomeTest.grid(row=3,column=3, sticky='news')
		self.boutonFermer.grid(row=1,column=5,padx=0,pady=0,sticky='news')
		self.frame.grid(row=0,column=0)
		
	def resolutionSet(self):
		
		self.win= tk.Toplevel()
		self.win.geometry('+400+80')
		self.win.title('Dome')
		self.win.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.win, background=_from_rgb(back_ground_color))
		
		
		self.listbox = Listbox(self.frame, background=_from_rgb(back_ground_color), width=40, height=10, selectmode=SINGLE)
		
		
		self.listbox.insert(1, "1")
		self.listbox.insert(2, "2")
		self.listbox.insert(3, "3")
		
		for i in self.listbox.curselection():
			resolution_ = self.listbox.get(i)
			print(resolution_)
			
		self.btn_valid = Button(self.frame, text="valider", command=listBox)
		
		
		"""   
		options = [
            'fullscreen',
            '1024, 900',
            '720, 600',
            '480, 360'
            ]
		
		clicked = StringVar()
		clicked.set(options[0])
		
		self.drop = OptionMenu(self.frame, clicked, *options)
		resolution_ = clicked   ###
		print(clicked) 
		
		self.btnretour = Button(self.frame, text="Retour", command=self.win.destroy)
		"""
        
		Grid.rowconfigure(self.win, 0, weight=1)
		Grid.columnconfigure(self.win, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.btn_valid.grid(row=4,column=5,sticky='news')
		self.listbox.grid(sticky='news')
		self.frame.grid(row=0,column=0)
		
		
	
		
	def tileSet(self):
		
		self.win = Tk()
		self.win.geometry('+400+80')        
		self.win.title('Dome')
		self.win.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.win, background=_from_rgb(back_ground_color))
		
	def CamTest(self):
		
		self.win = Tk()
		self.win.geometry('+400+80')
		self.win.title('Dome')
		self.win.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.win, background=_from_rgb(back_ground_color))
		
		### Add Buttons
		self.btn1 = Button(self.frame, text= "CAM ON", command=self.take_photo)
		self.btn2 = Button(self.frame, text= "CAM TEST", command=self.allumer_cam)
		self.btnRetour = Button(self.frame, text="Retour", command=self.win.destroy)
		Grid.rowconfigure(self.win, 0, weight=1)
		Grid.columnconfigure(self.win, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.btn1.grid(row=2,column=2,sticky='news')
		self.btn2.grid(row=2,column=3,sticky='news')
		self.btnRetour.grid(row=3,column=3, sticky='news')
		self.frame.grid(row=0,column=0)
		
		
	def DomeTest(self):
		
		self.win = Tk()
		self.win.geometry('+400+80')
		self.win.title('Dome')
		self.win.configure(background=_from_rgb(back_ground_color))
		self.frame = Frame(self.win, background=_from_rgb(back_ground_color))
		
		### Add Buttons
		self.btn1 = Button(self.frame, text= "ALL ON", command=self.allumer)
		self.btn2 = Button(self.frame, text= "ALL OFF", command=self.Eteindre)
		self.btn3 = Button(self.frame, text= "ONE LED", command=self.OneLed)
		self.btn4 = Button(self.frame, text= "CHENILL", command=self.chenillard)
		self.btnRetour = Button(self.frame, text="Retour", command=self.win.destroy)
		
		
		Grid.rowconfigure(self.win, 0, weight=1)
		Grid.columnconfigure(self.win, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.btn1.grid(row=2,column=2,sticky='news')
		# self.boutonCapturePhoto.grid(row=2,column=1,sticky='news')
		self.btn2.grid(row=2,column=3,sticky='news') #columnspan=2,
		self.btn3.grid(row=3,column=2, sticky='news')
		self.btn4.grid(row=3,column=3, sticky='news')
		self.btnRetour.grid(row=4,column=3, sticky='news')

		self.frame.grid(row=0,column=0)
		
		
		
	
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
		if os.path.exists("image.jpg"):
			os.remove("image.jpg")
    
	def allumer_cam(self):
		pass
	
        
def listBox():	
	for i in listbox.curselection():
		resolution_ = listbox.get(i)
		print(resolution_)
	
		
		
		
		
		
		
        

        
        

class FenetreCapture:

	def __init__(self, master):
		#Parametres globaux
		global nomprojet
		global CAMERASPEED
		global nbimg
		
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
		self.window.configure(background=_from_rgb(back_ground_color))
		
		#icons
		self.photoResolution = ImageTk.PhotoImage(Image.open(icons_path+"resolutions.png").resize((120,100),Image.BILINEAR)) 
		self.photoTile= ImageTk.PhotoImage(Image.open(icons_path+"dome_leds.png").resize((120,100),Image.BILINEAR)) 
		self.photoCamTest = ImageTk.PhotoImage(Image.open(icons_path+"camera_test.png").resize((120,100),Image.BILINEAR))
		self.photoDomeTest = ImageTk.PhotoImage(Image.open(icons_path+"dome_test.png").resize((120,100),Image.BILINEAR))
		self.photoSettings = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeSettings.png").resize((75,75),Image.BILINEAR))
		self.photoEteindre = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeEteindre.png").resize((75,75),Image.BILINEAR))
		
		
		#Frame
		self.frame = Frame(self.window,background=_from_rgb(back_ground_color))
		#Boutons
		self.boutonResolution = Button(self.frame, text="Résolution des images",foreground=_from_rgb((176,175,179)),relief="flat",
                                    background=_from_rgb(back_ground_color),image=self.photoResolution,compound=TOP,cursor="tcross",command=self.ouvrirCapture)
		
		self.boutonTile = Button(self.frame, text="Nombre de LEDs à Allumer",foreground=_from_rgb((176,175,179)),relief="flat",
                                         background=_from_rgb(back_ground_color),image=self.photoTile,compound=TOP,cursor="tcross",command=self.ouvrirCapturePhoto)
		
		self.boutonCamTest = Button(self.frame, text="Tester la caméra",foreground=_from_rgb((176,175,179)),bd=0,relief="flat",
                                       image=self.photoCamTest,compound=TOP,background=_from_rgb(back_ground_color),command=self.ouvrirRepertoire)
		
		self.boutonDomeTest = Button(self.frame, text="Tester le Dome",relief="flat",foreground=_from_rgb((176,175,179)),
                                   image=self.photoDomeTest,compound=TOP,background=_from_rgb(back_ground_color),command=self.bureau)
		
		self.boutonSettings = Button(self.frame,text="",image=self.photoSettings,foreground=_from_rgb((176,175,179)),relief="flat",
                                     compound=TOP,background=_from_rgb(back_ground_color),command=self.settings)
		
		self.boutonFermer = Button(self.frame,text="",image=self.photoEteindre,foreground=_from_rgb((176,175,179)),compound=TOP,
                                     highlightcolor=_from_rgb((176,175,179)),relief="flat",background=_from_rgb(back_ground_color),command=self.bureau)
		#label
		#self.labelMap = Label(self.fenetre,image=self.photoMAP)
	
	def afficher(self):
		Grid.rowconfigure(self.window, 0, weight=1)
		Grid.columnconfigure(self.window, 0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.boutonTile.grid(row=2,column=2,sticky='news')
		# self.boutonCapturePhoto.grid(row=2,column=1,sticky='news')
		self.boutonResolution.grid(row=2,column=3,sticky='news') #columnspan=2,
		self.boutonCamTest.grid(row=3,column=2, sticky='news')
		self.boutonFermer.grid(row=3,column=3, sticky='news')
		self.boutonFermer.grid(row=1,column=5,padx=0,pady=0,sticky='news')
		self.frame.grid(row=0,column=0)
		
		"""
		Grid.rowconfigure(self.window, 0, weight=1)
		Grid.columnconfigure(self.window, 0, weight=1)
		#Images
		self.iconeretour = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeRetour.png").resize((75,75),Image.BILINEAR))
		self.imageOk = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeOk.png").resize((75,75),Image.BILINEAR))
		#Frame
		self.frame = Frame(self.window,background=_from_rgb((200, 200, 200))) #,height=50,width=10
		#Label 
		self.labelExpo = Label(self.frame, text="Exposition",foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((200, 200, 200)), compound=TOP)
		self.labelLed = Label(self.frame, text="LED",foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((200, 200, 200)), compound=TOP)
		
		#Boutons
		self.labelProjet = Button(self.frame, text=nomprojet,foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((200, 200, 200)), command=self.OuvreTextEntry)
		self.boutonOk = Button(self.frame, text="Capture", image=self.imageOk,foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((41,40,46)), compound=TOP, command=self.startCapture)
		self.boutonRetour = Button(self.frame, text="Retour", image=self.iconeretour,foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((41,40,46)),compound=TOP, command=self.fermerFenetreCapture)
		self.boutonFrameCamera = Button(self.frame,textvariable=self.txtboutonFrameCamera, foreground=_from_rgb((176,175,179)),relief="flat",background=_from_rgb((41,40,46)),command=self.startPreview) 
		#Slides
		self.sliderExpo = Scale(self.frame, orient='vertical', from_=-25, to=25, resolution=1, tickinterval=5,relief = "flat",foreground=_from_rgb((176,175,179)),background=_from_rgb((41,40,46)), command=self.updateExposure)
		self.sliderLed = Scale(self.frame, orient='vertical', from_=0, to=64, resolution=1,relief = "flat",foreground=_from_rgb((176,175,179)),background=_from_rgb((41,40,46)),command=self.updateLed)
		self.progressbar = ttk.Progressbar(self.window,maximum=nbimgphotog,variable=self.varprogress,orient ="horizontal",mode ="determinate")
		#Camera
		#On récupère la taille de la fenêtre
		self.camerapreviewX = 400
		self.camerapreviewY = int(self.camerapreviewX * 3 / 4)
		self.cameraposX= int((self.window.winfo_screenwidth() / 2) - (self.camerapreviewX / 2))
		self.cameraposY= int((self.window.winfo_screenheight() / 2) - (self.camerapreviewY / 2))
		#print("cameraposX = "+ str(self.cameraposX))
		#On crée une frame pour décaler les boutons autour
		#self.frameCamera = Frame(self.frame,background=_from_rgb((100,100,100)),width=self.camerapreviewX+20, height=self.camerapreviewY+50)
		self.afficher()
		self.startPreview()
		"""

	def afficher(self):
		Grid.rowconfigure(self.window, 0, weight=1)
		Grid.columnconfigure(self.window, 0, weight=1)
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
	
#################
#	 Main	  #
#################
	
def main():
	# configGPIO()
	# zero()
	global nomprojet
	global defaultprojet
	os.system("rm "+PATHTMP+"*")
	#num = ConfigNumProjet(PATHPROJET)
	fenetrePrincipale = FenetrePrincipale()
	fenetrePrincipale.afficher()
	fenetrePrincipale.mainloop()


#demarre le programme
main()