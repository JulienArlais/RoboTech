import tkinter as tk
from module.affichage_2D import GUI
from threading import Thread
from module.element_simulation import Objet, Robot, Environnement, CollisionException, Simulation, run
from module.controleur import StrategieAvance, StrategieAngle, StrategieArretMur, StrategieSeq, StrategieSuivreBalise
import module.constante as cs

if __name__ == "__main__":

	# Création d'un environnement et d'un robot
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(cs.rob_x, cs.rob_y, cs.rob_thet, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue) # robot immobile, pour montrer ce que fait le controleur
	environnement.generer_obstacles(robot, cs.nb_objet)

	# Création d'une simulation, d'une interface graphique
	s = Simulation(environnement, robot)
	gui = GUI(environnement, robot)

	# Stratégies
	stavance = StrategieAvance(cs.stav_dist, cs.stav_vit, robot)
	stangle = StrategieAngle(cs.stan_an, cs.stan_dps, robot) 
	listeCarre = [stavance, stangle, stavance, stangle, stavance, stangle, stavance] # +1 stangle ?
	stseq = StrategieSeq(listeCarre)
	stsb = StrategieSuivreBalise(cs.data, robot)
	stArretMur = StrategieArretMur(robot, environnement, cs.stmur_vit)

	threadrun = Thread(target=run, args=(s, gui, stseq)) # remplacer gui par None si on veut pas d'interface graphique
	threadrun.start()
	gui.window.mainloop() # retirer cette ligne si on veut pas d'interface graphique
