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
		print(self.angleapplique, self.angle)
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
