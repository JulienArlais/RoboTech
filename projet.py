import tkinter as tk
from module.affichage_2D import GUI
from threading import Thread
from module.element_simulation import Objet, Robot, Environnement, CollisionException, Simulation, run
from module.controleur import StrategieAvance, StrategieAngle, StrategieArretMur, StrategieSeq, StrategieSuivreBalise
import module.constante as cs
from module.proxy import Robot_Virtuel, Robot_Reel

if __name__ == "__main__":

	# Création d'un environnement et d'un robot
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(cs.rob_x, cs.rob_y, cs.rob_thet, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue) # robot immobile, pour montrer ce que fait le controleur
	environnement.generer_obstacles(robot, cs.nb_objet)
	proxy_v = Robot_Virtuel(robot,environnement)

	# Création d'une simulation, d'une interface graphique
	s = Simulation(environnement, robot)
	gui = GUI(environnement, robot)

	# Stratégies
	stavance = StrategieAvance(cs.stav_dist, cs.stav_vit, proxy_v)
	stangle = StrategieAngle(cs.stan_an, cs.stan_dps, proxy_v) 
	listeCarre = [stavance, stangle, stavance, stangle, stavance, stangle, stavance] # +1 stangle ?
	stseq = StrategieSeq(listeCarre)
	stsb = StrategieSuivreBalise(cs.data, proxy_v)
	stArretMur = StrategieArretMur(proxy_v, environnement, cs.stmur_vit)

	threadrun = Thread(target=run, args=(s, gui, stseq)) # remplacer gui par None si on veut pas d'interface graphique
	threadrun.start()
	gui.window.mainloop() # retirer cette ligne si on veut pas d'interface graphique
