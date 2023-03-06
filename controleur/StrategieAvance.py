from module.constante import dt
import numpy as np
from module.toolbox import distance

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

