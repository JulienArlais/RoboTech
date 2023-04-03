import time
import numpy as np
from .element_simulation import Led 

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
		self.rayon = self.robot.rayon
		self.distance_parcourue = 0
		self.angle_parcouru = 0
		self.led1=Led(1,"red")
		self.led2=Led(2,"blue")
		self.abaisser=self.robot.abaisser

	def set_vitesse(self, dps1, dps2):
		"""fait avancer le robot à la vitesse donnée
		Args:
			vitesse (radian par seconde): vitesse angulaire 
		"""
		self.update()
		self.robot.set_vitesse(dps1, dps2)
	
	def dist_parcourue(self):
		self.distance_parcourue += self.robot.distance_parcourue()
	
	def reset_distance(self) :
		"""
		renvoie la distance parcourue par le robot depuis sa dernière réinitialisation
		"""
		self.distance_parcourue = 0
	
	def ang_parcouru(self):
		ang_g, ang_d = self.get_vitAng()
		self.angle_parcouru += (ang_d - ang_g) * self.rayon/self.dist_roue * dt * 180/np.pi
		
	def reset_angle(self):
		self.angle_parcouru = 0

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

	def tourner(self, dps):
		"""
		tourne le robot à un certain degré par seconde
		Args:
			dps: degré par seconde
		"""
		self.robot.tourner(dps)

	def update(self):
		"""
		met à jour le robot 
		"""
		self.last_update = time.time()

	def set_led(self, ID_LED, statut):
		self.robot.set_led(ID_LED,statut)

	def dessine(self,Bool):
		return self.robot.dessine(Bool)

	def getSignal(self,env):
		return self.robot.getSignal(env)




class Robot_Reel:

	def __init__(self, robot_reel):
		self.robot_reel = robot_reel
		self.dist_roue = self.robot_reel.WHEEL_BASE_WIDTH
		self.rayon = self.robot_reel.WHEEL_BASE_WIDTH/2 # techniquement la distance entre les deux roues c'est aussi le diamètre du robot non ?
		self.distance_parcourue = 0
		self.angle_parcouru = 0
		self.last_vitAng = (0, 0)
		self.last_update = 0

	def set_vitesse(self, dps1, dps2):
		self.robot_reel.set_motor_dps(self.robot_reel.MOTOR_LEFT, dps1)
		self.robot_reel.set_motor_dps(self.robot_reel.MOTOR_RIGHT, dps2)
		
	def dist_parcourue(self) :
		self.distance_parcourue += sum([i/360 * self.rayon for i in self.robot_reel.get_motor_position()])/2

	def reset_distance(self):
		self.robot_reel.offset_motor_encode(self.robot_reel.MOTOR_LEFT,self.robot_reel.read_encoders()[0])
		self.robot_reel.offset_motor_encode(self.robot_reel.MOTOR_RIGHT,self.robot_reel.read_encoders()[1])
		self.distance_parcourue = 0

	def ang_parcouru(self):
		ang_g, ang_d = self.get_vitAng()
		self.angle_parcouru += (ang_d - ang_g) * self.rayon/self.dist_roue * dt * 180/np.pi
		
	def reset_angle(self):
		self.robot_reel.offset_motor_encode(self.robot_reel.MOTOR_LEFT,self.robot_reel.read_encoders()[0])
		self.robot_reel.offset_motor_encode(self.robot_reel.MOTOR_RIGHT,self.robot_reel.read_encoders()[1])
		self.angle_parcouru = 0

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
