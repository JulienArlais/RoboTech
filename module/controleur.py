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

