import getch
import numpy as np


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def sub(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def rotate(self, angle):
        """Applique une rotation au vecteur d'un angle donnée en paramètre"""
        x = self.x * math.cos(angle) - self.y * math.sin(angle)
        y = self.x * math.sin(angle) + self.y * math.cos(angle)
        return Vector(x, y)

class Object:
    def __init__(self, height, speed):
        self.height = height
        self.speed = speed



class Robot:
	def __init__(self, x, y, theta, vitesse, rayon):
		#x et y des coordonnées en mètre, direction un angle par rapport à l'abscisse en float et la vitesse max du robot en m/s
		# on suppose que le robot est un cercle, pour faciliter les collisions
		self.x = x
		self.y = y
		self.theta = theta
		self.vitesse = vitesse
		self.rayon = rayon

	def avancer(self):
		""" fait avancer le robot pendant 1 seconde """
		self.x += self.vitesse*np.cos(robot.theta)
		self.y += self.vitesse*np.sin(robot.theta)
		

	def tourner(self, angle):
		# angle est la valeur d'angle que l'on va ajouter à notre angle. Elle peut être positive ou négative
		self.theta += angle
		while (self.theta < 0):
			self.theta = self.theta + 360
		self.theta = self.theta % 360
		#print("La nouvelle direction du robot est de", self.theta, "degrés par rapport à l'axe des abscisses")

	def reculer(self):
		""" fait reculer le robot pendant 1 seconde """
		self.x -= self.vitesse*np.cos(robot.theta)
		self.y -= self.vitesse*np.sin(robot.theta)


class Environnement:
	def __init__(self, width, height, scale): 
		# prendre width et height >= 3 
		self.width = width
		self.height = height
		self.scale = scale
		self.grid = [[' ' for _ in range(width)] for _ in range(height)]

class Simulation:

	def afficher_env(env):
		for _ in range(env.width+2):
			print('X', end=' ')
		print()
		for i in range(env.height):
			print('X', end=' ')
			for j in range(env.width):
				print(env.grid[i][j], end=' ')
			print('X')
		for _ in range(env.width+2):
			print('X', end=' ')	
		print()

	def retirer_robot_env(env,robot):
		x = int(robot.x / env.scale)
		y = int(robot.y / env.scale)
		if (env.grid[y][x] == 'R'):
			env.grid[y][x] = '.'
	
	def placer_robot_env(env, robot):
		x = int(robot.x / env.scale)
		y = int(robot.y / env.scale)
		if (env.grid[y][x] == ' ' or env.grid[y][x] == '.'):
			env.grid[y][x] = 'R'

	def avancer_robot_env(env, robot):
		env.grid[int(robot.y / env.scale)][int(robot.x / env.scale)] = ' '
		robot.avancer()
		if (env.grid[int(robot.y / env.scale)][int(robot.x / env.scale)] != 'X'):
			env.grid[int(robot.y / env.scale)][int(robot.x / env.scale)] = 'R'
			print("Le robot a avancé et s'est déplacé en (",robot.x,",",robot.y,")")
		else:
			print("Collision")

	def reculer_robot_env(env, robot):
		env.grid[int(robot.y / env.scale)][int(robot.x / env.scale)] = ' '
		robot.reculer()
		if (env.grid[int(robot.y / env.scale)][int(robot.x / env.scale)] != 'X'):
			env.grid[int(robot.y / env.scale)][int(robot.x / env.scale)] = 'R'
			print("Le robot a reculé et s'est déplacé en (",robot.x,",",robot.y,")")
		else:
			print("Collision")

	def distance(x1, y1, x2, y2): 
		dist = np.sqrt(np.square(x2 - x1)+np.square(y2 - y1))
		print("Distance entre (", x1, ",", y1, ") et (", x2, ",", y2, ") :", dist)





environnement = Environnement(20, 10, 1)
print("L'environnement fait",environnement.width,"case de large et",environnement.height,"de long, et chaque case fait",environnement.scale,"mètres de côté\n")

robot = Robot(9.9, 1.1, 0, 1, 1)

Simulation.placer_robot_env(environnement,robot)

Simulation.afficher_env(environnement)
for _ in range(3):
	Simulation.avancer_robot_env(environnement, robot)

for _ in range(3):
	Simulation.reculer_robot_env(environnement, robot)
Simulation.afficher_env(environnement)
Simulation.distance(robot.x, robot.y, 0, 0)
