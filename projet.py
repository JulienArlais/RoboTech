import numpy as np
import tkinter as tk
from module.module_outils import format, distance, create_circle
from module.module_projet import Objet, Robot, Environnement, Roue

mult = 10

class CollisionException(Exception):
	def __init__(self, message):
		"""Prend en paramètre le message à afficher lors de la collisions
		   :param message: message à afficher
		"""
		self.message = message

class Simulation:
	def __init__(self, env, robot, objets): 
		self.environnement = env
		self.robot = robot
		self.objets = objets
		self.window = tk.Tk()
		tk.Label(text="Interface Graphique")
		self.canvas = tk.Canvas(self.window, width=self.environnement.width*mult, height=self.environnement.height*mult)
		self.r = create_circle(self.robot.x*mult, self.robot.y*mult, self.robot.rayon*mult, self.canvas, "red")
		rdroite = self.robot.rdroite
		self.d = self.canvas.create_line(self.robot.x*mult, self.robot.y*mult, self.robot.x*mult+rdroite.vitesse_angulaire*rdroite.rayon*np.cos(robot.theta)*mult, self.robot.y*mult+rdroite.vitesse_angulaire*rdroite.rayon*np.sin(robot.theta)*mult, arrow=tk.LAST)
		for objet in self.objets:
			create_circle(objet.x*mult, objet.y*mult, objet.rayon*mult, self.canvas, "black")
		self.canvas.pack()

	def update(self):
		"""mise à jour de l'environnement

		Args:
			objet (Objet): objet de la simulation
		"""
		self.environnement.avancer_robot(self.robot, 1)
		rdroite = self.robot.rdroite
		self.canvas.coords(self.d, self.robot.x*mult, self.robot.y*mult, self.robot.x*mult+4*rdroite.vitesse_angulaire*rdroite.rayon*np.cos(self.robot.theta)*mult, self.robot.y*mult+4*rdroite.vitesse_angulaire*rdroite.rayon*np.sin(self.robot.theta)*mult) #taille de la flèche : 4
		self.canvas.move(self.r, rdroite.vitesse_angulaire*rdroite.rayon*np.cos(self.robot.theta)*mult, rdroite.vitesse_angulaire*rdroite.rayon*np.sin(self.robot.theta)*mult)
		if (self.robot.x+self.robot.rayon > self.environnement.width*self.environnement.scale) or (self.robot.x-self.robot.rayon < 0) or (self.robot.y+self.robot.rayon > self.environnement.height*self.environnement.scale) or (self.robot.y-self.robot.rayon < 0):
			print("Collision avec les limites de l'environnement")
			#raise CollisionException("Collision avec les limites de l'environnement")
			self.environnement.avancer_robot(self.robot, -1)
			self.canvas.move(self.r, -rdroite.vitesse_angulaire*rdroite.rayon*np.cos(self.robot.theta)*mult, -rdroite.vitesse_angulaire*rdroite.rayon*np.sin(self.robot.theta)*mult)
			self.canvas.coords(self.d, self.robot.x*mult, self.robot.y*mult, self.robot.x*mult+4*(-rdroite.vitesse_angulaire*rdroite.rayon)*np.cos(self.robot.theta)*mult, self.robot.y*mult+4*(-rdroite.vitesse_angulaire*rdroite.rayon)*np.sin(self.robot.theta)*mult)
			print(self.robot.x,self.robot.y)
			self.robot.tourner(np.random.uniform(90,270))
		for objet in self.objets:
			if self.environnement.collision_robot_objet(self.robot, objet)==True:
				print("Collision entre robot et un objet")
				raise CollisionException("Collision entre robot et un objet")
		if (np.random.rand() < 0.02):
			self.robot.tourner(np.random.uniform(0,360))
		
	def run(self):
		"""Exécution de la simulation
		"""
		try:
			self.update()
		except CollisionException as e:
			return
		self.canvas.after(35, self.run) #vitesse simulation, argument en millisecondes


# Création d'un environnement et d'un robot
environnement = Environnement(80, 80, 1)
r_gauche = Roue(90,1)
r_droite = Roue(90,1)
robot = Robot(40, 55.7, 0, 1.6, r_gauche, r_droite)

# Création d'une simulation et ajout du robot et des objets dans l'environnement et affichage de l'environnement
#environnement.placer_robot_env(robot)
liste_objets = environnement.generer_obstacles(5)
s = Simulation(environnement, robot, liste_objets)

# Mise à jour de la simulation
s.run()
s.window.mainloop()
