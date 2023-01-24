from Robot import Robot
from Environnement import Environnement


environment = Environnement(20, 20) 
robot=Robot(environment)

environment.afficher()
environment.obstacle()


robot.direction=input("Donner une direction au robot ")
robot.reculer() 

robot.auto_move()

robot.carre()

# place le robot en (1, 1)
robot.placer(1,1) 