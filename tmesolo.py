from module.element_simulation import Robot, Environnement, CollisionException, Simulation, Objet, run
from module.affichage_2D import GUI
from threading import Thread
import module.constante as cs
from module.proxy import Proxy_Virtuel, Proxy_Reel
from module.core import run_projet

def q1_1():
	# Création d'un environnement et d'un robot
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	ob1 = Objet(100, 100, 15)
	ob2 = Objet(700, 700, 15)
	ob3 = Objet(100, 700, 15)
	ob4 = Objet(700, 100, 15)
	environnement.placer_obstacle(ob1)
	environnement.placer_obstacle(ob2)
	environnement.placer_obstacle(ob3)
	environnement.placer_obstacle(ob4)
	robot = Robot(cs.rob_x, cs.rob_y, cs.rob_thet, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue) # robot immobile, pour montrer ce que fait le controleur
	gui = GUI(environnement, robot)
	proxy_v = Proxy_Virtuel(robot,environnement)
	# Création d'une simulation
	s = Simulation(environnement, robot)
	threadrun = Thread(target=run, args=(s, gui, None))
	threadrun.start()
	gui.window.mainloop()
	run_projet(robot,proxy_v,environnement,s)

if __name__ == "__main__":
	q1_1()