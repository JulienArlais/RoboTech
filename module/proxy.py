import time
import numpy as np

class simulation_proxy:

	def __init__(self, robot, env):
		self.robot = robot
		self.env = env
		
	def reset_position(self):
        	self.robot.last_update = time.time()

	def avancer(self, vitesse):
		self.robot.set_vitesse(vitesse, vitesse)
		
	def distance_parcourue(self) :
		return self.robot.distance_parcourue()

	def get_distance(self):
		return self.robot.get_distance(self.env)

	def get_vitAng(self):
		self.robot.get_vitAng()

	def stop(self):
		self.robot.set_vitesse(0, 0)

	def tourner(self, dps):
		self.robot.tourner(dps)

	def update(self):
		self.robot.update()

class realite_proxy:

	def __init__(self, robot):
		self.robot = robot
		self.last_vitAng = (0, 0)
		self.last_update = 0

	def reset_position(self):
        	self.robot.offset_motor_encode(self.robot.MOTOR_LEFT,self.robot.read_encoders()[0])
        	self.robot.offset_motor_encode(self.robot.MOTOR_RIGHT,self.robot.read_encoders()[1])

	def avancer(self, dps):
		self.robot.set_motor_dps(self.robot.MOTOR_LEFT+self.robot.MOTOR_RIGHT, dps)
		
	def distance_parcourue(self) :
		return self.robot.get_motor_position()*WHEEL_DIAMETER*np.pi/360

	def get_distance(self):
		return self.robot.get_distance()

	def get_vitAng(self):
		vitAng = self.robot.get_motor_position()
		now = time.time()
		delta = vitAng - self.last_vitAng
		duree = now - self.last_update
		return delta/duree

	def stop(self):
		self.robot.stop()

	def tourner(self, dps):
		delta = (self.robot.WHEEL_BASE_WIDTH * np.abs(np.radians(dps)))/(self.robot.WHEEL_DIAMETER/2)
		if dps > 0:
			self.robot.set_motor_dps(self.robot.MOTOR_LEFT, self.get_vitAng()[0]+delta)
		else:
			self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, self.get_vitAng()[1]+delta)

	def update(self):
		self.last_vitAng = self.robot.get_motor_position()
		self.last_update = time.time()
