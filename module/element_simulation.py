import numpy as np
from .toolbox import format, distance, create_circle


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
	def __init__(self, x, y, theta, rayon, rd, rg):
		"""constructeur de robot

		Args:
			x (float): coordonnée x réel
			y (float): coordonnée y réel
			theta (int): angle
			rayon (float): rayon
			rd (Roue): roue droite
			rg (Roue): roue gauche
		"""
		self.x = x
		self.y = y
		self.theta = np.radians(theta)
		self.rayon = rayon
		self.rdroite = rd
		self.rgauche = rg

	def tourner(self, angle):
		"""fait tourner le robot d'un certain angle

		Args:
			angle (int): angle en degré
		"""
		self.theta += np.radians(angle)

	def getXstep(self, dt):
		"""donne le déplacement en x en un pas de temps dt

		Args:
			dt (float): pas de temps

		Returns:
			float: déplacement en x
		"""
		return self.rdroite.vitesse_angulaire * self.rdroite.rayon * np.cos(self.theta) * dt

	def getYstep(self, dt):
		"""donne le déplacement en y en un pas de temps dt

		Args:
			dt (float): pas de temps

		Returns:
			float: déplacement en y
		"""
		return self.rdroite.vitesse_angulaire * self.rdroite.rayon * np.sin(self.theta) * dt


class Roue:
	def __init__(self, vitesse_angulaire, rayon):
		"""constructeur pour Roue

		Args:
			vitesse_angulaire (float): vitesse angulaire initiale en rad/s
			rayon (float): rayon de la roue
		"""
		self.vitesse_angulaire = np.radians(vitesse_angulaire)
		self.acceleration = 0
		self.rayon = rayon

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
			
	def generer_obstacles(self, robot, nb):
		"""génère nb objets et les place aléatoirement

		Args:
			nb (int): nombre d'objets à créer

		Returns:
			List[Objet]: liste des objets générés
		"""
		i = 0
		libre = True
		liste = []
		while i < nb :
			rayon = np.random.uniform(0.5,1)
			x = np.random.uniform(rayon, self.width-rayon)
			y = np.random.uniform(rayon, self.height-rayon)
			 # Rayon initialisé entre 0.5 et 1
			for obj in liste:
				if ((self.collision_entre_objets(x,y,rayon,obj)) or  (self.collision_robot_objet(robot,obj))):
					libre = False
					break
			if (libre):
				print("a",x,y)
				o = Objet(x, y, 0, 0, rayon)
				liste.append(o)
				i+=1
			libre = True
			
		return liste

	def avancer_robot(self, robot, dt):
		"""fait avancer pendant une durée dt le robot dans l'environnement

		Args:
			robot (Robot): robot à faire avancer
			dt (int): durée en seconde
		"""
		x = robot.x
		y = robot.y
		rdroite = robot.rdroite
		robot.x += rdroite.vitesse_angulaire * rdroite.rayon * np.cos(robot.theta) * dt
		robot.y += rdroite.vitesse_angulaire * rdroite.rayon * np.sin(robot.theta) * dt
		if (robot.rayon + robot.x > self.width*self.scale) or (robot.x - robot.rayon < 0) or (robot.y + robot.rayon > self.height*self.scale) or (robot.y - robot.rayon < 0):
			return

		print("Le robot en (", format(x), ",", format(y), ") a avancé et s'est déplacé en (",format(robot.x),",",format(robot.y),")")


	def collision_robot_objet(self, robot, objet):
		"""teste s'il y a eu collision entre le robot et l'objet

		Args:
			robot (Robot): robot à tester
			objet (Objet): objet à tester

		Returns:
			boolean: collision ou non entre le robot et l'objet
		"""
		if distance(robot.x, robot.y, objet.x, objet.y) <= robot.rayon + objet.rayon:
			return True
		return False
		
	def collision_entre_objets(self, x, y, ray, obj):
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
