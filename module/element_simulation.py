import numpy as np
from .toolbox import format, distance, create_circle


class CollisionException(Exception):
	def __init__(self, message):
		"""constructeur de l'exception

		Args:
			message (string): message de l'exception
		"""
		self.message = message


class Objet:
	def __init__(self, x, y, theta, vitesse, rayon):
		"""Constructeur pour objet
		Args:
			x (float): coordonnée x réel
			y (float): coordonnée y réel
			theta (int): angle
			vitesse (float): vitesse
			rayon (float): rayon
		"""
		self.x = x
		self.y = y
		self.theta = np.radians(theta)
		self.vitesse = vitesse
		self.rayon = rayon

class Robot:
	def __init__(self, x, y, theta, rayon, distroue, vitesse_angulaire_d, vitesse_angulaire_g, rayr):
		"""constructeur de robot

		Args:
			x (float): coordonnée x réel
			y (float): coordonnée y réel
			theta (int): angle
			rayon (float): rayon
			vitAngD (Roue): vitesse angulaire roue droite
			vitAngG (Roue): vitesse angulaire roue gauche
			rayr: rayon des roues
		"""
		self.x = x
		self.y = y
		self.theta = np.radians(theta)
		self.rayon = rayon
		self.distroue = distroue
		self.vitAngD = np.radians(vitesse_angulaire_d)
		self.vitAngG = np.radians(vitesse_angulaire_g)
		self.rayr = rayr

	def tourner(self, dps):
		delta = (self.distroue * np.radians(dps))/self.rayr
		if dps > 0:
			self.set_vitesse(self.vitAngD, self.vitAngG+delta)
		else:
			self.set_vitesse(self.vitAngD+delta, self.vitAngG)

	def set_vitesse(self, dps1, dps2):
		"""setter de vitesse pour les roues

		Args:
			dps1 (float): vitesse angulaire roue droite
			dps2 (float): vitesse angulaire roue gauche
		"""
		self.vitAngD = dps1
		self.vitAngG = dps2

	def getXstep(self, dt):
		"""donne le déplacement en x en un pas de temps dt

		Args:
			dt (float): pas de temps

		Returns:
			float: déplacement en x
		"""
		return self.vitAngD * self.rayr * np.cos(self.theta) * dt

	def getYstep(self, dt):
		"""donne le déplacement en y en un pas de temps dt

		Args:
			dt (float): pas de temps

		Returns:
			float: déplacement en y
		"""
		return self.vitAngD * self.rayr * np.sin(self.theta) * dt

	def capteur(self, env, distmax, obj):
		"""donne la distance par rapport au mur dans la direction du robot

		Args:
			env (Environnement): environnement
			distmax : la distance max à laquelle le capteur peut détecter des objets
			obj : la liste des objets dans l'environnement

		Returns:
			float: distance
		"""
		x = self.x
		y = self.y
		while not(((x+self.rayon) > env.width) or (x-self.rayon < 0) or ((y+self.rayon) > env.height) or (y-self.rayon < 0)):
			x += self.vitAngD * self.rayr * np.cos(self.theta) * 0.01
			y += self.vitAngG * self.rayr * np.sin(self.theta) * 0.01
			if distance(self.x, self.y, x, y) > distmax:
				return distmax
			for i in range(len(obj)):
				if env.collision(x, y, self.rayon, obj[i]):
					return distance(self.x, self.y, x, y)
		return distance(self.x, self.y, x, y)


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

		Returns:
			Objet: l'objet généré
		"""
		rayon = np.random.uniform(1, 20)
		while True:
			x = np.random.uniform(rayon, self.width - rayon)
			y = np.random.uniform(rayon, self.height - rayon)
			if all(not self.collision(x, y, rayon, obj) and not self.collision(robot, obj) for obj in self.objets):
				return Objet(x, y, 0, 0, rayon)

	def generer_obstacles(self, robot, nb):
		"""génère nb objets et les place aléatoirement dans l'environnement sans collision avec le robot

		Args:
			nb (int): nombre d'objets à créer

		Returns:
			List[Objet]: liste des objets générés
		"""
		return [self.generer_un_obstacle(robot) for _ in range(nb)]


	def avancer_robot(self, robot, dt): # changer les avancer en mvt
		"""fait avancer pendant une durée dt le robot dans l'environnement

		Args:
			robot (Robot): robot à faire avancer
			dt (int): durée en seconde
		"""
		print("Le robot en (", format(robot.x), ",", format(robot.y), ") a avancé et s'est déplacé en (",end='')
		if (robot.vitAngD == -robot.vitAngG and robot.vitAngD > 0):
			robot.theta += robot.vitAngD * dt
		elif (robot.vitAngD == -robot.vitAngG and robot.vitAngG > 0):
			robot.theta += robot.vitAngD * dt
		else:
			robot.theta += (robot.vitAngD - robot.vitAngG) * robot.rayon/robot.distroue
			robot.x += robot.vitAngD * robot.rayr * np.cos(robot.theta) * dt
			robot.y += robot.vitAngD * robot.rayr * np.sin(robot.theta) * dt
		print(format(robot.x),",",format(robot.y),")")


	def collision(self, x, y, ray, obj):
		"""Teste s'il y aura collision avec obj aux coordonnées (x, y)

		Args:
			x (float): coordonnées x réelle
			y (float): coordonnées y réelle
			ray (float): rayon
			obj (Objet): objet à tester

		Returns:
			boolean: collision ou non avec obj aux coordonnées (x, y)
		"""
		if distance(x, y, obj.x, obj.y) <= ray + obj.rayon:
			return True
		return False
