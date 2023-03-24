from .constante import dt
import numpy as np
from .toolbox import distance
import cv2
from .camera import detect, BaliseException


class StrategieAvance():
	def __init__(self, distance, vitesse, robot):
		"""constructeur de la stratégie pour avancer d'une distance voulu

		Args:
			distance (float): distance
			vitesse (int): vitesse des roues ( degré par seconde )
			robot (Robot): robot
		"""
		self.distance = distance
		self.vitesse = vitesse
		self.robot = robot
		self.parcouru = 0
		
	def update(self):
		"""itération de la stratégie
		"""
		if self.stop():
			return
		self.robot.set_vitesse(self.vitesse, self.vitesse)
		self.parcouru += distance(self.robot.x - self.robot.getXstep(dt), self.robot.y - self.robot.getYstep(dt), self.robot.x, self.robot.y)
		x= self.robot.distance_parcourue() # A RETIRER PLUS TARD, UTILE POUR TESTER LA FCT
			
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		if (self.parcouru >= self.distance):
			self.robot.set_vitesse(0, 0)
			self.parcouru = 0
			return True
		return False


class StrategieAngle():
	def __init__(self, angle, dps, robot):
		"""constructeur de la stratégie pour tourner d'un angle voulu

		Args:
			angle (int): angle souhaité ( en degré )
			dps (int): degré par seconde
			robot (Robot): robot
		"""
		self.angle = angle
		self.dps = dps
		self.robot = robot
		self.angleapplique = 0

	def update(self):
		"""itération de la stratégie
		"""
		if self.stop():
			return
		self.robot.tourner(self.dps * dt)
		delta_angle = (self.robot.vitAngD - self.robot.vitAngG) * self.robot.rayon/self.robot.dist_roue * dt * 180/np.pi
		self.angleapplique += delta_angle

	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		if np.abs(self.angleapplique) >= np.abs(self.angle):
			self.robot.set_vitesse(0, 0)
			self.angleapplique = 0
			return True
		else:
			return False


class StrategieArretMur():
	def __init__(self, robot, env, vitesse):
		"""constructeur de la stratégie pour s'arrêter à un mur

		Args:
			robot (Robot): robot
			env (Environnement): environnement
			vitesse (int): vitesse des roues ( degré par seconde )
		"""
		self.robot = robot
		self.env = env
		self.stavance = StrategieAvance(self.env.width*2, vitesse, self.robot)
	
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		return (self.robot.capteur(self.env, 10000) < 2*self.robot.rayon)

	def update(self):
		"""itération de la stratégie
		"""
		if self.stop():
			return
		self.stavance.update()


class StrategieSeq():
	def __init__(self, liste):
		"""constructeur de la stratégie séquentielle

		Args:
			liste (_type_): liste de stratégies
		"""
		self.liste = liste
		self.indlist = 0
		
	def update(self):
		"""itération de la stratégie
		"""
		if self.liste[self.indlist].stop():
			self.indlist += 1
			if self.stop():
				return
		self.liste[self.indlist].update()
		
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		return self.indlist >= len(self.liste)

class StrategieSuivreBalise():
	def __init__(self, data, robot):
		self.data = data
		self.robot = robot
		self.stangle1 = StrategieAngle(45, 45, self.robot)
		self.stangle2 = StrategieAngle(-45, -45, self.robot)

	def update(self):
		if self.stop():
			return

		if (detect(self.data) <= -5 or detect(self.data) >= 5): # si la balise se situe plus de ±5% du centre
			if detect(self.data) <= 0:
				self.stangle1.update()
				if self.stangle1.stop():
					StrategieAvance(5, 45, self.robot).update()
			else:
				self.stangle2.update()		
				if self.stangle2.stop():
					StrategieAvance(5, 45, self.robot).update()	
		else:
			StrategieAvance(15, 45, self.robot).update()

	def stop(self):
		try:
			detect(self.data)
		except BaliseException as e:
			return True
		return False
