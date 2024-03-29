import numpy as np
import cv2
import time
from ..camera import detect, BaliseException

class StrategieAvance():
	def __init__(self, distance, vitesse, proxy):
		"""constructeur de la stratégie pour avancer d'une distance voulue

		Args:
			distance (float): distance
			vitesse (int): vitesse des roues ( degré par seconde )
			proxy (Robot): proxy
		"""
		self.distance = distance
		self.vitesse = vitesse
		self.proxy = proxy
		self.proxy.reset_angle()
		
	def update(self):
		"""mise à jour de la stratégie
		"""
		self.proxy.set_vitesse(self.vitesse, self.vitesse)
			
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		print("StrategieAvance",self.proxy.distance_parcourue, self.distance)
		if (self.proxy.distance_parcourue >= self.distance):
			self.proxy.set_vitesse(0, 0)
			self.proxy.reset()
			return True
		return False


class StrategieAngle():
	def __init__(self, angle, dps, proxy):
		"""constructeur de la stratégie pour tourner d'un angle voulu

		Args:
			angle (int): angle souhaité ( en degré )
			dps (int): degré par seconde
			proxy (Robot): proxy
		"""
		self.angle = angle
		self.dps = dps
		self.proxy = proxy
		self.proxy.reset_angle()

	def update(self):
		"""mise à jour de la stratégie
		"""
		self.proxy.tourner(self.dps)

	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		print("StrategieAngle ",self.proxy.angle_parcouru,self.angle)
		if np.abs(self.proxy.angle_parcouru) >= np.abs(self.angle):
			self.proxy.set_vitesse(0, 0)
			self.proxy.reset()
			return True
		return False


class StrategieArretMur():
	def __init__(self, dist, vitesse, proxy):
		"""constructeur de la stratégie pour s'arrêter à un mur

		Args:
			dist (int): distance maximale à parcourir
			vitesse (int): vitesse des roues ( degré par seconde )
			proxy (Robot): proxy
		"""
		self.proxy = proxy
		self.dist = dist
		self.vitesse = vitesse
		self.capteur = 10000  # portée maximale du capteur
		self.dist_arret = 4*self.proxy.rayon  # distance robot/obstacle à laquelle le robot doit s'arrêter
		self.proxy.set_vitesse(self.vitesse, self.vitesse)
	
	def update(self):
		"""mise à jour de la stratégie
		"""
		self.proxy.set_vitesse(self.vitesse, self.vitesse)
	
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		self.capteur = self.proxy.get_capteur_distance()
		print("StrategieArretMur", self.capteur, 4*self.proxy.rayon, self.proxy.distance_parcourue, self.dist)
		if (self.proxy.distance_parcourue >= self.dist) or (self.capteur < self.dist_arret):
			self.proxy.reset()
			self.proxy.set_vitesse(0, 0)
			return True
		return False


class StrategieSeq():
	def __init__(self, liste, proxy):
		"""constructeur de la stratégie séquentielle

		Args:
			liste (_type_): liste de stratégies
		"""
		self.liste = liste
		self.indlist = 0
		self.proxy = proxy
		
	def update(self):
		"""mise à jour de la stratégie
		"""
		self.liste[self.indlist].update()
		if self.liste[self.indlist].stop():
			self.indlist += 1
			
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		if self.indlist >= len(self.liste):
			self.indlist = 0
			return True
		return False


class StrategieSuivreBalise():
	def __init__(self, data, proxy):
		self.data = data
		self.proxy = proxy
		self.stangle1 = StrategieAngle(45, 45, self.proxy)
		self.stangle2 = StrategieAngle(-45, -45, self.proxy)

	def update(self):
		if self.stop():
			return

		if (detect(self.data) <= -5 or detect(self.data) >= 5): # si la balise se situe plus de ±5% du centre
			if detect(self.data) <= 0:
				self.stangle1.update()
				if self.stangle1.stop():
					StrategieAvance(5, 45, self.proxy).update()
			else:
				self.stangle2.update()		
				if self.stangle2.stop():
					StrategieAvance(5, 45, self.proxy).update()	
		else:
			StrategieAvance(15, 45, self.proxy).update()

	def stop(self):
		try:
			detect(self.data)
		except BaliseException as e:
			return True
		return False
