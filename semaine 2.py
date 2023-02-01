import numpy as np
import math
import time 

class HorsLimitesException(Exception):
	def __init__(self,message):
		self.message = message
		
class Object:
    def __init__(self, height, speed):
        self.height = height
        self.speed = speed


class Robot:
	def __init__(self, x, y, theta, vitesse,rayon):
		# x et y des coordonnées en mètre, direction un angle par rapport à l'abscisse en float et la vitesse max du robot en m/s
		# on suppose que le robot est un cercle, pour faciliter les collisions
		self.x = x
		self.y = y
		self.theta = theta #math.radians(theta)
		self.vitesse = vitesse
		self.acceleration = 0
		self.rayon = rayon		
		

	def avancer(self, dt):
		self.vitesse += self.acceleration * dt
		self.vitesse = min(self.vitesse, self.vitesse)  # pour s'assurer que la vitesse ne dépasse pas la vitesse maximale
		self.x += self.vitesse * np.cos(robot.theta) * dt
		self.y += self.vitesse * np.sin(robot.theta) * dt
		print("sin(robot theta) = ",format_number(np.sin(robot.theta)))
		print("sin(robot theta) * vitesse = ",format_number(self.vitesse * np.sin(robot.theta)))
		

	def tourner(self, angle):
		# angle est la valeur d'angle que l'on va ajouter à notre angle. Elle peut être positive ou négative
		self.theta += math.radians(angle)
		#print("La nouvelle direction du robot est de", self.theta, "degrés par rapport à l'axe des abscisses")

		
	def reculer(self,dt):
		'''fait reculer le robot pendant 1 seconde'''
		self.vitesse += self.acceleration * dt
		self.vitesse = min(self.vitesse, self.vitesse)
		self.x -= self.vitesse*np.cos(robot.theta)*dt
		self.y -= self.vitesse*np.sin(robot.theta)*dt

def format_number(number):
    return "{:.2f}".format(number)

class Environnement:
	def __init__(self, width, height, scale): 
		# prendre width et height >= 3 
		self.width = width
		self.height = height
		self.scale = scale
		self.grid = [[' ' for _ in range(width)] for _ in range(height)]
		
	def retirer_robot_env(self,robot):
		x = int(robot.x / self.scale)
		y = int(robot.y / self.scale)
		if (self.grid[y][x] == 'R'):
			self.grid[y][x] = '.'
	
	def placer_robot_env(self, robot):
		x = int(robot.x / self.scale)
		y = int(robot.y / self.scale)
		if (self.grid[y][x] == ' ' or self.grid[y][x] == '.'):
			self.grid[y][x] = 'R'

	def avancer_robot_env(self, robot):
		''' changer le sens des > pour robot.y dans le if quand pb résolu '''
		x = robot.x / self.scale
		y = robot.y / self.scale
		self.grid[(int)(y)][(int)(x)] = '.'
		print("y pré avancer() =",format_number(robot.y))
		robot.avancer(1)
		print("y post avancer() =",format_number(robot.y))
		print("x=",format_number(int(robot.x / self.scale)), " y=",format_number(int(robot.y / self.scale)))
		print("xr=",format_number(robot.x), " yr=",format_number(robot.y))
		print("width=",self.width*self.scale, " height=",self.height*self.scale)
		if ((0 < robot.x < self.width*self.scale) and (0 > robot.y > -self.height*self.scale)):
			self.grid[int(robot.y / self.scale)][int(robot.x / self.scale)] = 'R'
			print("Le robot en (", format_number(x), ",", format_number(y), ") a avancé et s'est déplacé en (",format_number(robot.x),",",format_number(robot.y),")")
		else:
			#raise HorsLimitesException("Collision")
			print("collision à venir")
			exit()
			


	def reculer_robot_env(self, robot):
		x = robot.x / self.scale
		y = robot.y / self.scale
		self.grid[(int)(y)][(int)(x)] = '.'
		robot.reculer(1)#Le pas dt est égale à 1
		print("x=",format_number(int(robot.y / self.scale)), " y=",format_number(int(robot.x / self.scale)))
		if (self.grid[int(robot.y / self.scale)][int(robot.x / self.scale)] != 'X'):
			self.grid[int(robot.y / self.scale)][int(robot.x / self.scale)] = 'R'
			print("Le robot en (", x, ",", y, ") a reculé et s'est déplacé en (",format_number(robot.x),",",format_number(robot.y),")")
		else:
			print("Collision à venir")
			exit()

	
	def distance(self,x1, y1, x2, y2): 
		dist = np.sqrt(np.square(x2 - x1)+np.square(y2 - y1))
		print("Distance entre (", x1, ",", y1, ") et (", x2, ",", y2, ") :", "{:.2f}".format(dist))



class Simulation:

	def __init__(self,env,robot):
		self.environnement=env
		self.robot=robot
		
	def afficher_env(self, env):
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

	def update(self):
		#A completer 
		while True:
			self.environnement.avancer_robot_env(self.robot)
			self.afficher_env(self.environnement)
			time.sleep(1)
			
			
			
		self.afficher_env(self.environnement)

		for _ in range(4):
			self.environnement.avancer_robot_env(robot)

		self.afficher_env(self.environnement)

		# Le robot recule trois fois dans l'environnement
		for _ in range(3):
			self.environnement.reculer_robot_env(robot)

		# Donne la distance du robot par rapport au point ( 0 , 0 )
		self.environnement.distance(robot.x, robot.y, 0, 0)
		self.afficher_env(self.environnement)




#MAIN
robot=Robot(1,1,30,10,5)
env=Environnement(10,10,10)

env.placer_robot_env(robot)

sim=Simulation(env,robot)


sim.afficher_env(env)
sim.update()

environnement.retirer_robot_env(robot)
Simulation.afficher_env(environnement)


            



