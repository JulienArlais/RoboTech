from .constante import dt
import numpy as np
from .toolbox import distance

class FakeIA():
	def __init__(self, env, robot, objets):
		self.robot = robot
		self.env = env
		self.obj = objets
	
	def stop(self):
		return False

	def update(self):
		if (self.robot.capteur(self.env, 50, self.obj) < 2*self.robot.rayon):
			self.robot.tourner(1)
		else:
			#self.robot.set_vitesse((3*self.robot.vitAngD/4+self.robot.vitAngG/4), (3*self.robot.vitAngG/4+self.robot.vitAngD/4))
			self.robot.set_vitesse(max(self.robot.vitAngD,self.robot.vitAngD), max(self.robot.vitAngD,self.robot.vitAngD))

class StrategieAngle():
	def __init__(self, angle, dps, robot):
		"""constructeur de la stratégie Angle

		Args:
			angle: l'ange qu'on souohaite touner
			dps: indique au robot de combien de degré tourner par seconde pour obtenir l'angle souhaité
			robot: le robot à qui on veut appliquer la stratégie
		"""
		self.angle = angle
		self.dps = dps
		self.robot = robot
		self.angleapplique = 0

	def update(self):
		"""
		fonction de mise à jour de la stratégie StrategieAngle
		"""

		if self.stop():
			return
		self.robot.tourner(self.dps)
		self.angleapplique += (self.robot.vitAngD - self.robot.vitAngG) * self.robot.rayon/self.robot.distroue

	def stop(self):
		print("angles :",self.angleapplique, self.angle)
		if np.abs(self.angleapplique) >= self.angle :
			self.robot.set_vitesse(0, 0)
			self.angleapplique = 0
			return True
		else:
			return False


class StrategieAvance() :
	def __init__(self, distance, vitesse, robot):
		"""constructeur de la stratégie Avance

		Args:
			distance: distance qu'on souhaite parcourir
			vitesse: pour mettre la vitesse des roues
			robot: le robot à qui on veut appliquer la stratégie
		"""
		self.distance = distance
		self.vitesse = vitesse
		self.robot = robot
		self.parcouru = 0
		
	def update(self) :
		if self.stop():
			return
		self.robot.set_vitesse(self.vitesse, self.vitesse)
		self.parcouru += distance(self.robot.x - self.robot.getXstep(dt), self.robot.y - self.robot.getYstep(dt), self.robot.x, self.robot.y)
			
	def stop(self) :
		if (self.parcouru >= self.distance):
			self.robot.set_vitesse(0, 0)
			self.parcouru = 0
			return True
		return False

class StrategieForme():
	def __init__(self, liste):
		self.liste = liste
		self.indlist = 0
		
	def update(self):
		if self.liste[self.indlist].stop():
			self.indlist += 1
			if self.stop():
				return
		self.liste[self.indlist].update()
		
	def stop(self):
		if self.indlist >= len(self.liste):
			return True
		else:
			return False

	def run(self):
		while not self.stop():
			self.update()

