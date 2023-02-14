import numpy as np
import tkinter as tk
import time
from threading import Thread
from module.module_outils import format, distance, create_circle
from module.module_projet import Objet, Robot, Environnement, Roue

mult = 10 # multiplieur pour l'affichage graphique
dt = 0.05 # pas de temps

class CollisionException(Exception):
	def __init__(self, message):
		"""constructeur de l'exception

		Args:
			message (string): message de l'exception
		"""
		self.message = message


class GUI():
	def __init__(self, env, robot, objets):
		"""constructeur de l'interface graphique

		Args:
			env (Environnement): environnemment dans l'affichage
			robot (Robot): robot dans l'affichage
			objets (List[Objet]): liste des objets dans l'affichage
		"""
		self.environnement = env
		self.robot = robot
		self.objets = objets
		self.window = tk.Tk()
		self.window.title("Interface Graphique")
		self.canvas = tk.Canvas(self.window, width=self.environnement.width*mult, height=self.environnement.height*mult)
		self.r = create_circle(self.robot.x*mult, self.robot.y*mult, self.robot.rayon*mult, self.canvas, "red")
		rdroite = self.robot.rdroite
		self.d = self.canvas.create_line(self.robot.x*mult, self.robot.y*mult, self.robot.x*mult+self.robot.getXstep(dt)*mult, self.robot.y*mult+self.robot.getYstep(dt)*mult, arrow=tk.LAST)
		for objet in self.objets:
			create_circle(objet.x*mult, objet.y*mult, objet.rayon*mult, self.canvas, "black")
		self.canvas.pack()

	def update(self):
		self.canvas.coords(self.d, self.robot.x*mult-self.robot.getXstep(dt)*mult, self.robot.y*mult-self.robot.getYstep(dt)*mult, 1.0*self.robot.x*mult, self.robot.y*mult)
		self.canvas.move(self.r, self.robot.getXstep(dt)*mult, self.robot.getYstep(dt)*mult)


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