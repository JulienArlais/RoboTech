import time
from module_projet import Objet, Robot, Environnement
import module_outils as mo

class Simulation:
	def __init__(self,env,robot):
		"""Constructeur de simulation
		Args:
			env (Environnement): environnement dans la simulation
			robot (Robot): robot dans la simulation
		"""
		self.environnement=env
		self.robot=robot

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

	def run(self, liste):
		"""mise à jour de l'environnement
		Args:
			liste (List[Objet]): liste des objets de la simulation
		"""
		while True:
			self.environnement.avancer_robot_env(self.robot,1)
			if self.robot.x > self.environnement.width*self.environnement.scale or self.robot.x < 0 or self.robot.y > self.environnement.height*self.environnement.scale or self.robot.y < 0:
				print("Collision avec les limites de l'environnement")
				break
			self.afficher_env()
			for objet in liste:
				if self.environnement.collision_robot_objet(self.robot, objet)==True:
					print("Collision entre robot et un objet")
					return
			time.sleep(1)


# Création d'un environnement, d'un robot et d'une simulation
environnement = Environnement(20, 20, 1)
robot = Robot(9.9, 5.7, 0, 1, 1.6)
s = Simulation(environnement, robot)

# Ajout du robot et des objets dans l'environnement et affichage de l'environnement
environnement.placer_robot_env(robot)
liste_objets = environnement.generer_obstacles(30)
s.afficher_env()

# Mise à jour de la simulation
s.run(liste_objets)

# On fait reculer le robot
for _ in range (2):
	s.environnement.avancer_robot_env(s.robot,-1)
	s.afficher_env()
	time.sleep(1)

s.robot.tourner(225)
s.run(liste_objets)
