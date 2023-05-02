from .vue.affichage_2D import GUI
from threading import Thread, Lock
from .modele.element_simulation import Objet, Robot, Environnement, CollisionException, Simulation
from .controleur.controleur import StrategieAvance, StrategieAngle, StrategieArretMur, StrategieSeq, StrategieSuivreBalise, StrategieStop
from .modele.proxy import Proxy_Virtuel, Proxy_Reel
import module.constante as cs
import time

try :
	from Robot2I013 import Robot2I013
except :
	from .modele.robot_mock_up import Robot_Mock_Up as Robot2I013

stop = False

def run_strategie(strategie):
	while not strategie.stop():
		#lock.acquire()
		strategie.update()
		strategie.proxy.update()
		#lock.release()
		time.sleep(cs.dt) # faudrait le changer nan ?
	global stop
	stop = True # on arrete le thread de run_simulation lorsque run_strategie se termine
	strategie.proxy.set_vitesse(0, 0)

def run_simulation(simulation, gui):

	while not stop:
		try:
			#lock.acquire()
			t0 = time.time()
			simulation.update()
			if gui is not None:
				gui.update()
			t1 = time.time()
			#if (t1-t0) < cs.dt:
			#	time.sleep(cs.dt-(t1-t0))
			#lock.release()
		except CollisionException as e:
			break
			
def run(env,rob,prox):
	# Robot + Environnement
	environnement = env
	robot = rob
	proxy_v = prox

	#Activation ou D├ęsactivation des LEDS du robot 
	rob.blinker_off(1)
	rob.blinker_on(0)
	

	# Simulation + Interface graphique
	s = Simulation(environnement, robot)

	# Strat├ęgies
	stop = StrategieAvance(1, cs.stav_vit, proxy_v)

	t1 = Thread(target=run_simulation, args=(s, None))
	t2 = Thread(target=run_strategie, args=(stop,))
	t1.start()
	t2.start()