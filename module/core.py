import tkinter as tk
from .affichage_2D import GUI
from threading import Thread
from .element_simulation import Objet, Robot, Environnement, CollisionException, Simulation, run
from .controleur import StrategieAvance, StrategieAngle, StrategieArretMur, StrategieSeq, StrategieSuivreBalise
import module.constante as cs


def run_projet(robot,proxy_v,environnement,s):
	environnement.generer_obstacles(robot, cs.nb_objet)
	gui = GUI(environnement, robot)

	# Stratégies
	stavance = StrategieAvance(cs.stav_dist, cs.stav_vit, proxy_v)
	stangle = StrategieAngle(cs.stan_an, cs.stan_dps, proxy_v) 
	listeCarre = [stavance, stangle, stavance, stangle, stavance, stangle, stavance]
	stseq = StrategieSeq(listeCarre)
	stsb = StrategieSuivreBalise(cs.data, proxy_v)
	stArretMur = StrategieArretMur(proxy_v, environnement, cs.stmur_vit)

	threadrun = Thread(target=run, args=(s, gui, stseq))
	threadrun.start()
	gui.window.mainloop()
