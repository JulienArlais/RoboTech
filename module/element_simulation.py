import numpy as np
import time
from .toolbox import format, distance, create_circle
from module.controleur import dt


class CollisionException(Exception):
	def __init__(self, message):
		"""constructeur de l'exception

		Args:
			message (string): message de l'exception
		"""
		self.message = message


class Objet:
	def __init__(self, x, y, theta, rayon):
		"""constructeur pour objet

		Args:
			x (float): coordonnée x réel
			y (float): coordonnée y réel
			theta (int): angle
			rayon (float): rayon
		"""
		self.x = x
		self.y = y
		self.theta = np.radians(theta)
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

	def tourner(self, dps):
		"""fait tourner le robot d'un certain degré par seconde

		Args:
			dps (int): degré par seconde
		"""
		delta = (self.dist_roue * np.radians(dps))/self.rayon_roue
		if dps > 0:
			self.set_vitesse(self.vitAngD, self.vitAngG+delta)
		else:
			self.set_vitesse(self.vitAngD+delta, self.vitAngG)

	def set_vitesse(self, rps1, rps2):
		"""setter de vitesse pour les roues

		Args:
			rps1 (float): vitesse angulaire roue droite en radian par seconde
			rps2 (float): vitesse angulaire roue gauche en radian par seconde
		"""
		self.vitAngD = rps1
		self.vitAngG = rps2

	def getXstep(self, dt):
		"""donne le déplacement en x en un pas de temps dt

		Args:
			dt (float): pas de temps

		Returns:
			float: déplacement en x
		"""
		return self.vitAngD * self.rayon_roue * np.cos(self.theta) * dt

	def getYstep(self, dt):
		"""donne le déplacement en y en un pas de temps dt

		Args:
			dt (float): pas de temps

		Returns:
			float: déplacement en y
		"""
		return self.vitAngD * self.rayon_roue * np.sin(self.theta) * dt

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
			x += self.vitAngD * self.rayon_roue * np.cos(self.theta) * 0.01
			y += self.vitAngG * self.rayon_roue * np.sin(self.theta) * 0.01
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

		Args:
			robot (Robot): robot

		Returns:
			Objet: objet généré
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
			robot (Robot): robot
			nb (int): nombre d'objets à créer

		Returns:
			List[Objet]: liste des objets générés
		"""
		return [self.generer_un_obstacle(robot) for _ in range(nb)]


	def avancer_robot(self, robot, dt):
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
			robot.theta += (robot.vitAngD - robot.vitAngG) * robot.rayon/robot.dist_roue * dt
			robot.x += robot.vitAngD * robot.rayon_roue * np.cos(robot.theta) * dt
			robot.y += robot.vitAngD * robot.rayon_roue * np.sin(robot.theta) * dt
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
		if (self.robot.x+self.robot.rayon > self.environnement.width) or (self.robot.x-self.robot.rayon < 0) or (self.robot.y+self.robot.rayon > self.environnement.height) or (self.robot.y-self.robot.rayon < 0):
			print("Collision avec les limites de l'environnement")
			raise CollisionException("Collision avec les limites de l'environnement")		
		for objet in self.objets:
			if self.environnement.collision(self.robot.x, self.robot.y, self.robot.rayon, objet)==True:
				print("Collision entre robot et un objet")
				raise CollisionException("Collision entre robot et un objet")
				
def run(simulation, gui, ia):
	"""exécution de la simulation

	Args:
		simulation (Simulation): simulation à exécuter
		gui (GUI): interface graphique à afficher
	"""
	while True:
		try:
			if ia.stop():
				return
			ia.update()
			simulation.update()
			if gui is not None:
				gui.update()
			time.sleep(dt)
		except CollisionException as e:
			break
