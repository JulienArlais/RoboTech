import tkinter as tk
from module.affichage_2D import GUI
from threading import Thread
from module.element_simulation import Objet, Robot, Environnement, CollisionException, Simulation, run
from module.controleur import StrategieAvance, StrategieAngle, StrategieArretMur, StrategieSeq

if __name__ == "__main__":

	# Création d'un environnement et d'un robot
	environnement = Environnement(800, 800, 0.1)
	robot = Robot(400, 400, 0, 15, 25, 4) # robot immobile, pour montrer ce que fait le controleur

	# Création d'une simulation, d'une interface graphique
	liste_objets = environnement.generer_obstacles(robot, 0)
	s = Simulation(environnement, robot, liste_objets)
	gui = GUI(environnement, robot, liste_objets)

	# Stratégies
	stavance = StrategieAvance(100, 45, robot)
	stangle = StrategieAngle(90, 45, robot) # aucune idée de pourquoi 100, ça fonctionne c'est tout
	listeCarre = [stavance, stangle, stavance, stangle, stavance, stangle, stavance] # +1 stangle ?
	stseq = StrategieSeq(listeCarre)
	
	stArretMur = StrategieArretMur(robot, environnement, liste_objets, 720)

	threadrun = Thread(target=run, args=(s, gui, stseq)) # remplacer gui par None si on veut pas d'interface graphique

	threadrun.start()
	gui.window.mainloop() # retirer cette ligne si on veut pas d'interface graphique
