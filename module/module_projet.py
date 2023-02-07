import numpy as np
from .module_outils import format, distance, create_circle


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
		#self.vitesse = vitesse
		#self.acceleration = 0
		self.rayon = rayon
		self.rdroite = rd
		self.rgauche = rg

	def tourner(self, angle):
		"""fait tourner le robot d'un certain angle
		Args:
		angle (int): un angle en degré
		"""
		# angle est la valeur d'angle que l'on va ajouter à notre angle. Elle peut être positive ou négative
		self.rgauche.vitesse_angulaire *= -1
		while (self.theta != self.theta + np.radians(angle)):
			self.theta += np.radians(1)
		self.rgauche.vitesse_angulaire *= -1

class Roue:
	def __init__(self, vitesse_angulaire, rayon):
		"""Constructeur pour Roue
		Args:
			vitesse_angulaire (float): vitesse angulaire initiale en rad/s
			rayon (float): rayon en m de la roue
		"""
		self.vitesse_angulaire = np.radians(vitesse_angulaire)
		self.acceleration = 0
		self.rayon = rayon

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
		#self.grid = [[' ' for _ in range(width)] for _ in range(height)]
		
	#def retirer_robot_env(self,robot):
	#	"""retire le robot de l'environnement
	#	Args:
	#		robot (Robot): robot à retirer
	#	"""
	#	x = int(robot.x / self.scale)
	#	y = int(robot.y / self.scale)
	#	if (self.grid[y][x] == 'R'):
	#		self.grid[y][x] = '.'
	
	#def placer_robot_env(self, robot):
	#	"""place le robot dans l'environnement si possible, sinon ne fait rien
	#	Args:
	#		robot (Robot): robot à placer
	#	"""
	#	x = int(robot.x / self.scale)
	#	y = int(robot.y / self.scale)
	#	if (self.grid[y][x] == ' ' or self.grid[y][x] == '.'):
	#		self.grid[y][x] = 'R'

	#def placer_objet_env(self, objet): # à mettre private car pas automatiquement dans liste de generer ?
	#	"""place l'objet dans l'environnement si possible, sinon ne fait rien
	#	Args:
	#		objet (Objet): objet à placer
	#	"""
	#	x = int(objet.x / self.scale)
	#	y = int(objet.y / self.scale)
	#	if (self.grid[y][x] == ' ' or self.grid[y][x] == '.'):
	#		self.grid[y][x] = 'O'
			
	def generer_obstacles(self, nb):
		'''Génère nb objets et les place aléatoirement
		Args:
			nb (int): nombre d'objets à créer
		Returns:
			List[Objet]: liste des objets générés
		'''
		i = 0
		libre = True
		liste = []
		while i < nb :
			x = np.random.uniform(0,self.width)
			y = np.random.uniform(0,self.height)
			rayon = np.random.uniform(0.5,1) # Rayon initialisé entre 0.5 et 1
			for obj in liste:
				if (self.collision_entre_objets(x,y,rayon,obj)):
					libre = False
					break
			if (libre):
				o = Objet(x, y, 0, 0, rayon)
				#self.placer_objet_env(o)
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
		#self.grid[(int)(y)][(int)(x)] = '.'
		rdroite = robot.rdroite
		robot.x += rdroite.vitesse_angulaire * rdroite.rayon * np.cos(robot.theta) * dt
		robot.y += rdroite.vitesse_angulaire * rdroite.rayon * np.sin(robot.theta) * dt
		if (robot.rayon + robot.x > self.width*self.scale) or (robot.x - robot.rayon < 0) or (robot.y + robot.rayon > self.height*self.scale) or (robot.y - robot.rayon < 0):
			return
		#if (self.grid[int(robot.y / self.scale)][int(robot.x / self.scale)] != 'X'):
		#	self.grid[int(robot.y / self.scale)][int(robot.x / self.scale)] = 'R'
		#	x = x * self.scale
		#	y = y * self.scale
		print("Le robot en (", format(x), ",", format(y), ") a avancé et s'est déplacé en (",format(robot.x),",",format(robot.y),")")
		#else:
		#	print("Collision à venir")
		#	return
			

	def collision_robot_objet(self, robot, objet):
		"""Teste s'il y a eu collision entre le robot et l'objet
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
