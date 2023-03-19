from module.constante import dt
import numpy as np
from module.toolbox import distance

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
		self.robot.tourner(self.dps * dt)
		delta_angle = (self.robot.vitAngD - self.robot.vitAngG) * self.robot.rayon/self.robot.distroue * dt * 180/np.pi
		self.angleapplique += delta_angle

	def stop(self):
		print("angles :",self.angleapplique, self.angle)
		if np.abs(self.angleapplique) >= self.angle :
			self.robot.set_vitesse(0, 0)
			self.angleapplique = 0
			return True
		else:
			return False
