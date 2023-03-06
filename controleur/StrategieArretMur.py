from module.constante import dt
import numpy as np
from module.toolbox import distance
from .StrategieAvance import StrategieAvance

class StrategieArretMur():
	def __init__(self, robot, env, objets, vitesse):
		self.robot = robot
		self.env = env
		self.obj = objets
		self.stavance = StrategieAvance(self.env.width*2, vitesse, self.robot)
		print(self.robot.x, self.robot.y)
	
	def stop(self):
		print("stop robot ?",self.robot.x, self.robot.y)
		return (self.robot.capteur(self.env, 10000, self.obj) < 2*self.robot.rayon)
		#return False

	def update(self):
		if self.stop():
			return
		self.stavance.update()
		
	def run(self): # inutile ?
		while not self.stop():
			self.update()
