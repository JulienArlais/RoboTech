import robot_reel

class simulation_proxy:

	def __init__(self, robot, env):
		self.robot = robot
		self.env = env

	def avancer(self, vitesse):
		self.robot.set_vitesse(vitesse, vitesse)
		
	def distance_parcourue(self) :
		return self.robot.distance_parcourue()

	def get_distance(self):
		return self.robot.get_distance(self.env)

	def stop(self):
		self.robot.set_vitesse(0, 0)

	def tourner(self, dps):
		self.robot.tourner(dps)

class realite_proxy:

	def __init__(self, robot):
		self.robot = robot

	def avancer(self, vitesse):
		self.robot.set_motor_dps(self, MOTOR_LEFT+MOTOR_RIGHT, vitesse)
		
	def distance_parcourue(self) :
		return self.robot.get_motor_position()

	def get_distance(self):
		return self.robot.get_distance()

	def stop(self):
		self.robot.stop()

	#def tourner(self):