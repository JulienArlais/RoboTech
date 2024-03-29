import numpy as np

# unité de longueur : mm
# unité de vitesse : degré par seconde
# unité de temps : seconde

dt = 0.01# pas de temps pour notre simulation 
mult = 10 # multiplicateur pour l'affichage graphique

env_width = 800 # largeur de l'environnement
env_height = 800 #longueur de l'environnement
scale = 0.1 # échelle à l'affichage

rob_x = 400 # position x du robot
rob_y = 400 # position y du robot
rob_thet = 0 # angle de départ du robot
rob_r = 15 # rayon du robot
rob_dist_roue = 30 # distance entre les roues
rob_r_roue = 4 # rayon des roues

nb_objet = 5 # nombre d'objets dans la simulation

stav_dist = 200 # distance à avancer dans StrategieAvance
stav_vit = 200 #vitesse à laquelle avancer

stan_an = -95 # angle à tourner dans StrategieAngle
stan_dps = -60 # angle tourné par seconde

stmur_dist = 5000
stmur_vit = 200 # vitesse de déplacement de la StratégieMur 

data = 'camera_test/test3.jpg'
