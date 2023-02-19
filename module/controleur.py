dt = 0.01 # pas de temps

class FakeIA():
	def __init__(self, env, robot):
		self.robot = robot
		self.env = env

	def update(self):
		while (self.robot.capteur(self.env, 5) < 1.1*self.robot.rayon):
			self.robot.set_vitesse(-self.robot.vag, self.robot.vad) 
