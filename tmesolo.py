from module.element_simulation import Robot, Environnement, CollisionException, Simulation, run
from module.proxy import Proxy_Virtuel, Proxy_Reel
import tkinter as tk
from module.affichage_2D import GUI
from threading import Thread
from module.controleur import StrategieAvance, StrategieAngle, StrategieArretMur, StrategieSeq, StrategieSuivreBalise, Strategie_dessine1, Strategie_dessine0, Strategie_dessine01
import module.constante as cs

def q1_1():
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(400, 400, cs.rob_thet, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue)
	s = Simulation(environnement, robot)
	environnement.generer_un_obstacle(robot,50,50)
	environnement.generer_un_obstacle(robot,750,50)
	environnement.generer_un_obstacle(robot,50,750)
	environnement.generer_un_obstacle(robot,750,750)
	gui = GUI(environnement, robot,"black")
	gui.window.mainloop()
	
def q1_2():
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(400, 400, cs.rob_thet, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue)
	s = Simulation(environnement, robot)
	environnement.generer_un_obstacle(robot,50,50)
	environnement.generer_un_obstacle(robot,750,50)
	environnement.generer_un_obstacle(robot,50,750)
	environnement.generer_un_obstacle(robot,750,750)
	gui = GUI(environnement, robot,"orange")
	gui.window.mainloop()
	
def q1_3():
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(cs.rob_x, cs.rob_y, cs.rob_thet, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue)
	proxy_v = Proxy_Virtuel(robot,environnement)

	s = Simulation(environnement, robot)
	gui = GUI(environnement, robot,"orange")
	
	robot.dessine(False)
	
	stavance = StrategieAvance(cs.stav_dist, cs.stav_vit, proxy_v)

	threadrun = Thread(target=run, args=(s, gui, stavance))
	threadrun.start()
	gui.window.mainloop()
	
def q1_4():
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(cs.rob_x, cs.rob_y, cs.rob_thet, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue) 
	proxy_v = Proxy_Virtuel(robot,environnement)

	s = Simulation(environnement, robot)
	gui = GUI(environnement, robot, proxy_v, "orange")
	
	stavance = StrategieAvance(100,720, proxy_v)
	stangle = StrategieAngle(60, cs.stan_dps, proxy_v) 
	listeHexagone = [stavance, stangle, stavance, stangle, stavance, stangle, stavance, stangle, stavance, stangle, stavance]
	stseq = StrategieSeq(listeHexagone)

	threadrun = Thread(target=run, args=(s, gui, stseq))
	threadrun.start()
	gui.window.mainloop()
	
	
def q2_1():
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(400,400,-90, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue)
	proxy_v = Proxy_Virtuel(robot,environnement)

	s = Simulation(environnement, robot)
	gui = GUI(environnement, robot, proxy_v, "orange")
	
	stdessine1 = Strategie_dessine1(100,720, proxy_v)


	threadrun = Thread(target=run, args=(s, gui, stdessine1))
	threadrun.start()
	gui.window.mainloop()
	
def q2_2():
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(400,400,-90, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue) 
	proxy_v = Proxy_Virtuel(robot,environnement)

	s = Simulation(environnement, robot)
	gui = GUI(environnement, robot, proxy_v, "orange")
	
	stzero = Strategie_dessine0(proxy_v)

	threadrun = Thread(target=run, args=(s, gui, stzero))
	threadrun.start()
	gui.window.mainloop()
	
def q2_3():
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(400,400,-90, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue) 
	proxy_v = Proxy_Virtuel(robot,environnement)

	s = Simulation(environnement, robot)
	gui = GUI(environnement, robot, proxy_v, "orange")
	
	st01 = Strategie_dessine01(proxy_v)

	threadrun = Thread(target=run, args=(s, gui, st01))
	threadrun.start()
	gui.window.mainloop()
	
	
if __name__ == "__main__":
	q2_3()
	


