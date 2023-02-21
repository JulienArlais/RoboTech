from .constante import dt

class FakeIA():
	def __init__(self, env, robot, objets):
		self.robot = robot
		self.env = env
		self.obj = objets

	def update(self):
		if (self.robot.capteur(self.env, 50, self.obj) < 2*self.robot.rayon):
			self.robot.tourner(1)
		else:
			#self.robot.set_vitesse((3*self.robot.vitAngD/4+self.robot.vitAngG/4), (3*self.robot.vitAngG/4+self.robot.vitAngD/4))
			self.robot.set_vitesse(max(self.robot.vitAngD,self.robot.vitAngD), max(self.robot.vitAngD,self.robot.vitAngD))
			
class Avancer_strategie() :
	def __init__(self, robot, distance):#, vitesse) :
		self.robot = robot
		self.distance = distance
		#self.vitesse = vitesse
		parcouru = 0
	
	#def start(self) :
	#	self.robot.vitesse = vitesse
		
	def update(self) :
		if self.stop():
			return
		self.robot.set_vitesse(max(self.robot.vitAngD,self.robot.vitAngD), max(self.robot.vitAngD,self.robot.vitAngD))
		parcouru += 10 # pas le pb dans l'immédiat
			
	def stop(self) :
		if (parcouru == distance):
			return True
		return False
