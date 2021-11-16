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
import paths as p
import Settings
import FenetreCapture
import Data


#Pin connected to ST_CP of 74HC595
latchPin = 31
#Pin connected to SH_CP of 74HC595
clockPin = 29
#Pin connected to DS of 74HC595
dataPin = 33
nbbras = 8
tabled=[2**i for i in range(8)]
ledposition=[i for i in range(65)]

global nomprojet
global nbimg
global nbimgphotog

CAMERASPEED = None
EXPOSURECOMPENSATION = None
nomprojet = None
defaultprojet = str("Projet")
nbimg = 64
nbimgphotog = 50

PATHTEST = p.PATHTEST
PATHPROJET =  p.PATHPROJET
PATHTMP = p.PATHTMP
PATHRESSOURCES = p.PATHRESSOURCES
PATHPHOTOG = p.PATHPHOTOG
icons_path = p.icons_path

DIGITS_FONT_STYLE = ("Arial", 24, "bold")
back_ground_color = 175, 222, 255


def _from_rgb(rgb):
	return "#%02x%02x%02x" % rgb 

## Main Window 
class MainWindow:
	def __init__(self):
		self.fenetre = Tk()
# 		self.fenetre.geometry("+400+80")
		self.fenetre.attributes('-fullscreen', True)
		self.w = self.fenetre.winfo_screenwidth()
		self.fenetre.title("Dome")
		self.fenetre.configure(background=_from_rgb(back_ground_color))
		
		self.prop = self.w / 1024 
		#icons
		self.photoCamera = ImageTk.PhotoImage(Image.open(icons_path+"cam_projet.png").resize((int(168*self.prop), int(138*self.prop)),Image.BILINEAR)) 
		self.photoTurntable = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeTurntable.png").resize((int(self.prop*75),int(self.prop*75)),Image.BILINEAR)) 
		self.photoRepertoire = ImageTk.PhotoImage(Image.open(icons_path+"prev_projets.png").resize((int(180*self.prop), int(138*self.prop)),Image.BILINEAR))
		self.photoFermer = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeAnnuler.png").resize((int(self.prop*75),int(self.prop*75)),Image.BILINEAR))
		self.photoSettings = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeSettings.png").resize((int(self.prop*75),int(self.prop*75)),Image.BILINEAR))
		self.photoEteindre = ImageTk.PhotoImage(Image.open(PATHRESSOURCES+"IconeEteindre.png").resize((int(self.prop*75),int(self.prop*75)),Image.BILINEAR))

		#Frame
		self.frame = Frame(self.fenetre, background=_from_rgb(back_ground_color))
		self.frameReg = Frame(self.fenetre, background=_from_rgb(back_ground_color))
		self.frameRet = Frame(self.fenetre, background=_from_rgb(back_ground_color))
		self.frameEte = Frame(self.fenetre, background=_from_rgb(back_ground_color))
		
		#Boutons
		self.boutonCapture = Button(self.frame, text="Nouveau projet",foreground=_from_rgb((176,175,179)),relief="flat",
                                    background=_from_rgb(back_ground_color),image=self.photoCamera,compound=TOP,cursor="tcross",command=self.ouvrirCapture)
		
		self.boutonCapturePhoto = Button(self.frame, text="Turntable",foreground=_from_rgb((176,175,179)),relief="flat",
                                         background=_from_rgb(back_ground_color),image=self.photoTurntable,compound=TOP,cursor="tcross",command=self.ouvrirCapturePhoto)
		
		self.boutonRepertoire = Button(self.frame, text="Projets passés",foreground=_from_rgb((176,175,179)),bd=0,relief="flat",
                                       image=self.photoRepertoire,compound=TOP,background=_from_rgb(back_ground_color),command=self.ouvrirRepertoire)
		
		self.boutonFermer = Button(self.frameRet, text="Fermer",relief="flat",foreground=_from_rgb((176,175,179)),
                                   image=self.photoFermer,compound=TOP,background=_from_rgb(back_ground_color),command=self.bureau)
		
		self.boutonSettings = Button(self.frameReg, text="Réglages",image=self.photoSettings,foreground=_from_rgb((176,175,179)),relief="flat",
                                     compound=TOP,background=_from_rgb(back_ground_color),command=self.settings)
		
		self.boutonEteindre = Button(self.frameEte, text="Eteindre",image=self.photoEteindre,foreground=_from_rgb((176,175,179)),compound=TOP,
                                     highlightcolor=_from_rgb((176,175,179)),relief="flat",background=_from_rgb(back_ground_color),command=self.eteindre)

	def afficher(self):
		 ## Display Main Window
		self.fenetre.grid_rowconfigure(0, weight=1)
		self.fenetre.grid_columnconfigure(0, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 0, weight=1)
		self.boutonCapture.grid(row=1, column=1, padx=50)
		self.boutonRepertoire.grid(row=1, column=2, padx=50) 
		self.boutonFermer.grid(row=0, column=3, sticky='ne')
		self.boutonSettings.grid(row=0, column=0, padx=0, sticky='news')
		self.boutonEteindre.grid(row=3, column=3, sticky='news')
		self.frameReg.grid(row=0, column=0, sticky='nw')
		self.frameRet.grid(row=0, column=0, sticky='ne')
		self.frameEte.grid(row=0, column=0, sticky='se')
		self.frame.grid(row=0,column=0)
		# self.frame.pack(fill=X, expand=YES)
		
		

	def ouvrirCapture(self):
		fenetreCapture = FenetreCapture.FenetreCapture(self.fenetre)
		print("on ouvre la fenetre de capture")
		
	def ouvrirRepertoire(self): #ouvre un repertoire
		print("on ouvre le repertoire")
		fenetreprojet = Data.RevueProjet(self.fenetre)


	def ouvrirCapturePhoto(self):
		fenetreCapturePhoto = Data.FenetreCapturePhoto(self.fenetre)
		print("on ouvre la fenetre de capture")

	def mainloop(self):
		self.fenetre.mainloop()

	def bureau(self):
	#os.system('xdotool key ctrl+super+d')
		self.fenetre.destroy()
		
	def settings(self):
		fenetreReglages = Settings.settings(self.fenetre)

	def eteindre(self):
		os.system('sudo shutdown -h 0')
		print("on ferme ! ")
		
		
if __name__ == '__main__':
	FenetreCapture.configGPIO()
	FenetreCapture.zero()
	os.system("rm "+PATHTMP + "*")
	fenetre = MainWindow()
	fenetre.afficher()
	fenetre.mainloop()