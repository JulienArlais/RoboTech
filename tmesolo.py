from module.element_simulation import Robot, Environnement, CollisionException, Simulation, Objet, run
from module.affichage_2D import GUI
from threading import Thread
import module.constante as cs
from module.proxy import Proxy_Virtuel, Proxy_Reel
from module.controleur import StrategieAvance, StrategieAngle

class StrategieSeqDessine():
	def __init__(self, liste, robot):
		self.liste = liste
		self.indlist = 0
		self.robot = robot
		
	def update(self):
		if (self.indlist%2 == 1):
			self.robot.dessine(False)
		else:
			self.robot.dessine(True)
		self.liste[self.indlist].update()
		if self.liste[self.indlist].stop():
			self.indlist += 1
			
	def stop(self):
		if self.indlist >= len(self.liste):
			self.indlist = 0
			return True
		return False

class StrategieBoucle():
	def __init__(self, strat):
		self.strat = strat
		
	def update(self):
		self.strat.update()
			
	def stop(self):
		if self.strat.stop():
			return False
		return False


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

def q1_4():
	# Création d'un environnement et d'un robot
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(cs.rob_x, cs.rob_y, cs.rob_thet, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue) # robot immobile, pour montrer ce que fait le controleur
	gui = GUI(environnement, robot)
	proxy_v = Proxy_Virtuel(robot,environnement)
	# Création d'une simulation
	s = Simulation(environnement, robot)
	stavance = StrategieAvance(50, 720, proxy_v)
	stangle = StrategieAngle(60, 45, proxy_v)
	liste_strat = [stavance, stangle]*6
	stseq = StrategieSeqDessine(liste_strat, proxy_v)
	threadrun = Thread(target=run, args=(s, gui, stseq))
	threadrun.start()
	gui.window.mainloop()

def q2_1():
	# Création d'un environnement et d'un robot
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(cs.rob_x, cs.rob_y, -90, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue) # robot immobile, pour montrer ce que fait le controleur
	gui = GUI(environnement, robot)
	proxy_v = Proxy_Virtuel(robot,environnement)
	# Création d'une simulation
	s = Simulation(environnement, robot)
	stavance = StrategieAvance(150, 720, proxy_v)
	threadrun = Thread(target=run, args=(s, gui, stavance))
	threadrun.start()
	gui.window.mainloop()

def q2_2():
	# Création d'un environnement et d'un robot
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(cs.rob_x, cs.rob_y, cs.rob_thet, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue) # robot immobile, pour montrer ce que fait le controleur
	gui = GUI(environnement, robot)
	proxy_v = Proxy_Virtuel(robot,environnement)
	# Création d'une simulation
	s = Simulation(environnement, robot)
	stavance1 = StrategieAvance(50, 720, proxy_v)
	stavance2 = StrategieAvance(200, 720, proxy_v)
	stangle = StrategieAngle(90, 45, proxy_v)
	liste_strat = [stavance1, stangle, stavance2, stangle]*2
	stseq = StrategieSeqDessine(liste_strat, proxy_v)
	threadrun = Thread(target=run, args=(s, gui, stseq))
	threadrun.start()
	gui.window.mainloop()

def q2_3():
	# Création d'un environnement et d'un robot
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(700, 700, -90, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue) # robot immobile, pour montrer ce que fait le controleur
	gui = GUI(environnement, robot)
	proxy_v = Proxy_Virtuel(robot,environnement)
	# Création d'une simulation
	s = Simulation(environnement, robot)

	#pour le 1
	stavance1 = StrategieAvance(200, 1080, proxy_v)

	#Pour le 0
	stavance2 = StrategieAvance(50, 720, proxy_v)
	stangle = StrategieAngle(90, 45, proxy_v)
	liste_strat1 = [stavance2, stangle, stavance1, stangle]*2
	zero = StrategieSeqDessine(liste_strat1, proxy_v)

	#Pour l'espace
	liste_strat2 = [stangle, stavance1]
	espace1 = StrategieSeqDessine(liste_strat2, proxy_v)
	stangle2 = stangle = StrategieAngle(-90, -45, proxy_v)
	liste_strat3 = [stangle2, stavance1, stangle2]
	espace2 = StrategieSeqDessine(liste_strat3, proxy_v)

	liste_strat = [stavance1, espace1, zero]
	stseq = StrategieSeqDessine(liste_strat, proxy_v)

	strat_boucle = StrategieBoucle(stseq)
	threadrun = Thread(target=run, args=(s, gui, stseq))
	threadrun.start()
	gui.window.mainloop()

def q2_4():
	# Création d'un environnement et d'un robot
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(700, 700, -90, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue) # robot immobile, pour montrer ce que fait le controleur
	gui = GUI(environnement, robot)
	proxy_v = Proxy_Virtuel(robot,environnement)
	# Création d'une simulation
	s = Simulation(environnement, robot)

	#pour le 1
	stavance1 = StrategieAvance(200, 1080, proxy_v)

	#Pour le 0
	stavance2 = StrategieAvance(50, 720, proxy_v)
	stangle = StrategieAngle(90, 45, proxy_v)
	liste_strat1 = [stavance2, stangle, stavance1, stangle, stavance2, stangle, stavance1, stangle, stavance2, stangle, stavance1]
	zero = StrategieSeqDessine(liste_strat1, proxy_v)

	#Pour l'espace
	liste_strat2 = [stangle, stavance1]
	espace1 = StrategieSeqDessine(liste_strat2, proxy_v)
	stangle2 = stangle = StrategieAngle(-90, -45, proxy_v)

	liste_strat = [stavance1, espace1, zero]
	stseq = StrategieSeqDessine(liste_strat, proxy_v)

	threadrun = Thread(target=run, args=(s, gui, stseq))
	threadrun.start()
	gui.window.mainloop()

if __name__ == "__main__":
	q2_3()