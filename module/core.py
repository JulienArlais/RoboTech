import tkinter as tk
from .affichage_2D import GUI
from threading import Thread
from .element_simulation import Objet, Robot, Environnement, CollisionException, Simulation, run
from .controleur import *
import module.constante as cs


def run_projet(robot,proxy_v,environnement,s):

	gui = GUI(environnement, robot)



	#StrategieCarrée
	stavance = StrategieAvance(cs.stav_dist, cs.stav_vit, proxy_v)
	stangle = StrategieAngle(cs.stan_an, cs.stan_dps_neg, proxy_v) 
	listeCarre = [stavance, stangle, stavance, stangle, stavance, stangle, stavance] 
	stseq = StrategieSeq(listeCarre)


	

	#Pour StrategieTriangleEquilatéral
	
	treq=StrategieTriangleEq(proxy_v,100)

	#Pour strategie tracer hexegone

	tracerhex=StrategieHexagone(100,45,proxy_v)

	#Pouur strategie 0
	tracer0=Strategie0(100,proxy_v)

	#pour strategie 0
	tracer1=Strategie1(proxy_v,100)


	#Pouur tracer des 1 et des 0 à la suite

	liste_binaire=[tracer1,tracer0]

	loopseq=StrategieLoopSeq(liste_binaire,proxy_v)

	liste=[1,0,1,0]

	bina=StrategieBinaire(liste,proxy_v,100)


	threadrun = Thread(target=run, args=(s, gui, tracerhex)) # remplacer gui par None si on veut pas d'interface graphique
	threadrun.start()
	gui.window.mainloop() # retirer cette ligne si on veut pas d'interface graphique
