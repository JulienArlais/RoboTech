dt = 0.01# pas de temps

class FakeIA():
	def __init__(self, env, robot):
		self.robot = robot
		self.env = env

	def update(self):
		if (self.robot.capteur(self.env, 50) < 2*self.robot.rayon):
			self.robot.tourner(1)
		else:
			self.robot.set_vitesse(self.robot.vitAngD, self.robot.vitAngD)
