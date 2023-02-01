import numpy as np
import module_outils as mo


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
	def __init__(self, x, y, theta, vitesse, rayon):
		"""Constructeur du robot
		Args:
			x (float): coordonnée x réel
			y (float): coordonnée y réel
			theta (int): angle
			vitesse (float): vitesse
			rayon (float): rayon
		"""
		# x et y des coordonnées en mètre, direction un angle par rapport à l'abscisse en float et la vitesse max du robot en m/s
		# on suppose que le robot est un cercle, pour faciliter les collisions
		self.x = x
		self.y = y
		self.theta = np.radians(theta)
		self.vitesse = vitesse
		#self.acceleration = 0
		self.rayon = rayon

	def avancer(self, dt):
		"""fait avancer le robot pendant une durée dt
		Args:
			dt (int): durée en seconde
		"""
		#vitesse += self.acceleration * dt
		#self.vitesse = min(self.vitesse, vitesse)  # pour s'assurer que la vitesse ne dépasse pas la vitesse maximale
		self.x += self.vitesse * np.cos(self.theta) * dt
		self.y += self.vitesse * np.sin(self.theta) * dt

	def tourner(self, angle):
		"""fait tourner le robot d'un certain angle
		Args:
			angle (int): un angle en degré
		"""
		# angle est la valeur d'angle que l'on va ajouter à notre angle. Elle peut être positive ou négative
		self.theta += np.radians(angle)
		
	def reculer(self, dt):
		"""fait reculer le robot pendant une durée dt
		Args:
			dt (int): durée en seconde
		"""
		#self.vitesse += self.acceleration * dt
		#self.vitesse = min(self.vitesse, self.vitesse)  # pour s'assurer que la vitesse ne dépasse pas la vitesse maximale
		self.x -= self.vitesse*np.cos(self.theta)
		self.y -= self.vitesse*np.sin(self.theta)


class Environnement:
	def __init__(self, width, height, scale): 
		"""Constructeur pour l'environnement
		Args:
			width (int): largeur 
			height (int): hauteur
			scale (int): échelle
		"""
		self.width = width
		self.height = height
		self.scale = scale
		self.grid = [[' ' for _ in range(width)] for _ in range(height)]
		
	def retirer_robot_env(self,robot):
		"""retire le robot de l'environnement
		Args:
			robot (Robot): robot à retirer
		"""
		x = int(robot.x / self.scale)
		y = int(robot.y / self.scale)
		if (self.grid[y][x] == 'R'):
			self.grid[y][x] = '.'
	
	def placer_robot_env(self, robot):
		"""place le robot dans l'environnement si possible, sinon ne fait rien
		Args:
			robot (Robot): robot à placer
		"""
		x = int(robot.x / self.scale)
		y = int(robot.y / self.scale)
		if (self.grid[y][x] == ' ' or self.grid[y][x] == '.'):
			self.grid[y][x] = 'R'

	def placer_objet_env(self, objet):
		"""place l'objet dans l'environnement si possible, sinon ne fait rien
		Args:
			objet (Objet): objet à placer
		"""
		x = int(objet.x / self.scale)
		y = int(objet.y / self.scale)
		if (self.grid[y][x] == ' ' or self.grid[y][x] == '.'):
			self.grid[y][x] = 'O'

	def avancer_robot_env(self, robot):
		"""fait avancer pendant 1 seconde le robot dans l'environnement
		Args:
			robot (Robot): robot à faire avancer
		"""
		x = robot.x / self.scale
		y = robot.y / self.scale
		self.grid[(int)(y)][(int)(x)] = '.'
		robot.avancer(1)
		if robot.x > self.width*self.scale or robot.x < 0 or robot.y > self.height*self.scale or robot.y < 0:
			return
		if (self.grid[int(robot.y / self.scale)][int(robot.x / self.scale)] != 'X'):
			self.grid[int(robot.y / self.scale)][int(robot.x / self.scale)] = 'R'
			x = x * self.scale
			y = y * self.scale
			print("Le robot en (", format(x), ",", format(y), ") a avancé et s'est déplacé en (",format(robot.x),",",format(robot.y),")")
		else:
			print("collision à venir")
			return
			
	def reculer_robot_env(self, robot):
		"""fait reculer pendant une seconde le robot dans l'environnement
		Args:
			robot (Robot): robot à faire reculer
		"""
		x = robot.x / self.scale
		y = robot.y / self.scale
		self.grid[(int)(y)][(int)(x)] = '.'
		robot.reculer(1)#Le pas dt est égale à 1
		if (self.grid[int(robot.y / self.scale)][int(robot.x / self.scale)] != 'X'):
			self.grid[int(robot.y / self.scale)][int(robot.x / self.scale)] = 'R'
			x = x * self.scale
			y = y * self.scale
			print("Le robot en (", format(x), ",", format(y), ") a reculé et s'est déplacé en (",format(robot.x),",",format(robot.y),")")
		else:
			print("Collision à venir")
			exit()

	def collision(self, robot, objet):
		"""Teste s'il y a eu collision entre le robot et l'objet
		Args:
			robot (Robot): robot à tester
			objet (Objet): objet à tester
		Returns:
			boolean: collision ou non entre le robot et l'objet
		"""
		if mo.distance(robot.x, robot.y, objet.x, objet.y) < max(robot.rayon, objet.rayon):
			return True
		return False
		

