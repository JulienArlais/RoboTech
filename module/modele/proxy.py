import time
import numpy as np

class Proxy_Virtuel:

	def __init__(self, robot, env):
		"""constructeur de simualtion_proxy,simule les mouvements du robot dans l'environnement virtuel dans lequel il évolue. 

		Args:
			robot: Robot
			env: Environnement
		"""
		self.robot = robot
		self.env = env
		self.dist_roue = self.robot.dist_roue
		self.rayon = self.robot.rayon
		self.rayon_roue = self.robot.rayon_roue
		self.distance_parcourue = 0
		self.angle_parcouru = 0
		self.last_update = 0
		self.angle_depart = self.robot.theta

	def set_vitesse(self, rps1, rps2):
		"""fait avancer le robot à la vitesse donnée
		Args:
			vitesse (radian par seconde): vitesse angulaire 
		"""
		self.robot.vitAngG = rps1
		self.robot.vitAngD = rps2
		self.update()
	
	def update_distance(self):
		now = time.time()
		if self.last_update == 0:
			self.last_update = now
		else:
			ang_g, ang_d = self.get_vitAng()
			delta = self.robot.rayon_roue*(now-self.last_update)*(ang_g + ang_d)/2
			self.distance_parcourue += delta
	
	def reset_distance(self) :
		"""
		renvoie la distance parcourue par le robot depuis sa dernière réinitialisation

		"""
		self.distance_parcourue = 0
	
	def update_angle(self):
		now = time.time()
		if self.last_update == 0:
			self.last_update = now
		else:
			ang_g, ang_d = self.get_vitAng()
			self.angle_parcouru = self.robot.theta-self.angle_depart#(ang_d - ang_g) * self.rayon/self.dist_roue * (now-self.last_update)
		
	def reset_angle(self):
		self.angle_parcouru = 0
		self.angle_depart = self.robot.theta

	def get_distance(self):
		"""
		renvoyer la distance entre le robot et un objet de l'environnement virtuel
		
		"""
		return self.robot.get_distance(self.env)

	def get_vitAng(self):
		"""
		renvoie la vitesse angulaire du robot
		"""
		return self.robot.get_vitAng()

	def tourner(self, rps):
		"""
		tourne le robot à un certain degré par seconde
		Args:
			dps: degré par seconde
		"""
		delta = (self.dist_roue * np.abs(rps))/self.rayon_roue
		if rps > 0:
			self.set_vitesse(delta, 0)
		else:
			self.set_vitesse(0, delta)
		self.update()

	def reset(self):
		self.reset_angle()
		self.reset_distance()

	def blinker_on(self,id):
		return self.robot.blinker_on(id)
		
	def blinker_off(self,id):
		return self.robot.blinker_off(id)

	def update(self):
		"""
		met à jour le robot 

		"""
		now = time.time()
		self.update_distance()
		self.update_angle()
		self.last_update = now

class Proxy_Reel:

	def __init__(self, robot_reel):
		self.robot_reel = robot_reel
		self.dist_roue = self.robot_reel.WHEEL_BASE_WIDTH
		self.rayon = self.robot_reel.WHEEL_BASE_WIDTH/2 # techniquement la distance entre les deux roues c'est aussi le diamètre du robot non ?
		self.rayon_roue = self.robot_reel.WHEEL_DIAMETER/2
		self.distance_parcourue = 0
		self.angle_parcouru = 0
		self.last_Ang = (0, 0)

	def set_vitesse(self, dps1, dps2):
		self.robot_reel.set_motor_dps(self.robot_reel.MOTOR_LEFT, dps1)
		self.robot_reel.set_motor_dps(self.robot_reel.MOTOR_RIGHT, dps2)
		
	def update_distance(self) :
		self.distance_parcourue += sum([i/360 * self.rayon for i in self.robot_reel.get_motor_position()])/2

	def reset_distance(self):
		self.robot_reel.offset_motor_encode(self.robot_reel.MOTOR_LEFT,self.robot_reel.read_encoders()[0])
		self.robot_reel.offset_motor_encode(self.robot_reel.MOTOR_RIGHT,self.robot_reel.read_encoders()[1])
		self.distance_parcourue = 0

	def update_angle(self):
		ang_g, ang_d = self.get_vitAng()
		self.angle_parcouru += np.subtract([i/360 * self.rayon for i in self.robot_reel.get_motor_position()])/self.dist_roue* 180/np.pi
		
	def reset_angle(self):
		self.robot_reel.offset_motor_encode(self.robot_reel.MOTOR_LEFT,self.robot_reel.read_encoders()[0])
		self.robot_reel.offset_motor_encode(self.robot_reel.MOTOR_RIGHT,self.robot_reel.read_encoders()[1])
		self.angle_parcouru = 0

	def get_distance(self):
		return self.robot_reel.get_distance()

	def get_vitAng(self):
		Ang = self.robot_reel.get_motor_position()
		delta = np.subtract(Ang, self.last_Ang)
		return delta

	def tourner(self, rps):
		delta = (self.dist_roue * np.abs(rps))/self.rayon_roue
		if rps > 0:
			self.set_vitesse(delta, 0)
		else:
			self.set_vitesse(0, delta)
			
	def reset(self):
		self.reset_angle()
		self.reset_distance()

	def update(self):
		now = time.time()
		self.dist_parcourue()
		self.ang_parcouru()
		self.last_Ang = self.robot_reel.get_motor_position()
