import time
from module_projet import Objet, Robot, Environnement
import module_outils as mo

class CollisionException(BaseException):
	def __init__(self, message):
		self.message = message

class Simulation:
	def __init__(self,env,robot, objets):
		"""Constructeur de simulation
		Args:
			env (Environnement): environnement dans la simulation
			robot (Robot): robot dans la simulation
		"""
		self.environnement=env
		self.robot=robot
		self.objets=objets

	def afficher_env(self):
		"""affichage de l'environnement de la simulation
		"""
		for _ in range(self.environnement.width+2):
			print('X', end=' ')
		print()
		for i in range(self.environnement.height):
			print('X', end=' ')
			for j in range(self.environnement.width):
				print(self.environnement.grid[i][j], end=' ')
			print('X')
		for _ in range(self.environnement.width+2):
			print('X', end=' ')	
		print()
		print()

	def update(self):
		"""fait une itération de la simulation

		Raises:
			CollisionException: collision avec les limites de l'environnement
			CollisionException: collision entre robot et un objet
		"""
		self.environnement.avancer_robot_env(self.robot,1)
		if (self.robot.rayon+self.robot.x > self.environnement.width*self.environnement.scale) or (self.robot.x-self.robot.x < 0) or (self.robot.y+self.robot.y > self.environnement.height*self.environnement.scale) or (self.robot.y-self.robot.y < 0):
			raise CollisionException("Collision avec les limites de l'environnement")
			return
		for objet in self.objets:
			if self.environnement.collision_robot_objet(self.robot, objet)==True:
				raise CollisionException("Collision entre robot et un objet")

	def run(self):
		"""mise à jour de l'environnement
		"""
		while True:
			try:
				self.update()
			except CollisionException as e:
				print(e)
				break
			self.afficher_env()
			time.sleep(1)


# Création d'un environnement et d'un robot
environnement = Environnement(20, 20, 1)
robot = Robot(9.9, 5.7, 0, 1, 1.6)

# Création d'une simulation et ajout du robot et des objets dans l'environnement et affichage de l'environnement
environnement.placer_robot_env(robot)
liste_objets = environnement.generer_obstacles(30)
s = Simulation(environnement, robot, liste_objets)
s.afficher_env()

# Mise à jour de la simulation
s.run()

# On fait reculer le robot
for _ in range (2):
	s.environnement.avancer_robot_env(s.robot,-1)
	s.afficher_env()
	time.sleep(1)

s.robot.tourner(225)
s.run()
