from module.core import *

if __name__ == "__main__":
	environnement = Environnement(cs.env_width, cs.env_height, cs.scale)
	robot = Robot(cs.rob_x, cs.rob_y, cs.rob_thet, cs.rob_r, cs.rob_dist_roue, cs.rob_r_roue)
	proxy_v = Proxy_Virtuel(robot,environnement)
	run(environnement, robot, proxy_v)