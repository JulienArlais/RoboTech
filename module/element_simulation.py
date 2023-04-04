import numpy as np
import time
from .toolbox import format, distance, create_circle
from module.constante import dt


class CollisionException(Exception):
	def __init__(self, message):
		"""constructeur de l'exception

		Args:
			message (string): message de l'exception
		"""
		self.message = message


class Objet:
	def __init__(self, x, y, rayon):
		"""constructeur pour objet

		Args:
			x (float): coordonnée x réel
			y (float): coordonnée y réel
			rayon (float): rayon
		"""
		self.x = x
		self.y = y
		self.rayon = rayon


class Robot:
	def __init__(self, x, y, theta, rayon, dist_roue, rayon_roue):
		"""constructeur de robot

		Args:
			x (float): coordonnée x réel
			y (float): coordonnée y réel
			theta (int): angle
			rayon (float): rayon
			rayon_roue: rayon des roues
		"""
		self.x = x
		self.y = y
		self.theta = np.radians(theta)
		self.rayon = rayon
		self.dist_roue = dist_roue
		self.vitAngD = 0
		self.vitAngG = 0
		self.rayon_roue = rayon_roue
		self.last_update = 0

	def tourner(self, dps):
		"""fait tourner le robot d'un certain degré par seconde

		Args:
			dps (int): degré par seconde
		"""
		delta = (self.dist_roue * np.abs(np.radians(dps)))/self.rayon_roue
		if dps > 0:
			self.set_vitesse(np.degrees(self.vitAngG+delta), np.degrees(self.vitAngD))
		else:
			self.set_vitesse(np.degrees(self.vitAngG), np.degrees(self.vitAngD+delta))

	def set_vitesse(self, dps1, dps2):
		"""setter de vitesse pour les roues

		Args:
			rps1 (float): vitesse angulaire roue droite en radian par seconde
			rps2 (float): vitesse angulaire roue gauche en radian par seconde
		"""
		self.vitAngG = np.radians(dps1)
		self.vitAngD = np.radians(dps2)
	
	def get_vitAng(self):
		return (self.vitAngG, self.vitAngD)

	def getXstep(self):
		"""donne le déplacement en x en un pas de temps dt

		Args:
			dt (float): pas de temps

		Returns:
			float: déplacement en x
		"""
		return self.vitAngD * self.rayon_roue * np.cos(self.theta) * (time.time()-self.last_update)

	def getYstep(self):
		"""donne le déplacement en y en un pas de temps dt

		Args:
			dt (float): pas de temps

		Returns:
			float: déplacement en y
		"""
		return self.vitAngD * self.rayon_roue * np.sin(self.theta) * (time.time()-self.last_update)

	def get_distance(self, env):
		"""donne la distance par rapport au mur dans la direction du robot

		Args:
			env (Environnement): environnement
			distmax : la distance max à laquelle le capteur peut détecter des objets
		Returns:
			float: distance
		"""
		x = self.x
		y = self.y
		while not(((x+self.rayon) > env.width) or (x-self.rayon < 0) or ((y+self.rayon) > env.height) or (y-self.rayon < 0)):
			x += self.vitAngD * self.rayon_roue * np.cos(self.theta) * 0.01
			y += self.vitAngG * self.rayon_roue * np.sin(self.theta) * 0.01
			if distance(self.x, self.y, x, y) > 800:
				return 800
			if distance(self.x, self.y, x, y) < 0.5: 
				return 0.5
			for _ in range(len(env.objets)):
				if env.collision(x, y, self.rayon):
					return distance(self.x, self.y, x, y)
		return distance(self.x, self.y, x, y)

	def update(self):
		self.last_update = time.time()


class Environnement:
	def __init__(self, width, height, scale): 
		"""constructeur pour l'environnement

		Args:
			width (int): largeur 
			height (int): hauteur
			scale (int): échelle
		"""
		self.width = width
		self.height = height
		self.scale = scale
		self.objets = []
			
	def generer_un_obstacle(self, robot):
		"""génère un objet et le place aléatoirement dans l'environnement sans collision avec le robot

		Args:
			robot (Robot): robot
		"""
		rayon = np.random.uniform(1, 20)
		while True:
			x = np.random.uniform(rayon, self.width - rayon)
			y = np.random.uniform(rayon, self.height - rayon)
			if all(not self.collision(x, y, rayon) for obj in self.objets):
				self.objets.append(Objet(x, y, rayon))
				break

	def generer_obstacles(self, robot, nb):
		"""génère nb objets et les place aléatoirement dans l'environnement sans collision avec le robot

		Args:
			robot (Robot): robot
			nb (int): nombre d'objets à créer
		"""
		for _ in range(nb):
			self.generer_un_obstacle(robot)

	def update(self, robot):
		"""mise à jour de l'environnement

		Args:
			robot (Robot): robot à faire avancer
			dt (int): durée en seconde
		"""
		now = time.time()
		if robot.last_update == 0:
			robot.last_update = now
		else:
			print("Le robot en (", format(robot.x), ",", format(robot.y), ") a avancé et s'est déplacé en (",end='')
			robot.theta += (robot.vitAngD - robot.vitAngG) * robot.rayon/robot.dist_roue * (now - robot.last_update)
			robot.x += robot.vitAngD * robot.rayon_roue * np.cos(robot.theta) * (now - robot.last_update)			
			robot.y += robot.vitAngD * robot.rayon_roue * np.sin(robot.theta) * (now - robot.last_update)
			print(format(robot.x),",",format(robot.y),")")

	def collision(self, x, y, ray):
		"""Teste s'il y aura collision aux coordonnées (x, y)

		Args:
			x (float): coordonnées x réelle
			y (float): coordonnées y réelle
			ray (float): rayon
			obj (Objet): objet à tester

		Returns:
			boolean: collision ou non avec obj aux coordonnées (x, y)
		"""
		for objet in self.objets:
			if distance(x, y, objet.x, objet.y) <= ray + objet.rayon:
				return True
		return False
		

class Simulation:
	def __init__(self, env, robot):
		"""constructeur de la simulation

		Args:
			env (Environnement): environnemment de la simulation
			robot (Robot): robot de la simulation
		"""
		self.environnement = env
		self.robot = robot

	def update(self):
		"""mise à jour de la simulation (mise à jour du robot, de l'environnement et règles de la simulation)

		Raises:
			CollisionException: collision
		"""
		self.environnement.update(self.robot) # mise à jour de l'environnement
		self.robot.update()
		if (self.robot.x+self.robot.rayon > self.environnement.width) or (self.robot.x-self.robot.rayon < 0) or (self.robot.y+self.robot.rayon > self.environnement.height) or (self.robot.y-self.robot.rayon < 0):
			print("Collision avec les limites de l'environnement")
			raise CollisionException("Collision avec les limites de l'environnement")		
		for objet in self.environnement.objets:
			if self.environnement.collision(self.robot.x, self.robot.y, self.robot.rayon)==True:
				print("Collision entre robot et un objet")
				raise CollisionException("Collision entre robot et un objet")
				