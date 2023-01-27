import getch
import math
import numpy as np

class Robot:
	def __init__(self, x, y, direction, vitesse, rayon):
		# x et y des coordonnées en mètre, direction un angle par rapport à l'abscisse en float et la vitesse max du robot en m/s
		# on suppose que le robot est un cercle, pour faciliter les collisions
		self.x = x
		self.y = y
		self.direction = direction
		self.vitesse = vitesse
		self.rayon = rayon
		print("Le robot de rayon",self.rayon,"est aux coordonnées (",self.x,",",self.y,"), a une direction d'angle",self.direction,"degrés et une vitesse maximale de",self.vitesse)

class Environnement:
	def __init__(self, large, long, echelle): 
        # l'échelle donne la longueur des côtés d'une case de l'environnement
		self.largeur = large
		self.longueur = long
		self.grid = [[' ' for _ in range(large+2)] for _ in range(long+2)]
		self.echelle = echelle
		for i in range(long+1):
				for j in range(large+1):
					#self.grid[i][j] = '.'
					if i == 0 or i == long-1:
						self.grid[i][j] = chr(64+j)
					elif j == 0 or j == large-1:
						self.grid[i][j] = chr(64+i)
					else:
						self.grid[i][j] = " "

class Simulation:
	def tourner_robot(robot,angle):
		# angle est la valeur d'angle que l'on va ajouter à notre angle. Elle peut être positive ou négative
		robot.direction = robot.direction + angle
		while (robot.direction < 0):
			robot.direction = robot.direction + 360
		robot.direction = robot.direction % 360
		print("La nouvelle direction du robot est de",robot.direction,"degrés par rapport à l'axe des abscisses")
		
	def avancer_robot(environnement,robot):
		#fait avancer le robot pendant 1 seconde
		Simulation.retirer_robot_env(environnement,robot)
		robot.x = robot.x + robot.vitesse*math.cos(robot.direction)
		robot.y = robot.y + robot.vitesse*math.sin(robot.direction)
		Simulation.placer_robot_env(environnement,robot)
		print("Le robot a avancé et s'est déplacé en (",robot.x,",",robot.y,")")
	
	def reculer_robot(environnement,robot):
		#fait avancer le robot pendant 1 seconde
		robot.x = robot.x - robot.vitesse*math.cos(robot.direction)
		robot.y = robot.y - robot.vitesse*math.sin(robot.direction)
		Simulation.placer_robot_env(environnement,robot)
		print("Le robot a reculé et s'est déplacé en (",robot.x,",",robot.y,")")
	
	def afficher_env(env):
		for i in range(env.longueur):
			for j in range(env.largeur):
				print(env.grid[i][j], end=' ')
			print()
	
	def retirer_robot_env(env,robot):
		x = int(robot.x / env.echelle)
		y = int(robot.y / env.echelle)
		if (env.grid[y][x] == "R"):
			env.grid[y][x] = "."
		elif (env.grid[y][x] == "#"):
			env.grid[y][x] = "@"
	
	def placer_robot_env(env, robot):
		x = int(robot.x / env.echelle)
		y = int(robot.y / env.echelle)
		if (env.grid[y][x] == " " or env.grid[y][x] == "."):
			env.grid[y][x] = "R"
		elif (env.grid[y][x] == "@"):
			env.grid[y][x] = "#"
		#print("Le robot a été placé à ses coordonnées dans l'environnement")

ech = float(input("Entrez l'échelle de l'environnement. Chaque case aura une largeur et longueur en mètre égale à cette valeur: "))
while (ech < 1):
	ech = float(input("L'échelle doit au moins être de 1 mètre: "))
large = int(input("Entrez la largeur (abscisse) de l'environnement: "))
while (large < 0):
	large = int(input("La largeur doit être une valeur positive. Entrez à nouveau: "))
long = int(input("Entrez la longueur (abscisse) de l'environnement: "))
while (long < 0):
	long = int(input("La longueur doit être une valeur positive. Entrez à nouveau: "))

environnement = Environnement(large,long,ech)
print("L'environnement fait",environnement.largeur,"case de large et",environnement.longueur,"de long, et chaque case fait",environnement.echelle,"*",environnement.echelle,"mètres de côté\n")

x = float(input("Entrez l'abscisse initiale du robot: "))
y = float(input("Entrez l'ordonnée initiale du robot: "))
direction = float(input("Entrez l'angle du robot par rapport à l'abscisse: "))
vitesse = float(input("Entrez la vitesse maximale du robot: "))
rayon = float(input("Entrez le rayon du robot: "))
robot = Robot(x,y,direction,vitesse,rayon)

Simulation.placer_robot_env(environnement,robot)
print("Le robot a été placé à ses coordonnées dans l'environnement")
Simulation.afficher_env(environnement)
for _ in range(3):
	Simulation.avancer_robot(environnement,robot)
Simulation.afficher_env(environnement)
