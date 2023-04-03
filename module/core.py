import tkinter as tk
from .affichage_2D import GUI
from threading import Thread
from .element_simulation import Objet, Robot, Environnement, CollisionException, Simulation, run
from .controleur import StrategieAvance, StrategieAngle, StrategieArretMur, StrategieSeq, StrategieSuivreBalise, StrategieDessin
import module.constante as cs


def run_projet(robot,proxy_v,environnement,s):
	environnement.generer_obstacles_coins()
	gui = GUI(environnement, robot)

	# Stratégies
	stavance = StrategieAvance(cs.stav_dist, cs.stav_vit, proxy_v)
	stangle = StrategieAngle(cs.stan_an, cs.stan_dps, proxy_v) 
	listeCarre = [stavance, stangle, stavance, stangle, stavance, stangle, stavance]
	stseq = StrategieSeq(listeCarre)
	stsb = StrategieSuivreBalise(cs.data, proxy_v)
	stArretMur = StrategieArretMur(proxy_v, environnement, cs.stmur_vit)
	
	stavancehex = StrategieAvance(50, cs.stav_vit, proxy_v)
	stanglehex = StrategieAngle(-60, cs.stan_dps, proxy_v)
	stdessin = StrategieDessin(gui)
	listeHex = [stavancehex, stanglehex, stdessin, stavancehex, stanglehex, stdessin, stavancehex, stanglehex, stdessin, stavancehex, stanglehex, stdessin, stavancehex, stanglehex, stdessin, stavancehex, stanglehex, stdessin]
	stseqhex = StrategieSeq(listeHex)

	threadrun = Thread(target=run, args=(s, gui, stseqhex))
	threadrun.start()
	gui.window.mainloop()
