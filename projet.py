from module.core import *

try :
	from module.modele.robot_api import Robot2IN013
except :
	from module.modele.robot_mock_up import Robot_Mock_Up as Robot2IN013

if __name__ == "__main__":
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(cs.rob_x, cs.rob_y, cs.rob_thet, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue)
	proxy_v = Proxy_Virtuel(robot,environnement)
	proxy_r = Proxy_Reel(Robot2IN013())
	run(environnement, robot, proxy_r)
