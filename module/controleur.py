from .constante import dt
import numpy as np
from .toolbox import distance

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
		if np.abs(self.angleapplique) >= self.angle :
			self.robot.set_vitesse(0, 0)
			self.angleapplique = 0
			return True
		else:
			return False


class StrategieArretMur():
	def __init__(self, robot, env, objets, vitesse):
		"""constructeur de la stratégie pour s'arrêter à un mur

		Args:
			robot (Robot): robot
			env (Environnement): environnement
			objets (Objet): objets
			vitesse (int): vitesse des roues ( degré par seconde )
		"""
		self.robot = robot
		self.env = env
		self.obj = objets
		self.stavance = StrategieAvance(self.env.width*2, vitesse, self.robot)
	
	def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		return (self.robot.capteur(self.env, 10000, self.obj) < 2*self.robot.rayon)

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