# unité de longueur : centimètre
# unité de vitesse : degré par seconde
# unité de temps : seconde

dt = 0.01# pas de temps pour notre simulation 
mult = 10 # multiplieur pour l'affichage graphique

env_width = 800 # largeur de l'environnement
env_height = 800 #longueur de l'environnements
scale = 0.1 #échelle à l'affichage

rob_x = 200 #position x du robot
rob_y = 200 #position y du robot
rob_thet = 90 #angle de départ du robot
rob_r = 15 #rayon du robot
rob_dist_roue = 30 #distance entre les roues
rob_r_roue = 4 #rayon des roues

nb_objet =0#nombre d'objets dans la simulation
nb_éméteur=1

stav_dist = 200 #distance à avancer dans StrategieAvance
stav_vit = 720 #vitesse à laquelle avancer

stan_an = -90 #angle à tourner dans StrategieAngle
stan_dps_neg = -45 #angle tourné par seconde
stan_dps_pos=45

#StrategieSeq2
stan_an2 = -45 #angle à tourner dans StrategieSeq2c
stan_dps2 = -22 #angle tourné par seconde dans StrategieSeq2


stmur_vit = 1000 #vitesse de déplacement de la StratégieMur 

data = 'camera_test/test3.jpg'
