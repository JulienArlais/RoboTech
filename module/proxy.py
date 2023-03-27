import time
import numpy as np

dt = 0.01

class Robot_Virtuel:

	def __init__(self, robot, env):
		"""constructeur de simualtion_proxy,simule les mouvements du robot dans l'environnement virtuel dans lequel il évolue. 

		Args:
			robot: Robot
			env: Environnement
		"""
		self.robot = robot
		self.env = env
		self.dist_roue = self.robot.dist_roue
		self.dist_parcourue = 0
		self.delta_angle = 0
		self.rayon = self.robot.rayon
	
	def reset_position(self):
		""" 
		réinitialise la position du robot
		"""
		self.update()
		self.robot.last_update=time.time()

	def set_vitesse(self, dps1, dps2):
		"""fait avancer le robot à la vitesse donnée
		Args:
			vitesse (radian par seconde): vitesse angulaire 
		"""
		self.update()
		self.robot.set_vitesse(dps1, dps2)
	
	def distance_parcourue(self):
		self.dist_parcourue += self.robot.distance_parcourue()
	
	def get_distanceParcourue(self) :
		"""
		renvoie la distance parcourue par le robot depuis sa dernière réinitialisation

		"""
		self.distance_parcourue()
		return self.dist_parcourue
	
	def reset_distance(self) :
		"""
		renvoie la distance parcourue par le robot depuis sa dernière réinitialisation

		"""
		self.update()
		self.dist_parcourue = 0
	
	def diff_angle(self):
		self.update()
		ang_g, ang_d = self.get_vitAng()
		self.delta_angle += (ang_d - ang_g) * self.rayon/self.dist_roue * dt * 180/np.pi
		
	def reset_angle(self):
		self.update()
		self.delta_angle = 0

	def get_distance(self):
		"""
		renvoyer la distance entre le robot et un objet de l'environnement virtuel
		
		"""
		self.update()
		return self.robot.get_distance(self.env)

	def get_vitAng(self):
		"""
		renvoie la vitesse angulaire du robot
		"""
		self.update()
		return self.robot.get_vitAng()

	def tourner(self, dps):
		"""
		tourne le robot à un certain degré par seconde
		Args:
			dps: degré par seconde
		"""
		self.update()
		self.robot.tourner(dps)

	def update(self):
		"""
		met à jour le robot 

		"""
		self.last_update = time.time()


class Robot_Reel:

	def __init__(self, robot_reel):
		self.robot_reel = robot_reel
		self.last_vitAng = (0, 0)
		self.last_update = 0
		self.dist_roue = self.robot_reel.WHEEL_BASE_WIDTH

	def reset_position(self):
		self.robot_reel.offset_motor_encode(self.robot_reel.MOTOR_LEFT,self.robot_reel.read_encoders()[0])
		self.robot_reel.offset_motor_encode(self.robot_reel.MOTOR_RIGHT,self.robot_reel.read_encoders()[1]) # pourquoi 1? et pas 0

	def set_vitesse(self, dps1, dps2):
		self.robot_reel.set_motor_dps(self.robot_reel.MOTOR_LEFT, dps1)
		self.robot_reel.set_motor_dps(self.robot_reel.MOTOR_RIGHT, dps2)
		
	def distance_parcourue(self) :
		return sum([i/360 * self.robot_reel.WHEEL_CIRCUMFERENCE for i in self.robot_reel.get_motor_position()])/2

	def get_distance(self):
		return self.robot_reel.get_distance()

	def get_vitAng(self):
		vitAng = self.robot_reel.get_motor_position()
		now = time.time()
		delta = np.subtract(vitAng, self.last_vitAng)
		duree = now - self.last_update
		return tuple(delta/duree)

	def tourner(self, dps):
		delta = (self.robot_reel.WHEEL_BASE_WIDTH * np.abs(np.radians(dps)))/(self.robot_reel.WHEEL_DIAMETER/2)
		if dps > 0:
			self.robot_reel.set_motor_dps(self.robot_reel.MOTOR_LEFT, self.get_vitAng()[0]+delta)
		else:
			self.robot_reel.set_motor_dps(self.robot_reel.MOTOR_RIGHT, self.get_vitAng()[1]+delta)

	def update(self):
		self.last_vitAng = self.robot_reel.get_motor_position()
		self.last_update = time.time()
