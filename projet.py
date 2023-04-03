from module.element_simulation import Robot, Environnement, CollisionException, Simulation
import module.constante as cs
from module.proxy import Robot_Virtuel, Robot_Reel
from module.core import run_projet

if __name__ == "__main__":

	# Création d'un environnement et d'un robot
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(cs.rob_x, cs.rob_y, cs.rob_thet, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue) # robot immobile, pour montrer ce que fait le controleur
	environnement.generer_obstacles(robot, cs.nb_objet)
	environnement.generer_emetteurs(robot,cs.nb_éméteur)

	proxy_v = Robot_Virtuel(robot,environnement)

	# Création d'une simulation
	s = Simulation(environnement, robot)
	run_projet(robot,proxy_v,environnement,s)
