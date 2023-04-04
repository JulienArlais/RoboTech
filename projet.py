from module.core import *

stop = False
lock = Lock()

def run_strategie(strategie):
	while not strategie.stop():
		#lock.acquire()
		strategie.update()
		#lock.release()
		time.sleep(cs.dt) # faudrait le changer nan ?
	global stop
	stop = True # on arrete le thread de run_simulation lorsque run_strategie se termine

def run_simulation(simulation, gui):

	while not stop:
		try:
			#lock.acquire()
			t0 = time.time()
			simulation.update()
			if gui is not None:
				gui.update()
			t1 = time.time()
			if (t1-t0) < cs.dt:
				time.sleep(cs.dt-(t1-t0))
			#lock.release()
		except CollisionException as e:
			break

def run():
	# Robot + Environnement
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(cs.rob_x, cs.rob_y, cs.rob_thet, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue)
	proxy_v = Proxy_Virtuel(robot,environnement)

	# Simulation + Interface graphique
	s = Simulation(environnement, robot)
	gui = GUI(environnement, robot)

	# Stratégies
	strat_avance = StrategieAvance(146, 720, proxy_v)
	strat_angle = StrategieAngle(-90, -45, proxy_v)
	liste_strat = [strat_avance, strat_angle]*4
	strat_carre = StrategieSeq(liste_strat)

	t1 = Thread(target=run_simulation, args=(s, gui))
	t2 = Thread(target=run_strategie, args=(strat_carre, ))
	t1.start()
	t2.start()
	gui.window.mainloop()

if __name__ == "__main__":
	run()
