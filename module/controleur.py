import numpy as np
from .toolbox import distance
import cv2
import time
from .camera import detect, BaliseException

class Strategie_dessine1():
	def __init__(self, distance, vitesse, proxy):
		"""constructeur de la stratégie pour avancer d'une distance voulu

		Args:
			distance (float): distance
			vitesse (int): vitesse des roues ( degré par seconde )
			robot (Robot): robot
		"""
		self.distance = distance
		self.vitesse = vitesse
		self.proxy = proxy
		self.proxy.dessine(True)
		
	def update(self):
		"""itération de la stratégie
		"""
		self.proxy.set_vitesse(self.vitesse, self.vitesse)
			
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		if (self.proxy.distance_parcourue >= self.distance):
			self.proxy.set_vitesse(0, 0)
			self.proxy.reset()
			return True
		return False
		
		
class Strategie_dessine0():
	def __init__(self, proxy):
		"""constructeur de la stratégie séquentielle

		Args:
			liste (_type_): liste de stratégies
		"""
		self.proxy = proxy
		self.stavance_long = Strategie_dessine1(90,720,proxy)
		self.stavance_court = Strategie_dessine1(30,720,proxy)
		self.stangle = StrategieAngle(90, 10, proxy)
		self.liste = [self.stavance_long, self.stangle, self.stavance_court, self.stangle, self.stavance_long, self.stangle, self.stavance_court]
		self.indlist = 0
		
	def update(self):
		"""itération de la stratégie
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
			
class Strategie_dessine01():
	def __init__(self, proxy):
		"""constructeur de la stratégie séquentielle

		Args:
			liste (_type_): liste de stratégies
		"""
		self.proxy = proxy
		self.st1 = Strategie_dessine1(90,720, proxy)
		self.st0 = Strategie_dessine0(proxy)
		self.stavance = StrategieAvance(60,720, proxy)
		self.stangle = StrategieAngle(90, 10, proxy)
		self.liste = [self.st0, self.stavance, self.stangle, self.st1]
		self.indlist = 0
		
	def update(self):
		"""itération de la stratégie
		"""

		self.liste[self.indlist].update()
		if self.liste[self.indlist].stop():
			self.indlist += 1
			if (self.indlist == 1 or self.indlist == 2):
				self.liste[self.indlist].proxy.dessine(False)
			else :
				self.liste[self.indlist].proxy.dessine(True)
			
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		if self.indlist >= len(self.liste):
			self.indlist = 0
			return True
		return False

class StrategieAvance():
	def __init__(self, distance, vitesse, proxy):
		"""constructeur de la stratégie pour avancer d'une distance voulu

		Args:
			distance (float): distance
			vitesse (int): vitesse des roues ( degré par seconde )
			robot (Robot): robot
		"""
		self.distance = distance
		self.vitesse = vitesse
		self.proxy = proxy
		
	def update(self):
		"""itération de la stratégie
		"""
		self.proxy.set_vitesse(self.vitesse, self.vitesse)
			
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
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

	def update(self):
		"""itération de la stratégie
		"""
		self.proxy.tourner(self.dps * (time.time()-self.proxy.last_update))

	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		print("angle :", self.proxy.angle_parcouru)
		if np.abs(self.proxy.angle_parcouru) >= np.abs(self.angle):
			self.proxy.set_vitesse(0, 0)
			self.proxy.reset()
			return True
		return False


class StrategieArretMur():
	def __init__(self, proxy, env, vitesse):
		"""constructeur de la stratégie pour s'arrêter à un mur

		Args:
			robot (Robot): robot
			env (Environnement): environnement
			vitesse (int): vitesse des roues ( degré par seconde )
		"""
		self.proxy = proxy
		self.env = env
		self.stavance = StrategieAvance(self.env.width*2, vitesse, self.proxy)
	
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		return (self.proxy.get_distance() < 2*self.proxy.rayon)

	def update(self):
		"""itération de la stratégie
		"""
		self.stavance.update()


class StrategieSeq():
	def __init__(self, liste):
		"""constructeur de la stratégie séquentielle

		Args:
			liste (_type_): liste de stratégies
		"""
		self.liste = liste
		self.indlist = 0
		self.cpt = 0
		
	def update(self):
		"""itération de la stratégie
		"""

		self.liste[self.indlist].update()
		if self.liste[self.indlist].stop():
			self.cpt = self.cpt + 1
			if (self.liste[self.indlist].proxy.trace_bool and self.cpt ==2):
				self.liste[self.indlist].proxy.dessine(False)
				self.cpt = 0
			elif (not(self.liste[self.indlist].proxy.trace_bool) and self.cpt ==2):
				self.liste[self.indlist].proxy.dessine(True)
				self.cpt = 0
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
