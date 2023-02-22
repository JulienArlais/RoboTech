from .constante import dt
import numpy as np
from .toolbox import distance

class StrategieAngle():
	def __init__(self, angle, dps, robot):
		self.angle = angle
		self.dps = dps
		self.robot = robot
		self.angleapplique = 0

	def update(self):
		if self.stop():
			return
		self.robot.tourner(self.dps)
		self.angleapplique += (self.robot.vitAngD - self.robot.vitAngG) * self.robot.rayon/self.robot.distroue

	def stop(self):
		if np.abs(self.angleapplique) >= self.angle :
			self.robot.set_vitesse(0, 0)
			self.angleapplique = 0
			return True
		else:
			return False


class StrategieAvance() :
	def __init__(self, distance, vitesse, robot):
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


class StrategieCarre():
	def __init__(self, stratavancer, starttourner):
		self.list = [stratavancer, starttourner, stratavancer, starttourner, stratavancer, starttourner, stratavancer, starttourner]
		self.indlist = 0

	def update(self):
		if self.list[self.indlist%2].stop():
			self.indlist += 1
			if self.stop():
				return
		self.list[self.indlist%2].update()

	def stop(self):
		if self.indlist >= 7:
			return True
		else:
			return False

	def run(self):
		while not self.stop():
			self.update()
