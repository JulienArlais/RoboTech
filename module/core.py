from .vue.affichage_2D import GUI
from threading import Thread, Lock
from .modele.element_simulation import Objet, Robot, Environnement, CollisionException, Simulation
from .controleur.controleur import StrategieAvance, StrategieAngle, StrategieArretMur, StrategieSeq, StrategieSuivreBalise
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
		strategie.update()
		strategie.proxy.update()
		time.sleep(cs.dt)
	global stop
	stop = True # on arrete le thread de run_simulation lorsque run_strategie se termine
	strategie.proxy.set_vitesse(0, 0)

def run_simulation(simulation, gui):

	while not stop:
		try:
			simulation.update()
			if gui is not None:
				gui.update()
		except CollisionException as e:
			break
			
def run(env,rob,prox):
	# Robot + Environnement
	environnement = env
	robot = rob
	proxy = prox	

	# Simulation + Interface graphique
	s = Simulation(environnement, robot)
	gui = GUI(environnement, robot) ### � commenter pour utiliser le robot r�el

	# Stratégies
	strat_avance = StrategieAvance(cs.stav_dist, cs.stav_vit, proxy)
	strat_angle = StrategieAngle(cs.stan_an, cs.stan_dps, proxy)
	liste_strat = [strat_avance, strat_angle]*4
	strat_carre = StrategieSeq(liste_strat, proxy)
	strat_mur = StrategieArretMur(cs.stmur_dist, cs.stmur_vit, proxy)

	t1 = Thread(target=run_simulation, args=(s, gui)) ### remplacer gui par None pour utiliser le robot r�el
	t2 = Thread(target=run_strategie, args=(strat_mur,))
	t1.start()
	t2.start()
	gui.window.mainloop() ### � commenter pour utiliser le robot r�el
