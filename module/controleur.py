dt = 0.01 # pas de temps

class FakeIA():
	def __init__(self, env, robot, objets):
		self.env = env
		self.robot = robot
		self.objets = objets

	def update(self):
		if(self.robot.capteur(self.env, 5) < 2*self.robot.rayon):
			self.robot.set_vad(-self.robot.vag) 
			self.env.avancer_robot(self.robot, dt)
			self.robot.set_vad(self.robot.vag)
		else:
			self.env.avancer_robot(self.robot, dt)
