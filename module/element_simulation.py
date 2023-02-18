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
	def __init__(self, x, y, theta, rayon, vitesse_angulaire_d, vitesse_angulaire_g, rayr):
		"""constructeur de robot

		Args:
			x (float): coordonnée x réel
			y (float): coordonnée y réel
			theta (int): angle
			rayon (float): rayon
			vad (Roue): vitesse angulaire roue droite
			vag (Roue): vitesse angulaire roue gauche
			rayr: rayon des roues
		"""
		self.x = x
		self.y = y
		self.theta = np.radians(theta)
		self.rayon = rayon
		self.vad = np.radians(vitesse_angulaire_d)
		self.vag = np.radians(vitesse_angulaire_g)
		self.rayr = rayr

	def set_vad(self,vitesse_angulaire):
		''' setter de vad '''
		self.vad = vitesse_angulaire
		
	def set_vag(self,vitesse_angulaire):
		''' setter de vag '''
		self.vag = vitesse_angulaire

	def getXstep(self, dt):
		"""donne le déplacement en x en un pas de temps dt

		Args:
			dt (float): pas de temps

		Returns:
			float: déplacement en x
		"""
		return self.vad * self.rayr * np.cos(self.theta) * dt

	def getYstep(self, dt):
		"""donne le déplacement en y en un pas de temps dt

		Args:
			dt (float): pas de temps

		Returns:
			float: déplacement en y
		"""
		return self.vad * self.rayr * np.sin(self.theta) * dt

	def capteur(self, env, distmax):
		"""donne la distance par rapport au mur dans la direction du robot

		Args:
			env (Environnement): environnement

		Returns:
			float: distance
		"""
		x = self.x
		y = self.y
		while not((x+self.rayon > env.width*env.scale) or (x-self.rayon < 0) or (y+self.rayon > env.height*env.scale) or (y-self.rayon < 0)):
			x += self.vad * self.rayr * np.cos(self.theta) * 0.01
			y += self.vag * self.rayr * np.sin(self.theta) * 0.01
			if distance(self.x, self.y, x, y) > distmax:
				return distmax
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
		rayon = np.random.uniform(0.5, 1)
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
		if (robot.vad == robot.vag):
			robot.x += robot.vad * robot.rayr * np.cos(robot.theta) * dt
			robot.y += robot.vad * robot.rayr * np.sin(robot.theta) * dt
		elif (robot.vad == -robot.vag and robot.vad > 0):
			robot.theta += robot.vad * dt
		elif (robot.vad == -robot.vag and robot.vag > 0):
			robot.theta += robot.vad * dt
		#if (robot.rayon + robot.x > self.width*self.scale) or (robot.x - robot.rayon < 0) or (robot.y + robot.rayon > self.height*self.scale) or (robot.y - robot.rayon < 0):
		#	return

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
