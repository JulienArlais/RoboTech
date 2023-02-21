import numpy as np
import tkinter as tk
import time
from module.affichage_2D import GUI
from threading import Thread
from module.element_simulation import Objet, Robot, Environnement, CollisionException
from module.controleur import FakeIA, Avancer_strategie, dt

def run(simulation, gui, ia):
	"""exécution de la simulation

	Args:
		simulation (Simulation): simulation à exécuter
		gui (GUI): interface graphique à afficher
	"""
	while True:
		try:
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
		for objet in self.objets:
			if self.environnement.collision(self.robot.x, self.robot.y, self.robot.rayon, objet)==True:
				print("Collision entre robot et un objet")
				raise CollisionException("Collision entre robot et un objet")


if __name__ == "__main__":

	# Création d'un environnement et d'un robot
	environnement = Environnement(800, 800, 0.1)
	robot = Robot(400, 400, 0, 15, 25, 720, 720, 4)

	# Création d'une simulation, d'une interface graphique
	liste_objets = environnement.generer_obstacles(robot, 15)
	s = Simulation(environnement, robot, liste_objets)
	gui = GUI(environnement, robot, liste_objets)
	#ia = FakeIA(environnement, robot, liste_objets)
	ia = Avancer_strategie(robot, 100)
	threadrun = Thread(target=run, args=(s, gui, ia)) # remplacer gui par None si on veut pas d'interface graphique

	threadrun.start()
	gui.window.mainloop() # retirer cette ligne si on veut pas d'interface graphique
