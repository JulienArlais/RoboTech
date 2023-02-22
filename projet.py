import numpy as np
import tkinter as tk
import time
from module.affichage_2D import GUI
from threading import Thread
from module.element_simulation import Objet, Robot, Environnement, CollisionException
from module.controleur import FakeIA, StrategieAngle, StrategieAvance, StrategieCarre, dt

def run(simulation, gui, ia):
	"""exécution de la simulation

	Args:
		simulation (Simulation): simulation à exécuter
		gui (GUI): interface graphique à afficher
	"""
	while True:
		try:
			if ia.stop():
				return
			ia.update()
			simulation.update()
			if gui is not None:
				gui.update()
			time.sleep(dt)
		except CollisionException as e:
			break


class Simulation:
	def __init__(self, env, robot, objets):
		"""constructeur de la simulation

		Args:
			env (Environnement): environnemment de la simulation
			robot (Robot): robot de la simulation
			objets (List[Objet]): liste des objets
		"""
		self.environnement = env
		self.robot = robot
		self.objets = objets

	def update(self):
		"""mise à jour de la simulation

		Raises:
			CollisionException: collision
		"""
		self.environnement.avancer_robot(self.robot, dt)
		if (self.robot.x+self.robot.rayon > self.environnement.width) or (self.robot.x-self.robot.rayon < 0) or (self.robot.y+self.robot.rayon > self.environnement.height) or (self.robot.y-self.robot.rayon < 0):
			print("Collision avec les limites de l'environnement")
			raise CollisionException("Collision avec les limites de l'environnement")		
		for objet in self.objets:
			if self.environnement.collision(self.robot.x, self.robot.y, self.robot.rayon, objet)==True:
				print("Collision entre robot et un objet")
				raise CollisionException("Collision entre robot et un objet")


if __name__ == "__main__":

	# Création d'un environnement et d'un robot
	environnement = Environnement(800, 800, 0.1)
	robot = Robot(400, 400, 0, 15, 25, 0, 0, 4) # robot immobile, pour montrer ce que fait le controleur

	# Création d'une simulation, d'une interface graphique
	liste_objets = environnement.generer_obstacles(robot, 0)
	s = Simulation(environnement, robot, liste_objets)
	gui = GUI(environnement, robot, liste_objets)

	# Stratégies
	stavance = StrategieAvance(100, 36, robot)
	stangle = StrategieAngle(90, 180, robot) # aucune idée de pourquoi 100, ça fonctionne c'est tout
	stcarre = StrategieCarre(stavance, stangle)
	
	#IA
	ia = FakeIA(environnement, robot, liste_objets)

	threadrun = Thread(target=run, args=(s, gui, stcarre)) # remplacer gui par None si on veut pas d'interface graphique

	threadrun.start()
	gui.window.mainloop() # retirer cette ligne si on veut pas d'interface graphique
