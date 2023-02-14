import numpy as np
import tkinter as tk
import time
from module._2D import GUI
from threading import Thread
from module.element_simulation import Objet, Robot, Environnement, Roue


dt = 0.05 # pas de temps

class CollisionException(Exception):
	def __init__(self, message):
		"""constructeur de l'exception

		Args:
			message (string): message de l'exception
		"""
		self.message = message

		
def run(simulation, gui):
	"""exécution de la simulation

	Args:
		simulation (Simulation): simulation à exécuter
		gui (GUI): interface graphique à afficher
	"""
	while True:
		try:
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
		if (self.robot.x+self.robot.rayon > self.environnement.width*self.environnement.scale) or (self.robot.x-self.robot.rayon < 0) or (self.robot.y+self.robot.rayon > self.environnement.height*self.environnement.scale) or (self.robot.y-self.robot.rayon < 0):
			print("Collision avec les limites de l'environnement")
			#raise CollisionException("Collision avec les limites de l'environnement")
			self.environnement.avancer_robot(self.robot, -dt)
			print(self.robot.x,self.robot.y)
			self.robot.tourner(np.random.uniform(90,270))
		for objet in self.objets:
			if self.environnement.collision_robot_objet(self.robot, objet)==True:
				print("Collision entre robot et un objet")
				raise CollisionException("Collision entre robot et un objet")
		if (np.random.rand() < 0.02):
			self.robot.tourner(np.random.uniform(0,360))

if __name__ == "__main__":

	# Création d'un environnement et d'un robot
	environnement = Environnement(80, 80, 1)
	roue = Roue(720,1)
	robot = Robot(40, 55.7, 0, 1.6, roue, roue)

	# Création d'une simulation, d'une interface graphique
	liste_objets = environnement.generer_obstacles(robot, 5)
	s = Simulation(environnement, robot, liste_objets)
	gui = GUI(environnement, robot, liste_objets)
	threadrun = Thread(target=run, args=(s, gui)) # remplacer gui par None si on veut pas d'interface graphique

	threadrun.start()
	gui.window.mainloop() # retirer cette ligne si on veut pas d'interface graphique