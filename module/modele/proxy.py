import time
import numpy as np

class Proxy_Virtuel:

	def __init__(self, robot, env):
		"""constructeur du robot virtuel 

		Args:
			robot (Robot): robot
			env (Environnement): environnement
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

	def set_vitesse(self, dps1, dps2):
		"""fait avancer le robot à la vitesse donnée

		Args:
			dps1 (int): degré par seconde voulu
			dps2 (int): degré par seconde voulu
		"""
		self.robot.vitAngG = dps1/20
		self.robot.vitAngD = dps2/20
		self.update()
	
	def update_distance(self):
		"""mise à jour de la distance parcourue
		"""
		now = time.time()
		if self.last_update == 0:
			self.last_update = now
		else:
			ang_g, ang_d = self.get_vitAng()
			delta = self.robot.rayon_roue*(now-self.last_update)*(ang_g + ang_d)/2
			self.distance_parcourue += delta
	
	def reset_distance(self) :
		"""réinitialise la distance parcourue
		"""
		self.distance_parcourue = 0
	
	def update_angle(self):
		"""mise à jour de l'angle parcouru
		"""
		now = time.time()
		if self.last_update == 0:
			self.last_update = now
		else:
			ang1, ang2 = self.get_vitAng()
			self.angle_parcouru += (now-self.last_update)*(ang1-ang2)*self.rayon/self.dist_roue* 180/np.pi
		
	def reset_angle(self):
		"""réinitialise l'angle parcouru
		"""
		self.angle_parcouru = 0
		self.angle_depart = self.robot.theta

	def get_capteur_distance(self):
		"""donne la distance par rapport au premier obstacle devant le robot

		Returns:
			float: distance par rapport au premier obstacle
		"""
		return self.robot.get_distance(self.env)

	def get_vitAng(self):
		"""donne les vitesses angulaire dans un couple

		Returns:
			tupe[int, int]: couple représentant les vitesses angulaire
		"""
		return self.robot.get_vitAng()

	def tourner(self, dps):
		"""tourne le robot à un certain degré par seconde

		Args:
			dps (int): degré par seconde
		"""
		delta = (self.dist_roue * np.abs(dps))/self.rayon_roue/2
		if dps > 0:
			self.set_vitesse(delta, -delta)
		else:
			self.set_vitesse(-delta, delta)
		self.update()

	def reset(self):
		"""réinitialise l'angle et la distance parcourue
		"""
		self.reset_angle()
		self.reset_distance()

	def update(self):
		"""mise à jour du robot
		"""
		now = time.time()
		self.update_distance()
		self.update_angle()
		self.last_update = now

class Proxy_Reel:

	def __init__(self,robot):
		print("init")
		self.robot = robot
		self.dist_roue = self.robot.WHEEL_BASE_WIDTH
		self.rayon = self.robot.WHEEL_BASE_WIDTH/2
		self.rayon_roue = self.robot.WHEEL_DIAMETER/2
		self.circonf_roue = self.robot.WHEEL_CIRCUMFERENCE
		self.distance_parcourue = 0
		self.angle_parcouru = 0
		self.last_update = 0
		self.last_Ang = (0, 0)
		
		self.robot.offset_motor_encoder(self.robot._gpg.MOTOR_LEFT,self.robot.read_encoders()[0])
		self.robot.offset_motor_encoder(self.robot._gpg.MOTOR_RIGHT,self.robot.read_encoders()[1])

	def set_vitesse(self, dps1, dps2):
		print("set vitesse ",dps1," ",dps2)
		self.robot.set_motor_dps(self.robot._gpg.MOTOR_LEFT, dps1)
		self.robot.set_motor_dps(self.robot._gpg.MOTOR_RIGHT, dps2)
		
	def update_distance(self) :
		self.distance_parcourue = sum([i/360 * self.circonf_roue for i in self.robot.get_motor_position()])/2

	def reset_distance(self):
		self.distance_parcourue = 0

	def update_angle(self):
		ang1, ang2 = self.get_vitAng()
		now = time.time()
		self.angle_parcouru += (now-self.last_update)*(ang1-ang2)*self.rayon/self.dist_roue* 180/np.pi
		
	def reset_angle(self):
		self.robot.offset_motor_encoder(self.robot._gpg.MOTOR_LEFT,self.robot.read_encoders()[0])
		self.robot.offset_motor_encoder(self.robot._gpg.MOTOR_RIGHT,self.robot.read_encoders()[1])
		ang = self.robot.get_motor_position()
		print("reset_angle", ang[0], ang[1])
		self.angle_parcouru = 0

	def get_capteur_distance(self):
		return self.robot.get_distance()

	def get_vitAng(self):
		now = time.time()
		Ang = self.robot.get_motor_position()
		a1, a2 = np.subtract(Ang, self.last_Ang)
		a1 = a1*(now-self.last_update)
		a2 = a2*(now-self.last_update)
		return (a1,a2)

	def tourner(self, rps):
		print("tourner ",rps)
		delta = (self.dist_roue * np.abs(rps))/self.rayon_roue/2
		if rps > 0:
			self.set_vitesse(delta, -delta)
		else:
			self.set_vitesse(-delta, delta)
			
	def reset(self):
		self.reset_angle()
		self.reset_distance()

	def update(self):
		now = time.time()
		self.update_distance()
		self.update_angle()
		self.last_Ang = self.robot.get_motor_position()
		self.last_update = now
