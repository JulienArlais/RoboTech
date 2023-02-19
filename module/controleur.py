dt = 0.01 # pas de temps

class FakeIA():
	def __init__(self, env, robot):
		self.robot = robot
		self.env = env

	def update(self):
		if (self.robot.capteur(self.env, 5) < 2*self.robot.rayon):
			self.robot.tourner(10)
		else:
			self.robot.set_vitesse(self.robot.vad, self.robot.vad)
